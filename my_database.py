import sqlite3

conn = sqlite3.connect('videos.sqlite')
cur = conn.cursor()

def create_database():
    # Create the 'Videos' and 'Channels' tables in the database
    cur.executescript('''
    DROP TABLE IF EXISTS Videos;
    DROP TABLE IF EXISTS Channels;

    CREATE TABLE Videos (
        id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        title   TEXT UNIQUE, 
        publish_datetime DATE,
        view_count INTEGER,
        like_count INTEGER,
        comment_count INTEGER,
        url TEXT UNIQUE,
        channel_id INTEGER
    );

    CREATE TABLE Channels (
        id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name   TEXT UNIQUE
    )
    ''')
    
def insert_record(title, publish_datetime, view_count, like_count, comment_count, url, channel_name):
    # Insert a new record in the 'Channels' table, ignore if the channel name already exists
    cur.execute('''INSERT OR IGNORE INTO Channels (name)
        VALUES ( ? )''', (channel_name,))
    # Get the channel ID associated with the channel name
    cur.execute('SELECT id FROM Channels WHERE name = ? ', (channel_name,))
    channel_id = cur.fetchone()[0]
    
    # Insert a new record in the 'Videos' table
    cur.execute('''INSERT OR IGNORE INTO Videos 
        (title, publish_datetime, view_count, like_count, comment_count, url, channel_id)
        VALUES ( ?, ?, ?, ?, ?, ?, ? )''', 
        (title, publish_datetime, view_count, like_count, comment_count, url, channel_id))
    
    # Commit the changes to the database
    conn.commit()

def close_database():
    # Close the database connection
    conn.close()   

 
