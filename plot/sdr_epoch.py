import matplotlib.pyplot as plt
import os
import csv
from pathlib import Path

data_folder = Path('data')
files = os.listdir(data_folder)

plt.figure(dpi=300)
for file in files:
    csv_file = data_folder / file

    with open(csv_file, 'r') as f:
        r = csv.reader(f)
        next(r)
        a = [(time, int(epoch), float(sdr)) for time, epoch, sdr in r]
        times, epochs, sdrs = zip(*a)
        print(epochs)
        print(sdrs)
        plt.plot(list(epochs), list(sdrs), label=file.split('.')[0])
    # break

plt.xlabel("epoch")
plt.ylabel("sdr(dB)")
plt.title("PyPlot First Example")
plt.ylim(-2.5, 5)
plt.legend(loc='lower right')

plt.show()