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
    'delete_repo <name_of_repo_to_delete>'
+ To delete a complete project (git repository AND local files) open terminal and type\
    'delete_complete_project <name_of_project_to_delete>'

* Make sure to spell the commands correctly. There is no checking.

### Example:
* The following command creates a new public project called "this_is_a_new_project" and installs numpy, pandas and matplotlib in the conda environment:
```
create public this_is_a_new_project numpy pandas matplotlib
```

* The following command deletes a repository called "this_is_a_repo":
```
delete_repo this_is_a_repo
```

* The following command deletes a complete project (git repository and all local files) called "this_is_a_project":
```
delete_repo this_is_a_project
```


## Installation for Mac OS

* For the create functionality, you need to have miniconda installed. See [minconda installation](https://docs.conda.io/en/latest/miniconda.html).
* If you have Google Chrome installed, you need to install Chromedriver for the delete functionality to work. Install with [Homebrew](https://formulae.brew.sh/cask/chromedriver) or [manually](https://sites.google.com/chromium.org/driver/downloads).
* Maybe Mac OS won't allow Chromedriver to operate. To give permission, open settings, navigate to "Security and Privacy" and click on the "alllow" button in the bottom half of the page.
* The buttom will be displayed after the first try to use the delete functionality.
* Both functionalities work independently, e.g. you do not need to install Chromedriver if you are using the create functionality only.

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
2. Add two new lines:
```
source PATH/TO/YOUR/PROJECTS/FOLDER/project_creation_automation/my_commands.sh
source PATH/TO/YOUR/PROJECTS/FOLDER/project_creation_automation/.env
```

### 5) Attention:
* Changing the location of the .env or my_commands.sh file (or of the projects folder) will break the procedure.
* If changed, the paths to (or in) the .zshrc and the .env files must be respecified.

### 6) ENV File Format:
```
UN="Username123"
TK="Token123"
PW="Password123"
FP="DESIRED/PATH/TO/NEW/PROJECTS/"
```