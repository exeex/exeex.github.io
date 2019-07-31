import hashlib
import os
import random


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

gt_vocal_file_names = [f'gt_vocal-{_id + 1}.mp3' for _id in range(song_number)]
gt_mix_file_names = [f'gt_mix-{_id + 1}.mp3' for _id in range(song_number)]
our_vocal_file_names = [f'our-{_id + 1}.mp3' for _id in range(song_number)]
jy3_vocal_file_names = [f'jy3-{_id + 1}.mp3' for _id in range(song_number)]
tak_vocal_file_names = [f'tak-{_id + 1}.mp3' for _id in range(song_number)]

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


def print_questions(ag_vocal_file_names, seed):
    for idx in range(song_number):
        # 確保每次是否swap的隨機種子是固定的
        random.seed(idx + seed)

        # 把檔名hash，並印出檔名
        gt_mix = hash_file_name(gt_mix_file_names[idx])
        gt_vocal = hash_file_name(gt_vocal_file_names[idx])
        our = hash_file_name(our_vocal_file_names[idx])
        ag = hash_file_name(ag_vocal_file_names[idx])

        print(f'\n=======Question {idx}=======')
        if idx < song_number // 2:
            print(q1_str % (gt_mix, *random_swap(our, ag)))
        else:
            print(q2_str % (gt_vocal, *random_swap(our, ag)))

        print(f'\n------Answer {idx}------')
        print(f'our : {our} , {our_vocal_file_names[idx]}')
        print(f'ag  : {ag} , {ag_vocal_file_names[idx]}')


if __name__ == '__main__':

    print('###########問卷A###########')
    print_questions(jy3_vocal_file_names, 0)

    print('###########問卷B###########')
    print_questions(tak_vocal_file_names, 0)
