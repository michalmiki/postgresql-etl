# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays
 (songplay_id SERIAL, start_time timestamp NOT NULL, user_id varchar NOT NULL, level text, song_id varchar,
 artist_id varchar, session_id integer, location text, user_agent varchar, 
 PRIMARY KEY (songplay_id));
 """)

user_table_create = ("""CREATE TABLE IF NOT EXISTS users 
 (user_id integer, first_name varchar, last_name varchar, gender text, level text, 
 PRIMARY KEY (user_id));
""")

song_table_create = ("""CREATE TABLE  IF NOT EXISTS songs 
(song_id varchar, title varchar, artist_id varchar, year float, duration float, 
 PRIMARY KEY (song_id));
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists
 (artist_id varchar, name varchar, location text, latitude real, longitude real,
 PRIMARY KEY (artist_id));
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time
 (start_time timestamp, hour integer, day integer, week integer, month integer, year integer, weekday integer,
 PRIMARY KEY (start_time));
""")

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplays
 (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 
 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
 ON CONFLICT DO NOTHING;
""")

user_table_insert = ("""INSERT INTO users 
 (user_id, first_name, last_name, gender, level) 
 VALUES (%s, %s, %s, %s, %s)
 ON CONFLICT (user_id) DO UPDATE set level=excluded.level;
""")

song_table_insert = ("""INSERT INTO songs
 (song_id, title, artist_id, year, duration)
 VALUES (%s, %s, %s, %s, %s)
 ON CONFLICT DO NOTHING;
""")

artist_table_insert = ("""INSERT INTO artists
 (artist_id, name, location, latitude, longitude)
 VALUES (%s, %s, %s, %s, %s)
 ON CONFLICT DO NOTHING;
""")


time_table_insert = ("""INSERT INTO time
 (start_time, hour, day, week, month, year, weekday) 
 VALUES (%s, %s, %s, %s, %s, %s, %s)
 ON CONFLICT DO NOTHING;
""")

# FIND SONGS

song_select = ("""SELECT a.song_id, a.artist_id 
 FROM songs as a 
 LEFT JOIN artists as b
 ON a.artist_id = b.artist_id
 WHERE a.title = %s
 AND b.name = %s
 AND a.duration = %s;
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]