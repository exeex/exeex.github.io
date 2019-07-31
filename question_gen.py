import hashlib
import os
import random


class Question:
    def __init__(self, question_type, gt_mix, gt_vocal, our, ag):
        # Interference
        q1_str = """1. 聽參考音檔 mix_gt: %s
2. 聽樣本A: %s
3. 聽樣本B: %s
請問，哪一個樣本殘留的非人聲伴奏聲音較少?"""

        # Audio quality
        q2_str = """1. 聽參考音檔 vocal_gt: %s
2. 聽樣本A: %s
3. 聽樣本B: %s
請問，哪一個樣本的人聲與參考音檔的人聲較相近?"""
        self.question_type = question_type
        if question_type == 0:
            self.question = q1_str
        else:
            self.question = q2_str

        self.answer = """
our : %s , %s
ag  : %s , %s
"""

        self.gt_mix = gt_mix
        self.gt_vocal = gt_vocal
        self.our = our
        self.ag = ag
        self.qstr = self.question % (self.gt_mix, *random_swap(self.our, self.ag))

    def __repr__(self):
        return self.qstr

    def get_answer(self):
        return self.answer % (self.our, hash_file_name(self.our), self.ag, hash_file_name(self.ag))

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


song_number = 20

gt_vocal_file_names = [f'gt_vocal-{_id + 1}.mp4' for _id in range(50)]
gt_mix_file_names = [f'gt_mix-{_id + 1}.mp4' for _id in range(50)]
our_vocal_file_names = [f'our-{_id + 1}.mp4' for _id in range(50)]
jy3_vocal_file_names = [f'jy3-{_id + 1}.mp4' for _id in range(50)]
tak_vocal_file_names = [f'tak-{_id + 1}.mp4' for _id in range(50)]

select_id = [x * 2 for x in range(1, song_number + 1)]
print(select_id)


def print_questions(ag_vocal_file_names, seed):
    file_name_map = {}

    q_list = []
    for idx in range(song_number):
        # 確保每次是否swap的隨機種子是固定的
        random.seed(idx + seed)
        i = select_id[idx] - 1
        # 把檔名hash，並印出檔名
        gt_mix = gt_mix_file_names[i]
        gt_vocal = gt_vocal_file_names[i]
        our = our_vocal_file_names[i]
        ag = ag_vocal_file_names[i]

        if idx < song_number // 2:
            q = Question(0, gt_mix, gt_vocal, our, ag)
        else:
            q = Question(1, gt_mix, gt_vocal, our, ag)
        q_list.append(q)

    for q in q_list:
        print(f'\n======Question {idx}======')
        print(q.get_question())

        print(f'\n------Answer {idx}------')
        print(q.get_answer())

        file_name_map[q.gt_mix] = hash_file_name(q.gt_mix)
        file_name_map[q.gt_vocal] = hash_file_name(q.gt_vocal)
        file_name_map[q.our] = hash_file_name(q.our)
        file_name_map[q.ag] = hash_file_name(q.ag)

    return file_name_map


if __name__ == '__main__':
    from pathlib import Path
    from shutil import copyfile

    print('###########問卷A###########')

    file_name_map1 = print_questions(jy3_vocal_file_names, 0)

    print('###########問卷B###########')
    file_name_map2 = print_questions(tak_vocal_file_names, 0)

    total_name_map = {**file_name_map1, **file_name_map2}

    in_folder = Path('output')
    out_folder = Path('hashed_output')

    print('\n ###########對照表###########')
    for source, target in total_name_map.items():
        print(source, ',', target)
        copyfile(in_folder / source, out_folder / target)
