import serial
import os
import time
import tkinter.messagebox
from datetime import datetime
from ProgramName import ProgramName
from Trigger import Trigger
from BarcodeNotification import BarcodeNotification

# pyinstaller -F --paths=C:\BarcodeReaderPythonVer\venv\Lib\site-packages C:\BarcodeReaderPythonVer\main.py
# pyinstaller -F --paths=C:\BarcodeReaderPythonVer\venv\Lib\site-packages C:\BarcodeReaderPythonVer\main.py --noconsole
# C:\Users\tczmkolo\dist

try:
    ser = serial.Serial(port='COM10',
                        baudrate=115200,  # 9600
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=0)
    obj_welcome_notification = BarcodeNotification("Connection to COM10 is successful", "Connected")
    obj_welcome_notification.show_notification("Ready to intercept!")
    try:
        barcode_init = open('C:\\cpi\\barcode\\barcodelist.bar', 'w')
        barcode_init.write("Barcode0")
        barcode_init.close()
        if os.path.exists('C:\\Defects\\BuyOffControl.exe'):
            os.rename('C:\\Defects\\BuyOffControl.exe', 'C:\\Defects\\BuyOffControl0.exe')
        amount_of_file_vvts = os.listdir('C:\\Defects\\ComportSignal')  # TODO if not exist create
        for file_vvts in amount_of_file_vvts:
            os.remove(f"C:\\Defects\\ComportSignal\\{file_vvts}")
        amount_of_file_index = os.listdir('C:\\Defects\\index')
        for file_index in amount_of_file_index:
            os.remove(f"C:\\Defects\\index\\{file_index}")
    except FileNotFoundError:
        exit()
except serial.SerialException:
    root = tkinter.Tk()
    root.withdraw()
    tkinter.messagebox.showinfo("Connection Error!", "COM 10 does not exist!", icon='error')
    exit()

convert_barcode: str = ""
captured_barcode_str: list = []
flag_ready_to_send: bool = False
ASCII_SELECTED: tuple = (48, 49, 50, 51, 52, 53, 54, 55, 56, 57,

                         65, 66, 67, 68, 69, 70, 71, 72, 73, 74,
                         75, 76, 77, 78, 79, 80, 81, 82, 83, 84,
                         85, 86, 87, 88, 89, 90,

                         97, 98, 99, 100, 101, 102, 103, 104, 105,
                         106, 107, 108, 109, 110, 111, 112, 113, 114,
                         115, 116, 117, 118, 119, 120, 121, 122,
                         )
INVALID_BARCODE: tuple = ('NOREAD', 'noread', 'NoRead',)


if __name__ == "__main__":

    obj_prog_name = ProgramName("C:\\cpi\\data\\names.txt")

    while True:
        #  turn on BuyOffControl - Start
        amount_of_file_index = os.listdir('C:\\Defects\\index')
        for file_index in amount_of_file_index:
            if str(file_index) == 'testPermission.txt':
                if os.path.exists('C:\\Defects\\BuyOffControl.exe'):
                    os.rename('C:\\Defects\\BuyOffControl.exe', 'C:\\Defects\\BuyOffControl0.exe')
                    process_name = "BuyOffControl"
                    try:
                        killed = os.system('tskill ' + process_name)
                    except Exception:
                        pass
        #  turn on BuyOffControl - The End

        for line in ser.read():
            if line in ASCII_SELECTED:
                captured_barcode_str.append(chr(line))
            if line == 10:  # ascii 10 == Line Feed
                convert_barcode = ''.join(captured_barcode_str)

                print(f"join: {convert_barcode}")
                if (convert_barcode in INVALID_BARCODE) or (len(convert_barcode) > 14) or (len(convert_barcode) < 8):
                    convert_barcode = 'Barcode0'

                file = open('barcode02.txt', 'w')
                file.write(convert_barcode)
                file.close()
                flag_ready_to_send = True
                convert_barcode = ""
                captured_barcode_str.clear()

        # start to send the barcode to AOI
        if flag_ready_to_send is True:
            file_to_read = open('barcode02.txt')
            content = file_to_read.read()
            file_to_read.close()
            print(f"Contents of barcode02 file: {content}")

            flag_ready_to_send = False

            barcode_list = open('C:\\cpi\\barcode\\barcodelist.bar')
            barcode_list_get = barcode_list.read()
            barcode_list.close()

            print(time.strftime("%m/%d/%Y %I:%M:%S %p", time.localtime()))
            datestamp = time.strftime("%m/%d/%Y %I:%M:%S %p", time.localtime())

            if barcode_list_get == 'Barcode0':
                obj_trigger = Trigger(f"C:\\cpi\\cad\\{obj_prog_name.read_program_name_one()}.plx")
                print(f"C:\\cpi\\cad\\{obj_prog_name.read_program_name_one()}.plx")

                # Save for multiple recipe ERBHROA1287281_11R1B-BOTL1 / ERBHROA1287281_11R1B-BOTL2
                if str(obj_prog_name.read_program_name_one()[-2:]) == "L1" and obj_trigger.turn_on_off() is not True:
                    print(f"\n{obj_prog_name.read_program_name_one()[-2:]}\n")

                    # if obj_trigger.turn_on_off() is True:  # Check the .plx file
                    print("The recipe is not able to read barcode.")
                    barcode_list = open('C:\\cpi\\barcode\\barcodelist.bar', 'w')
                    barcode_list.write(
                        f"#Board: {obj_prog_name.read_program_name_one()}, {datestamp}\n\n#Number Of Panel	Barcode\nBarcode#1	*{content}\n#End")
                    barcode_list.close()
                    print("Ready!")
                    obj_notification = BarcodeNotification(str(obj_prog_name.read_program_name_one()), str(content))
                    obj_notification.show_notification(str(datestamp))

                    print("\n--------------------------------------\n")
                    print(f"ProgramName: {obj_prog_name.read_program_name_many()}")
                    print("\n--------------------------------------\n")

                    print(f"C:\\cpi\\cad\\{obj_prog_name.read_program_name_one()}.plx")
                    # else:
                    print("The recipe is able to read barcode.")

                    status_info = os.stat("C:\\cpi\\data\\names.txt")
                    modified_date = datetime.fromtimestamp(status_info.st_mtime)
                    modified_date_l1 = modified_date.strftime("%Y%m%d%H%M")

                    time.sleep(1)
                    while True:
                        print(f"\nI am waiting for switch to another recipe...\n")
                        status_info1 = os.stat("C:\\cpi\\data\\names.txt")
                        modified_date1 = datetime.fromtimestamp(status_info1.st_mtime)
                        modified_date_l2 = modified_date1.strftime("%Y%m%d%H%M")

                        barcode_list = open('C:\\cpi\\barcode\\barcodelist.bar')
                        barcode_list_get = barcode_list.read()
                        barcode_list.close()

                        if (int(modified_date_l1) < int(modified_date_l2)) and barcode_list_get == 'Barcode0':
                            time.sleep(1)
                            print("The recipe is not able to read barcode.")
                            barcode_list = open('C:\\cpi\\barcode\\barcodelist.bar', 'w')
                            barcode_list.write(
                                f"#Board: {obj_prog_name.read_program_name_one()}, {datestamp}\n\n#Number Of Panel	Barcode\nBarcode#1	*{content}\n#End")
                            barcode_list.close()
                            print("Ready!")

                            print("\n--------------------------------------\n")
                            print(f"ProgramName from L2 suffix: {obj_prog_name.read_program_name_many()}")
                            print("\n--------------------------------------\n")
                            break

                else:
                    # Save for usual recipe
                    if obj_trigger.turn_on_off() is not True:  # Check the .plx file
                        print("The recipe is not able to read barcode.")
                        # if content is barcode0 than save only barcode0 to barcodelist.bar, but I am not sure(??)
                        barcode_list = open('C:\\cpi\\barcode\\barcodelist.bar', 'w')
                        barcode_list.write(f"#Board: {obj_prog_name.read_program_name_one()}, {datestamp}\n\n#Number Of Panel	Barcode\nBarcode#1	*{content}\n#End")
                        barcode_list.close()

                        obj_notification = BarcodeNotification(str(obj_prog_name.read_program_name_one()), str(content))
                        obj_notification.show_notification(str(datestamp))

                        print("Ready!")

                        # test of multiple recipes
                        print("\n--------------------------------------\n")
                        print(f"ProgramName: {obj_prog_name.read_program_name_many()}")
                        print("\n--------------------------------------\n")

                        print(f"C:\\cpi\\cad\\{obj_prog_name.read_program_name_one()}.plx")
                    else:
                        print("Single Recipe - The recipe is able to read barcode.")

                #  turn on BuyOffControl - Start
                if os.path.exists('C:\\Defects\\BuyOffControl0.exe'):
                    os.rename('C:\\Defects\\BuyOffControl0.exe', 'C:\\Defects\\BuyOffControl.exe')
                #  turn on BuyOffControl - The End

    ser.close()  # for the moment it is out of reach
