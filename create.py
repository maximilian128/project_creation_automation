import sys
import os

from dotenv import load_dotenv
from github import Github


def create():

    load_dotenv()
    path = os.getenv("FP")
    username = os.getenv("UN")
    password = os.getenv("PW")

    privacy = True
    if len(sys.argv) == 2:
        folderName = str(sys.argv[1])
    else:
        folderName = str(sys.argv[2])
        if str(sys.argv[1]) == "public":
            privacy = False
    
    os.makedirs(path + str(folderName))
    path += str(folderName + "/")
    with open(path + '.gitignore', 'w') as f:
        f.write("*.pyc \n *~ \n __pycache__ \n .DS_Store \n .vscode \n .env \n env")
    with open(path + 'README.md', 'w') as f:
        f.write(f"# {folderName}")

    user = Github(username, password).get_user()
    user.create_repo(folderName, private=privacy)
    print(f"\n Succesfully created project {folderName} \n")


if __name__ == "__main__":
    create()


"""
variable
help page


"""