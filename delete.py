# annotaions import not necessary from Python 3.11 on
# release on 24th October 2022
from __future__ import annotations

from os import getenv
from os.path import exists
import sys
from time import sleep

from dotenv import load_dotenv
from selenium.webdriver import Safari, Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Remover():
    def __init__(self, driver: Chrome, user: User) -> None:
        # driver can be Safari webdriver, if Chrome is not installed
        self.driver = driver
        self.user = user


    def delete_project(self, project_name: str, wait_period: int = 0) -> None:

        # Open Github Website
        self.driver.get('http://github.com/login')

        # Wait until login form is available and log into account
        self.get_element_by_name(name="login").send_keys(self.user.username)
        self.get_element_by_name(name="password").send_keys(self.user.password)
        self.get_element_by_name(name="commit").click()

        # Wait until user is loged in and go to repository settings.
        # We don't need the element, we just wait until the main page is loaded (that is, we are logged in).
        self.get_element_by_x_path(x_path="html/body[@class='logged-in env-production page-responsive full-width']")
        self.driver.get('https://github.com/' + self.user.username + '/' + project_name + '/settings')

        # Check if page (and therefore project) is not found:
        if "Page not found" in self.driver.title:
            print(f"The project {project_name} could not be found on Github!")
            print()
        else:
            # Wait until "Delete this repository" button is available and click on it.
            delete_this_repository_button = self.get_element_by_x_path(x_path="//*[@id='options_bucket']/div[9]/ul/li[4]/details/summary")
            delete_this_repository_button.click()

            # Wait until the validation_form is available and fill it.
            validation_form = self.get_element_by_x_path(x_path="//*[@id='options_bucket']/div[9]/ul/li[4]/details/details-dialog/div[3]/form/p/input")
            validation_form.send_keys(self.user.username + "/" + project_name)

            # Click on the final button for deleting the project.
            final_delete_button = self.get_element_by_x_path(x_path="//*[@id='options_bucket']/div[9]/ul/li[4]/details/details-dialog/div[3]/form/button")
            final_delete_button.click()

            print(f"The project {project_name} was removed from Github.")
            print()

        sleep(wait_period)
        self.driver.quit()

    # currently not in use
    def get_element_by_id(self, id: str) -> WebElement:
        try:
            return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, id)))
        except:
            self.driver.quit()

    def get_element_by_name(self, name: str) -> WebElement:
        try:
            return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, name)))
        except:
            self.driver.quit()

    def get_element_by_x_path(self, x_path: str) -> WebElement:
        try:
            return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, x_path)))
        except:
            self.driver.quit()


class User():
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password


def main(wait_period) -> None:
    # Try Except so that we can run the file for testing purposes from an IDE without a terminal.
    # Set the project name for testing this file in the except block!
    try:
        project_name = str(sys.argv[1])
    except:
        project_name = "ddd"

    # Create user instance and pass username and password
    load_dotenv()
    username = getenv("UN")
    password = getenv("PW")
    user = User(username, password)

    # Select the browser. Chrome is first choice, because of the option to hide the browser.
    if exists("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"):
        options = ChromeOptions()
        options.add_argument("--headless")
        driver = Chrome(options=options)
    else:
        driver = Safari()

    # Create Remover instance and call "delete_project" function
    remover = Remover(driver, user)
    remover.delete_project(project_name, wait_period)



if __name__ == "__main__":
    main(wait_period=0)