import csv

def find(data, key):
    count = 0
    for row in data:
        if row[0] == str(key):
            break
        count += 1
    return count


def write_result_to_csv(result):
    with open('results.csv') as file:
        data = [r for r in csv.reader(file, delimiter=" ")]
        count = find(data, result)
        if count < len(data):
            data[count][1] = str(int(data[count][1]) + 1)
            update_top_csv(data[count])
        else:
            new_row = [result, '1']
            data.append(new_row)
        with open('results.csv', 'w') as file:
            file_writer = csv.writer(file, delimiter=" ", )
            for row in data:
                file_writer.writerow(row)


def write_id_to_csv(user_id, username, result):
    with open('users.csv') as file:
        data = [r for r in csv.reader(file, delimiter=" ")]
        count = find(data, user_id)
        if count < len(data):
            data[count][2] = str(int(data[count][2]) + 1)

            if result != -1:
                data[count][4] = str(int(data[count][4]) + 1)
            else:
                data[count][3] = str(int(data[count][3]) + 1)

        else:
            new_row = [user_id, username, '1']
            if result != -1:
                new_row.append('0')
                new_row.append('1')
            else:
                new_row.append('1')
                new_row.append('0')
            data.append(new_row)
        with open('users.csv', 'w') as file:
            file_writer = csv.writer(file, delimiter=" ", )
            for row in data:
                file_writer.writerow(row)

def write_new_top_csv():
    with open('results.csv') as file:
        data = [r for r in csv.reader(file, delimiter=" ")]
        array = []
        data.pop(0)
        array.append(data[0])
        data.pop(0)
        for result in data:
            number = int(result[1])
            add = True
            for i in range(len(array)):
                if number > int(array[i][1]):
                    array.insert(i, result)
                    add = False
                    break
            if add == True:
                array.append(result)
            array = array[0:5]
        array.insert(0, ['Teacher', 'Number'])
        with open('top.csv', 'w') as topfile:
            file_writer = csv.writer(topfile, delimiter=" ", )
            for row in array:
                file_writer.writerow(row)


def update_top_csv(data):
    array = []
    with open('top.csv') as topfile:
        array = [r for r in csv.reader(topfile, delimiter=" ")]
        array.pop(0)
       # for i in range(5):
           # if int(data[1]) > int(array[i][1]):
               # for g in range(5):
                   # if data[0] == array[g][0]:
                       # array.pop(g)
               # array.insert(i, data)
               # break
       # array = array[0:5]
       # array.insert(0, ['Teacher', 'Number'])
       # with open('top.csv', 'w') as topfile:
           # file_writer = csv.writer(topfile, delimiter=" ", )
           # for row in array:
               # file_writer.writerow(row)
        for i in range(5):
            if array[i][0] == data[0]:
                array.pop(i)
                break
        for i in range(len(array)):
            if int(data[1]) >= int(array[i][1]):
                array.insert(i, data)
                break
        array = array[0:5]
        array.insert(0, ['Teacher', 'Number'])
    with open('top.csv', mode="w") as topfile:
        file_writer = csv.writer(topfile, delimiter=" ")
        for row in array:
            file_writer.writerow(row)

if __name__ == '__main__':
    #with open("users.csv", mode="w") as file:
        #file_writer = csv.writer(file, delimiter=" ")
       # file_writer.writerow(["Id", "Username", "Results", "US_result", "S_result"])

    #with open("results.csv", mode="w") as file:
        #file_writer = csv.writer(file, delimiter=" ")
       # file_writer.writerow(["Teacher", "Number"])

    with open("top.csv", mode="w") as file:
        file_writer = csv.writer(file, delimiter=" ")
        file_writer.writerow(["Teacher", "Number"])

    write_new_top_csv()

