#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

command_help=help
command_get=get
command_set=set
command_update=update
command_unset=unset
command_check=check

module=pyfix
py=python
pyname_source=DEFAULT
pyname_env=PYNAME_MHBOT
pyname_file=$SCRIPT_DIR/.pyname
pyname_default=python

helpmsg="
Usage: $module <command> {python-name}

  Commands:
    set {python-name}   sets the python command name
    get                 returns the set python name to output
    check               checks which python name is set for use
    unset               removes a name set with '$command_set'
    help                displays this help message

  Description:

    This module main purpose is to set a specific executable name to call
    for cases where the name may differ on each system.
    It is useful when a script/application requires a specific python version to
    be used, and the name under which this version is may be system-specific.

    To achieve this, a call to '$module $command_set {python-name}'
    creates a file '$pyname_file', and stores {python-name} in it.
    Scripts/applications can then retreive {python-name} with '$module $command_get'
    and swap it with 'python' with in command calls.
    Executing '$module $command_unset' removes the set name.
    
    Note that an environment variable named $pyname_env can be set (not with this module) 
    with the desired {python-name} as value, and when '$module $command_get'
    is called, it returns the first found variable, in the following priority:
        File > Environment Variable > Default

  Examples:
        $module set python3     sets python3 as the variable name to use
"

command=$1
options=${@:2}


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

# Updates this script's variable containing python executable name 
# from environment variable or a file.
# This is required if multiple python version are installed on the system
# and the default 'python' version is not high enough.
update_pyname() {

    pyname_from_env=${!pyname_env}
    pyname_from_file=$(cat $pyname_file 2>/dev/null)
    pyname_from_default=$pyname_default

    if ! [[ -z "$pyname_from_file" ]]
    then
        py=$pyname_from_file
        pyname_source="FILE"

    elif ! [[ -z "$pyname_from_env" ]]
    then
        py=$pyname_from_env
        pyname_source="ENV"

    else
        py=$pyname_default
        pyname_source="DEFAULT"
    fi
}

get_pyname() {

    update_pyname
    echo "$py"
}

set_pyname() {

    new_pyname=$2

    if ! [[ $new_pyname =~ ^[a-zA-Z][^\s]+ ]]
    then
        echo "$new_pyname is not a valid executable name."
        return 1
    fi

    echo "${new_pyname:pyname_default}" > $pyname_file
    update_pyname
    echo "Python executable name set to $py"
}

unset_pyname() {

    rm -f $pyname_file
    update_pyname
    echo "Python executable name has been unset from file."
    check_pyname
}

check_pyname() {

    update_pyname
    echo "Python executable name: $py ($pyname_source)"
}

show_help() {

    echo "$helpmsg"
}


cmd=""

if [ "$command" == "$command_help" ] 
then # HELP COMMAND
    cmd="show_help"

elif [ "$command" == "$command_get" ]
then # GET COMMAND
    cmd="get_pyname"

elif [ "$command" == "$command_set" ]
then # SET COMMAND
    cmd="set_pyname"

elif [ "$command" == "$command_check" ]
then # CHECK COMMAND
    cmd="check_pyname"

elif [ "$command" == "$command_update" ]
then # UPDATE COMMAND
    cmd="update_pyname"

elif [ "$command" == "$command_unset" ]
then # UNSER COMMAND
    cmd="unset_pyname"

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

$cmd "$@"