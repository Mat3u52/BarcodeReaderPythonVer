try:
    from winotify import Notification
    flag = True
except ImportError:
    print("Lib import error!")
    flag = False


class BarcodeNotification:
    def __init__(self, prog_name: str = 'ProgName', title: str = 'Title') -> None:
        self.prog_name = prog_name
        self.title = title

    def show_notification(self, message: str = 'Message') -> None:
        if flag:  # Check the flag directly
            try:
                toast = Notification(app_id=self.prog_name,
                                     title=self.title,
                                     msg=message,
                                     duration="long",
                                     icon="C:\\cpi\\barcode\\img\\board.png")
                # Uncomment and use the add_actions and show methods as needed
                # toast.add_actions(label="Click here!",
                #                   launch="file:///C:/Notification_v01/Notification_v01/index.html")
                toast.show()
            except Exception as e:
                print(f"[Notification] An error occurred: {e}")
                pass
        else:
            print("Notification library not available.")


if __name__ == "__main__":
    obj_welcome_notification = BarcodeNotification("Connection to COM10 is successful", "Connected")
    obj_welcome_notification.show_notification("Ready to intercept!")
# try:
#     from winotify import Notification
#     flag = True
# except ImportError:
#     print("Lib import error!")
#     pass
#
#
# class BarcodeNotification:
#     def __init__(self, prog_name: str = 'ProgName', title: str = 'Title') -> None:
#         self.prog_name = prog_name
#         self.title = title
#
#     def show_notification(self, message: str = 'Message') -> None:
#         message = message
#         if flag is True:
#             try:
#                 toast = Notification(app_id=self.prog_name,
#                                      title=self.title,
#                                      msg=message,
#                                      duration="long",
#                                      # icon=r"C:\cpi\barcode\img\board.png")
#                                      icon=f"C:\\cpi\\barcode\\img\\board.png")
#             except Exception as e:
#                 print(f"[Notification] An error occurred: {e}")
#                 pass
#
#         # toast.add_actions(label="Click here!",
#         #                   # launch="file:///C:/index.html")
#         #                   launch="file:///C:/Notification_v01/Notification_v01/index.html")
#
#         # toast.show()
#
#
# if __name__ == "__main__":
#
#     obj_welcome_notification = BarcodeNotification("Connection to COM10 is successful", "Connected")
#     obj_welcome_notification.show_notification("Ready to intercept!")
