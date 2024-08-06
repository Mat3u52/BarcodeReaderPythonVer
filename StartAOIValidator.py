import os
import time


class StartAOIValidator:
    def __init__(self, path_to_txt: str, path_to_barcode_txt: str) -> None:
        self.path_to_txt = path_to_txt
        self.path_to_barcode_txt = path_to_barcode_txt

    def start_on_off(self) -> bool:
        try:
            # Get the absolute path of the file
            names_path = os.path.abspath(self.path_to_txt)
            names_barcode_path = os.path.abspath(self.path_to_barcode_txt)

            # Check if the file exists
            if not os.path.exists(names_path):
                return False

            if not os.path.exists(names_barcode_path):
                return False

            # Get the last modification time of the file
            file_mod_time = os.path.getmtime(names_path)
            file_barcode_mod_time = os.path.getmtime(names_barcode_path)

            # Get the current time
            # current_time = time.time()

            # Check the time difference
            # if (file_barcode_mod_time - file_mod_time) > 10:
            if file_barcode_mod_time > file_mod_time:
                return False

            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False


if __name__ == "__main__":
    obj_StartAOIValidator = StartAOIValidator("C:\\cpi\\data\\currentBoardMode.txt")
    if obj_StartAOIValidator.start_on_off():
        print('File exists and is recently modified')
    else:
        print('File does not exist or is not recently modified')
