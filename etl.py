import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """Pre-processing song file

    :param cur: string - query being executed
    :param filepath: string - path to file file being extracted
    :return: nothing - data is being loaded into table
    """

    # open song file
    df = pd.read_json(filepath, lines=True)

    # Need to change type of year in order to make it work
    df.year = df.year.astype(float)
    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].iloc[0].values.tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].loc[0].values.tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """Pre-processing log file

    :param cur: string - query being executed
    :param filepath: string - path to file file being extracted
    :return: nothing - data is being loaded into table
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df.ts, unit='ms', origin="unix")
    
    # insert time data records
    time_data = (t, t.dt.hour, t.dt.day, t.dt.weekofyear, t.dt.month, t.dt.year, t.dt.weekday)
    column_labels = ("Timestamp", "Hour", "Day", "Week of Year", "Month", "Year", "Weekday")
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', "firstName", "lastName", "gender", "level"]]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        results = cur.execute(song_select, (row.song, row.artist, row.length))
        songid, artistid = results if results else None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts, unit="ms"), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """

    :param cur: string - query being executed
    :param conn: connection to server
    :param filepath: string - path to file file being extracted
    :param func: function being processed
    :return: print # files being processed
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():

    host = os.getenv('HOST')
    port = os.environ.get("PORT")
    dbname = os.environ.get("DBNAME")
    user = os.environ.get("USER")
    password = os.environ.get("PASSWORD")

    conn = psycopg2.connect(host=host, port=port, user=user, dbname=dbname, password=password)
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()