import api


def face_number(image_numpy_array):
    face_count = 0
    try:
        face_locations = api.face_locations(image_numpy_array)
        face_count = len(face_locations)
    except Exception as e:  # фото не распознано
        print(e)
    return face_count


if __name__ == '__main__':
    print(face_number('https://upload.wikimedia.org/wikipedia/commons/4/41/Siberischer_tiger_de_edit02.jpg'))
