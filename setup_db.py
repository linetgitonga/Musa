import sqlite3

# Connect to SQLite database (creates if not exists)
conn = sqlite3.connect('songs.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create song_history table
cursor.execute('''
CREATE TABLE IF NOT EXISTS song_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    song_id INTEGER,
    title TEXT,
    artist TEXT,
    emotion TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Commit changes and close connection
conn.commit()
conn.close()

print("Database setup complete.")
