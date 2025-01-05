# Talk2Linux(Chinese Version)
## Overview
Talk2Linux 是一个命令行界面（CLI），用于通过 OpenAI 与 Linux 系统交互。它允许用户以自然语言描述他们的需求，然后生成并执行相应的 Linux 命令来满足这些需求。这个项目旨在简化 Linux 系统的管理和操作，使用户能够更高效地完成任务。

## Features
- 自然语言交互：用户可以使用自然语言描述他们的需求，无需记忆复杂的命令。
- 命令生成：根据用户的输入，生成可执行的 Linux 命令。
- 命令执行：自动执行生成的命令，并显示执行结果。
- 历史记录：保存对话历史，方便用户回顾和重用之前的命令。
- 安全检查：内置禁止指令列表，防止执行危险命令。

## 这个项目目前处于开发阶段，可能存在一些问题，**请勿用于生产环境。**

## Installation
### Prerequisites
- Python 3.6 或更高版本
- OpenAI API 密钥
### Installation Steps
#### 克隆仓库：

```
sh
git clone https://github.com/phosphorusp4/talk2linux.git
cd talk2linux
```
#### 安装依赖：

```
sh
pip install -r requirements.txt
```
#### 安装项目：

```
sh
python setup.py install
```

## Usage
### Basic Usage
#### 运行 CLI：

```
sh
talk2 "你的需求描述"
```
#### 查看帮助信息：

```
sh
talk2 --help
```
### Advanced Usage

#### 更改 API 密钥：

```
sh
talk2 --change-apikey "新的API密钥"
```
#### 更改 OpenAI URL：
```
sh
talk2 --change-url "新的URL"
```
#### 清除对话历史：

```
sh
talk2 --erase-history
```
## Configuration

- API 密钥和 URL
首次运行时，系统会提示您输入 OpenAI API 密钥和 URL。您也可以通过命令行参数或配置文件更改这些设置。

- 禁止指令列表
默认的禁止指令列表包括 poweroff、rm -rf、nano 和 vim。您可以在 ~/.config/talk2linux/banned_instructions.json 文件中自定义此列表。

## History
对话历史默认保存在 ~/.config/talk2linux/history.json 文件中。您可以随时查看或清除历史记录。

## License
MIT License

## Contact
如果有任何问题或建议，请联系 bailinwp4@163.com。

# Talk2Linux(English Version)
## Overview
Talk2Linux is a command-line interface (CLI) that enables interaction with Linux systems through OpenAI. It allows users to describe their needs in natural language, and then generates and executes corresponding Linux commands to fulfill these needs. This project aims to simplify the management and operation of Linux systems, enabling users to complete tasks more efficiently.

## Features
- **Natural Language Interaction**: Users can describe their needs in natural language without having to memorize complex commands.
- **Command Generation**: Generates executable Linux commands based on user input.
- **Command Execution**: Automatically executes generated commands and displays the results.
- **History Record**: Saves conversation history for easy review and reuse of previous commands.
- **Security Check**: Built-in list of prohibited instructions to prevent dangerous commands from being executed.

## This project is currently in development, there may be some problems, **please do not use it in production environment.**

## Installation
### Prerequisites
- Python 3.6 or higher
- OpenAI API key

### Installation Steps
#### Clone Repository:

```
sh
git clone https://github.com/phosphorusp4/talk2linux.git
cd talk2linux
```
#### Install：

```
sh
python setup.py install
```

## Usage
### Basic Usage
#### Run CLI：

```
sh
talk2 "Your need description"
```
#### View the help information：

```
sh
talk2 --help
```
### Advanced Usage

#### Change API Key：

```
sh
talk2 --change-apikey "New API key"
```
#### Change OpenAI URL：
```
sh
talk2 --change-url "New URL"
```
#### Erase History：

```
sh
talk2 --erase-history
```
## Configuration

- API key and URL
The API key and URL will prompt you to enter an OpenAI API key and URL on the first run. You can also change these settings through command-line arguments or configuration files.

- Banned Instructions
Prohibited instruction list: By default, the list includes poweroff, rm -rf, nano, and vim. You can customize this list in the ~/.config/talk2linux/banned_instructions.json file.

## History
Conversation history is saved by default in the ~/.config/talk2linux/history.json file. You can view or clear the history at any time.

## License
MIT License

## Contact
If you have any questions or suggestions, please contact bailinwp4@163.com.

