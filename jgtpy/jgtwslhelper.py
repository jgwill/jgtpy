import subprocess
import sys

import os


def pwsd_wsl_run_command(bash_command_to_run):
    powershell_command = 'wsl.exe bash -c \'' + bash_command_to_run + '\''
    result = subprocess.run(
        ["pwsh.exe", "-Command", powershell_command], stdout=subprocess.PIPE, shell=True
    )
    return result.stdout.decode("utf-8")

def run(bash_command):
    return pwsd_wsl_run_command(bash_command)

def jgtfxcli_wsl1(cli_path, instrument, timeframe, quote_count, verbose_level):
    if cli_path == "" or cli_path is None:
        cli_path = "/home/jgi/.local/bin/jgtfxcli"
    bash_command_to_run = f"pwd;{cli_path} -i '{instrument}' -t '{timeframe}' -c {quote_count} -o -v {verbose_level}"
    powershell_command = 'wsl.exe bash -c "' + bash_command_to_run + '"'
    result = subprocess.run(
        ["pwsh.exe", "-Command", powershell_command], stdout=subprocess.PIPE, shell=True
    )
    return result.stdout.decode("utf-8")


def jgtfxcli_wsl(instrument, timeframe, quote_count,cli_path="", verbose_level=0):
    if cli_path == "" or cli_path is None:
        cli_path = '$HOME/.local/bin/jgtfxcli'
        #cli_path = "/home/jgi/.local/bin/jgtfxcli"
    bash_command_to_run = f"pwd;{cli_path} -i \"{instrument}\" -t \"{timeframe}\" -c {quote_count} -o -v {verbose_level}"
    return pwsd_wsl_run_command(bash_command_to_run)


def wsl_cd(directory):
    # Define the command to be executed
    command = ["wsl.exe", "cd", directory]

    # Execute the command
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    # Print the error (if any)
    if result.stderr:
        return result.stderr.decode("utf-8")
    else:
        # Print the output
        return result.stdout.decode("utf-8")
        

def cd(tpath):
    wsl_cd(tpath)

def execute_wsl_command_v1_with_cd(directory, command_to_execute):
    # Define the command to be executed
    command = ["wsl.exe", "cd", directory, "&&", command_to_execute]

    # Execute the command
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Print the output
    print(result.stdout.decode("utf-8"))

    # Print the error (if any)
    if result.stderr:
        print("Error:", result.stderr.decode("utf-8"))
