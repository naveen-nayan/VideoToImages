import os
import math
import cv2
from tqdm import tqdm


def main(videoPath, outfps, outFolder):
    print("Starting conversion")
    # for idx, file in enumerate(files):
    vidcap = cv2.VideoCapture(videoPath)
    sourcefps = vidcap.get(cv2.CAP_PROP_FPS)
    if outfps > sourcefps:
        outfps = 0
    print(f"converting file: {videoPath}")
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
        cv2.imwrite(os.path.join(outFolder, f"{videoPath[:-4]}_{i}.png"), image)
        success, image = vidcap.read()

if __name__ == '__main__':
    videoPath = input("Enter video path: ")
    outfps = input("Enter output FPS: ") 
    outFolder = os.path.join(videoPath.split('.')[0], "imagesConverted")
    try:
        os.mkdir(outFolder)
    except OSError:
        print("Creation of the directory %s failed, or it already exists." % outFolder)
    else:
        print("Successfully created the directory %s " % outFolder)

    main(videoPath, outfps, outFolder)