# annotaions import not necessary from Python 3.11 on
# release on 24th October 2022
from __future__ import annotations

from os.path import exists
import sys
from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Safari, Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from user import User


class Remover():
    def __init__(self, driver: Chrome, user: User) -> None:
        # driver can be Safari webdriver, if Chrome is not installed
        self.driver = driver
        self.user = user


    def delete_git_repo(self, project_name: str, wait_period: int = 0) -> None:

        # Open Github Website
        self.driver.get('http://github.com/login')

        # Wait until login form is available and log into account
        self.get_element(By.NAME, value="login").send_keys(self.user.username)
        self.get_element(By.NAME, value="password").send_keys(self.user.password)
        self.get_element(By.NAME, value="commit").click()

        # Wait until user is loged in and go to repository settings.
        # We don't need the element, we just wait until the main page is loaded (that is, we are logged in).
        self.get_element(By.XPATH, value="html/body[@class='logged-in env-production page-responsive full-width']")
        self.driver.get('https://github.com/' + self.user.username + '/' + project_name + '/settings')

        # Check if page (and therefore project) is not found:
        if "Page not found" in self.driver.title:
            print(f"\nThe project {project_name} could not be found on Github!")
        else:
            # Wait until "Delete this repository" button is available and click on it.
            delete_this_repository_button = self.get_element(By.XPATH, value="//*[@id='options_bucket']/div[9]/ul/li[4]/details/summary")
            delete_this_repository_button.click()

            # Wait until the validation_form is available and fill it.
            validation_form = self.get_element(By.XPATH, value="//*[@id='options_bucket']/div[9]/ul/li[4]/details/details-dialog/div[3]/form/p/input")
            validation_form.send_keys(self.user.username + "/" + project_name)

            # Click on the final button for deleting the project.
            final_delete_button = self.get_element(By.XPATH, value="//*[@id='options_bucket']/div[9]/ul/li[4]/details/details-dialog/div[3]/form/button")
            final_delete_button.click()

            print(f"The project {project_name} was removed from Github.")

        sleep(wait_period)
        self.driver.quit()

    def get_element(self, get_by: str, value: str, wait_for:int = 10) -> WebElement:
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
            print(e.msg)
            self.driver.quit()


def main(project_name: str, wait_period: int, option: str = "--headless") -> None:
    user = User.by_dot_env()

    # Try Except so that we can run the file for testing purposes from an IDE without a terminal.
    # If run from terminal, project_name will be reassigned
    try:
        project_name = str(sys.argv[1])
    except:
        print("File runs from IDE. No parameters were given.")

    # Select the browser. Chrome is first choice, because of the option to hide the browser.
    if exists("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"):
        options = ChromeOptions()
        options.add_argument(option)
        driver = Chrome(options=options)
    else:
        driver = Safari()

    # Create Remover instance and call "delete_project" function
    remover = Remover(driver, user)
    remover.delete_git_repo(project_name, wait_period)



if __name__ == "__main__":
    # wait_period: before driver gets closed at the end
    # project_name can be set for testing purposes
    main(project_name="test_project_1", wait_period=0)