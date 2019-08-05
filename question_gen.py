import hashlib
import os
import random
import csv


class Question:
    def __init__(self, question_type, gt_mix, gt_vocal, our, ag):
        table = []
        with open('/home/dccv/Desktop/Code/exeex.github.io/table.csv', mode='r', newline="") as csvfile:
            rows = csv.reader(csvfile)
            for r in rows:
                table += [r]
        self.table = table
        # Interference
        q1_str = """以下三個音檔分別為：參考歌曲，人聲A，人聲B
請依據參考歌曲，辨識A與B何者殘餘之非人聲伴奏較少
The audio below are : reference song, vocal sample A, vocal sample B.
Please select the sample (A or B) which had less residual of accompaniments(non-vocal sounds) according to the reference

1. 參考音檔 reference song  mix_gt: %s
2. 人聲樣本 vocal sample A  : %s
3. 人聲樣本 vocal sample B  : %s

請問，聽完參考歌曲後，比較人聲A與B，何者殘餘之非人聲伴奏較少? 
Which sample (A or B) had less residual of accompaniments(non-vocal sounds) according to the reference track ?"""

        # Audio quality
        q2_str = """以下三個音檔分別為：參考人聲，人聲A，人聲B
請依據參考人聲，辨識A與B何者與參考音檔的音質較相近
The audio below are : reference vocal, vocal sample A, vocal sample B.
Please select the sample (A or B) which was closer to the reference in terms of audio quality

1. 參考人聲 reference vocal  vocal_gt: %s
2. 人聲樣本 vocal sample A  : %s
3. 人聲樣本 vocal sample B  : %s

請問，聽完參考人聲後，比較人聲A與B，何者與參考人聲的音質較相近?
Which sample (A or B) was closer to the reference in terms of audio quality ?"""
        self.question_type = question_type
        if question_type == 0:
            self.question = q1_str
        else:
            self.question = q2_str

        self.answer = """
ref : %s , %s , %s
our : %s , %s , %s
ag  : %s , %s , %s
A    B   無法分辨 (Unable to distinguish)
"""

        self.gt_mix = gt_mix
        self.gt_vocal = gt_vocal
        self.our = our
        self.ag = ag
        self.qstr = self.question % (self.gt_mix, *random_swap(self.our, self.ag))

    def __repr__(self):
        return self.qstr

    def get_ut(self):
        gt_mix_ut, ag_ut, our_ut = 0, 0, 0
        for t in self.table:
            if t[0] == self.gt_mix:
                gt_mix_ut = t[2]
            if t[0] == self.gt_vocal:
                gt_vocal_ut = t[2]
            if t[0] == self.ag:
                ag_ut = t[2]
            if t[0] == self.our:
                our_ut = t[2]
        return gt_mix_ut, gt_vocal_ut, ag_ut, our_ut

    def get_answer_mix(self):
        gt_mix_ut, gt_vocal_ut, ag_ut, our_ut = self.get_ut()
        return self.answer % (
            self.gt_mix, hash_file_name(self.gt_mix), gt_mix_ut,
            self.our, hash_file_name(self.our), our_ut,
            self.ag, hash_file_name(self.ag), ag_ut)

    def get_answer_vocal(self):
        gt_mix_ut, gt_vocal_ut, ag_ut, our_ut = self.get_ut()
        return self.answer % (self.gt_vocal, hash_file_name(self.gt_vocal), gt_vocal_ut,
                              self.our, hash_file_name(self.our), our_ut,
                              self.ag, hash_file_name(self.ag), ag_ut)

    def get_question(self):
        if self.question_type == 0:
            return self.question % (self.gt_mix, *random_swap(self.our, self.ag))
        else:
            return self.question % (self.gt_vocal, *random_swap(self.our, self.ag))


def hash_name(input_str: str):
    a = hashlib.md5(input_str.encode('utf8'))
    return a.hexdigest()[:5]


def hash_file_name(file_name):
    name, ext = os.path.splitext(file_name)
    hashed_name = hash_name(name)
    return hashed_name + ext


def random_swap(a, b):
    if random.choice([True, False]):
        return b, a
    else:
        return a, b


gt_vocal_file_names = [f'gt_vocal-{_id + 1}.mp4' for _id in range(40)]
gt_mix_file_names = [f'gt_mix-{_id + 1}.mp4' for _id in range(40)]
our_vocal_file_names = [f'our-{_id + 1}.mp4' for _id in range(40)]
jy3_vocal_file_names = [f'jy3-{_id + 1}.mp4' for _id in range(40)]
tak_vocal_file_names = [f'tak-{_id + 1}.mp4' for _id in range(40)]

song_number = 10
# id_start = [x * 4 for x in range(10)]
select_id = [x * 4 for x in range(0, song_number)]
print("select ids", select_id)


def print_questions(ag_vocal_file_names, seed, type_add=0, flip=False):
    oppo_name = ag_vocal_file_names[0].split("-")[0]
    id_add = type_add

    print(" . . . (", oppo_name, ", id +", id_add, ", flip :", str(flip), ")")
    file_name_map = {}
    q_list = []
    for idx in range(song_number):
        # 確保每次是否swap的隨機種子是固定的
        random.seed(idx + seed)
        i = select_id[idx]
        # 把檔名hash，並印出檔名

        _a = i + type_add

        gt_mix = gt_mix_file_names[i + type_add]
        gt_vocal = gt_vocal_file_names[i + type_add]
        our = our_vocal_file_names[i + type_add]
        ag = ag_vocal_file_names[i + type_add]

        if idx < song_number // 2:
            if flip:
                q = Question(1, gt_mix, gt_vocal, our, ag)
            else:
                q = Question(0, gt_mix, gt_vocal, our, ag)
        else:
            if flip:
                q = Question(0, gt_mix, gt_vocal, our, ag)
            else:
                q = Question(1, gt_mix, gt_vocal, our, ag)
        q_list.append(q)

    for i, q in enumerate(q_list):
        sid = q.ag.split("-")[1].split(".mp4")[0]
        m_v = q.question.split(":")[0].split(" ")[-1]
        oppo = q.ag.split("-")[0]
        print(f'\n======Question {i + 1}======      kinds=', sid, m_v, oppo)
        print(i + 1, ".")
        _q = q.get_question()
        print(q.get_question())

        # print('\n')
        # print(f'\n------Answer {i + 1}------')
        if i < len(q_list) // 2:
            if flip:
                print(q.get_answer_vocal())
            else:
                print(q.get_answer_mix())
        else:
            if flip:
                print(q.get_answer_mix())
            else:
                print(q.get_answer_vocal())

        file_name_map[q.gt_mix] = hash_file_name(q.gt_mix)
        file_name_map[q.gt_vocal] = hash_file_name(q.gt_vocal)
        file_name_map[q.our] = hash_file_name(q.our)
        file_name_map[q.ag] = hash_file_name(q.ag)

        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

    return file_name_map


if __name__ == '__main__':
    from pathlib import Path
    from shutil import copyfile

    print('\n\n                                                   ###########問卷A###########', end=" . . .")

    file_name_map_a = print_questions(jy3_vocal_file_names, 0, type_add=0)

    print('\n\n                                                   ###########問卷B###########', end=" . . .")
    file_name_map_b = print_questions(jy3_vocal_file_names, 0, type_add=0, flip=True)

    print('\n\n                                                   ###########問卷C###########', end=" . . .")

    file_name_map_c = print_questions(jy3_vocal_file_names, 0, type_add=2)

    print('\n\n                                                   ###########問卷D###########', end=" . . .")
    file_name_map_d = print_questions(jy3_vocal_file_names, 0, type_add=2, flip=True)

    print('\n\n                                                   ###########問卷E###########', end=" . . .")

    file_name_map_e = print_questions(tak_vocal_file_names, 0, type_add=0)

    print('\n\n                                                   ###########問卷F###########', end=" . . .")
    file_name_map_f = print_questions(tak_vocal_file_names, 0, type_add=0, flip=True)

    print('\n\n                                                   ###########問卷G###########', end=" . . .")

    file_name_map_g = print_questions(tak_vocal_file_names, 0, type_add=2)

    print('\n\n                                                   ###########問卷H###########', end=" . . .")
    file_name_map_h = print_questions(tak_vocal_file_names, 0, type_add=2, flip=True)

    #
    #
    #
    #
    #
    # print('\n\n                                                   ###########問卷E###########')
    #
    # file_name_map_e = print_questions(jy3_vocal_file_names, 0, type_add=2)
    #
    # print('\n\n                                                   ###########問卷F###########')
    # file_name_map_f = print_questions(tak_vocal_file_names, 0, type_add=2, flip=True)
    #
    # print('\n\n                                                   ###########問卷G###########')
    #
    # file_name_map_g = print_questions(jy3_vocal_file_names, 0, type_add=3)
    #
    # print('\n\n                                                   ###########問卷H###########')
    # file_name_map_h = print_questions(tak_vocal_file_names, 0, type_add=3, flip=True)

    total_name_map = {**file_name_map_a, **file_name_map_b, **file_name_map_c, **file_name_map_d,
                      **file_name_map_e, **file_name_map_f, **file_name_map_g, **file_name_map_h}

    # output_folder = Path('output2')
    in_folder = Path('output_sdr5')
    import os

    if not os.path.exists('hashed_output'):
        os.mkdir('hashed_output')
    out_folder = Path('hashed_output')

    print('\n ###########對照表###########')
    for source, target in total_name_map.items():
        print(source, ',', target)
        copyfile(in_folder / source, out_folder / target)
