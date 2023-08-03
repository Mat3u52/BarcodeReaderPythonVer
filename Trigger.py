import os


class Trigger:
    def __init__(self, path_to_plx: str) -> None:
        self.path_to_plx = path_to_plx

    def turn_on_off(self) -> bool:
        flag_exist: bool = False
        try:
            cwd = os.path.abspath(os.path.dirname(__file__))
            names_path = os.path.abspath(os.path.join(cwd, self.path_to_plx))
            file_plx = open(names_path, 'r').read()
            lines = file_plx.split('\n')
            for line in lines:
                # print(line)
                # print(type(line))
                if line.find("barcode") != -1 or \
                        line.find("Barcode") != -1 or \
                        line.find("BARCODE") != -1:
                    # print("\ntrue")
                    # continue
                    flag_exist = True
                    break
                else:
                    flag_exist = False
            return flag_exist
        except FileExistsError:
            return False
