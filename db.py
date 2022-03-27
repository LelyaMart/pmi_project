import csv
import sqlite3

conn = sqlite3.connect('statistic.db')
cursor = conn.cursor()

def make_db():
    global cursor
    text = '''CREATE TABLE users (
        user_id INTEGER,
        username TEXT,
        results TEXT,
        US_result TEXT,
        S_result TEXT
    );'''
    cursor.execute(text)
    make_users()
    text = '''CREATE TABLE results (
        teacher TEXT,
        number INTEGER
    );'''
    conn.execute(text)
    make_results()
    conn.commit()

def make_users():
    global cursor
    with open('users.csv') as file:
        data = [r for r in csv.reader(file, delimiter=" ")]
        data.pop(0)
        for i in data:
            text = "INSERT INTO users (user_id, username, results, US_result, S_result) VALUES ( ?, ?, ?, ?, ?);"
            cursor.execute(text, (int(i[0]), i[1], int(i[2]), int(i[3]), int(i[4]),))
        conn.commit()

def make_results():
    global cursor
    with open('results.csv') as file:
        data = [r for r in csv.reader(file, delimiter=" ")]
        data.pop(0)
        for i in data:
            text = "INSERT INTO results (teacher, number) VALUES ( ?, ?);"
            cursor.execute(text, (i[0], int(i[1])))
    conn.commit()

def update_results(fio):
    conn = sqlite3.connect('statistic.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM results WHERE teacher=?;", (fio,))
    data = cursor.fetchall()
    if len(data) == 0:
        text = "INSERT INTO results (teacher, number) VALUES ( ?, ?);"
        cursor.execute(text, (fio, 0, ))
    else:
        cursor.execute("UPDATE results SET number = ? WHERE teacher=?;", (int(data[0][1])+1, fio,))
    conn.commit()


def update_users(user_id, username, result):
    conn = sqlite3.connect('statistic.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    data = cursor.fetchall()
    print(data)
    if len(data) == 0:
        if result != -1:
            cursor.execute("INSERT INTO users (user_id, username, results, US_result, S_result) VALUES ( ?, ?, ?, ?, ?);" , (user_id, username, 1, 0, 1, )) 
        else:
            cursor.execute("INSERT INTO users (user_id, username, results, US_result, S_result) VALUES ( ?, ?, ?, ?, ?);", (user_id, username, 1, 1, 0, )) 
    else:
        if result != -1:
            cursor.execute("UPDATE users SET results = ?, S_result = ? WHERE user_id=?;", (int(data[0][2])+1, int(data[0][4])+1, data[0][0], ))
        else:
            cursor.execute("UPDATE users SET results = ?, US_result = ? WHERE user_id=?;", (int(data[0][2])+1, int(data[0][3])+1, data[0][0], ))
    conn.commit()


def top():
    conn = sqlite3.connect('statistic.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM results ORDER BY number DESC")
    data = cursor.fetchall()
    return data[0:5]


def check():
    conn = sqlite3.connect('statistic.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", ("Godlike03", ))
    data = cursor.fetchall()
    for i in data:
        print(i)

if __name__ == '__main__':
    check()

