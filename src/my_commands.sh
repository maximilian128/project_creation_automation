#!/bin/bash

function create() {
    # Uses the create.py file to create a new python project folder.
    # Usage explained in README.md file.

    if [ "$1" != "public" ]
        then
            project_name=$1
            privacy="private"
            shift 1
    else
            project_name=$2
            privacy="public"
            shift 2
    fi

    # $* are all the packages to install as separate strings
    python $FP/project_creation_automation/src/create.py $privacy $project_name $*
}

function delete() {
    # set delete options to false
    declare -i delete_repo=0
    declare -i delete_local_files=0

    # colon in first position: turn off error messages
    # colon after an option: the option will be followed by an argument
    opt_str=":hp:rl"
    while getopts $opt_str option; do
        case $option in
            h) # display Help
                help_delete;;
            p) # set project name
                project_name=${OPTARG};;
            r) # set delete repo
                declare -i delete_repo=1;;
            l) # set delete local files
                declare -i delete_local_files=1;;
            \?) # Invalid option
                echo "Error: Invalid options."
                return;;
        esac
    done

    # check if a project was given
    if [ "$project_name" = "" ] || \
        [ "$project_name" = " " ] || \
        [ "$project_name" = "-h" ] || \
        [ "$project_name" = "-r" ] || \
        [ "$project_name" = "-l" ]
        then
            echo "Enter a project name."
            return
    fi

     if [ $delete_repo -eq 0 ] && [ $delete_local_files -eq 0 ]
        then
            echo "You need to specify what data you want to delete."
            echo "For help, type 'delete -h'."
            return
    elif [ $delete_repo -eq 1 ] && [ $delete_local_files -eq 0 ]
        then
            echo "Do you really want do delete the git repository of project $project_name?"
    elif [ $delete_repo -eq 0 ] && [ $delete_local_files -eq 1 ]
        then
            echo "Do you really want do delete ALL LOCAL FILES from project $project_name?"
    elif [ $delete_repo -eq 1 ] && [ $delete_local_files -eq 1 ]
        then
            echo "Do you really want do delete the ENTIRE project $project_name? Including ALL LOCAL FILES?"
    fi
    
    echo "Type the name of the project for deleting and 'no' for aborting deletion."
    while true; do
        read input
        echo
        case $input in
            $project_name )
                echo "Please wait."
                python $FP/project_creation_automation/src/delete.py $project_name $delete_repo $delete_local_files
                break;;
            no )
                echo "Aborted deletion!"
                break;;
            * ) echo "Please answer 'name_of_project' or 'no'.";;
        esac
    done

}

function help_create() {
    echo "this is the help_create function."
}

function help_delete() {
    echo "this is the help_delete function."
}