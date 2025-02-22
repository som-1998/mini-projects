import sqlite3
import numpy as np
import pandas as pd



similarity = np.load('similarity.npy')

# Load movie data into a pandas DataFrame
conn = sqlite3.connect('movies.db')
movies_df = pd.read_sql_query("SELECT ROWID - 1 as idx, id, title FROM (SELECT ROWID, id, title FROM movies)", conn)
movies_df.set_index('idx', inplace=True)
movies_df.rename(columns={'id': 'movie_id'}, inplace=True)
conn.close()