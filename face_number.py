import requests
from skimage import io
from io import BytesIO
import api as fr

def face_number(path):
    try:
        imag = requests.get(path).content
        imag = BytesIO(imag)
    except:
        imag = io.imread(path)

    img = fr.load_image_file(imag)
    face_loc = fr.face_locations(img)
    faces_number = len(face_loc)

    return faces_number