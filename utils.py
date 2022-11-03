import hashlib
import flask_login
import flask
import globalss as gb
import apsw
from apsw import Error
import os 


iterations = 200_000

def hash_users(users):
    for user in users:
        psw = users[user]['password'].encode()
        salt = users[user]['salt']
        h = hashlib.pbkdf2_hmac('sha256', psw, salt, iterations)
        users[user]['password'] = h


def hash_string(s, salt):
    h = hashlib.pbkdf2_hmac('sha256', s, salt, iterations)
    return h


class User(flask_login.UserMixin):
    pass


def user_name_safe(username):
    safe = "_.123456789qwertyuiopasdfghjklzxcvbnm"
    for a in username:
        if a not in safe:
            return False
    return True
    

from urllib.parse import urlparse, urljoin

def is_safe_url(target):
    ref_url = urlparse(flask.request.host_url)
    test_url = urlparse(urljoin(flask.request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


# https://www.geeksforgeeks.org/python-program-check-validity-password/
def is_password_strong(s):
    l, u, d = 0, 0, 0
    if (len(s) >= 8):
        for i in s:
            # counting lowercase alphabets
            if (i.islower()):
                l+=1           
    
            # counting uppercase alphabets
            if (i.isupper()):
                u+=1           
    
            # counting digits
            if (i.isdigit()):
                d+=1           
    if (l>=1 and u>=1 and d>=1):
        return True
    else:
        return False


def is_username_valid(name):
    alphabet = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ._"
    for a in name:
        if a not in alphabet:
            return False
    return True


def is_username_taken(name, verbose=False):
    stmt = f"SELECT * FROM users WHERE name=?"
    try:
        c = gb.conn.execute(stmt, (name,))
        rows = c.fetchall()
        if (verbose):
            print(f"The result of searching for {name}: {rows}")
        c.close()
        if len(rows) == 0:
            if (verbose):
                print(f"Username {name} not taken")
            return False
        else:
            if (verbose):
                print(f"Username {name} taken")
            return True
    except Error as e:
        print (e)
        return (f'{result}ERROR: {e}', 500)


def register(username, password):
    salt = os.urandom(16)
    psw = hash_string(password.encode(), salt)
    stmt = f"INSERT INTO users VALUES (?, ?, ?)"
    try:
        gb.conn.execute(stmt, (username, psw, salt))
        print("query executed")
    except Error as e:
        print (e)
        return (f'{result}ERROR: {e}', 500)


def check_user(username, password):
    stmt = f"SELECT * FROM users WHERE name=?"
    try:
        c = gb.conn.execute(stmt, (username,))
        rows = c.fetchall()
        print(f"The result of searching for {username}: {rows}")
        c.close()
        if len(rows) == 1:
            hashed_psw = rows[0][1]
            salt = rows[0][2]
            if hash_string(password.encode(), salt) == hashed_psw:
                print(f"psw checks out")
                return True
            else:
                return False 
        else:
            print(f"Username {username} not found (or found duplicates who knows)")
            return False
    except Error as e:
        print (e)
        return (f'{result}ERROR: {e}', 500)

    return False


def insert_message(sender, timestamp, content, replyId, recipients):
    try:
        stmt = f"INSERT INTO messages (sender, timestamp, content, replyId, recipients) values (?, ?, ?, ?, ?);"
        gb.conn.execute(stmt, (sender, timestamp, content, replyId, recipients))
        print(f"Successfuly inserted {sender} {timestamp} {content} {replyId} {recipients}")
        return format_messages_html([format_message((">", sender, timestamp, content, replyId, recipients))])
    except Error as e:
        return f'ERROR: {e}'


def fetch_message_id(query, user):
    stmt = f"SELECT * FROM messages WHERE (recipients=? or recipients='#all' or sender=?) and id=?"
    try:
        c = gb.conn.execute(stmt, (user, user, query))
        rows = c.fetchall()
        print(f"The result of searching for {query}: {rows}")
        c.close()
        return rows
    except Error as e:
        print (e)
        return (f'ERROR: {e}', 500)


def fetch_messages(user):
    stmt = f"SELECT * FROM messages WHERE recipients=? or recipients='#all' or sender=?"
    try:
        c = gb.conn.execute(stmt, (user, user))
        rows = c.fetchall()
        print(f"The result of searching all: {rows}")
        c.close()
        return rows
    except Error as e:
        print (e)
        return (f'ERROR: {e}', 500)


def format_message(message):
    id, sender, timestamp, content, replyId, recipients = message
    head = f"[{id}] {sender} to {recipients} at {timestamp.split('.')[0]} "
    if replyId > -1:
        head += f"in reply to [{replyId}]"
    return [f"{head}", f"{content}"]

def format_messages_html(messages):
    output=f""
    for message in messages:
        output += f"<h3> {message[0]} </h3> {message[1]} <p></p>"
    return output

