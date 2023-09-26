import sqlite3


def setup_database():
    conn = sqlite3.connect('alfred_database.db')
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserName TEXT,
                LastActive TEXT,
                TotalInteractions INTEGER
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS Commands (
                CommandID INTEGER PRIMARY KEY AUTOINCREMENT,
                CommandName TEXT,
                CommandDescription TEXT
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS UserCommands (
                UserCommandID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER,
                CommandID INTEGER,
                TimeUsed TEXT,
                FOREIGN KEY (UserID) REFERENCES Users(UserID),
                FOREIGN KEY (CommandID) REFERENCES Commands(CommandID)
            );
        """)


if __name__ == '__main__':
    setup_database()
