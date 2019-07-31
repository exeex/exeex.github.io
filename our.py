import os
import pathlib

data_folder = pathlib.Path('data_our')
output_folder = pathlib.Path('output2')
files = os.listdir(data_folder)

song_name_idx_dict = {1: 'Sambasevam Shanmugam - Kaathaadi', 2: 'Lyndsey Ollard - Catching Up',
                      3: 'Side Effects Project - Sing With Me', 4: 'The Sunshine Garcia Band - For I Am The Moon',
                      5: 'Cristina Vane - So Easy', 6: 'Enda Reilly - Cur An Long Ag Seol',
                      7: 'AM Contra - Heart Peripheral', 8: 'BKS - Too Much', 9: 'Moosmusic - Big Dummy Shake',
                      10: "Angels In Amplifiers - I'm Alright", 11: 'M.E.R.C. Music - Knockout',
                      12: 'Signe Jakobsen - What Have You Done To Me', 13: 'Mu - Too Bright',
                      14: 'Punkdisco - Oral Hygiene', 15: 'Triviul feat. The Fiend - Widow',
                      16: 'Forkupines - Semantics', 17: 'Zeno - Signs', 18: 'Nerve 9 - Pray For The Rain',
                      19: "Little Chicago's Finest - My Own", 20: "Juliet's Rescue - Heartbeats",
                      21: 'Al James - Schoolboy Facination', 22: 'Detsky Sad - Walkie Talkie',
                      23: 'The Easton Ellises (Baumi) - SDRNR', 24: 'The Mountaineering Club - Mallory',
                      25: 'The Doppler Shift - Atrophy', 26: 'Tom McKenzie - Directions',
                      27: 'Speak Softly - Like Horses', 28: 'Secretariat - Over The Top',
                      29: 'The Long Wait - Dark Horses', 30: 'James Elder & Mark M Thompson - The English Actor',
                      31: 'Louis Cressy Band - Good Time', 32: 'Bobby Nobody - Stitch Up',
                      33: 'Hollow Ground - Ill Fate', 34: 'Georgia Wonder - Siren', 35: 'BKS - Bulldozer',
                      36: 'The Easton Ellises - Falcon 69', 37: 'Carlos Gonzalez - A Place For Us',
                      38: 'Arise - Run Run Run', 39: 'Raft Monk - Tiring', 40: 'We Fell From The Sky - Not You',
                      41: 'Girls Under Glass - We Feel Alright', 42: 'Secretariat - Borderline',
                      43: 'Buitraker - Revo X', 44: 'Timboz - Pony', 45: 'Speak Softly - Broken Man',
                      46: "Ben Carrigan - We'll Talk About It All Tonight", 47: 'PR - Oh No',
                      48: 'Skelpolu - Resurrection', 49: 'Motor Tapes - Shore', 50: 'PR - Happy Daze'}

inv_map = {v: k for k, v in song_name_idx_dict.items()}


def transfer_wav(input_file, output_file, cover_image):
    assert os.path.splitext(input_file)[-1] == '.wav'
    assert os.path.splitext(output_file)[-1] == '.mp4'
    assert os.path.splitext(cover_image)[-1] == '.jpg'

    _input_file = str(input_file)
    # _input_file = _input_file.replace("\'", r"\'")
    print(_input_file)

    cmd = f"ffmpeg -y -framerate 1 -i \"{cover_image}\" -i \"{_input_file}\" -b:v 1024k -bufsize 1024k -c:a aac -b:a 128k -s 1280x720 \"{output_file}\""
    print(cmd)
    # subprocess.run(['ffmpeg', cmd])
    os.system(cmd)


# our_vocal_file_names = [f'our-{_id + 1}.mp4' for _id in range(song_number)]


for file in files:
    if file.split('[')[0] == 'vocal':
        song_name = file.replace('vocal[2]', '').replace('_vocal_pred.wav', '')
        sid = inv_map[song_name]
        print(sid)

        if sid == 19:
            input_file = data_folder / file
            output_file = output_folder / f'our-{sid}.mp4'
            transfer_wav(input_file, output_file, 'a.jpg')
