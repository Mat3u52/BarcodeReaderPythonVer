import os
import datetime


class BarcodeReaderLog:
    def __init__(self, log_name: str) -> None:
        self.log_name = f"log\\{log_name}"

    def write_log(self, msg_prog: str, mgs_barcode: str) -> None:

        if not os.path.exists('log'):
            # Create the directory
            os.makedirs('log')
            print(f'Directory "log" created.')
        else:
            print(f'Directory "log" already exists.')

        with open(self.log_name, 'a') as file:
            # Write a line of text to the file
            file.write(f'{datetime.datetime.now()};{msg_prog};{mgs_barcode}\n')
