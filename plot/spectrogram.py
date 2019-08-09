import numpy as np
import matplotlib.pyplot as plt
import librosa

from pathlib import Path

data_foler = Path(r'C:\Users\cswu\PycharmProjects\sir\output')


def spec_mag(aud):
    D = librosa.stft(aud)
    M, P = librosa.magphase(D)
    M = librosa.amplitude_to_db(M)
    return M[0:800, 500:500 + 129]


times = [0.5, 1, 1.5]
frames_to_time = librosa.core.time_to_frames(times, sr=44100, hop_length=512, n_fft=None)
print(frames_to_time)

fft_frequencies = librosa.core.fft_frequencies(sr=44100, n_fft=2048)
hz_per_bin = fft_frequencies[3]-fft_frequencies[2]
hzs = [2000 * i for i in range(10)]
khzs = [hz//1000 for hz in hzs]
f_idxs = [int(round(hz/hz_per_bin, 0)) for hz in hzs]

for sid in range(18, 19):
    vocal_gt, _ = librosa.load(str(data_foler / f"gt_vocal-{sid}.mp4"), sr=44100)
    mix_gt, _ = librosa.load(str(data_foler / f"gt_mix-{sid}.mp4"), sr=44100)

    vocals_mag = spec_mag(vocal_gt)
    accomp_mag = spec_mag(mix_gt - vocal_gt)
    mix_mag = spec_mag(mix_gt)

    _plot = np.concatenate((vocals_mag, mix_mag, accomp_mag), axis=1)

    plt.figure(dpi=300)
    plt.jet()
    fig, axes = plt.subplots(nrows=1, ncols=3, dpi=300)

    title_str = "vocal"
    axes[0].set_ylabel("Frequency (kHz)")
    axes[0].set_xlabel("Time (s)")
    axes[0].set_yticks(f_idxs)
    axes[0].set_yticklabels(khzs)
    axes[0].set_title(title_str)
    axes[0].imshow(vocals_mag, origin='lower', aspect='auto')
    axes[0].set_xticks(frames_to_time)
    axes[0].set_xticklabels(times)

    title_str = "mixture"
    axes[1].set_xlabel("Time (s)")
    axes[1].tick_params(
        axis='y',  # changes apply to the y-axis
        which='both',  # both major and minor ticks are affected
        left=False,  # ticks along the left edge are off
        top=False,  # ticks along the top edge are off
        labelleft=False)  # labels along the bottom edge are off
    axes[1].set_title(title_str)
    im = axes[1].imshow(mix_mag, origin='lower', aspect='auto')
    axes[1].set_xticks(frames_to_time)
    axes[1].set_xticklabels(times)

    # plt.subplot(1, 3, 3)
    title_str = "accompaniment"
    axes[2].set_xlabel("Time (s)")
    axes[2].tick_params(
        axis='y',  # changes apply to the y-axis
        which='both',  # both major and minor ticks are affected
        left=False,  # ticks along the left edge are off
        top=False,  # ticks along the top edge are off
        labelleft=False)  # labels along the bottom edge are off
    axes[2].set_title(title_str)
    axes[2].imshow(accomp_mag, origin='lower', aspect='auto')
    axes[2].set_xticks(frames_to_time)
    axes[2].set_xticklabels(times)

    # cbar = fig.colorbar(im)
    # cbar.ax.set_ylabel('Magnitude (dB)', rotation=270)

    plt.savefig('spec.png')

    # plt.show()

    # break

