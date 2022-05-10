import requests
import sqlite3
from bs4 import BeautifulSoup
import dlib
from skimage import io
from scipy.spatial import distance
import numpy as np
from PIL import Image
from io import BytesIO

def face_Descriptor(img):
    win1 = dlib.image_window()
    win1.clear_overlay()
    win1.set_image(img)

    dets = detector(img, 1)
    for k, d in enumerate(dets):
        shape = sp(img, d)
        win1.clear_overlay()
        win1.add_overlay(d)
        win1.add_overlay(shape)

    face_descriptor1 = facerec.compute_face_descriptor(img, shape)
    return face_descriptor1

sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
detector = dlib.get_frontal_face_detector()

url = 'https://home.mephi.ru/people'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
pagination = soup.find_all('ul', class_='pagination')
allA = pagination[0].find_all('a')
hrefs = []
for a in allA:
    hrefs.append('https://home.mephi.ru/' + a.get('href'))

newHrefs = []

for href in hrefs:
    response = requests.get(href)
    soup = BeautifulSoup(response.text, 'lxml')
    pagination = soup.find_all('ul', class_='pagination')
    newHrefs.append(href)
    if len(pagination) > 1:
        pagination = pagination[1]
        allA = pagination.find_all('a')
        for i in range(1,len(allA)-2,1):
            newHrefs.append(href+'&page='+(str)(i+1))
prepod = []

k = 0
for href in newHrefs:
    response = requests.get(href)
    soup = BeautifulSoup(response.text, 'lxml')
    userResponsive = soup.find_all('a', class_='list-group-item list-group-item-user-public')
    for user in userResponsive:
        newHref = 'https://home.mephi.ru' + user.get('href')
        response = requests.get(newHref)
        soup = BeautifulSoup(response.text, 'lxml')
        user_responsive = soup.find_all('img', class_='user-responsive')[0]
        src = 'https://home.mephi.ru/' + user_responsive.get('src')
        fio = (str)(user_responsive.get('alt')).replace("\xa0",' ')
        if (src != 'https://home.mephi.ru//assets/user-370efeda38c984a57bc973952b1e6da588e0af98957fe51a0a8599b54847d76f.svg'):
            list1 = []
            imag = requests.get(src).content
            imag = Image.open(BytesIO(imag))
            imag = np.array(imag)
            try:
                face_Descriptor(imag)
            except:
                continue
            else:
                f0 = face_Descriptor(imag)
            k += 1
            list1.append(k)
            list1.append(src)
            list1.append(fio)
            list1.append(str(f0))
            prepod.append(list1)


conn = sqlite3.connect("teachers2.db")

cursor = conn.cursor()

cursor.executemany("INSERT INTO teachers VALUES(?, ?, ?, ?)", prepod)
conn.commit()
conn.close()