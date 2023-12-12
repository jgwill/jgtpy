import subprocess
import sys

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import jgtcommon

import platform

def pwsd_wsl_run_command1(bash_command_to_run):
    powershell_command = 'wsl.exe bash -c \'' + bash_command_to_run + '\''
    result = subprocess.run(
        ["pwsh.exe", "-Command", powershell_command], stdout=subprocess.PIPE, shell=True
    )
    return result.stdout.decode("utf-8")





def run_bash_command_by_platform(bash_cmd):
    if platform.system() == "Windows":
        shell = os.environ.get('COMSPEC', 'cmd.exe')
        if 'powershell' in shell.lower():
            # The interpreter is PowerShell            
            return subprocess.run(bash_cmd, shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8")
        else:
            # The interpreter is cmd.exe
            return wsl_run_bash_on_cmd(bash_cmd)
    else:
        # The system is Linux
        return subprocess.run(bash_cmd, shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8")
    
def wsl_run_bash_on_cmd(bash_cmd):   
    
    powershell_command = 'wsl.exe bash -c \'' + bash_cmd + '\''
    result = subprocess.run(
        ["pwsh.exe", "-Command", powershell_command], stdout=subprocess.PIPE, shell=True
    )
    return result.stdout.decode("utf-8")



def run(bash_command):
    return run_bash_command_by_platform(bash_command)


    
    
def jgtfxcli_wsl1(cli_path, instrument, timeframe, quote_count, verbose_level):
    if cli_path == "" or cli_path is None or cli_path == 0:
        cli_path = "/home/jgi/.local/bin/jgtfxcli"
    bash_command_to_run = f"pwd;{cli_path} -i '{instrument}' -t '{timeframe}' -c {quote_count} -o -v {verbose_level}"
    powershell_command = 'wsl.exe bash -c "' + bash_command_to_run + '"'
    result = subprocess.run(
        ["pwsh.exe", "-Command", powershell_command], stdout=subprocess.PIPE, shell=True
    )
    return result.stdout.decode("utf-8")


def resolve_cli_path(cli_path):
    if cli_path == "" or cli_path is None or cli_path == 0 or cli_path == '0':
        cli_path = '$HOME/.local/bin/jgtfxcli'
    return cli_path #@STCIssue Should install : pip install --user jgtfxcon    (if not found)

def jgtfxcli_wsl(instrument, timeframe, quote_count,cli_path="", verbose_level=0):
    cli_path=resolve_cli_path(cli_path)
    if cli_path == "" or cli_path is None or cli_path == 0 or cli_path == '0':
        cli_path = '$HOME/.local/bin/jgtfxcli'
        #cli_path = "/home/jgi/.local/bin/jgtfxcli"
    bash_command_to_run = f"pwd;{cli_path} -i \"{instrument}\" -t \"{timeframe}\" -c {quote_count} -o -v {verbose_level}"
    return run_bash_command_by_platform(bash_command_to_run)


def _mkbash_cmd_string_jgtfxcli_range(instrument, timeframe,tlid_range=None,cli_path="", verbose_level=0):
    cli_path=resolve_cli_path(cli_path)
    
    date_from,date_to=jgtcommon.tlid_range_to_jgtfxcon_start_end_str(tlid_range)
    
    bash_command_to_run = f"pwd;{cli_path} -i \"{instrument}\" -t \"{timeframe}\" -s \"{date_from}\" -e \"{date_to}\" -o -v {verbose_level}"
    return bash_command_to_run

def jgtfxcli_wsl_range(instrument, timeframe, quote_count,tlid_range=None,cli_path="", verbose_level=0):
    bash_command_to_run = _mkbash_cmd_string_jgtfxcli_range(instrument, timeframe, quote_count,tlid_range,cli_path, verbose_level)
    return run_bash_command_by_platform(bash_command_to_run)

def jgtfxcli(instrument, timeframe, quote_count,cli_path="", verbose_level=0):
    return jgtfxcli_wsl(instrument,timeframe,quote_count,cli_path,verbose_level)

def getPH(instrument, timeframe, quote_count,tlid_range=None, verbose_level=0):
    return jgtfxcli_wsl_range(instrument, timeframe, quote_count,tlid_range,"", verbose_level)


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


minimum_quote_count = 335

# Define the dividers for each timeframe
timeframe_dividers = {
    "m1": 0.0166,
    "mi1": 0.0166,
    "m5": 0.8,
    "m15": 0.25,
    "m30": 0.5,
    "H1": 1,
    "H2": 2,
    "H3": 3,
    "H4": 4,
    "H5": 5,
    "H6": 6,
    "H8": 8,
    "D1": 24,
    "W1": 110,
    "M1": 400
}

#@STCIssue Locks us to H1, should be interactive and receive an input from the user, lower TF
def get_timeframe_dividers(base_tf="H1"):
    return timeframe_dividers[base_tf]
