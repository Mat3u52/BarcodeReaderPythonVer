from winotify import Notification


class BarcodeNotification:
    def __init__(self, prog_name: str = 'ProgName', title: str = 'Title') -> None:
        self.prog_name = prog_name
        self.title = title

    def show_notification(self, message: str = 'Message') -> None:
        message = message
        toast = Notification(app_id=self.prog_name,
                             title=self.title,
                             msg=message,
                             duration="long",
                             icon=r"C:\cpi\barcode\img\board.png")

        # toast.add_actions(label="Click here!",
        #                   # launch="file:///C:/index.html")
        #                   launch="file:///C:/Notification_v01/Notification_v01/index.html")

        toast.show()
