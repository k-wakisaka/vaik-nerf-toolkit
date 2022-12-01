import numpy as np
from sklearn.cluster import KMeans
import audiofile
import argparse
import os
import subprocess
import shutil


def main(input_wav_path, depth_bit, sample_rate, output_wav_path):
    if depth_bit >= 16:
        shutil.copy2(input_wav_path, output_wav_path)
        return
    base, ext = os.path.splitext(output_wav_path)
    temp_output_wav_path = os.path.join(os.path.dirname(output_wav_path), f'{base}_tmp{ext}')
    signal, sampling_rate = audiofile.read(input_wav_path)
    model = KMeans(n_clusters=2 ** depth_bit, random_state=0, init='random')
    model.fit(signal[0].reshape(-1, 1))
    clusters = model.predict(signal[0].reshape(-1, 1))

    new_signal = np.zeros_like(signal)
    for index in range(signal.shape[-1]):
        cluster_index = clusters[index]
        new_signal[0][index] = model.cluster_centers_[cluster_index][0]
        new_signal[1][index] = model.cluster_centers_[cluster_index][0]
    ratio1 = min(np.min(signal[0][:]) / np.min(new_signal[0][:]), np.max(signal[0][:]) / np.max(new_signal[0][:]))
    ratio2 = min(np.min(signal[1][:]) / np.min(new_signal[1][:]), np.max(signal[1][:]) / np.max(new_signal[1][:]))
    new_signal[0][:] = np.clip((new_signal[0][:] - np.average(new_signal[0][:])) * ratio1, -0.8, 0.8)
    new_signal[1][:] = np.clip((new_signal[1][:] - np.average(new_signal[1][:])) * ratio2, -0.8, 0.8)
    audiofile.write(temp_output_wav_path, new_signal, sampling_rate)

    subprocess.run(['sox', f'{temp_output_wav_path}', '-r', f'{sample_rate}', f'{output_wav_path}'])
    os.remove(temp_output_wav_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='bit converter')
    parser.add_argument('--input_wav_path', type=str, default="~/Downloads/Saved/bicycle.wav")
    parser.add_argument('--depth_bit', type=int, default=3, choices=[1, 3, 16])
    parser.add_argument('--sample_rate', type=int, default=14025, choices=[11025, 14025, 44100])
    parser.add_argument('--output_wav_path', type=str, default="~/Downloads/Saved/bicycle_1bit.wav")
    args = parser.parse_args()

    args.input_wav_path = os.path.expanduser(args.input_wav_path)
    args.output_wav_path = os.path.expanduser(args.output_wav_path)

    main(args.input_wav_path, args.depth_bit, args.sample_rate, args.output_wav_path)
