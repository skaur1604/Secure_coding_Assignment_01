import os
import re
import ssl
import smtplib
import pymysql

from urllib.request import urlopen, Request
from email.message import EmailMessage

db_config = {
    "host": os.getenv("DB_HOST", "mydatabase.com"),
    "user": os.getenv("DB_USER", "app_writer"),
    "password": os.getenv("DB_PASSWORD", "CHANGE_ME"),
    "database": os.getenv("DB_NAME", "mydb"),
    "ssl": {"ssl": {}} 
}

def get_user_input():
    name = input("Enter your name: ")
    if not re.fullmatch(r"[A-Za-z ,.'-]{1,80}", name):
        raise ValueError("Invalid name")
    return name

def send_email(to, subject, body):
    msg = EmailMessage()
    msg["From"] = "no-reply@example.com"
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    with smtplib.SMTP("localhost") as s:
        s.send_message(msg)

def get_data():
    url = "https://secure-api.example.com/get-data"
    req = Request(url, headers={"User-Agent": "secure-demo"})
    with urlopen(req, timeout=10, context=ssl.create_default_context()) as r:
        return r.read().decode("utf-8", "replace")

def save_to_db(data):
    sql = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
    conn = pymysql.connect(**db_config)
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (data, "Another Value"))
        conn.commit()
    finally:
        conn.close()

if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)
