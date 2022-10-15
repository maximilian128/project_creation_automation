# Project information

* Inspired by Kalle Hallden's [ProjectInitializationAutomation](https://github.com/KalleHallden/ProjectInitializationAutomation).
* With this project you can use the terminal to create new Python projects and initialize GitHub repositories.
* A conda environment is created within the projects folder.
* Build for Mac OS.

## Usage:

* To create and initialize a new project open the terminal and type\
    'create <name_of_your_project> <name_of_packages_to_install>' for a private repository\
    'create public <name_of_your_project> <name_of_packages_to_install> for a public reppository
* The packages need to be seperated by spaces.
+ Make sure to spell the command correctly. There is no checking.

### Example:
```
create public this_is_a_new_project numpy pandas matplotlib
```
* This command creates a new public project called "this_is_a_new_project" and installs numpy, pandas and matplotlib in the conda environment.

## Installation for Mac OS

* You need to have miniconda installed. See [minconda installation](https://docs.conda.io/en/latest/miniconda.html).

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
2. Store your username, password, and desired path for new projects.
* The password is the generated token.
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
2. Add a new line with "source PATH/TO/YOUR/PROJECTS/FOLDER/project_creation_automation/my_commands.sh"
3. Add a new line with "source PATH/TO/YOUR/PROJECTS/FOLDER/project_creation_automation/.ENV_FILE/.env"

### 5) Attention:
* Changing the location of the .env or my_commands.sh file (or of the projects folder) will break the procedure.
* If changed, the paths to (or in) the .zshrc and the .env files must be respecified.

### 6) ENV File Format:
```
UN="Username123"
PW="Password123"
FP="DESIRED/PATH/TO/NEW/PROJECTS/"
```