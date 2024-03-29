# annotaions import not necessary from Python 3.11 on
from __future__ import annotations

from os.path import exists
from pathlib import Path
from subprocess import run
from sys import argv

from selenium.common.exceptions import TimeoutException, SessionNotCreatedException
from selenium.webdriver import Safari, Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from helper import create_shell_comand_list, get_project_folder_path
from logger import logger
from user import User


class Remover():
    def __init__(self, user: User) -> None:
        # driver can be Safari webdriver, if Chrome is not installed
        self.driver = self.get_driver("--headless")
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

        # Open Github Website
        self.driver.get('http://github.com/login')

        # Wait until login form is available and log into account
        self.get_web_element(By.NAME, value="login").send_keys(self.user.username)
        self.get_web_element(By.NAME, value="password").send_keys(self.user.password)
        self.get_web_element(By.NAME, value="commit").click()

        # Wait until user is loged in and go to repository settings.
        # We don't need the element, we just wait until the main page is loaded (that is, we are logged in).
        self.get_web_element(By.XPATH, value="html/body[@class='logged-in env-production page-responsive full-width']")
        self.driver.get('https://github.com/' + self.user.username + '/' + project_name + '/settings')

        # Check if page (and therefore project) is not found:
        if "Page not found" in self.driver.title:
            logger.error(f"The project {project_name} could not be found on Github!")
        else:
            # Wait until "Delete this repository" button is available and click on it.
            delete_this_repository_button = self.get_web_element(By.XPATH, value="//*[@id='options_bucket']/div[9]/ul/li[4]/details/summary")
            delete_this_repository_button.click()

            # Wait until the validation_form is available and fill it.
            validation_form = self.get_web_element(By.XPATH, value="//*[@id='options_bucket']/div[9]/ul/li[4]/details/details-dialog/div[3]/form/p/input")
            validation_form.send_keys(self.user.username + "/" + project_name)

            # Click on the final button for deleting the project.
            final_delete_button = self.get_web_element(By.XPATH, value="//*[@id='options_bucket']/div[9]/ul/li[4]/details/details-dialog/div[3]/form/button")
            final_delete_button.click()

            logger.info(f"The project {project_name} was removed from Github.")

        self.driver.quit()

    def delete_local_files(self, project_folder_path: Path):
        if project_folder_path.exists():
            run(create_shell_comand_list(f"rm -rf {project_folder_path}"))
            logger.info("All local files were deleted.")
        else:
            logger.error(f"No local project called {project_folder_path.name}.")

    def get_web_element(self, get_by: str, value: str, wait_for:int = 10) -> WebElement:
        # ID = "id"
        # XPATH = "xpath"
        # LINK_TEXT = "link text"
        # PARTIAL_LINK_TEXT = "partial link text"
        # NAME = "name"
        # TAG_NAME = "tag name"
        # CLASS_NAME = "class name"
        # CSS_SELECTOR = "css selector"
        try:
            return WebDriverWait(self.driver, wait_for).until(EC.presence_of_element_located((get_by, value)))
        except TimeoutException as e:
            logger.error(e)
            print(e.msg)
            self.driver.quit()
            raise TimeoutException
    
    def get_driver(self, option: str):
        # Select the browser. Chrome is first choice, because of the option to hide the browser.
        if exists("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"):
            try:
                options = ChromeOptions()
                options.add_argument(option)
                driver = Chrome(options=options)
            except SessionNotCreatedException as e:
                logger.error(e)
                logger.info("The Safari browser was selected.")
                driver = Safari()
        else:
            driver = Safari()
        return driver

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