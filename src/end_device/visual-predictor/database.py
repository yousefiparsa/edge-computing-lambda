import mysql.connector as sql
import yaml


def connection():
    # Read config parameters for mysql
    with open('config.yaml') as f:
        config = yaml.safe_load(f)
        host = config['cloud_mysql_hostname']
        username = config['cloud_mysql_username']
        password = config['cloud_mysql_password']
        database = config['cloud_mysql_database']
        port = config['cloud_mysql_port']

    conn = sql.connect(host=host,
                       user=username,
                       passwd=password,
                       db=database,
                       port=port)
    c = conn.cursor()

    return c, conn
