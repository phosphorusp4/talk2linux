# __main__.py
#!/usr/bin/env python3

from openai import OpenAI, AuthenticationError, BadRequestError
import json
import subprocess
import sys
import os
import argparse
import re
import time

class Talk2Linux:
    def __init__(self):

        self.request_interval = 0.5

        self.config_dir = os.path.join(os.path.expanduser('~'), '.config', 'talk2linux')
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

        self.history_path = os.path.join(self.config_dir, 'history.json')
        self.apikey_path = os.path.join(self.config_dir, 'apikey.txt')

        self.banned_instructions_path = os.path.join(self.config_dir, 'banned_instructions.json')

        if os.path.exists(self.banned_instructions_path):
            with open(self.banned_instructions_path, 'r') as f:
                self.banned_instructions = json.load(f)
        else:
            default_banned_instructions = [
                "poweroff", "rm -rf"
            ]
            with open(self.banned_instructions_path, 'w') as f:
                json.dump(default_banned_instructions, f, indent=4)
            self.banned_instructions = default_banned_instructions

        if os.path.exists(self.apikey_path):
                with open(self.apikey_path, 'r') as f:
                    apikey = f.read().strip()
        else:
            print("You haven't entered the API Key，please enter your API Key:")
            apikey = input()
            with open(self.apikey_path, 'w') as f:
                f.write(apikey)

        self.user = subprocess.check_output("whoami", shell=True).decode().strip()

        self.prompt = [
            {"role": "system",
             "content": "1.你是一个ai运维员，你会根据人类指令(用<h></h>包裹)和终端输出(用<t></t>包裹)来输出终端命令来部署用户要求的服务并自动维护它。2.你只需要输出终端命令。其他什么都不要输出，包括中文和markdown语法，不要解释你的指令。3.如果你需要中断当前的任务，请只输出""stop""4你的用户是" + self.user}
        ]

        self.llm_client = OpenAI(
            api_key=apikey,
            base_url="https://api.moonshot.cn/v1",
        )

        if os.path.exists(self.history_path):
            with open(self.history_path, 'r') as f:
                self.history = json.load(f)
        else:
            self.history = self.prompt
            with open(self.history_path, 'w') as f:
                json.dump(self.prompt, f, indent=4)


    def save_conversation(self):
        with open(self.history_path, 'w') as f:
            json.dump(self.history, f, indent=4)


    def clear_history(self):
        with open(self.history_path, 'w') as f:
            json.dump(self.prompt, f, indent=4)

    def chat(self, query: str, retry_count: int = 0, max_retries: int = 3) -> str:

        self.history.append({
            "role": "user",
            "content": query
        })

        try:
            completion = self.llm_client.chat.completions.create(
                model="moonshot-v1-8k",
                messages=self.history,
                temperature=0.3,
            )

        except Exception as e:
            print(e)

            time.sleep(self.request_interval)

            if retry_count < max_retries:
                print(f"Failed to generate response, retrying... ({retry_count}/{max_retries})")
                if len(self.history) > 1:
                    self.history = [self.prompt[0], self.history[-1]]
                else:
                    self.history = self.prompt
                self.save_conversation()
                print(self.history)
                return self.chat(query, retry_count=retry_count + 1)
            else:
                print("Failed to generate response after multiple attempts.Please check your apikey,or if the single instruction or execute result is too long")
                return "Failed"

        result = completion.choices[0].message.content

        self.history.append({
            "role": "assistant",
            "content": result
        })

        self.save_conversation()

        return result

    def execute_commands(self, commands: str, print_output=True) -> str:
        # 确保命令是以换行符分隔的多行命令
        command_list = commands.strip().splitlines()
        results = []

        for command in command_list:
            # 检查命令是否包含禁止指令
            banned = any(banned_instruction in command.strip() for banned_instruction in self.banned_instructions)

            # 如果命令包含禁止指令，则跳过执行
            if banned:
                print("[W]Detected prohibited instruction:" + command.strip() + ",Execution skipped.")
                results.append("[W]Detected prohibited instruction:" + command.strip() + ",Execution skipped,don't try to execute it again,and don't execute instruction which Similar to it.")
                continue

            # 如果命令是空行，则跳过
            if not command.strip():
                continue

            try:
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                           text=True, bufsize=1, universal_newlines=True)

                command_output = ""

                while True:
                    output = process.stdout.readline()
                    error = process.stderr.readline()

                    if output == '' and error == '' and process.poll() is not None:
                        break

                    if output:

                        command_output += output
                        if print_output:
                            sys.stdout.write(output)
                            sys.stdout.flush()


                    if error:
                        command_output += error
                        if print_output:
                            sys.stderr.write(error)
                            sys.stderr.flush()

                process.wait()
                results.append(command_output)

            except Exception as e:
                if print_output:
                    print(f"Error executing command '{command}': {str(e)}")
                results.append(f"Error executing command '{command}': {str(e)}\n")

        return ''.join(results)

    def run(self, query):
        chat_result = self.chat("<h>" + query + "</h>")
        if chat_result == "Failed":
            return
        else:
            print(chat_result)
        while True:
            if chat_result == "Failed":
                break
            elif "stop" == chat_result:
                break
            else:
                re.sub(r'<t>.*?</t>', '', chat_result)
                execute_result = self.execute_commands(chat_result)
                chat_result = self.chat("<t>"+execute_result+"</t>")
                time.sleep(self.request_interval)

def main():
    parser = argparse.ArgumentParser(description="TalkToLinux Command Line Interface")
    parser.add_argument('-c', '--change-apikey', type=str, help='Change the API Key')
    parser.add_argument('-e', '--erase-history', action='store_true', help='Erase the conversation history')
    parser.add_argument('-v', '--version', action='version', version='0.1.0a1')
    parser.add_argument('query', type=str, nargs='?', help='The query to be processed')

    args = parser.parse_args()

    if args.change_apikey:
        with open(os.path.join(self.config_dir, 'apikey.txt'), 'w') as f:
            f.write(args.change_apikey)
        print(f"API Key changed to: {args.change_apikey}")

    if args.erase_history:
        talk_to_linux = Talk2Linux()
        talk_to_linux.clear_history()
        print("Conversation history erased.")

    # 检查是否提供了 -c 或 -e 参数
    if args.change_apikey or args.erase_history:
        if args.query is not None:
            talk_to_linux = Talk2Linux()
            talk_to_linux.run(args.query)
    else:
        if args.query is None:
            parser.error("query is required when neither -c nor -e is provided.")
        else:
            talk_to_linux = Talk2Linux()
            talk_to_linux.run(args.query)

if __name__ == "__main__":
    main()
