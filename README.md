# Project information

* With this project you can use the terminal to create new Python projects and initialize GitHub repositories as well as delete existing projects.
* When creating a new project, a conda environment is created within the project folder.

+ Build for Mac OS.
+ Inspired by Kalle Hallden's [ProjectInitializationAutomation](https://github.com/KalleHallden/ProjectInitializationAutomation).

## Usage:

* To create and initialize a new project open the terminal and type\
    'create <name_of_your_project> <name_of_packages_to_install>' for a private repository\
    'create public <name_of_your_project> <name_of_packages_to_install> for a public reppository
* The packages need to be seperated by spaces.
* Projects must be named without spaces. ("new_project" instead of "new project")

+ To delete a git repository open the terminal and type\
    'delete -p <name_of_repo_to_delete> -r'
+ To delete ALL LOCAL FILES of a project open the terminal and type\
    'delete -p <name_of_project_to_delete> -l'
+ To delete a git repository and ALL LOCAL FILES open the terminal and type\
    'delete -p <name_of_project_to_delete> -r -l'

* Make sure to spell the commands correctly. There is no checking.
* If the automated deletion does not work it may be the case that you have to log in manually once in a while.

### Example:
* The following command creates a new public project called "this_is_a_new_project" and installs numpy, pandas and matplotlib in the conda environment:
```
create public this_is_a_new_project numpy pandas matplotlib
```

* The following command deletes all local files of a project called "this_is_a_repo":
```
delete -p this_is_a_repo -l
```


## Installation for Mac OS

* For the create functionality, you need to have miniconda installed. See [minconda installation](https://docs.conda.io/en/latest/miniconda.html).


### 1) Add code command for opening VS Code in Terminal

1. Launch VS Code.
2. Open the Command Palette (Cmd+Shift+P) and type 'shell command' to find the command named
    "Shell Command: Install 'code' command in PATH".
3. Click on the command.
* Now you will be able to type 'code .' in any folder to start editing files in that folder.
* If a terminal was open, you have to restart it first.


### 2) Create Github Login Token

1. Go to https://github.com/settings/tokens
2. Create a new Login token, checking  the option "repo" and "delete_repo".
* Do not close the website. You need the token for the next step.
* Once closed, you can't see the token again and have to create a new one.


### 3) Clone this repo, install requirements and create and modify .env file
1. Open terminal and execute:
```
    cd PATH/TO/YOUR/PROJECTS/FOLDER
    mkdir project_creation_automation
    cd project_creation_automation
    git clone https://github.com/maximilian128/project_creation_automation.git .
    pip install -r requirements.txt
    touch .env
    open .env
```
2. Store your username, password, token and desired path for new projects.
* TK is the generated token.
* PW is your normal password.
* The path must NOT end with a forward slash (/).
* Use the provided format at the bottom of this README.
* Save and close the .env file.

### 4) Modify .zshrc file
* If you use Mac OS Mojave or older, do the following with the .bashrc file!
1. Open terminal and execute:
```
    touch ~/.zshrc
    open ~/.zshrc
```
2. Add two new lines:
```
source PATH/TO/YOUR/PROJECTS/FOLDER/project_creation_automation/my_commands.sh
source PATH/TO/YOUR/PROJECTS/FOLDER/project_creation_automation/.env
```

### 4) Modify custom files
* in the custom_files folder in this project are a gitignore.txt and a settings.json file.
* these files get copied to a newly created project.
* modify these files according to your needs.
* if you need more custom files in every new project, add them into the custom_files folder and modify the create_local_files method within the create.py file to specify where these files should get copied to.

### Attention:
* Changing the location of the .env or my_commands.sh file (or of the projects folder) will break the procedure.
* If changed, the paths to (or in) the .zshrc and the .env files must be respecified.

### ENV File Format:
```
UN="Username123"
TK="Token123"
PW="Password123"
FP="DESIRED/PATH/TO/NEW/PROJECTS"
```