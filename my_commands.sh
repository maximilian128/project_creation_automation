#!/bin/bash

function create() {
    # Uses the create.py file to create a new python project folder
    # as well as a README.md and .gitignore file.
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

    python $FP/project_creation_automation/create.py $privacy $project_name
    # python file creates "$FP/project_name/.vscode" folder, among doing other things

    cd $FP/$project_name
    conda create --prefix $FP/$project_name/env python=3 -y
    conda activate $FP/$project_name/env
    for package in $*
        pip install $package
    conda deactivate

    git init
    git remote add origin git@github.com:$UN/$project_name.git
    git add .
    git commit -m "initial commit"
    git push -u origin master
    code .
    echo
    echo "Succesfully created project $project_name."
    echo
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
                python $FP/project_creation_automation/delete.py $project_name
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
                python $FP/project_creation_automation/delete.py $project_name
                rm -rf $FP/$project_name
                echo "All local project files deleted."
                break;;
            no )
                echo "Aborted deletion!"
                break;;
            * ) echo "Please answer 'name_of_project' or 'no'.";;
        esac
    done
}