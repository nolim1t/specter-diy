import asyncio
from .core import init, update
from .screens import Menu, Alert, QRAlert, Prompt
import lvgl as lv

class AsyncGUI:

    def __init__(self):
        # unlock event for host signalling
        # to avoid spamming GUI
        self.waiting = False
        # only one popup can be active at a time
        # another screen goes to the background
        self.background = None
        self.scr = None

    def release(self, *args, **kwargs):
        """
        Unlocks the GUI
        """
        self.args = args
        self.kwargs = kwargs
        self.waiting = True

    async def load_screen(self, scr):
        while self.background is not None:
            await asyncio.sleep_ms(10)
        old_scr = lv.scr_act()
        lv.scr_load(scr)
        self.scr = scr
        old_scr.del_async()

    async def open_popup(self, scr):
        # wait for another popup to finish
        while self.background is not None:
            await asyncio.sleep_ms(10)
        self.background = self.scr
        self.scr = scr
        lv.scr_load(scr)

    def close_popup(self):
        scr = self.background
        self.background = None
        self.load_screen(scr)

    def start(self, rate:int=30):
        init()
        asyncio.create_task(self.update_loop(rate))

    async def update_loop(self, dt):
        while True:
            update(dt)
            await asyncio.sleep_ms(dt)

    async def menu(self, buttons:list=[], title:str="What do you want to do?", last=None):
        """
        Creates a menu with buttons. 
        buttons argument should be a list of tuples:
        (value, text)
        value is retured when the button is pressed
        text is the text on the button

        If add_back_button is set to True,
        < Back button is added to the bottom of the screen
        and if it is pressed AsyncGUI.BTN_CLOSE is returned (-99)
        """
        menu = Menu(buttons=buttons, title=title, last=last)
        await self.load_screen(menu)
        return await menu.result()

    async def alert(self, title, msg, button_text="OK"):
        """Shows an alert"""
        alert = Alert(title, msg, button_text=button_text)
        await self.load_screen(alert)
        await alert.result()

    async def qr_alert(self, title, msg, qr_msg, qr_width=None, button_text="OK"):
        """Shows an alert with QR code"""
        alert = QRAlert(title, msg, qr_msg, qr_width=qr_width, button_text=button_text)
        await self.load_screen(alert)
        return await alert.result()

    async def error(self, msg, popup=False):
        """Shows an error"""
        alert = Alert("Error!", msg, button_text="OK")
        if popup:
            await self.open_popup(alert)
        else:
            await self.load_screen(alert)
        res = await alert.result()
        if popup:
            self.close_popup()
        return res

    async def prompt(self, title, msg):
        """Asks the user to confirm action"""
        scr = Prompt(title, msg)
        await self.load_screen(scr)
        return await scr.result()
