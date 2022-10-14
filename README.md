### Usage:
```
To create and initialize a new project open the terminal and type 'create <name_of_your_project>'
If you want a pubblic project, type 'create public <name_of_your_project>
```
## Installation for Mac OS

### 1) Add code command for opening VS Code in Terminal
```
1. Launch VS Code.
2. Open the Command Palette (Cmd+Shift+P) and type 'shell command' to find the Shell Command: Install 'code' command in PATH command.
3. Restart the terminal for the new $PATH value to take effect. You'll be able to type 'code .' in any folder to start editing files in that folder.
```

### 2) Create Github Login Token
```
Go to https://github.com/settings/tokens
Create a new Login token, chekcing only the option "repo".
Don't close the website. You need the token for the next step. Once closed, you can't see the token again and have to create a new one.
```

### 3) CLone this repo as well as create and modify .env file
```
open Terminal and execute:
    cd PATH/TO/YOUR/PROJECTS/FOLDER
    mkdir project_creation_automation
    cd project_creation_automation
    git clone https://github.com/maximilian128/project_creation_automation.git .
    pip install -r requirements.txt
    touch .env
    open .env
Store your username, password, and desired path for new projects.
The password is the generated token.
The path must end with a forward slash (/)
Use the provided format at the bottom of this README.
Save and close the .env file.
Copy the project_creation_automation folder into the desired path for new projects.
```

### 4) create my_commands.sh file
```
Create a file which contains custom terminal commands. Save this file in your projects folder if you plan to add more custom commands in the future or directly in the project_creation_automation folder:
open Terminal and execute:

    cd PATH/TO/YOUR/DESIRED/FOLDER/LOCATION/FOR/THE/CUSTOM_COMMANDS_FILE
    touch my_commands.sh
    open my_commands.sh

Copy the following function into the file:

    #!/bin/bash
    function create() {
    # Uses the create.py file to create a new python project folder as well as a README.md and .gitignore file.
    # write create public NAME_OF_NEW_REPO for a new public repo
    # wirte create NAME_OF_NEW_REPO for a new private repo

    cd $FP/project_creation_automation/
    python create.py $1 $2
    # set standard value for $1:
    ${2:=$1}

    cd $FP$2
    git init
    git remote add origin git@github.com:$UN/$2.git
    git add .
    git commit -m "initial commit"
    git push -u origin master
    code .
}
```

### 5) Modify .zshrc file
```
open Terminal and execute:
    open ~/.zshrc
Add a new line with "source /PATH/TO/YOUR/MY_COMMANDS_FILE/"
    don't forget the my_commands.sh at the end
Add a new line with "source /PATH/TO/YOUR/.ENV_FILE/"
    don't forget the .env at the end
```

### 6) Attention:
```
Keep in mind that changing the location of the .env or my_commands.sh file will break the procedure. If changed, the paths in the .zshrc and the .env file must be respecified.
```

### 7) ENV File Format:
```
UN="Username123"
PW="Password123"
FP="DESIRED/PATH/TO/NEW/Projects/"
```