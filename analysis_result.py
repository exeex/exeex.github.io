import csv
import os
from pathlib import Path
import json
from collections import Counter

data_folder = Path('data')
files = os.listdir(data_folder)

with open('questions.json', 'r') as f:
    questionnaires = json.load(f)

# print(questionnaires)

all_answers = {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': []}

for questionnaire in questionnaires:
    name = questionnaire['name']
    csv_file = name + '.csv'
    print(csv_file)

    # q_standard_answers = questionnaire['questions']
    q_standard_answers = [{'A': questionnaire['questions'][str(idx)]['A'].split('-')[0],
                           'B': questionnaire['questions'][str(idx)]['B'].split('-')[0],
                           'type': questionnaire['questions'][str(idx)]['type']}
                          for idx in range(1, 11)]

    q_types = ['qua' if 'audio_quality' in q_standard_answer['type'] else 'int' for q_standard_answer in
               q_standard_answers]

    if q_types[0] == 'qua':
        flip = True
    else:
        flip = False

    if flip:
        q_types = q_types[5:] + q_types[:5]

    with open(f'data_processed/{csv_file}', 'w') as out_file:
        print(','.join(q_types), file=out_file)
        print(','.join(q_types))

        with open(data_folder / csv_file, encoding='utf8') as f:
            r = csv.reader(f)
            next(r)  # skip header

            for line in r:
                q_user_answers = line[6:16]

                user_choices = []
                for idx in range(10):
                    try:
                        user_choice = q_standard_answers[idx][q_user_answers[idx]]
                    except KeyError:
                        user_choice = '==='
                    user_choices.append(user_choice)

                if flip:
                    user_choices = user_choices[5:] + user_choices[:5]

                print(','.join(user_choices))
                print(','.join(user_choices), file=out_file)
                all_answers[name].append(user_choices)

    # break


# print(all_answers)

def count_nb(jy3_ag_int_answers):
    a = []
    for t in jy3_ag_int_answers:
        a += list(t)
    return Counter(a)


# against jy3

jy3_ag_answers = all_answers['A'] + all_answers['B'] + all_answers['C'] + all_answers['D']
_jy3_ag_answers = list(zip(*jy3_ag_answers))
jy3_ag_int_answers = _jy3_ag_answers[:5]
jy3_ag_qua_answers = _jy3_ag_answers[5:]

print("# against jy3")
print(count_nb(jy3_ag_int_answers))
print(count_nb(jy3_ag_qua_answers))

# against tak1

tak1_ag_answers = all_answers['E'] + all_answers['F'] + all_answers['G'] + all_answers['H']
_tak1_ag_answers = list(zip(*tak1_ag_answers))
tak1_ag_int_answers = _tak1_ag_answers[:5]
tak1_ag_qua_answers = _tak1_ag_answers[5:]

print("# against tak1")
print(count_nb(tak1_ag_int_answers))
print(count_nb(tak1_ag_qua_answers))
