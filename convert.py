import os
import math
import cv2
from tqdm import tqdm


def main(videoPath, outFolder, videoName):
    print("Starting conversion")
    # for idx, file in enumerate(files):
    vidcap = cv2.VideoCapture(videoPath)
    sourcefps = vidcap.get(cv2.CAP_PROP_FPS)
    outfps = int(sourcefps)
    print(f"converting file: {videoPath} with FPS: {outfps}")
    frameCount = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    skip = 0
    if outfps > 0:
        vidcap.set(cv2.CAP_PROP_FPS, outfps)
        # Estimating total frames to extract
        frameCount = math.ceil((frameCount / sourcefps) * outfps)
        skip = 1000 * math.floor(1000 / (outfps * 1000))
    success, image = vidcap.read()
    for i in tqdm(range(frameCount)):
        if not success:
            break
        if skip > 0:
            vidcap.set(cv2.CAP_PROP_POS_MSEC, (i * skip))
        cv2.imwrite(os.path.join(outFolder, f"{videoName[:-4]}_{i}.png"), image)
        success, image = vidcap.read()

if __name__ == '__main__':
    videoPath = input("Enter video folder path: ")
    files = [file for file in os.listdir(videoPath) if file.endswith(".mp4") or file.endswith(".MP4")]

    for idx, file in enumerate(files):
        outFolder = os.path.join(videoPath, file.split('.')[0])
        print(outFolder)
        compFilePath = os.path.join(videoPath, file)
        try:
            os.makedirs(outFolder)
        except OSError:
            print("Creation of the directory %s failed, or it already exists." % outFolder)
        else:
            print("Successfully created the directory %s " % outFolder)

        main(compFilePath, outFolder, file)
