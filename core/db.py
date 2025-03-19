import psycopg2


def connect_db():
    conn = psycopg2.connect(
        dbname="iq_trainer_users",
        user="postgres",
        password="Kekiv118",
        host="localhost"
    )
    return conn