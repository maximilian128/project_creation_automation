# annotaions import not necessary from Python 3.11 on
# release on 24th October 2022
from __future__ import annotations

from pathlib import Path
from subprocess import run
from sys import argv

from github import Github
from github.GithubException import GithubException, BadCredentialsException

from helper import create_shell_comand_list, get_project_folder_path
from logger import logger
from user import User


class Creator():
    def __init__(self, user: User) -> None:
        self.user = user

    def create_new_project(self, project_name: str, privacy: bool, packages_to_install: list[str]):
        # if run from terminal, get_project_info gets called and reassigns variables
        if len(argv) > 1:
            project_name, privacy, packages_to_install = self.get_project_info()
        else:
            logger.info("File runs from IDE. No parameters were given.")

        project_folder_path = get_project_folder_path(self.user.projects_path, project_name)
        self.create_local_files(project_name, project_folder_path)
        self.create_conda__env(project_name, project_folder_path, packages_to_install)
        self.create_git_repo(project_name, privacy)
        self.add_repo_to_local_files(project_name, project_folder_path)

        # TODO check if everything was indeed successful
        print()
        logger.info(f"Succesfully created project {project_name}.")
        if packages_to_install:
            logger.info(f"Installed packages {packages_to_install}.")
        print()

    def create_local_files(self, project_name: str, project_folder_path: Path):
        try:
            # create directories
            project_folder_path.mkdir()
            (project_folder_path / ".vscode").mkdir()
            (project_folder_path / "src").mkdir()

            # create files
            (project_folder_path / "project_TODO_overview.txt").touch()
            (project_folder_path / "README.md").touch()

            # write initial text to files
            (project_folder_path / "project_TODO_overview.txt").write_text(f"Project goals and way to get there:")
            (project_folder_path / "README.md").write_text(f"# {project_name}")

            # copy files from custom_files folder
            run(["cp", str(Path(__file__).parent.parent / "custom_files" / "gitignore.txt"), project_folder_path / ".gitignore"])
            run(["cp", str(Path(__file__).parent.parent / "custom_files" / "settings.json"), project_folder_path / ".vscode" / "settings.json"])

        except FileExistsError as e:
            # if the project directory already exists none of the above directories and files get created in try block.
            logger.warning(f"A project called {project_name} already exists.")

    def create_conda__env(self, project_name: str, project_folder_path: Path, packages_to_install: list[str]):

        packages_string = ' '.join(map(str, packages_to_install))

        env_path = project_folder_path / "env"
        run(create_shell_comand_list(f"conda create --prefix {env_path} python=3 -y"))
        if packages_to_install != []:
            run(create_shell_comand_list(f"conda run -p {env_path} pip install {packages_string}"))


    def create_git_repo(self, project_name: str, privacy: bool):
        try:
            git_user = Github(self.user.username, self.user.token).get_user()
        except BadCredentialsException as e:
            logger.exception("Wrong login credentials.")
        try:
            git_user.create_repo(project_name, private=privacy)
        except GithubException as e:
            logger.warning(f"A repository called {project_name} already exists.")

    def add_repo_to_local_files(self, project_name: str, project_folder_path: Path):
        run(cwd=project_folder_path, args=create_shell_comand_list(f"git init"))
        run(cwd=project_folder_path, args=create_shell_comand_list(f"git remote add origin git@github.com:{self.user.username}/{project_name}.git"))
        run(cwd=project_folder_path, args=create_shell_comand_list(f"git add ."))
        run(cwd=project_folder_path, args=create_shell_comand_list(f"git commit -m 'initial commit'"))
        run(cwd=project_folder_path, args=create_shell_comand_list(f"git push -u origin master"))
        run(cwd=project_folder_path, args=create_shell_comand_list(f"code ."))

    def get_project_info(self) -> tuple[str, bool, list]:
        if str(argv[1]) == "public":
            privacy = False
        else:
            privacy = True
        project_name = str(argv[2])
        packages_to_install = []
        for package in argv[3:]:
            packages_to_install.append(package)
        return project_name, privacy, packages_to_install



if __name__ == "__main__":
    # project_name,privacy and packages_to_install can be set for testing purposes
    # does not affect call from terminal (see get_project_info method)

    project_name="test_project_1"
    privacy=True
    packages_to_install=["numpy", "shapely"]


    user = User.by_dot_env()
    creator = Creator(user)
    creator.create_new_project(project_name, privacy, packages_to_install)