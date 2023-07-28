import sqlite3


conn = sqlite3.connect('videos.sqlite')
cur = conn.cursor()

def create_database():
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
    
def insert_record(title, publish_datetime, view_count, like_count,
                     comment_count, url, channel_name):
    
    # inserting a new record in channel's table
    cur.execute('''INSERT OR IGNORE INTO Channels (name)
        VALUES ( ? )''', ( channel_name, ) )
    cur.execute('SELECT id FROM Channels WHERE name = ? ', (channel_name, ))
    channel_id = cur.fetchone()[0]
    
    cur.execute('''INSERT OR IGNORE INTO Videos 
        (title, publish_datetime, view_count, like_count, comment_count, url, channel_id)
        VALUES ( ?, ?, ?, ?, ?, ?, ? )''', 
        (title, publish_datetime, view_count, like_count, comment_count, url, channel_id) )
 
    conn.commit()

def close_database():
    conn.close()   
    
 
