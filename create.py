import sys
import os

from dotenv import load_dotenv
from github import Github

def create():

    load_dotenv()
    path = os.getenv("FP")
    username = os.getenv("UN")
    password = os.getenv("PW")

    privacy = True
    if len(sys.argv) == 2:
        folderName = str(sys.argv[1])
    else:
        folderName = str(sys.argv[2])
        if str(sys.argv[1]) == "public":
            privacy = False
    
    project_folder_path = path + "/" + str(folderName)
    os.makedirs(project_folder_path)
    os.makedirs(project_folder_path + "/.vscode")

    with open(project_folder_path + '/.gitignore', 'w') as f:
        f.write("*.pyc \n *~ \n __pycache__ \n .DS_Store \n .vscode \n .env \n env")
    with open(project_folder_path + '/README.md', 'w') as f:
        f.write(f"# {folderName}")
    with open(project_folder_path + "/.vscode/settings.json", 'w') as f:
        f.writelines([
            '{ \n',
            '    "python.terminal.activateEnvironment": true, \n',
            f'    "python.defaultInterpreterPath": "{project_folder_path}/env/bin/python", \n',
            '    "python.analysis.typeCheckingMode": "off" \n',
            '}'
        ])

    user = Github(username, password).get_user()
    user.create_repo(folderName, private=privacy)
    print(f"\n Succesfully created project {folderName} \n")


if __name__ == "__main__":
    create()


"""
variable
help page


"""