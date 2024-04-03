from PySide6.QtCore import QObject, Slot
from src.model import ChatModel
from src.database import Database
from src.view import ChatView
from src.keyHandler import KeyHandler
from src.settings import Settings


class ChatController(QObject):
    """
    Chat controller responsible for coordinating the interaction between the view and the model.
    """

    def __init__(self):
        super().__init__()
        # Init all the components
        self.settings = Settings()
        self.model = ChatModel(self.settings.variables.api_key, self.settings.variables.base_url, self.settings.variables.model, self.settings.variables.temperature)
        self.view = ChatView()
        self.database = Database()
        self.update_UI_table()
        self.keyHandler = KeyHandler()
        self.update_setttings()

        # Connect signals and slots
        self.model.on_word_receive.connect(self.handle_msg_received)
        self.view.msg_submit.connect(self.handle_msg_sent)
        self.view.switch_session.connect(self.switch_session)
        self.view.save_settings.connect(self.update_setttings)
        self.keyHandler.key_pressed.connect(self.key_events)

        # Other variables
        self.bot_response = ""  # Store current AI responses
        self.cur_session = 0    # Current session ID, 0 means no session
        self.last_session = 0

        # Show UI
        self.view.show()

    def update_setttings(self):
        """
        Update settings and save them to model.
        """
        self.settings.load()
        self.model.api_key = self.settings.variables.api_key
        self.model.base_url = self.settings.variables.base_url
        self.model.model = self.settings.variables.model
        self.model.temperature = self.settings.variables.temperature
        self.model.system_prompt = self.settings.variables.system_prompt
        

    def handle_msg_sent(self, msg: str, query_session: int = 0):
        """ 
        Handle message sent from user.
        query_session: 
            0   continue current session; if there's not an ongoing session, create new one.
            -1  create a new session.
            1+  query a session of the id.
        """
        is_new_session = False
        if not msg and query_session == -1:
            # Clear button is clicked
            self.cur_session = 0
            return
        
        # Disable UI input
        self.view.toggle_input(False)
        
        # Update current/last session ID
        if query_session == -1:
            is_new_session = True
            self.last_session = self.database.fetch_last_session_id() + 1
            self.cur_session = self.last_session
        elif query_session == 0:
            if self.cur_session == 0:
                is_new_session = True
                self.last_session = self.database.fetch_last_session_id() + 1
                self.cur_session = self.last_session
        else:
            self.cur_session = query_session

        # Prepare list of messages("msgs") to send
        session = self.database.fetch_by_session(self.cur_session)
        if msg:
            last_msg_id = self.database.fetch_last_message_id()
            # Add system prompt for new session
            if is_new_session:
                msgs = [["system", self.settings.variables.system_prompt, 0],["user", msg, last_msg_id + 1]]
            else:
                msgs = session + [["user", msg, last_msg_id + 1]]
        else:
            msgs = session
        self.model.send_messages(msgs)

        # Remove the first message if it's a system message
        if is_new_session:
            msgs = msgs[1:]
        # Insert messages into database
        self.database.insert(self.cur_session, "user", msg)
        # Display messages in UI(message area)
        for msg in msgs:
            self.view.append_msg(msg[0], msg[1], msg[2])
        self.view.append_msg("bot", "", last_msg_id + 2)
        self.update_UI_table()

    def switch_session(self, session_id: int):
        """
        Switch to a different session.
        """
        # Clear the current session
        self.view.clear_screen()
        self.cur_session = session_id
        session = self.database.fetch_by_session(self.cur_session)
        for msg in session:
            self.view.append_msg(msg[0], msg[1], msg[2])
        self.update_UI_table()

    def handle_msg_received(self, msg: str):
        """
        Handle messages received from AI.
        """
        # End of bot response
        if msg == "" and self.bot_response != "":
            self.database.insert(self.cur_session, "assistant", self.bot_response)
            response = self.bot_response
            self.bot_response = ""
            self.update_UI_table()
            return response
            
        self.view.append_word(msg)
        self.view.toggle_input(True)
        self.bot_response += msg

    def update_UI_table(self):
        sessions = self.database.fetch_all_sessions()[::-1]
        self.view.update_session_table(sessions)
        
    @Slot(str)
    def key_events(self, func: str):
        """
        Handle key events.
        """
        if func == "toggle_visibility":
            self.view.toggle_visibility()
        elif func == "enter":
            self.view.enter_pressed()
        elif func == "new_chat":
            self.view.ui.clear_btn.click()