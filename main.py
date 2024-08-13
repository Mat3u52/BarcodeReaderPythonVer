import serial
import os
import time
import json
import tkinter.messagebox
from datetime import datetime
from ProgramName import ProgramName
from Trigger import Trigger
from BarcodeNotification import BarcodeNotification
from StartAOIValidator import StartAOIValidator
from BarcodeReaderLog import BarcodeReaderLog
# import logging

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

        if os.path.exists('C:\\Defects\\ComportSignal'):
            amount_of_file_vvts = os.listdir('C:\\Defects\\ComportSignal')
        else:
            os.mkdir('C:\\Defects\\ComportSignal')
            amount_of_file_vvts = os.listdir('C:\\Defects\\ComportSignal')

        for file_vvts in amount_of_file_vvts:
            os.remove(f"C:\\Defects\\ComportSignal\\{file_vvts}")
        amount_of_file_index = os.listdir('C:\\Defects\\index')
        for file_index in amount_of_file_index:
            os.remove(f"C:\\Defects\\index\\{file_index}")

        if os.path.exists('C:\\cpi\\barcode\\log\\readerLog.txt'):
            os.remove(f"C:\\cpi\\barcode\\log\\readerLog.txt")
        if os.path.exists('C:\\cpi\\barcode\\log\\AOILog.txt'):
            os.remove(f"C:\\cpi\\barcode\\log\\AOILog.txt")
        if os.path.exists('C:\\cpi\\barcode\\log\\VVTSLog.txt'):
            os.remove(f"C:\\cpi\\barcode\\log\\VVTSLog.txt")
        if os.path.exists('C:\\cpi\\barcode\\log\\progLog.txt'):
            os.remove(f"C:\\cpi\\barcode\\log\\progLog.txt")

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
flag_pass: bool = True
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
    obj_barcode_reader_log = BarcodeReaderLog("readerLog.txt")
    obj_barcode_aoi_log = BarcodeReaderLog("AOILog.txt")
    obj_barcode_vvts_log = BarcodeReaderLog("VVTSLog.txt")
    obj_barcode_prog_log = BarcodeReaderLog("progLog.txt")


    obj_prog_name = ProgramName("C:\\cpi\\data\\names.txt")

    obj_barcode_vvts_flag = False
    index_temp: str = ""
    prog_temp: str = ""
    while True:
        #  turn on BuyOffControl - Start

        amount_of_file_index = os.listdir('C:\\Defects\\index')
        file_index = ""
        for file_index in amount_of_file_index:
            if str(file_index) == 'testPermission.txt':

                if os.path.exists('C:\\Defects\\BuyOffControl.exe'):
                    os.rename('C:\\Defects\\BuyOffControl.exe', 'C:\\Defects\\BuyOffControl0.exe')
                    process_name = "BuyOffControl"
                    try:
                        killed = os.system('tskill ' + process_name)
                    except Exception as e:
                        print(f"[Process BuyOffControl] An error occurred: {e}")
                        pass
            elif str(obj_prog_name.read_program_name_one()) in str(file_index):
                obj_barcode_vvts_flag = True

        #  turn on BuyOffControl - The End

        if obj_barcode_vvts_flag:
            obj_barcode_vvts_flag = False
            index = str(file_index)
            if str(index) not in str(index_temp):
                part = index.split("[@$@]")
                obj_barcode_vvts_log.write_log(f"{part[0]}", f"{part[1]}")
                index_temp = index

        if obj_prog_name.read_program_name_one() not in prog_temp:
            obj_barcode_prog_log.write_log(f"{obj_prog_name.read_program_name_one()}",
                                           f"Program status")
            prog_temp = obj_prog_name.read_program_name_one()
            #  If recipe is change clean up the logs
            if os.path.exists('C:\\cpi\\barcode\\log\\readerLog.txt'):
                os.remove(f"C:\\cpi\\barcode\\log\\readerLog.txt")
            if os.path.exists('C:\\cpi\\barcode\\log\\AOILog.txt'):
                os.remove(f"C:\\cpi\\barcode\\log\\AOILog.txt")
            if os.path.exists('C:\\cpi\\barcode\\log\\VVTSLog.txt'):
                os.remove(f"C:\\cpi\\barcode\\log\\VVTSLog.txt")

        for line in ser.read():
            if line in ASCII_SELECTED:
                captured_barcode_str.append(chr(line))
            if line == 10:  # ascii 10 == Line Feed
                convert_barcode = ''.join(captured_barcode_str)

                print(f"join: {convert_barcode}")

                obj_barcode_reader_log.write_log(f"{obj_prog_name.read_program_name_one()}", f"{convert_barcode}")
                # obj_barcode_aoi_log.write_log(f"{obj_prog_name.read_program_name_one()}", f".........")

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

            # flag_ready_to_send = False # !!! - Latest modification for epsilon and gamma line.

            barcode_list = open('C:\\cpi\\barcode\\barcodelist.bar')
            barcode_list_get = barcode_list.read()
            barcode_list.close()

            print(time.strftime("%m/%d/%Y %I:%M:%S %p", time.localtime()))
            datestamp = time.strftime("%m/%d/%Y %I:%M:%S %p", time.localtime())

            if barcode_list_get == 'Barcode0':
                obj_trigger = Trigger(f"C:\\cpi\\cad\\{obj_prog_name.read_program_name_one()}.plx")
                print(f"C:\\cpi\\cad\\{obj_prog_name.read_program_name_one()}.plx")

                # Save for multiple recipe ERBHROA1287281_11R1B-BOTL1 / ERBHROA1287281_11R1B-BOTL2
                # TODO: I should add additional verification of existing 'barcode' string in L2 .plx section for large boards
                if (
                        (str(obj_prog_name.read_program_name_one()[-3:]) == "TL1" or str(obj_prog_name.read_program_name_one()[-3:]) == "PL1") and
                        obj_trigger.turn_on_off() is not True
                ):
                    print(f"\n{obj_prog_name.read_program_name_one()[-3:]}\n")

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

                    countdown = 0
                    flag_board_inside = False
                    obj_StartAOIValidator = StartAOIValidator(
                        path_to_txt="C:\\cpi\\data\\currentBoardMode.txt",
                        path_to_barcode_txt="C:\\cpi\\barcode\\barcode02.txt"
                    )

                    # Run the loop while countdown is less than 8
                    while countdown < 8:
                        print(f"I am waiting... {8 - countdown}")

                        if obj_StartAOIValidator.start_on_off():
                            flag_board_inside = True
                            break

                        time.sleep(1)
                        countdown += 1  # Increment the countdown

                    if flag_board_inside:
                        print('File exists and is recently modified - [Status validation][OK]')
                        obj_barcode_aoi_log.write_log(f"{obj_prog_name.read_program_name_one()}", f"{content}")
                        flag_pass = True
                    else:
                        print('File does not exist or is not recently modified - [Status validation][NOK]')
                        with open('C:\\cpi\\barcode\\barcodelist.bar', 'w') as barcode_list:
                            barcode_list.write("Barcode0")
                        obj_barcode_aoi_log.write_log(f"{obj_prog_name.read_program_name_one()}", f"Barcode0")
                        flag_pass = False

                    status_info = os.stat("C:\\cpi\\data\\names.txt")
                    modified_date = datetime.fromtimestamp(status_info.st_mtime)
                    modified_date_l1 = modified_date.strftime("%Y%m%d%H%M")

                    if flag_pass:
                        # time.sleep(1)
                        while True:
                            print(f"\nI am waiting for switch to another recipe...\n")
                            status_info1 = os.stat("C:\\cpi\\data\\names.txt")
                            modified_date1 = datetime.fromtimestamp(status_info1.st_mtime)
                            modified_date_l2 = modified_date1.strftime("%Y%m%d%H%M")

                            barcode_list = open('C:\\cpi\\barcode\\barcodelist.bar')
                            barcode_list_get = barcode_list.read()
                            barcode_list.close()

                            if (int(modified_date_l1) < int(modified_date_l2)) and barcode_list_get == 'Barcode0':
                                # time.sleep(1)
                                print("The recipe is not able to read barcode.")
                                barcode_list = open('C:\\cpi\\barcode\\barcodelist.bar', 'w')
                                barcode_list.write(
                                    f"#Board: {obj_prog_name.read_program_name_one()}, {datestamp}\n\n#Number Of Panel	Barcode\nBarcode#1	*{content}\n#End")
                                barcode_list.close()
                                print("Ready!")

                                print("\n--------------------------------------\n")
                                print(f"ProgramName from L2 suffix: {obj_prog_name.read_program_name_many()}")
                                print("\n--------------------------------------\n")
                                # flag_ready_to_send = False  # !!! - Latest modification for epsilon and gamma line. To ver on alpha.
                                break




                elif (
                        (
                                str(obj_prog_name.read_program_name_one()[-9:]) == "L1_preAOI" or
                                str(obj_prog_name.read_program_name_one()[-9:]) == "_preAOIL1"
                        ) and
                        obj_trigger.turn_on_off() is not True
                ):
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
                    # print("The recipe is able to read barcode.")

                    countdown = 0
                    flag_board_inside = False
                    obj_StartAOIValidator = StartAOIValidator(
                        path_to_txt="C:\\cpi\\data\\currentBoardMode.txt",
                        path_to_barcode_txt="C:\\cpi\\barcode\\barcode02.txt"
                    )

                    # Run the loop while countdown is less than 8
                    while countdown < 8:
                        print(f"I am waiting... {8 - countdown}")

                        if obj_StartAOIValidator.start_on_off():
                            flag_board_inside = True
                            break

                        time.sleep(1)
                        countdown += 1  # Increment the countdown

                    if flag_board_inside:
                        print('File exists and is recently modified - [Status validation][OK]')
                        obj_barcode_aoi_log.write_log(f"{obj_prog_name.read_program_name_one()}", f"{content}")
                        flag_pass = True
                    else:
                        print('File does not exist or is not recently modified - [Status validation][NOK]')
                        with open('C:\\cpi\\barcode\\barcodelist.bar', 'w') as barcode_list:
                            barcode_list.write("Barcode0")
                        obj_barcode_aoi_log.write_log(f"{obj_prog_name.read_program_name_one()}", f"Barcode0")
                        flag_pass = False

                    status_info = os.stat("C:\\cpi\\data\\names.txt")
                    modified_date = datetime.fromtimestamp(status_info.st_mtime)
                    modified_date_l1 = modified_date.strftime("%Y%m%d%H%M")

                    if flag_pass:
                        # status_info = os.stat("C:\\cpi\\data\\names.txt")
                        # modified_date = datetime.fromtimestamp(status_info.st_mtime)
                        # modified_date_l1 = modified_date.strftime("%Y%m%d%H%M")

                        # time.sleep(1)
                        while True:
                            print(f"\nI am waiting for switch to another recipe...\n")
                            status_info1 = os.stat("C:\\cpi\\data\\names.txt")
                            modified_date1 = datetime.fromtimestamp(status_info1.st_mtime)
                            modified_date_l2 = modified_date1.strftime("%Y%m%d%H%M")

                            barcode_list = open('C:\\cpi\\barcode\\barcodelist.bar')
                            barcode_list_get = barcode_list.read()
                            barcode_list.close()

                            if (int(modified_date_l1) < int(modified_date_l2)) and barcode_list_get == 'Barcode0':
                                # time.sleep(1)
                                print("The recipe is not able to read barcode.")
                                barcode_list = open('C:\\cpi\\barcode\\barcodelist.bar', 'w')
                                barcode_list.write(
                                    f"#Board: {obj_prog_name.read_program_name_one()}, {datestamp}\n\n#Number Of Panel	Barcode\nBarcode#1	*{content}\n#End")
                                barcode_list.close()
                                print("Ready!")

                                print("\n--------------------------------------\n")
                                print(f"ProgramName from L2 suffix: {obj_prog_name.read_program_name_many()}")
                                print("\n--------------------------------------\n")
                                # flag_ready_to_send = False  # !!! - Latest modification for epsilon and gamma line. To ver on alpha.
                                break


                elif str(obj_prog_name.read_program_name_one()[-4:]) == "PASS" and obj_trigger.turn_on_off() is not True:

                    print("The AOI recipe is not able to read barcode")

                    barcode_list = open('C:\\cpi\\barcode\\barcodelist.bar', 'w')
                    barcode_list.write("Barcode0")
                    barcode_list.close()

                    obj_notification = BarcodeNotification(str(obj_prog_name.read_program_name_one()), str(content))
                    obj_notification.show_notification(str(datestamp))

                    print("Ready!")
                    obj_barcode_aoi_log.write_log(f"{obj_prog_name.read_program_name_one()}", f"Barcode0")
                    # test of multiple recipes
                    print("\n--------------------------------------\n")
                    print(f"ProgramName: {obj_prog_name.read_program_name_many()}")
                    print("\n--------------------------------------\n")

                    print(f"C:\\cpi\\cad\\{obj_prog_name.read_program_name_one()}.plx")
                    # flag_ready_to_send = False  # !!! - Latest modification for epsilon and gamma line. To ver on alpha.


                else:
                    # Save for usual recipe

                    if obj_trigger.turn_on_off() is not True:  # Check the .plx file
                        print("The AOI recipe is not able to read barcode")

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
                        # flag_ready_to_send = False  # !!! - Latest modification for epsilon and gamma line. To ver on alpha.
                        # this section is for remove the barcode from AOI if PCB is not go inside

                        countdown = 0
                        flag_board_inside = False
                        obj_StartAOIValidator = StartAOIValidator(
                            path_to_txt="C:\\cpi\\data\\currentBoardMode.txt",
                            path_to_barcode_txt="C:\\cpi\\barcode\\barcode02.txt"
                        )

                        # Run the loop while countdown is less than 8
                        while countdown < 10:
                            print(f"I am waiting... {10 - countdown}")

                            if obj_StartAOIValidator.start_on_off():
                                flag_board_inside = True
                                break

                            time.sleep(1)
                            countdown += 1  # Increment the countdown

                        if flag_board_inside:
                            print('File exists and is recently modified - [Status validation][OK]')
                            obj_barcode_aoi_log.write_log(f"{obj_prog_name.read_program_name_one()}", f"{content}")
                        else:
                            print('File does not exist or is not recently modified - [Status validation][NOK]')
                            with open('C:\\cpi\\barcode\\barcodelist.bar', 'w') as barcode_list:
                                barcode_list.write("Barcode0")
                            obj_barcode_aoi_log.write_log(f"{obj_prog_name.read_program_name_one()}", f"Barcode0")
                    else:
                        print("Single Recipe - The AOI recipe is able to read barcode.")

                        # flag_ready_to_send = False  # !!! - Latest modification for epsilon and gamma line. To ver on alpha.

                flag_ready_to_send = False  # !!! - Latest modification for epsilon and gamma line. To ver on alpha.
                #  turn on BuyOffControl - Start
                if os.path.exists('C:\\Defects\\BuyOffControl0.exe'):
                    os.rename('C:\\Defects\\BuyOffControl0.exe', 'C:\\Defects\\BuyOffControl.exe')
                #  turn on BuyOffControl - The End
            else:
                pass

    # ser.close()  # for the moment it is out of reach
