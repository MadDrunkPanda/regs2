import csv
import re
from pprint import pprint


def repair_data():
    header = ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']
    data = []
    data.append(header)
    pattern1 = r'\+7\s\((\d{3})\)\s(\d{3})\-(\d+)\-(\d+)\s\(*(доб.)\s(\d+)\)*'
    subst1 = r'+7 (\1) \2-\3-\4 \5\6'
    pattern2 = r'(\+7|8)\s*\(*(\d{3})\)*\s*\-*(\d{3})\-*(\d{2})\-*(\d{2})'
    subst2 = r'+7 (\2) \3-\4-\5'
    with open("phonebook_raw.csv", encoding='utf8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['phone'] = re.sub(pattern1, subst1, row['phone'])
            row['phone'] = re.sub(pattern2, subst2, row['phone'])
            conc_name = (row['lastname'] + ' ' + row['firstname'] + ' ' + row['surname']).split()
            while len(conc_name) != 3:
                conc_name.append(' ')
            row['lastname'] = conc_name[0]
            row['firstname'] = conc_name[1]
            row['surname'] = conc_name[2]
            x = [row['lastname'], row['firstname'], row['surname'], row['organization'], row['position'], row['phone'],
                 row['email']]
            line = x.copy()
            data.append(line)
    return data


def delete_clones():
    clones = []
    list1 = repair_data().copy()
    list2 = repair_data().copy()
    for line in list1:
        for person in list2:
            if line != person and line[0] == person[0] and line[1] == person[1]:
                united_line = []
                united_line.append(line[0])
                united_line.append(line[1])
                united_line.append(''.join(set([line[2], person[2]])))
                united_line.append(''.join(set([line[3], person[3]])))
                united_line.append(''.join(set([line[4], person[4]])))
                united_line.append(''.join(set([line[5], person[5]])))
                united_line.append(''.join(set([line[6], person[6]])))
                x = united_line[:]
                clones.append(x)
                list2.remove(person)
                list2.remove(line)
    for el in clones:
        list2.append(el)
    return list2

def write_csv():
    with open("phonebook.csv", "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(delete_clones())



