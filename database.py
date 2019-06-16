import sqlite3


class Message_database:
    def __init__(self):
        self._db_file = sqlite3.connect("messages.db")
        self._cursor = self._db_file.cursor()
        self._cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='messages' ''')
        if  self._cursor.fetchone()[0] != 1:
            self._db_setup()
        self._db_file.commit()

    def __del__(self):
        self._db_file.commit()
        self._db_file.close()

    def _db_setup(self):
        self._cursor.execute("CREATE TABLE messages (sender text, receiver text, message text)")
        self._db_file.commit()

    def save_message(self, sender, receiver, message):
        args = (sender, receiver, message)
        self._cursor.execute("INSERT INTO messages VALUES(?, ?, ?)", args)
        self._db_file.commit()

    def get_messages(self, receiver):
        args = (receiver,)
        self._cursor.execute("SELECT * FROM messages WHERE receiver=?", args)
        new_messages = self._cursor.fetchall()
        self._db_file.commit()
        return new_messages

    def delete_messages_of_receiver(self, receiver):
        args = (receiver,)
        self._cursor.execute("DELETE FROM messages WHERE receiver=?", args)

