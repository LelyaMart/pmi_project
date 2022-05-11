from classification import *


def clas(image_numpy_array):
    x = face_Descriptor(image_numpy_array, sp, facerec, detector)
    f = read_sqlite_table()

    scores = np.linalg.norm(x - np.asarray(f), axis=1)
    min_el_ind = scores.argmin()

    return print_src(min_el_ind)


if __name__ == '__main__':
    print(clas(input()))
