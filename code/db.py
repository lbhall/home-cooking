import psycopg2
import logging

class Postgres:
    @staticmethod
    def connect():
        try:
            conn = psycopg2.connect(
                host="192.168.0.11",
                database="homecooking-dev",
                user="bhall",
                password="bandit")
            return conn
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error("{}:{}".format(type(error).__name__, str(error)))

    @staticmethod
    def execute(conn, sql, args):
        try:
            cur = conn.cursor()
            cur.execute(sql, args)
            return cur
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error("{}:{}".format(type(error).__name__, str(error)))

    @staticmethod
    def close(conn):
        try:
            if conn:
                conn.close()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error("{}:{}".format(type(error).__name__, str(error)))

    @staticmethod
    def closecursor(cur):
        try:
            if cur:
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error("{}:{}".format(type(error).__name__, str(error)))

    @staticmethod
    def closeall(conn, cur):
        try:
            if cur:
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error("{}:{}".format(type(error).__name__, str(error)))
        finally:
            if conn:
                conn.close()

    @staticmethod
    def fetchall(cur):
        try:
            return cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error("{}:{}".format(type(error).__name__, str(error)))

    @staticmethod
    def fetchone(cur):
        try:
            return cur.fetchone()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error("{}:{}".format(type(error).__name__, str(error)))
