from classification import *

def clas(src):
    try:
        imag = requests.get(src).content
        imag = Image.open(BytesIO(imag))
        imag = np.array(imag)
    except:
        imag = io.imread(src)

    x = face_Descriptor(imag)

    f = read_sqlite_table()

    scores = np.linalg.norm(x - np.asarray(f), axis=1)
    min_el_ind = scores.argmin()

    return print_src(min_el_ind)

if __name__ == '__main__':
    print(clas(input()))