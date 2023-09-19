from cassandra.cluster import Cluster
import os
import spotify_consume
import json
from datetime import datetime


# Environment variables for Cassandra
endpoint_node1 = os.environ.get("endpoint_node1")
endpoint_node2 = os.environ.get("endpoint_node2")


# Environment variables for Spotify
client_id = os.environ.get("client_id_spotify")
client_secret = os.environ.get("client_secret_spotify")


def connect_cassandra_cluster():
    """This function connects to the Cassandra Cluster

    Returns:
        object: connection
    """
    try:
        cluster = Cluster([endpoint_node1, endpoint_node2])
        session = cluster.connect()
        print(f"[ INFO | Connecting to Cassandra Cluster {session.hosts}]")
        return session
    except Exception as e:
        print(f"[ ERROR | Connecting to Cassandra Cluster {e}]")
        return None


def create_keyspace(keyspace:str):
    """This function creates a keyspace in Cassandra Cluster

    Args:        
        keyspace (string): keyspace name
    """
    try:
        session = connect_cassandra_cluster()
        session.execute(
            f"CREATE KEYSPACE IF NOT EXISTS {keyspace} WITH REPLICATION = {{ 'class' : 'SimpleStrategy', 'replication_factor' : 2 }};"
        )
        print(f"[ INFO | Creating keyspace {keyspace} if not exists]")
        session.shutdown()
        return keyspace
    except Exception as e:
        print(f"[ ERROR | Creating keyspace {keyspace} {e}]")
        session.shutdown()


def create_table(keyspace:str, table:str, schema:tuple):
    """This function creates a table in Cassandra Cluster

    Args:        
        keyspace (string): keyspace name
        table (string): table name
    """
    try:
        session = connect_cassandra_cluster()        
        session.execute(
            f"CREATE TABLE IF NOT EXISTS {keyspace}.{table} {' '.join(schema.split())};"
        )
        print(f"[ INFO | Creating table {table} if not exists]")
        session.shutdown()
        return keyspace, table
    except Exception as e:
        print(f"[ ERROR | Creating table {table} {e}]")
        session.shutdown()


def insert_data(keyspace:str, table:str, data:dict):
    """ This function inserts data into a table in Cassandra Cluster
    Args:        
        keyspace (str): name of the keyspace
        table (str): name of the table
        data (dict): data to be inserted
    """
    try:
        session = connect_cassandra_cluster()
        for k, v in data.items():        
            match v['date_release']:
                case s if isinstance(s, str):                    
                    v = json.dumps(v).replace("'", "")                  
                    session.execute(
                        f"INSERT INTO {keyspace}.{table} JSON '{v}';"
                    )
        print(f"[ INFO | Inserting data into table {table} {k}]")
        session.shutdown()
    except Exception as e:
        print(f"[ ERROR | Inserting data into table {table} {e}]")
        session.shutdown() 
            
def main(band:str, qnt_albums:int):
    """This function is the main function
    Args:
        band (string): name of the band
        qnt_albums (int): quantity of albums
    """
    try:
        keyspace = create_keyspace("spotifydb")
        table = create_table(
            keyspace=keyspace,
            table="albums",
            schema='(\
                album_id varchar ,\
                album_name varchar,\
                date_release varchar,\
                total_tracks int,\
                artist_name varchar,\
                PRIMARY KEY(album_id)\
            )',
        )
        data_albums = spotify_consume.get_artist_for_name(
            client_id, client_secret, band, qnt_albums
        )
        insert_data(keyspace, table[1], data_albums)
    except Exception as e:
        print(f"[ ERROR | In main function {e}]")
        return None

if __name__ == "__main__":
    list_of_bands = ["Metallica", "Iron Maiden", "Pink Floyd", "AC/DC", "Queen", "Led Zeppelin"]
    for band in list_of_bands:
        main(band, 50)
