'''
database.py
Store messages from every session.
'''

import sqlite3
from typing import List

class Database:
    def __init__(self, table_name: str = "messages_group_0") -> None:
        # variables
        self.table_name = table_name
        
        # initialize database
        self.con = sqlite3.connect("res/msgs.db")
        self.cur = self.con.cursor()
        self.cur.execute(f'''CREATE TABLE IF NOT EXISTS {self.table_name} (
            session INTEGER NOT NULL,
            role TEXT CHECK(role IN ('system', 'user', 'assistant')) NOT NULL,
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Auto-generated
            content TEXT,
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )''')
        
    def __del__(self) -> None:
        self.cur.close()
        self.con.close()
    
    def insert(self, session: int, role: str, content: str) -> None:
        self.cur.execute(f"INSERT INTO {self.table_name} (session, role, content) VALUES (?, ?, ?)", (str(session), role, content))
        self.con.commit()
        

    def fetch_last_session(self) -> List:
        '''
        Fetch messages from the last session.
        return: [
            (session_id, role, message_content, message_id),
            (...), ...
        ]
        '''
        self.cur.execute("SELECT * FROM {} WHERE session=(SELECT MAX(session) FROM {})".format(self.table_name, self.table_name))
        result = self.cur.fetchall()
        if result:
            return list(map(lambda x: [x[1], x[3], x[4]], result))
        else:
            return []

    def fetch_by_session(self, id: int) -> List:
        """
        return: [
            (session_id, role, message_content, message_id),
            (...), ...
        ]
        """
        self.cur.execute("SELECT * FROM {} WHERE session=={}".format(self.table_name, id))
        result = self.cur.fetchall()
        if result:
            return list(map(lambda x: [x[1], x[3], x[4]], result))
        else:
            return []

    def fetch_last_session_id(self) -> int:
        self.cur.execute("SELECT MAX(session) FROM {}".format(self.table_name))
        id = self.cur.fetchone()[0]
        if not id:
            id = 0
        return id
    
    def fetch_last_message_id(self) -> int:
        self.cur.execute(f"select max(id) from {self.table_name}")
        id = self.cur.fetchone()[0]
        if not id:
            id = 0
        return id
    
    def fetch_all_sessions(self) -> List[List]:
        '''
        Fetch all session IDs and the first 2 content(merged).
        '''
        self.cur.execute(f"SELECT session, group_concat(content, ' / ') FROM {self.table_name} GROUP BY session")
        sessions = self.cur.fetchall()
        if not sessions:
            sessions = []
        return sessions

    def delete_all(self) -> None:
        self.cur.execute("DELETE FROM {}".format(self.table_name))
        self.con.commit()

    def delete_by_session(self, session: int) -> None:
        self.cur.execute("DELETE FROM {} WHERE session=?".format(self.table_name), (session,))
        self.con.commit()
