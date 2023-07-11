import sqlite3
from datetime import datetime
from fernet import Fernet


class DatabaseService:
    def __init__(self):
        self.database_name = 'passwords.db'
        self.table_name = "passwords"
        self.createTableIfNotExists()

    def createTableIfNotExists(self):
        try:
            self.createTable()
            key = Fernet.generate_key().decode()
            print(f'Your key is: {key} Keep it in a safe place and do not share with anyone...')
        except sqlite3.OperationalError:
            pass

    def createTable(self):
        command_to_execute = f"CREATE TABLE {self.table_name}(source, login, password, creation_date)"
        self.executeDatabaseCommand(command_to_execute)

    def addPasswordToDatabase(self, login, password_to_save, source,
                              database_password=b'y4hCz3NXgj2NfCsEIPWYfh3p29x3d6GcZGuLftSeHl0='):
        f = Fernet(database_password)
        token = f.encrypt(password_to_save.encode())
        command_to_execute = f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?)"
        values = (source, login, token, datetime.now().isoformat())
        self.executeDatabaseCommand(command_to_execute, values)

    @staticmethod
    def decryptPassword(password_to_decrypt, database_password=b'y4hCz3NXgj2NfCsEIPWYfh3p29x3d6GcZGuLftSeHl0='):
        f = Fernet(database_password)
        return f.decrypt(password_to_decrypt)

    def getAllResultsFromDatabase(self):
        command_to_execute = f"SELECT * FROM {self.table_name}"
        return self.executeDatabaseCommand(command_to_execute)

    def removeResultFromDatabase(self, item_date_id):
        command_to_execute = f"DELETE FROM {self.table_name} WHERE creation_date='{item_date_id}'"
        self.executeDatabaseCommand(command_to_execute)

    def executeDatabaseCommand(self, command_to_execute, values=None):
        with sqlite3.connect(self.database_name) as con:
            cur = con.cursor()
            if values:
                con.commit()
                return cur.execute(command_to_execute, values)
            else:
                con.commit()
                return cur.execute(command_to_execute)
