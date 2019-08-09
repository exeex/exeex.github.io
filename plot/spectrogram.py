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
    axes[0].set_ylabel("Frequency (Hz)")
    axes[0].set_xlabel("Time (s)")
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

    # break

    # fig, axes = plt.subplots(nrows=2, ncols=2)
    # for ax in axes.flat:
    #     im = ax.imshow(np.random.random((10, 10)), vmin=0, vmax=1)
    #
    # fig.subplots_adjust(right=0.8)
    # cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    # fig.colorbar(im, cax=cbar_ax)
    #
    # plt.show()
    # break
