import csv
import re

sub_num_pattern = r'[\D]+((доб[.])\W+(\d{4}))[)\W]+'
phone_number_pattern = r'([+]7|[8])((\W?){2}(\d{3}))((\W?){2}(\d{3}))((\W?){2}(\d{2}))((\W?){2}(\d{2}))'
name_pattern = r'^((\w+)(\s+|[,]))(((\w+))(\s+|[,]))'


def del_empty_el_from_list(txt):
    for i in txt:
        while '' in i:
            i.remove('')
    return txt


def name_structure(my_list):
    pretty_names = []
    for i in my_list:
        row = ','.join(i)
        pretty_name = re.sub(name_pattern, r'\2,\6,', row)
        pretty_names.append(pretty_name.split(','))
        my_list = pretty_names
    return my_list


def delete_dupl(my_list):
    check = {}
    merged_list = []
    for i in my_list:
        if i[0] not in check.keys():
            check[i[0]] = i
        else:
            n = 1
            for l in range(len(i)):
                if i[n] in check[i[0]]:
                    n += 1
                else:
                    check[i[0]].append(i[n])
    for k, v in check.items():
        merged_list.append(v)
    return merged_list


def phone_structure(my_text):
    pretty_phone = []
    for i in my_text:
        row = ','.join(i)
        pretty_number = re.sub(phone_number_pattern, r'+7(\4)\7-\10-\13', row)
        pretty_sub_number = re.sub(sub_num_pattern, r' \2\3,', pretty_number)
        pretty_phone.append(pretty_sub_number.split(','))
    return pretty_phone


if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        spaces_fix = del_empty_el_from_list(contacts_list)
        name_fix = name_structure(spaces_fix)
        del_dupl = delete_dupl(name_fix)
        pretty_text = phone_structure(del_dupl)

    with open("phonebook.csv", "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(pretty_text)


