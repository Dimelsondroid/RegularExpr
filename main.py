from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re

with open('phonebook_raw.csv', 'r', encoding='utf-8') as f:
    rows = csv.DictReader(f)
    contacts_list = list(rows)

def formating(data, position):
    for row in data:
        tmp_list = row[position].split(' ')
        # print(tmp_list)
        if len(tmp_list) == 3:
            row['surname'] = str(tmp_list[2])
            row['firstname'] = str(tmp_list[1])
            row['lastname'] = str(tmp_list[0])
            # print(row)
            continue
        elif len(tmp_list) == 2:
            if position == 'firstname':
                row['surname'] = str(tmp_list[1])
                row['firstname'] = str(tmp_list[0])
            elif position == 'lastname':
                row['firstname'] = str(tmp_list[1])
                row['lastname'] = str(tmp_list[0])
            # print(row)
            continue
        elif len(tmp_list) == 1:
            row[position] = str(tmp_list[0])
            # print(row)


def del_duplicate(data):
    for num, row in enumerate(data):
        for i in range(len(data)-1, -1, -1):
            if num == i:
                continue
            elif row['lastname'] == data[i]['lastname'] and row['firstname'] == data[i]['firstname']:
                for key, value in row.items():
                    if not value:
                        row[key] = data[i][key]
                    else:
                        continue
                del data[i]
                break


def format_phones():
    pattern = r'(\+7|8)?\s*?\(?(\d{3})\)?[-|\s*]?(\d{3})[-|\s]*(\d{2})[-|\s]*(\d{2})[^,]?\s?\(?([а-я.]+)?\s?(\d{4})?\)?'
    replace = r'+7(\2)\3-\4-\5 \6\7'
    replace_noADD = r'+7(\2)\3-\4-\5'
    for item in contacts_list:
        if 'доб.' in item['phone']:
            item['phone'] = re.sub(pattern, replace, item['phone'])
        else:
            item['phone'] = re.sub(pattern, replace_noADD, item['phone'])


if __name__ == '__main__':

# Formating LFS
    formating(contacts_list, 'lastname')
    formating(contacts_list, 'firstname')
    formating(contacts_list, 'surname')

# Deleting duplicate query
    del_duplicate(contacts_list)

# Reformat phone numbers
    format_phones()

    header = contacts_list[0].keys()
    with open("phonebook.csv", "w", newline='', encoding='utf-8') as f:
        datawriter = csv.DictWriter(f, header, delimiter=',')
      # Вместо contacts_list подставьте свой список
        datawriter.writeheader()
        datawriter.writerows(contacts_list)
