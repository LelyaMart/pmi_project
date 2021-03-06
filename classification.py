import sqlite3

import dlib
import numpy as np

sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')

detector = dlib.get_frontal_face_detector()


def read_sqlite_table(gender):
    sqlite_connection = sqlite3.connect('teachers4.db')
    cursor = sqlite_connection.cursor()
    try:
        f = []
        if(gender != "error"):
            sqlite_select_query = """SELECT * from teachers WHERE WM=?"""
            cursor.execute(sqlite_select_query, (gender,))
        else:
            sqlite_select_query = """SELECT * from teachers"""
            cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        for row in records:
            x = row[3].split('\n')
            f.append(np.array(x, dtype=float))
    finally:
        cursor.close()
        sqlite_connection.close()
    return f


def face_Descriptor(img, sp, facerec, detector):
    dets = detector(img, 1)
    for k, d in enumerate(dets):
        shape = sp(img, d)

    face_descriptor1 = facerec.compute_face_descriptor(img, shape)
    return face_descriptor1


def print_src(id):
    sqlite_connection = sqlite3.connect('teachers4.db')
    cursor = sqlite_connection.cursor()
    sql_select_query = "select * from teachers"
    cursor.execute(sql_select_query)
    records = cursor.fetchall()
    cursor.close()
    sqlite_connection.close()
    return records[id]
