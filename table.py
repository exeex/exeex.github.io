import csv


def merge_youtube_hamehash():
    csv_table = {}
    i = 0
    with open('/home/dccv/Desktop/Code/exeex.github.io/youtube.csv', mode='r', newline="") as csvfile:
        rows_ut = csv.reader(csvfile)
        rows_ut_local = []
        for row in rows_ut:
            hash_name = row[0]
            ut_name = row[1]
            rows_ut_local += [row]
            # print(".")

    with open('/home/dccv/Desktop/Code/exeex.github.io/name_hash.csv', mode='r', newline="") as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            file_name = row[0].replace(" ", "")
            hash_name = row[1].replace(".mp4", "")
            for row_ut in rows_ut_local:
                _a = row_ut[0].replace(" ", "")
                _b = hash_name.replace(" ", "")
                if _a == _b:
                    print(file_name, end=",")
                    print(hash_name, end=",")
                    print(row_ut[1])
                    csv_table.update({i: [file_name, hash_name, row_ut[1]]})
                    i += 1
                    # print(".")

            # print(".")
        print(".")


if __name__ == '__main__':
    import operator

    with open('/home/dccv/Desktop/Code/exeex.github.io/table.csv', mode='r', newline="") as csvfile:
        rows = csv.reader(csvfile)
        sortedlist = sorted(rows, key=operator.itemgetter(0), reverse=False)
        for r in sortedlist:
            print(r[0], end=",")
            print(r[1], end=",")
            print(r[2])
        # rows_local = []
        # for row in rows:
        #     hash_name = row[0]
        #     ut_name = row[1]
        #     rows_local += [row]
        #     # print(".")

    print(".")
