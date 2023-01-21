# annotaions import not necessary from Python 3.11 on
from __future__ import annotations

from os.path import exists
from pathlib import Path
from subprocess import run
from sys import argv

from github import Github
from github.GithubException import GithubException, BadCredentialsException

from helper import create_shell_comand_list, get_project_folder_path
from logger import logger
from user import User


class Remover():
    def __init__(self, user: User) -> None:
        # driver can be Safari webdriver, if Chrome is not installed
        self.user = user


    def delete_project(self, project_name: str, del_repo: bool, del_local: bool):
        try:
            if len(argv) > 1:
                project_name, del_repo, del_local = self.get_del_info()
            else:
                logger.info("File runs from IDE. No parameters were given.")

            project_folder_path = get_project_folder_path(self.user.projects_path, project_name)

            if del_repo:
                self.delete_git_repo(project_name)
            if del_local:
                self.delete_local_files(project_folder_path)
        except Exception as e:
            logger.exception("Something went wrong!")


    def delete_git_repo(self, project_name: str) -> None:
        try:
            git_user = Github(self.user.username, self.user.token).get_user()
        except BadCredentialsException as e:
            logger.exception("Username or token credentials are wrong or outdated.")
            raise e
        try:
            git_user.get_repo(project_name).delete()
            logger.info("The Github repository was deleted.")
        except GithubException as e:
            logger.warning(f"A repository called {project_name} does not exist.")


    def delete_local_files(self, project_folder_path: Path):
        if project_folder_path.exists():
            run(create_shell_comand_list(f"rm -rf {project_folder_path}"))
            logger.info("All local files were deleted.")
        else:
            logger.error(f"No local project called {project_folder_path.name}.")


    def get_del_info(self):
        project_name = str(argv[1])
        del_repo = bool(int(argv[2]))
        del_local = bool(int(argv[3]))
        return project_name, del_repo, del_local



if __name__ == "__main__":
    # project_name, del_repo and del_local can be set for testing purposes
    # does not affect call from terminal (gets overridden in remover.delete_project method)

    project_name = "test_project_1"
    del_repo = True
    del_local = True

    user = User.by_dot_env()
    remover = Remover(user)
    remover.delete_project(project_name, del_repo, del_local)