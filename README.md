# Project information

* Inspired by Kalle Hallden's [ProjectInitializationAutomation](https://github.com/KalleHallden/ProjectInitializationAutomation).\
* With this project you can use the terminal to create new projects and initialize GitHub repositories.\
* Build for Mac OS.

## Usage:

* To create and initialize a new project open the terminal and type\
    'create <name_of_your_project>' for a private repository\
    'create public <name_of_your_project> for a public reppository

## Installation for Mac OS

### 1) Add code command for opening VS Code in Terminal

1. Launch VS Code.
2. Open the Command Palette (Cmd+Shift+P) and type 'shell command' to find the command named
    "Shell Command: Install 'code' command in PATH".
3. Click on the command.
* Now you will be able to type 'code .' in any folder to start editing files in that folder.
* If a terminal was open, you have to restart it first.


### 2) Create Github Login Token

1. Go to https://github.com/settings/tokens
2. Create a new Login token, checking only the option "repo".
* Do not close the website. You need the token for the next step.
* Once closed, you can't see the token again and have to create a new one.


### 3) Clone this repo as well as create and modify .env file
1. open Terminal and execute:
```
    cd PATH/TO/YOUR/PROJECTS/FOLDER
    mkdir project_creation_automation
    cd project_creation_automation
    git clone https://github.com/maximilian128/project_creation_automation.git .
    pip install -r requirements.txt
    touch .env
    open .env
```
2. Store your username, password, and desired path for new projects.
* The password is the generated token.
* The path must NOT end with a forward slash (/).
* Use the provided format at the bottom of this README.
* Save and close the .env file.
Copy the project_creation_automation folder into the desired path for new projects.

### 4) create my_commands.sh file
* The my_commands.sh file contains custom terminal commands.
* Save this file in your projects folder if you plan to add more custom commands in the future
or directly in the project_creation_automation folder:
1. open Terminal and execute:
```
    cd PATH/TO/YOUR/DESIRED/FOLDER/LOCATION/FOR/THE/CUSTOM_COMMANDS_FILE
    touch my_commands.sh
    open my_commands.sh
```

2. Copy the following function into the file:
```
    #!/bin/bash
    function create() {
        # Uses the create.py file to create a new python project folder
        # as well as a README.md and .gitignore file.
        # write create public NAME_OF_NEW_REPO for a new public repo
        # write create NAME_OF_NEW_REPO for a new private repo

        if [ "$1" != "public" ]
            then
                project_name=$1
                privacy="private"
                shift 1
        elif [ condition ]
            then
                project_name=$2
                privacy="public"
                shift 2
        fi

        mkdir $FP/$project_name
        mkdir $FP/$project_name/.vscode

        cd $FP/$project_name
        conda create --prefix $FP/$project_name/env python=3.10 -y
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
```

### 5) Modify .zshrc file
* If you use Mac OS Mojave or older, do the following with the .bashrc file!
1. open Terminal and execute:
```
    touch ~/.zshrc
    open ~/.zshrc
```
2. Add a new line with "source /PATH/TO/YOUR/MY_COMMANDS_FILE/my_commands.sh"
3. Add a new line with "source /PATH/TO/YOUR/.ENV_FILE/.env"

### 6) Attention:
* Changing the location of the .env or my_commands.sh file will break the procedure.
* If changed, the paths in the .zshrc and the .env file must be respecified.

### 7) ENV File Format:
```
UN="Username123"
PW="Password123"
FP="DESIRED/PATH/TO/NEW/Projects/"
```