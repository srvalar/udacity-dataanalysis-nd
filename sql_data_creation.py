import sqlite3

sqlite_file = 'sanjose_osm_project.db'
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()


# --------------------------------------------
#          CREATE SQL TABLES
# --------------------------------------------
cur.execute('DROP TABLE IF EXISTS nodes')
conn.commit()
cur.execute("CREATE TABLE nodes (\
    id INTEGER PRIMARY KEY NOT NULL,\
    lat REAL,\
    lon REAL,\
    user TEXT,\
    uid INTEGER,\
    version INTEGER,\
    changeset INTEGER,\
    timestamp TEXT\
);")
conn.commit()

cur.execute('DROP TABLE IF EXISTS nodes_tags')
conn.commit()
cur.execute("CREATE TABLE nodes_tags (\
    id INTEGER,\
    key TEXT,\
    value TEXT,\
    type TEXT,\
    FOREIGN KEY (id) REFERENCES nodes(id)\
);")
conn.commit()

cur.execute('DROP TABLE IF EXISTS ways')
conn.commit()
cur.execute("CREATE TABLE ways (\
    id INTEGER PRIMARY KEY NOT NULL,\
    user TEXT,\
    uid INTEGER,\
    version TEXT,\
    changeset INTEGER,\
    timestamp TEXT\
);")
conn.commit()

cur.execute('DROP TABLE IF EXISTS ways_tags')
conn.commit()
cur.execute("CREATE TABLE ways_tags (\
    id INTEGER NOT NULL,\
    key TEXT NOT NULL,\
    value TEXT NOT NULL,\
    type TEXT,\
    FOREIGN KEY (id) REFERENCES ways(id)\
);")

cur.execute('DROP TABLE IF EXISTS ways_nodes')
conn.commit()
cur.execute("CREATE TABLE ways_nodes (\
    id INTEGER NOT NULL,\
    node_id INTEGER NOT NULL,\
    position INTEGER NOT NULL,\
    FOREIGN KEY (id) REFERENCES ways(id),\
    FOREIGN KEY (node_id) REFERENCES nodes(id)\
);")
conn.commit()

# --------------------------------------------
#          READ DATA FROM CSV FILES
# --------------------------------------------

with open('nodes.csv','rb') as fin:
    dr = csv.DictReader(fin)
    to_db_nodes = [(i['id'], i['lat'],i['lon'], i['user'].decode("utf-8"), i['uid'],
                    i['version'].decode("utf-8"), i['changeset'], i['timestamp'])
             for i in dr]
    
with open('nodes_tags.csv','rb') as fin:
    dr = csv.DictReader(fin)
    to_db_nodes_tags = [(i['id'], i['key'],i['value'].decode("utf-8"), 
                         i['type'].decode("utf-8"))
             for i in dr]

with open('ways.csv','rb') as fin:
    dr = csv.DictReader(fin)
    to_db_ways = [(i['id'], i['user'].decode("utf-8"),i['uid'],
                   i['version'].decode("utf-8"), i['changeset'], i['timestamp'])
             for i in dr]

with open('ways_tags.csv','rb') as fin:
    dr = csv.DictReader(fin)
    to_db_ways_tags = [(i['id'], i['key'],i['value'].decode("utf-8"),
                        i['type'].decode("utf-8")) for i in dr]

with open('ways_nodes.csv','rb') as fin:
    dr = csv.DictReader(fin)
    to_db_ways_nodes = [(i['id'], i['node_id'],i['position']) for i in dr]
    
    
# --------------------------------------------
#          INSERT DATA INTO SQL TABLES
# --------------------------------------------

# NODES Table: insert the formatted data
cur.executemany("INSERT INTO nodes(id, lat, lon, user, uid, version, changeset, timestamp) \
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db_nodes)
# commit the changes
conn.commit()

# NODES_TAGS table: insert the formatted data
cur.executemany("INSERT INTO nodes_tags(id, key, value, type) \
                 VALUES (?, ?, ?, ?);", to_db_nodes_tags)
# commit the changes
conn.commit()

# WAYS Table: insert the formatted data
cur.executemany("INSERT INTO ways(id, user, uid, version, changeset, timestamp) \
                 VALUES (?, ?, ?, ?, ?, ?);", to_db_ways)
# commit the changes
conn.commit()

# WAYS_TAGS Table: insert the formatted data
cur.executemany("INSERT INTO ways_tags(id, key, value, type) \
                 VALUES (?, ?, ?, ?);", to_db_ways_tags)
# commit the changes
conn.commit()

# WAYS_NODES Table: insert the formatted data
cur.executemany("INSERT INTO ways_nodes(id, node_id, position) \
                 VALUES (?, ?, ?);", to_db_ways_nodes)
# commit the changes
conn.commit()

# --------------------------------------------
#          DATA CHECKS
# --------------------------------------------

cur.execute('SELECT * FROM nodes LIMIT 2')
all_rows = cur.fetchall()
pprint.pprint(all_rows)
