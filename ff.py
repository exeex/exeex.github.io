import pathlib
from pathlib import Path
import os
import subprocess

data_folder = Path('data')
# print(os.listdir(data_folder))

song_folders = os.listdir(data_folder)


def get_idx(folder_name):
    return int(folder_name.split(']')[0].replace('[', ''))


song_folders = {get_idx(song_folder): data_folder / song_folder for song_folder in song_folders}

# 篩選要做的歌
selected_idx = [x + 1 for x in range(50)]


def transfer_m4a(input_file, output_file, cover_image):
    assert os.path.splitext(input_file)[-1] == '.m4a'
    assert os.path.splitext(output_file)[-1] == '.mp4'
    assert os.path.splitext(cover_image)[-1] == '.jpg'

    cmd = f"ffmpeg -y -framerate 1 -i '{cover_image}' -i '{input_file}' -b:v 1024k -bufsize 1024k -c:a copy -s 1280x720 '{output_file}'"
    print(cmd)
    # subprocess.run(['ffmpeg', cmd])
    os.system(cmd)


def split_files(sound_files: list):
    jy3 = ''
    tak = ''
    gt_mix = ''
    gt_vocal = ''

    for file in sound_files:
        if 'JY3' in file:
            jy3 = file
        elif 'TAK' in file:
            tak = file
        elif 'mixture' in file:
            gt_mix = file
        elif 'vocals' in file:
            gt_vocal = file
        else:
            raise FileNotFoundError

    return jy3, tak, gt_mix, gt_vocal


# gt_vocal_file_names = [f'gt_vocal-{_id + 1}.mp4' for _id in range(song_number)]
# gt_mix_file_names = [f'gt_mix-{_id + 1}.mp4' for _id in range(song_number)]
# our_vocal_file_names = [f'our-{_id + 1}.mp4' for _id in range(song_number)]
# jy3_vocal_file_names = [f'jy3-{_id + 1}.mp4' for _id in range(song_number)]
# tak_vocal_file_names = [f'tak-{_id + 1}.mp4' for _id in range(song_number)]


file_name_map = []

for idx in selected_idx:
    folder = song_folders[idx]
    output_folder = pathlib.Path('output')

    sound_files = os.listdir(song_folders[idx])
    jy3, tak, gt_mix, gt_vocal = split_files(sound_files)

    new_jy3 = f'jy3-{idx}.mp4'
    new_tak = f'tak-{idx}.mp4'
    new_gt_mix = f'gt_mix-{idx}.mp4'
    new_gt_vocal = f'gt_vocal-{idx}.mp4'

    l1 = [folder / jy3, folder / tak, folder / gt_mix, folder / gt_vocal]
    l2 = [new_jy3, new_tak, new_gt_mix, new_gt_vocal]
    l = zip(l1, l2)
    # print(list(l))
    # file_name_map += l

    for _in, _out in l:
        print(_in, _out)
        transfer_m4a(_in, output_folder / _out, cover_image='a.jpg')

# print(file_name_map)
#
# for idx in range(len(song_folders)):
#     i = idx + 1
#     print(i, str(song_folders[i]).split(']')[-1])
#
# song_name_idx_dict = {i: str(song_folders[i]).split(']')[-1] for i in range(1, len(song_folders) + 1)}
# print(song_name_idx_dict)

# ffmpeg -y -framerate 1 -i 'a.jpg' -i 'data/[8]BKS - Too Much/vocals-BKS - Too Much.m4a' -b:v 1024k -bufsize 1024k -c:a copy -s 1280x720 'output/gt_mix-8.mp4'
# ffmpeg -y -framerate 1 -i 'a.jpg' -i 'data/[8]BKS - Too Much/data/[8]BKS - Too Much/mixture.m4a' -b:v 1024k -bufsize 1024k -c:a copy -s 1280x720 'output/gt_mix-8.mp4'