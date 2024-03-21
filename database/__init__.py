import psycopg2

def connect_to_db():
    connection = psycopg2.connect(user="dummy",
                            password="pswd1",
                            host="localhost",
                            database="flask_db")
    return connection
"""
Did not implement ORM abstraction
would use SQLAlchemy, define tables->classes to map to them
add SQLAlchemy session
rewrite the plain SQL commands to ORM provided query-s
"""