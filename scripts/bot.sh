#!/bin/bash

# sets 'bot' as temporary command call name for this script
#   alias bot=.scripts/bot.sh

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

command_help=help
command_start=start
command_tail=tail
command_stop=stop
command_check=check
command_restart=restart
command_pyfix=pyfix
command_install=install
command_attach=attach

option_check="-c"
option_force="-f"
option_log="-l"
option_silent="-s"

module="bot"
psname=py-mhbot-7940
output_file=.output
modules_file=files/modules.list
py=python
version_major_req=3
version_minor_req=9
sys_cmds="dos2unix pkill ps grep screen nohup tee tail pidof"

helpmsg="
Usage: $module <command> {args} [options]

  Commands:
    start       starts an instance
    check       displays info about running instances
    tail        displays bot log output in real time
    stop        stops all running instances
    restart     executes <stop> then <start> command
    pyfix       sets up a variable to use another python version
    install     install missing python modules required by the bot
    attach      switch to the instance running screen
    help        displays this help message

  Options:
    -f      ignore command verification and forces execution
            even if a required dependency is missing
    -l      saves output to an extra log file
            <start> and <restart> only    
    -c      check module requirements without installing
            <install> only                      
"
command=$1
options=${@:2}
cmd=""

# parameters
# 1 : module name
# 2 : options
execute_module() {
    $SCRIPT_DIR/$1.sh ${@:2}
}

_echo() {
    if has_option $option_silent
    then
        return 0
    fi
    echo "$@"
}

# specify the option (as a string) to check for as first parameter and $@ as second 
# to look check all options passed into this command
# e.g. 'has_arg -i $@' will search if '-i' is included in the options
# and returns 0 if it is, else 1
has_option() {
    
    if [[ " ${options[*]} " =~ " $1 " ]]
    then
        return 0
    else
        return 1
    fi
}

check_python() {

    command_output="$($py --version 2> /dev/null)"

    # if user defined python is not found
    if [[ -z "$command_output" ]]
    then 
        echo "$py executable not found. Fallback to python."
        py=python
        command_output="$($py --version 2> /dev/null)"

        # if default python is not found
        if [[ -z "$command_output" ]]
        then
            echo "$py executable not found."
            return 1
        fi
    fi

    version=($command_output)
    version_number=${version[1]}
    IFS='.' read -r -a v_array <<< "$version_number"
    version_major=${v_array[0]}
    version_minor=${v_array[1]}

    if [ $version_major -lt $version_major_req ] || [ $version_minor -lt $version_minor_req ]
    then
        echo "The bot may not run with $command_output. (version > 3.9 required)"
        echo "If a correct version is installed under another name, set it with with:"
        echo "  '$module $command_pyfix set [name]'"
        return 1
    fi

    return 0
}

verify_cmds() {
    
    if [ "$command" == "$command_help" ] || [ "$command" == "$command_pyfix" ]
    then
        return
    fi

    if has_option $option_force
    then
        echo "Skipping command requirement checks."
        return
    fi

    exit_code=$((0))

    if ! check_python
    then
        exit_code=$((11))
    fi

    # check system commands
    for sys_cmd in ${sys_cmds[@]}
    do
        if ! $(command -v $sys_cmd 2>&1 > /dev/null) 
        then
            echo "'$sys_cmd' system command not found."
            exit_code=$((11))
        fi
    done

    if [ "$exit_code" -gt 0 ]
    then
        echo
        echo "Cannot run commands due to missings system commands."
        echo "They must be installed for this module to fully work."
        echo
        echo "Use $option_force to ignore system commands requirements and force execution."
        exit $exit_code
    fi
}

start_instance() {

    if screen -list | grep -q "$psname"
    then
        echo "An instance is already running."
        check_instances
        return 1
    fi

    echo "Starting bot instance..."

    log_filepath="/dev/null"

    if has_option $option_log
    then
        mkdir -p .log
        log_filepath=.log/$(date +%d-%m-%Y_%H-%M-%S).output.log
        echo "Output log file: $log_filepath"
    fi
    
    # nohup "$py" -u run.py 2>&1 | tee $log_filepath | tee $output_file > /dev/null &
    
    screen -S $psname -t "titlez" -dm bash -c "$py -u run.py 2>&1 | tee $log_filepath | tee $output_file"

    echo "The instance has started."
} 

tail_output() {

    echo "CTRL + C to exit."
    sleep 2
    tail -f $output_file
}

check_instances() {

    echo "Checking for bot running instances..."

    pids="$(pidof $psname)"
    pid_array=($pids)
    pid_count=${#pid_array[@]}

    # if there is at least one instance running
    if [ "$pid_count" -gt 0 ]
    then
        echo "$pid_count" "instances(s) running".
        echo
        ps -A | grep --color=never -e PID -e "$psname"

        echo 
        echo "Use '$module stop' to stop them all."
    else
        echo "No instance running."
    fi
}

stop_instances() {

    pids="$(pidof $psname)"
    pid_array=($pids)
    pid_count=${#pid_array[@]}

    # if there is at least one instance running
    if [ "$pid_count" -gt 0 ]
    then
        echo "Stopping running instances..."
        pkill $psname
        echo "$pid_count instances stopped."
    else
        echo "No instance running."
    fi
}

restart_instance() {
    stop_instances
    start_instance "$@"
}

# Separates module name, comparator and version from a string line
# used for modules.list file
# function args:
#   $1 module_string
# output array:
#   name [separator] [version]
decompose_requirement() {

    line="$1"
    char='='

    substring=${line##*$char}
    module_name=$line

    # if there is a version requirement
    if [[ ${#substring} -lt ${#line} ]]
    then
        comparator_pos=$(( ${#line} - ${#substring} - ${#char} - 1 ))
        version_pos=$(( $comparator_pos + 2 ))

        module_name=${line:0:comparator_pos}
        comparator=${line:comparator_pos:2}
        version=${line:version_pos}

        echo $module_name" "$comparator" "$version
        return 0
    fi

    echo $module_name
    return 0
}

install_py_module() {
    $py -m pip install --force-reinstall "$1"
}

install_py_modules() {

    reqs=$(dos2unix < "$modules_file")

    for module_line in ${reqs[@]}
    do  
        module=($(decompose_requirement "$module_line"))
        module_name=${module[0]}
        module_comp=${module[1]}
        module_version=${module[2]}
        requires_installation=""

        echo "Checking requirement: $module ..."

        result=$("$py" -m pip --disable-pip-version-check list | grep "$module_name")

        # if the module is installed
        if [[ $result ]]
        then
            result_array=($result)
            installed_version=${result_array[1]}

            echo "  Requires: $module_comp $module_version | Installed: $installed_version"

            # if there is a version requirement
            if [[ $module_version ]]
            then
                # echo "  Requires: $module_comp $module_version | Installed: $installed_version"

                # if installed version is not equal
                if [[ $module_comp == "==" ]] && ! [[ $installed_version == $module_version ]]
                then
                    requires_installation=i
                fi

                # if installed version is not greater 
                if [[ $module_comp == ">=" ]]
                then
                    requires_installation=u
                fi

                # if installed version is not smaller 
                if [[ $module_comp == "<=" ]]
                then
                    
                    requires_installation=u
                fi
            fi 
        else
            echo "  $module_name is not installed"
            requires_installation=i
        fi

        # if its just a check
        if has_option $option_check
        then
            continue
        fi

        # if an installation is required
        if [[ $requires_installation == "i" ]]
        then
            echo "  Installation required."
            install_py_module $module_line
        elif [[ $requires_installation == "u" ]]
        then
            echo "  Unsupported comparaison operator $module_comp"
            echo "  This module will be skipped."
        else
            echo "  OK"
        fi
    done
}

switch_screen() {

    if screen -list | grep -q $psname
    then
        echo '<CTRL + A> <D> to go back'
        sleep 2
    fi
    screen -r $psname
}

show_help() {
    echo "$helpmsg"
}


py=$(execute_module pyfix get)

if [ "$command" == "$command_help" ] 
then # HELP COMMAND
    cmd="show_help"

elif [ "$command" == "$command_start" ]
then # START COMMAND
    cmd="start_instance"

elif [ "$command" == "$command_tail" ]
then # TAIL COMMAND
    cmd="tail_output"

elif [ "$command" == "$command_stop" ]
then # STOP COMMAND
    cmd="stop_instances"

elif [ "$command" == "$command_check" ]
then # CHECK COMMAND
    cmd="check_instances"

elif [ "$command" == "$command_restart" ]
then # RESTART COMMAND
    cmd="restart_instance"

elif [ "$command" == "$command_pyfix" ]
then # PY-FIX COMMAND
    cmd="execute_module"

elif [ "$command" == "$command_install" ]
then # INSTALL COMMAND
    cmd="install_py_modules"

elif [ "$command" == "$command_attach" ]
then # ATTACH COMMAND
    cmd="switch_screen"

elif [ -z "$command" ]
then # UNSPECIFIED COMMAND
    echo "No command specified."
    echo "Use '$module $command_help' to see available ones."
    exit 2

else
    echo "Unrecognized command '$command'"
    echo "Use '$module $command_help' to see available ones."
    exit 3
fi

verify_cmds "$@"
$cmd "$@"
