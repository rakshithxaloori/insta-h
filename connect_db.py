import psycopg2
from config import password


class DatabaseOperations:
    def __init__(self):
        self.conn = self.connect()
        if self.conn is None:
            raise EnvironmentError
        # self.create_tables()

    def connect(self):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(
                database="insta_h",
                user="postgres",
                password=password,
                host="insta-h.caszfqc7hout.ap-south-1.rds.amazonaws.com",
                port='5432')

            # create a cursor
            cur = conn.cursor()

            # execute a statement
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = cur.fetchone()
            print(db_version)

            # close the communication with the PostgreSQL
            return conn
            # cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            return None
            print(error)
        # finally:
        #     if conn is not None:
        #         conn.close()
        #         print('Database connection closed.')

    def create_tables(self):
        try:
            command = "CREATE TABLE insta_usernames(id SERIAL PRIMARY KEY, username VARCHAR(100) NOT NULL, status CHAR(1) NOT NULL)"
            cur = self.conn.cursor()
            cur.execute(command)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if cur is not None:
                cur.close()

    def add_to_database(self, username):
        try:
            command = "INSERT INTO insta_usernames (username, status) SELECT %s, %s WHERE NOT EXISTS (SELECT 1 FROM insta_usernames WHERE username=%s LIMIT 1)"
            cur = self.conn.cursor()
            cur.execute(command, (username, "P", username))
            self.conn.commit()
            print(username, "ADDED DB")
        except Exception as e:
            print(e)
        finally:
            if cur is not None:
                cur.close()

    def fetch_username(self):
        try:
            command = "SELECT username, status FROM insta_usernames WHERE status LIKE 'P' LIMIT 1"
            cur = self.conn.cursor()
            cur.execute(command)
            row = cur.fetchone()
            return row
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if cur is not None:
                cur.close()

    def update_username(self, username):
        try:
            command = "UPDATE insta_usernames SET status = %s WHERE username = %s"
            cur = self.conn.cursor()
            cur.execute(command, ("S", username))
            self.conn.commit()
            print(username, "UPDATED DB")

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if cur is not None:
                cur.close()


    def close_connection(self):
        self.conn.close()
        print("CONNECTION CLOSED DB")


# if __name__ == '__main__':
#     new_database_operation = DatabaseOperations()
#     # new_database_operation.create_tables()
#     new_database_operation.add_to_database("randoma")
#     print(new_database_operation.fetch_username()[0])
#     new_database_operation.update_username("randoma")
#     new_database_operation.conn.close()
#     print("CONNECTION CLOSED")
