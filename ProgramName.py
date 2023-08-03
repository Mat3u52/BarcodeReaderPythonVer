import os


class ProgramName:
    def __init__(self, path_to_names: str) -> None:
        """
        Initiate the path to the file named 'names'. The file contain information about using program currently.

        :param path_to_names: Given the path to directory with file named names.txt
        :type path_to_names: str
        :return: Initialization of variables
        :rtype: None
        """

        self.path_to_names = path_to_names

    def read_program_name_one(self) -> str:
        """
        The function read the file and gives line with recipe name.

        :return: Name of the recipe
        :rtype: str
        """
        container_names: list[str] = []
        cwd = os.path.abspath(os.path.dirname(__file__))
        names_path = os.path.abspath(os.path.join(cwd, self.path_to_names))
        file_names = open(names_path, 'r').read()
        lines = file_names.split('\n')
        for line in lines:
            container_names.append(line)

        return container_names[0][2:-4]

    def read_program_name_many(self) -> list:
        """
        The function read the file and gives list of all lines.

        :return: list of all lines
        :rtype: list
        """
        container_names: list[str] = []
        cwd = os.path.abspath(os.path.dirname(__file__))
        names_path = os.path.abspath(os.path.join(cwd, self.path_to_names))
        file_names = open(names_path, 'r').read()
        lines = file_names.split('\n')
        for line in lines:
            container_names.append(line)

        return container_names
