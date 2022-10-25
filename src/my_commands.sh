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

function delete_repo() {
    project_name=$1
    delete_project $project_name
}

function delete_project() {

    if [ "$1" != "all" ]
        then
            project_name=$1
            del_local="no"
            echo
            echo "Do you really want do delete the git repository of project $project_name?"
    else
            project_name=$2
            del_local="yes"
            echo
            echo "Do you really want do delete the ENTIRE project $project_name? including LOCAL files?"
            echo "There is no going back after deleting!"
    fi

    echo "Type 'name_of_project' for deleting and 'no' for aborting deletion."
    while true; do
        read input
        echo
        case $input in
            $project_name )
                echo "Please wait."
                python $FP/project_creation_automation/src/delete.py $del_local $project_name
                break;;
            no )
                echo "Aborted deletion!"
                break;;
            * ) echo "Please answer 'name_of_project' or 'no'.";;
        esac
    done
}

# TODO make one delete function with optional flags --all, --repo, --local and call corresponding functions
# functions could be delete_all, delete_repo, delete_local