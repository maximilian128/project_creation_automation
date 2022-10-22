# annotaions import not necessary from Python 3.11 on
# release on 24th October 2022
from __future__ import annotations

from os import makedirs
from pathlib import Path
from subprocess import run
import sys

from github import Github
from github.GithubException import GithubException, BadCredentialsException

import logging
from logger import logger
# from logger import c_handler, f_handler
from user import User


class Creator():
    def __init__(self, user: User) -> None:
        self.user = user

    def create(self, project_name: str, privacy: bool):
        project_folder_path = self.user.path + "/" + project_name

        try:
            makedirs(project_folder_path + "/" + ".vscode")
        except FileExistsError as e:
            logger.warning(f"A project called {project_name} already exists.")

        with open(project_folder_path + '/README.md', 'w') as f:
            f.write(f"# {project_name}")

        # copy files from custom_files folder
        run(["cp", str(Path(__file__).parent.parent / "custom_files" / "gitignore.txt"), project_folder_path + "/.gitignore"])
        run(["cp", str(Path(__file__).parent.parent / "custom_files" / "settings.json"), project_folder_path + "/.vscode/settings.json"])

        try:
            git_user = Github(self.user.username, self.user.token).get_user()
        except BadCredentialsException as e:
            logger.exception("Wrong login credentials.")
        try:
            git_user.create_repo(project_name, private=privacy)
        except GithubException as e:
            logger.warning(f"A repository called {project_name} already exists.")



def main(project_name: str, privacy: bool):
    """
    Main function controlling the creation of a new project.

    Args:
    ----
        project_name (str): Name of the newproject.
        privacy (bool): True equals privat repository, false equals public repository.
    """
    user = User.by_dot_env()

    # Try Except so that we can run the file for testing purposes from an IDE without a terminal.
    # If run from terminal, project_name and privacy will be reassigned
    try:
        if str(sys.argv[1]) == "private":
            privacy = True
        else:
            privacy = False
        project_name = str(sys.argv[2])
    except IndexError as e:
        logger.info("File runs from IDE. No parameters were given.")
    
    # Create Creator instance and pass project name, path to project, selected privacy (public or private repository)
    creator = Creator(user)
    creator.create(project_name, privacy)


if __name__ == "__main__":
    # project_name and privacy can be set for testing purposes
    main("test_project_1", privacy=False)