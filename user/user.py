from flask import Blueprint
from flask import request, jsonify

import datetime

from database import connect_to_db


user = Blueprint("user", __name__)

# establish one cursor connection vs
# in each endpoint reconnect and disconnect cur
# connection cursort jobban megnézni a connection.commit() miatt
# utolsó tesztek, unit test nem volt
"""
Increasing load-> database reading and writing will be slowed,
only one cursor for the operations
concurrent writing requests to the database-> not handled
"""
cur = connect_to_db().cursor()

#ez biztos jó így?
connection = connect_to_db()

@user.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    """password is stored as text, not ideal should use hash
       funciton sha256/bcrypt/flask-hashing
       install extension -> implement password hashing
       before storing the hashed password"""
    sql_query = "INSERT INTO users \
                (name,email,password,last_login)\
                VALUES \
                (%s,%s,%s,%s);"
    try:
        cur.execute(sql_query,
                    (data['name'],
                     data['email'],
                     data['password'],
                     datetime.datetime.now()))
        connection.commit()
        return jsonify(message="user created")
    except Exception as e:
        print(e)
        return jsonify(message="Something went wrong"), 500


@user.route("/user", methods=["GET"])
def list_all_users():
    sql_query = "SELECT name,email,last_login \
                 FROM users;"
    try:
        cur.execute(sql_query)
        users = cur.fetchall()
        return jsonify(users)
    except Exception as e:
        print(e)
        return jsonify(message="Something went wrong"), 500


@user.route("/user", methods=["DELETE"])
def delete_user():
    data = request.get_json()
    sql_query = "DELETE FROM users WHERE users.email= %s;"
    try:
        cur.execute(sql_query,
                    ([data['email'],]))
        if not cur.rowcount:
            return jsonify(message="user does not exist"), 404
        connection.commit()
        return jsonify(message="user deleted")
    except Exception as e:
        print(e)
        return jsonify(message="Something went wrong"), 500


@user.route("/user/modify", methods=["PATCH"])
def update_user():
    # does not check if given data is new or not
    # compare the existing database data to the requested data
    # if the 2 list is not equal let it update 
    # otherwise return "alredy updated with provided data" 
    data = request.get_json()
    sql_query = "UPDATE users \
                SET name= %s, password = %s \
                WHERE users.email= %s;"
    try:
        cur.execute(sql_query,
                    (data['name'],
                     data['password'],
                     data['email'],))
        if not cur.rowcount:
            return jsonify(message="user does not exist"), 404
        connection.commit()
        return jsonify(message="user updated")
    except Exception as e:
        print(e)
        return jsonify(message="Something went wrong"), 500


@user.route("/login", methods=["GET"])
def login():
    data = request.get_json()
    """ if hashing implented, could check for existing email,
        then compare the stored password and the hashed one,
        or do this in one step, the 2 step implementation
        could spare the resources for computing the hash
    """
    sql_query = "SELECT name \
                FROM users \
                WHERE users.email= %s AND users.password= %s;"
    try:
        cur.execute(sql_query,
                    (data['email'],
                     data['password'],))
        if not cur.rowcount:
            return jsonify(message="no user found"), 404
        sql_query = "UPDATE users \
                    SET last_login= %s \
                    WHERE users.email= %s;"
        cur.execute(sql_query,
                    (datetime.datetime.now(),
                     data['email'],))
        connection.commit()
        return jsonify(message="sucessful login")
    except Exception as e:
        print(e)
        return jsonify(message="something went wrong"), 500