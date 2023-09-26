import sqlite3


class DBHandler:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)

    def create_user(self, user_id, username, last_active, total_interactions):
        with self.conn:
            self.conn.execute("INSERT INTO Users (UserID, UserName, LastActive, TotalInteractions) VALUES (?, ?, ?, ?)",
                              (user_id, username, last_active, total_interactions))

    def log_command(self, user_id, command_id, time_used):
        with self.conn:
            self.conn.execute("INSERT INTO UserCommands (UserID, CommandID, TimeUsed) VALUES (?, ?, ?)",
                              (user_id, command_id, time_used))

    def update_user(self, username, last_active, total_interactions):
        with self.conn:
            self.conn.execute("INSERT OR IGNORE INTO Users (UserName, LastActive, TotalInteractions) VALUES (?, ?, ?)",
                              (username, last_active, total_interactions))
            self.conn.execute("UPDATE Users SET LastActive = ?, TotalInteractions = ? WHERE UserName = ?",
                              (last_active, total_interactions, username))

    def get_user_id(self, username):
        with self.conn:
            cur = self.conn.execute("SELECT UserID FROM Users WHERE UserName = ?", (username,))
            row = cur.fetchone()
            return row[0] if row else None

    def get_user_by_id(self, user_id):
        with self.conn:
            cur = self.conn.execute("SELECT * FROM Users WHERE UserID = ?", (user_id,))
            row = cur.fetchone()
            return row if row else None

    async def handle_database_dump(message, db_handler):
        if message.content == '&select *':
            cursor = db_handler.conn.execute("SELECT * FROM Users")
            rows = cursor.fetchall()

            # Format the output as a string.
            output = "UserID | UserName | LastActive | TotalInteractions\n"
            output += "-" * 50 + "\n"
            for row in rows:
                output += f"{row[0]} | {row[1]} | {row[2]} | {row[3]}\n"

            # Send the message wrapped in backticks for code formatting.
            await message.channel.send(f"```{output}```")

    def close(self):
        self.conn.close()
