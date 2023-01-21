#from typing_extensions import Self
from typing import Self

from dotenv import load_dotenv
from dataclasses import dataclass
from os import getenv
from pathlib import Path

from logger import logger


@dataclass
class User():
    username: str
    password: str = ""
    token: str = ""
    projects_path: str = ""

    @classmethod
    def by_dot_env(cls: Self, projects_path: str = None) -> Self:
        """
        Creates a user instance with information from a .env file.

        Parameters
        ----------
        path (str, optional): Path to the .env file. Defaults to None.

        Returns
        -------
            Self: Returns a User instance.
        """
        load_dotenv(projects_path)
        username = getenv("UN")
        password = getenv("PW")
        token = getenv("TK")
        projects_path = getenv("FP")
        return cls(username, password, token, projects_path)


if __name__ == "__main__":
    user = User.by_dot_env()
    print(user)