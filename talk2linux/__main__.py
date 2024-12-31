# __main__.py
#!/usr/bin/env python3

from openai import OpenAI
import json
import subprocess
import sys
import os
import argparse
import re

class Talk2Linux:
    def __init__(self):

        if os.path.exists('apikey.txt'):
                with open('apikey.txt', 'r') as f:
                    apikey = f.read().strip()
        else:
            print("You haven't entered the API Key，please enter your API Key:")
            apikey = input()
            with open('apikey.txt', 'w') as f:
                f.write(apikey)

        self.user = subprocess.check_output("whoami", shell=True).decode().strip()

        prompt = [
            {"role": "system",
             "content": "1.你是一个ai运维员，你会根据人类指令(用<h></h>包裹)和终端输出(用<t></t>包裹)来输出终端命令来部署用户要求的服务并自动维护它。2.你只需要输出终端命令。其他什么都不要输出，包括中文和markdown语法，不要解释你的指令。3.如果你需要中断当前的任务，请只输出""stop""4你的用户是" + self.user}
        ]

        self.llm_client = OpenAI(
            api_key=apikey,
            base_url="https://api.moonshot.cn/v1",
        )


        if os.path.exists('history.json'):
            with open('./history.json', 'r') as f:
                self.history = json.load(f)
        else:
            self.history = prompt
            with open('history.json', 'w') as f:
                json.dump(prompt, f, indent=4)

    def save_conversation(self):
        with open('history.json', 'w') as f:
            json.dump(self.history, f, indent=4)

    @staticmethod
    def clear_history():
        prompt = [
            {"role": "system",
             "content": "1.你是一个ai运维员，你会根据人类指令(用<h></h>包裹)和终端输出(用<t></t>包裹)来输出终端命令来部署用户要求的服务并自动维护它。2.你只需要输出终端命令。其他什么都不要输出，包括中文和markdown语法，不要解释你的指令。3.如果你需要中断当前的任务，请只输出""stop""4你的用户是" + subprocess.check_output("whoami", shell=True).decode().strip()}
        ]
        with open('history.json', 'w') as f:
            json.dump(prompt, f, indent=4)

    def chat(self, query: str) -> str:
        self.history.append({
            "role": "user",
            "content": query
        })
        completion = self.llm_client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=self.history,
            temperature=0.3,
        )
        result = completion.choices[0].message.content
        self.history.append({
            "role": "assistant",
            "content": result
        })

        self.save_conversation()

        return result

    @staticmethod
    def execute_commands(commands: str, print_output=True) -> str:
        # 确保命令是以换行符分隔的多行命令
        command_list = commands.strip().splitlines()
        results = []

        for command in command_list:
            if not command.strip():
                continue  # 跳过空行

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
        try:
            chat_result = self.chat("<h>"+query+"</h>")
        except Exception as e:
            print(f"Client connection failed,please check your apikey!{e}")
            return
        print(chat_result)
        while True:
            if "stop" in chat_result:
                break
            else:
                re.sub(r'<t>.*?</t>', '', chat_result)
                execute_result = self.execute_commands(chat_result)
                chat_result = self.chat("<t>"+execute_result+"</t>")

def main():
    parser = argparse.ArgumentParser(description="TalkToLinux Command Line Interface")
    parser.add_argument('-c', '--change-apikey', type=str, help='Change the API Key')
    parser.add_argument('-e', '--erase-history', action='store_true', help='Erase the conversation history')
    parser.add_argument('-v', '--version', action='version', version='Talk2Linux alpha test version')
    parser.add_argument('query', type=str, nargs='?', help='The query to be processed')

    args = parser.parse_args()

    if args.change_apikey:
        with open('apikey.txt', 'w') as f:
            f.write(args.change_apikey)
        print(f"API Key changed to: {args.change_apikey}")

    if args.erase_history:
        Talk2Linux.clear_history()
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

