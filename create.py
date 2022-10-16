from os import getenv
import sys

from dotenv import load_dotenv
from github import Github


def create():

    load_dotenv()
    path = getenv("FP")
    username = getenv("UN")
    token = getenv("TK")
    
    if str(sys.argv[1]) == "private":
        privacy = True
    else:
        privacy = False

    project_name = str(sys.argv[2])
    project_folder_path = path + "/" + project_name

    with open(project_folder_path + '/README.md', 'w') as f:
        f.write(f"# {project_name}")
    with open(project_folder_path + '/.gitignore', 'w') as f:
        f.writelines([
            "*.pyc\n",
            "*~\n",
            "__pycache__\n",
            ".DS_Store\n",
            ".vscode\n",
            ".env\n",
            "env"
        ])
    with open(project_folder_path + "/.vscode/settings.json", 'w') as f:
        f.writelines([
            '{ \n',
            '    "python.terminal.activateEnvironment": true,\n',
            f'    "python.defaultInterpreterPath": "{project_folder_path}/env/bin/python",\n',
            '    "python.analysis.typeCheckingMode": "off"\n',
            '}'
        ])

    user = Github(username, token).get_user()
    user.create_repo(project_name, private=privacy)
    print(f"\n Succesfully created project {project_name} \n")


if __name__ == "__main__":
    create()
