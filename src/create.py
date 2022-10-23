# annotaions import not necessary from Python 3.11 on
# release on 24th October 2022
from __future__ import annotations

from os import makedirs
from pathlib import Path
from subprocess import run
import sys

from github import Github
from github.GithubException import GithubException, BadCredentialsException

from logger import logger
from user import User


class Creator():
    def __init__(self, user: User) -> None:
        self.user = user


    def create_shell_comand_list(self, command_string: str):
        """ Paths in command_String can be quoted with ' but they don't have to.
            If paths include spaces they must be separated by '!
            If command includes ' and ' is not used to separate a path then this method will fail!
        """
        command_as_list = []
        sections = command_string.split("'")
        for number, section in enumerate(sections):
            if number % 2 == 0:
                for part in section.split(" "):
                    if part != "":
                        command_as_list.append(part)
            else:
                command_as_list.append(section)
        return command_as_list

    def create_new_project(self, project_name: str, privacy: bool, packages_to_install: list):
        project_folder_path = self.get_project_folder_path(project_name)

        self.create_local_files(project_name, project_folder_path)
        # self.create_conda__env(project_name, project_folder_path, packages_to_install)
        self.create_git_repo(project_name, privacy)
        self.add_repo_to_local_files(project_name, project_folder_path)

        logger.info(f"SSuccesfully created project {project_name}.")

    def get_project_folder_path(self, project_name):
        return self.user.path + "/" + project_name

    def create_local_files(self, project_name: str, project_folder_path: str):
        try:
            makedirs(project_folder_path + "/" + ".vscode")
            makedirs(project_folder_path + "/" + "src")
        except FileExistsError as e:
            logger.warning(f"A project called {project_name} already exists.")

        with open(project_folder_path + '/README.md', 'w') as f:
            f.write(f"# {project_name}")

        # copy files from custom_files folder
        run(["cp", str(Path(__file__).parent.parent / "custom_files" / "gitignore.txt"), project_folder_path + "/.gitignore"])
        run(["cp", str(Path(__file__).parent.parent / "custom_files" / "settings.json"), project_folder_path + "/.vscode/settings.json"])

    def create_conda__env(self, project_name: str, project_folder_path: str, packages_to_install: list):

        packages_string = ' '.join(map(str, packages_to_install))

        run(self.create_shell_comand_list(f"conda create --prefix {project_folder_path}/env python=3 -y"))
        if packages_to_install != []:
            run(self.create_shell_comand_list(f"conda run -p {project_folder_path}/env pip install {packages_string}"))


    def create_git_repo(self, project_name: str, privacy: bool):
        try:
            git_user = Github(self.user.username, self.user.token).get_user()
        except BadCredentialsException as e:
            logger.exception("Wrong login credentials.")
        try:
            git_user.create_repo(project_name, private=privacy)
        except GithubException as e:
            logger.warning(f"A repository called {project_name} already exists.")

    def add_repo_to_local_files(self, project_name: str, project_folder_path: str):
        run(cwd=project_folder_path, args=self.create_shell_comand_list(f"git init"))
        run(cwd=project_folder_path, args=self.create_shell_comand_list(f"git remote add origin git@github.com:{self.user.username}/{project_name}.git"))
        run(cwd=project_folder_path, args=self.create_shell_comand_list(f"git add ."))
        run(cwd=project_folder_path, args=self.create_shell_comand_list(f"git commit -m 'initial commit'"))
        run(cwd=project_folder_path, args=self.create_shell_comand_list(f"git push -u origin master"))
        run(cwd=project_folder_path, args=self.create_shell_comand_list(f"code ."))



def main(project_name: str, privacy: bool = True, packages_to_install: list = []):
    """
    Main function controlling the creation of a new project.

    Args:
    ----
        project_name (str): Name of the newproject.
        privacy (bool): True equals privat repository, False equals public repository.
    """
    user = User.by_dot_env()

    # Try Except so that we can run the file for testing purposes from an IDE without a terminal.
    # If run from terminal, project_name and privacy will be reassigned
    try:
        if str(sys.argv[1]) == "public":
            privacy = False
        project_name = str(sys.argv[2])
        packages_to_install = []
        for package in sys.argv[3:]:
            packages_to_install.append(package)
    except IndexError as e:
        logger.info("File runs from IDE. No parameters were given.")
    
    # Create Creator instance and pass project name, selected privacy (public or private repository)
    creator = Creator(user)
    creator.create_new_project(project_name, privacy, packages_to_install)
    


if __name__ == "__main__":
    # project_name and privacy can be set for testing purposes
    main("test_project_1", privacy=True, packages_to_install=["numpy", "shapely"])