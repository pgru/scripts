import os, sys
import matplotlib.pyplot as plt


if __name__ == "__main__":
    os.system("rm movie.mp4")
    fps = 10
    os.system("ffmpeg -r "+str(fps)+" -b 1800 -i ghe_smallerAMP_parte2.out/m*.png movie.mp4")
    # os.system("rm _tmp*.png")