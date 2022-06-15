import re


def levenshtein(a, b):
    m = [[*range(len(a) + 1)] for _ in range(len(b) + 1)]
    for i in range(len(b) + 1):
        m[i][0] = i
    for i in range(1, len(b) + 1):
        for j in range(1, len(a) + 1):
            m[i][j] = min(m[i - 1][j] + 1, m[i][j - 1] + 1, m[i - 1][j - 1] + (b[i - 1] != a[j - 1]))
    return m[-1][-1]


def valid_plate_num(plate_num):
    pattern = "[A-Za-z]{1,3}-[a-zA-Z]{1,2}[1-9]{0,1}[0-9]{0,1}[0-9]{0,1}[0-9]{0,1}"
    return True if re.fullmatch(pattern, plate_num) else False


def get_time_stamp(datetime_obj):
    return datetime_obj.strftime("%Y-%m-%d") + "T" + datetime_obj.strftime("%H:%M:%S") + "Z"

