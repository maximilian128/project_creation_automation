from pathlib import Path

def create_shell_comand_list(command_string: str):
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

def get_project_folder_path(user_path:str, project_name: str) -> Path:
        return Path(user_path) / project_name