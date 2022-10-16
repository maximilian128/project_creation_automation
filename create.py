# annotaions import not necessary from Python 3.11 on
# release on 24th October 2022
from __future__ import annotations

from os import getenv
import sys

from dotenv import load_dotenv
from github import Github


class Creator():
    def __init__(self, user: User) -> None:
        self.user = user

    def create(self, project_name: str = "", privacy: bool = True):
        project_folder_path = self.user.path + "/" + project_name

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

        user = Github(self.user.username, self.user.token).get_user()
        user.create_repo(project_name, private=privacy)
        print(f"\n Succesfully created project {project_name} \n")


class User():
    def __init__(self, username, token, path) -> None:
        self.username = username
        self.token = token
        self.path = path


def main():
    # Create user instance and pass username, token and path to projects folder
    load_dotenv()
    path = getenv("FP")
    username = getenv("UN")
    token = getenv("TK")
    user = User(username, token, path)

    if str(sys.argv[1]) == "private":
        privacy = True
    else:
        privacy = False

    project_name = str(sys.argv[2])
    
    # Create Creator instance and pass project name, path to project, selected privacy (public or private repository)
    creator = Creator(user)
    creator.create(project_name, privacy)


if __name__ == "__main__":
    main()