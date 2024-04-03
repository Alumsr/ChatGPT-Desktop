'''
This module is responsible for handling the key events.
'''

import keyboard
from PySide6.QtCore import QObject, Signal


class KeyHandler(QObject):
    """
    Key handler responsible for handling the key events.
    """

    # Signals
    key_pressed = Signal(str)

    def __init__(self):
        super().__init__()

        # Register the hotkey
        keyboard.add_hotkey('ctrl+alt+q', self.toggle_visibility)
        keyboard.add_hotkey('enter', self.enter)
        keyboard.add_hotkey('ctrl+k', self.new_chat)

    def toggle_visibility(self):
        self.key_pressed.emit('toggle_visibility')
    def enter(self):
        self.key_pressed.emit('enter')
    def new_chat(self):
        self.key_pressed.emit('new_chat')