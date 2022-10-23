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

    python $FP/project_creation_automation/src/create.py $privacy $project_name $*
}

function delete_repo() {
    project_name=$1
    echo
    echo "Do you really want do delete the git repository of project $project_name?"
    echo "Type 'name_of_project' for deleting and 'no' for aborting deletion."
    while true; do
        read input
        echo
        case $input in
            $project_name )
                echo "Please wait."
                python $FP/project_creation_automation/src/delete.py $project_name
                break;;
            no )
                echo "Aborted deletion!"
                break;;
            * ) echo "Please answer 'name_of_project' or 'no'.";;
        esac
    done
}

function delete_complete_project() {
    project_name=$1
    echo
    echo "Do you really want do delete the ENTIRE project $project_name? including LOCAL files?"
    echo "There is no going back after deleting!"
    echo "Type 'name_of_project' for deleting and 'no' for aborting deletion."
    while true; do
        read input
        echo
        case $input in
            $project_name )
                echo "Please wait."
                python $FP/project_creation_automation/src/delete.py $project_name
                rm -rf $FP/$project_name
                echo "All local project files deleted."
                echo
                break;;
            no )
                echo "Aborted deletion!"
                break;;
            * ) echo "Please answer 'name_of_project' or 'no'.";;
        esac
    done
}