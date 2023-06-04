from math import log10, sqrt
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt


def PSNR(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if (mse == 0):  # MSE is zero means no noise is present in the signal .
        # Therefore PSNR have no importance.
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr


def BBP(file_name):
    file = cv2.imread(file_name)
    stats = os.stat(file_name).st_size
    bits = file.size / 3
    return stats / bits


def main():
    images = ["lena.png", "pappers.png", "baboon.png"]
    x = []
    y = []
    y1 = []
    for name in images:
        original = cv2.imread(f'images/{name}')
        compressed = cv2.imread(f'results/{name}', 1)
        compressed_j = cv2.imread(f'results_jpeg/{name}', 1)
        value = PSNR(original, compressed)
        value_jpeg = PSNR(original, compressed_j)
        bbp = BBP(f'images/{name}')
        x.append(bbp)
        y.append(value)
        y1.append(value_jpeg)
        print(f"PSNR value is {value} dB")
        print(f"PSNR value is {value_jpeg} dB")
        print(f"BPP value is {bbp}")
    plt.plot(x, y, '-ok', color='gray', label='my algo')
    plt.plot(x, y1, '-ok', color='blue', label='jpeg')
    plt.legend(numpoints=1)
    plt.xlabel("BPP (bit per pixel)")
    plt.ylabel("PSNR")
    plt.show()


if __name__ == "__main__":
    main()
