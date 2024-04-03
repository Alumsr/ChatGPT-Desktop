from PySide6.QtCore import QThread, Signal
import openai

'''
model.py
Handle the API calling. Send and receive messages.
'''


class ChatModel(QThread):
    on_word_receive = Signal(str)
    
    def __init__(self, api_key, base_url, model: str, temperature):
        super().__init__()
        self.model = model
        self.msgs = []  # Previous context to send 
        self.temperature = temperature
        self.system_prompt = ""
        self.api_key = api_key
        self.base_url = base_url
        
        

    def run(self):
        """
        Send message request in a new thread.
        """
        self._send_message()
        
    def send_messages(self, msgs: list):
        '''
        Set messages to send and start thread
        '''
        if not self.isRunning():
            self.msgs = msgs
            self.start()

    def _send_message(self):
        """
        Send a message, get responses and broadcast it.
        """
        # convert list : [[role, message], [role, message], ...]
        # to dict : {"role": "message", "role": "message", ...}
        messages = [{"role": role, "content": content} for role, content, msg_id in self.msgs]
        try:
            self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)
            # Create a streaming response
            stream = self.client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                messages=messages,
                stream=True
            )
            for chunk in stream:
                word = chunk.choices[0].delta.content
                if word != "":
                    # Send assistant response
                    self.on_word_receive.emit(word)
            self.on_word_receive.emit("")
        except Exception as e:
            # Handle API errors
            self.on_word_receive.emit(f"---\n\n{str(e)}\n\n---")
            self.on_word_receive.emit("")
            return
