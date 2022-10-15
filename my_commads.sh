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
        then
            project_name=$2
            privacy="public"
            shift 2
    fi

    mkdir $FP/$project_name
    mkdir $FP/$project_name/.vscode

    cd $FP/$project_name
    conda create --prefix $FP/$project_name/env python=3 -y
    conda activate $FP/$project_name/env
    for package in $*
        pip install $package
    conda deactivate

    python $FP/project_creation_automation/create.py $privacy $project_name

    git init
    git remote add origin git@github.com:$UN/$project_name.git
    git add .
    git commit -m "initial commit"
    git push -u origin master
    code .
}

function delete() {
    echo placeholdertext
}