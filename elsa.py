#!/usr/bin/env python
import sys
import os
import subprocess


# PROMPT COLORS
class PROMPT_COLOR:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    RESTORE = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# GENERAL METHODS - BEGIN
def __get_command():
    return sys.argv


def __get_command_arg(index, exit=True):
    try:
        return __get_command()[index]
    except IndexError:
        if exit:
            __print_error('missing or wrong argument, check if your command "' + " ".join(__get_command()) + '" is ok or try the same command (press arrow up key) with the following argument "--help" or "elsa --help"')
            sys.exit()


def __print_error(message):
    print(PROMPT_COLOR.RED + 'ERROR: ' + message + PROMPT_COLOR.RESTORE)


def __print_success(message):
    print(PROMPT_COLOR.GREEN + message + PROMPT_COLOR.RESTORE)


def __validate_arg_length(index):
    if len(__get_command()) <= index:
        __print_error('command args missing in "' + " ".join(__get_command()) + '", for more info execute: ' + PROMPT_COLOR.BOLD + 'elsa --help')
        sys.exit()


def __get_env_jira_project_key():
    return 'ELSA_JIRA_PROJECT'


def __get_env_jira_project_value():
    return os.getenv(__get_env_jira_project_key())
# GENERAL METHODS - END


# COMMIT COMMANDS METHODS - BEGIN
def _build_commit_base_name(jira_card_number):
    if not jira_card_number.isdigit():
        __print_error('"' + jira_card_number + '" is not valid Jira card number (should be an "int"), check the card of Jira you are working on...')
        sys.exit()

    return __get_env_jira_project_value() + '-' + jira_card_number


def _git_commit(message):
    try:
        subprocess.check_output('git commit -m "' + message + '"', shell=True)
        __print_success('elsa committed "' + message + '" successfully!')
    except subprocess.CalledProcessError as e:
        __print_error('elsa tried to commit "' + message + '" but Gitlab told her... \n' + e.output)
        sys.exit()


def _git_push():
    try:
        branch = subprocess.check_output('git rev-parse --abbrev-ref HEAD', shell=True)
        subprocess.check_output('git push origin ' + branch, shell=True)
        __print_success('elsa pushed successfully on ' + branch)
    except subprocess.CalledProcessError as e:
        __print_error('elsa tried to push but something happen with Gitlab...' + e.output)
        sys.exit()


def _print_commit_args_help():
    print(PROMPT_COLOR.BOLD + "------------------------------------------------ Elsa --commit Help  ---------------------------------------------------" + PROMPT_COLOR.RESTORE)
    print("Options:")
    print("-p :  push the commit on the remote current branch (also --push)")
    print('      e.g.: elsa -c 777 -p')
    print
    print("-m :  concat a commit message to the Jira card key (also --message)")
    print('      e.g.: elsa -c 777 -m "add tests for feature" [--push]')
    print
    print(PROMPT_COLOR.BOLD + "------------------------------------------------------------------------------------------------------------------------" + PROMPT_COLOR.RESTORE)


def call_commit_args():
    arg = __get_command_arg(2)
    if arg in ['--help', '-h']:
        _print_commit_args_help()
        sys.exit()

    message = _build_commit_base_name(arg)
    sub_arg = __get_command_arg(3, False)
    push_options = [None, "-p", "--push"]
    if sub_arg in ["-m", "--message"]:
        commit_message = __get_command_arg(4)
        message = message + ': ' + commit_message
    elif sub_arg is not None and sub_arg not in push_options:
        __get_command_arg(99999)

    _git_commit(message)

    if any(a in [sub_arg, __get_command_arg(5, False)] for a in push_options):
        _git_push()
# COMMIT COMMAND METHODS - END


# PROJECT COMMAND METHODS - BEGIN
def _set_env_jira_project():
    try:
        jira_project_key = raw_input('Type the Jira project key to put in the Elsa commit messages, e.g. "ICDMNG": ')
    except KeyboardInterrupt:
        print
        sys.exit()
    print
    print(PROMPT_COLOR.RED + 'Execute the command below to set the Jira project key in the environment variables: ' + PROMPT_COLOR.RESTORE)
    print(PROMPT_COLOR.BOLD + 'export ' + __get_env_jira_project_key() + '=' + jira_project_key + PROMPT_COLOR.RESTORE)
    print


def _print_env_jira_project():
    jira_project = os.getenv(__get_env_jira_project_key())
    print(jira_project if jira_project else 'Jira project key is not set, please execute the following command "elsa -p -s"')


def print_project_args_help():
    print(PROMPT_COLOR.BOLD + "------------------------------------------------ Elsa --project Help  ---------------------------------------------------" + PROMPT_COLOR.RESTORE)
    print("Options:")
    print("-s :  print the command to set the current project Jira key as an environment variable to build commits (also --set)")
    print("      e.g.: elsa -p -s")
    print
    print("-g :  print the current Jira project set as an environment variable (also --get)")
    print("      e.g.: elsa -p -g")
    print(PROMPT_COLOR.BOLD + "-------------------------------------------------------------------------------------------------------------------------" + PROMPT_COLOR.RESTORE)


def call_project_args():
    arg = __get_command_arg(2)

    app_code_commands = {
        '--set': _set_env_jira_project, '-s': _set_env_jira_project,
        '--get': _print_env_jira_project, '-g': _print_env_jira_project,
        '--help': print_project_args_help, '-h': print_project_args_help,
    }
    app_code_commands[arg].__call__()
# PROJECT COMMAND METHODS - END


# PROJECT COMMAND METHODS - BEGIN
def print_args_help():
    print(PROMPT_COLOR.BOLD + "------------------------------------------------------ Elsa Help --------------------------------------------------------" + PROMPT_COLOR.RESTORE)
    print("Options (* = needs an argument):")
    print("-p :  commands related to setup Jira project for commit and push on Gitlab (also --project) *")
    print("      e.g.: elsa -p [--help, --set, --get]")
    print
    print("-c :  commands related to commit and push in Gitlab, receives the number of the jira card to commit (also --commit)")
    print("      e.g.: elsa -c [${jira_card_number}, --help]")
    print(PROMPT_COLOR.BOLD + "-------------------------------------------------------------------------------------------------------------------------" + PROMPT_COLOR.RESTORE)
# PROJECT COMMAND METHODS - BEGIN


# BASE COMMANDS
base_arguments = {
    '--project': call_project_args, '-p': call_project_args,
    '--commit': call_commit_args, '-c': call_commit_args,
    '--help': print_args_help, '-h': print_args_help,
}

if __get_env_jira_project_value() is None:
    print(PROMPT_COLOR.WARNING + "Before executing any elsa command you should complete the following step..." + PROMPT_COLOR.RESTORE)
    _set_env_jira_project()
    sys.exit()


first_arg = __get_command_arg(1)

argument_function = base_arguments[first_arg]

argument_function.__call__()
