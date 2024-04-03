import sys
from PySide6.QtWidgets import QApplication
from src.controller import ChatController
'''
main.py
Contain interfaces operated by users.
'''


if __name__ == "__main__":
    app = QApplication(sys.argv)

    chat_controller = ChatController()
    
    app.exec()