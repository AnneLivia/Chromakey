import numpy as np
import cv2
import argparse

parser = argparse.ArgumentParser('Chroma Keying', epilog='-vf: foreground video -vb: background video')
parser.add_argument('-vf', required=True)
parser.add_argument('-vb', required=True)

args = parser.parse_args()

# -vf "data\green\dance.mp4" -vb "data\background\beach.mp4"
foreground = cv2.VideoCapture(args.vf)
background = cv2.VideoCapture(args.vb)

foreground_width = int(foreground.get(cv2.CAP_PROP_FRAME_WIDTH))
foreground_height = int(foreground.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = background.get(cv2.CAP_PROP_FPS)

cv2.namedWindow('Video [Chroma Keying]', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Video [Chroma Keying]', 900, 500)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output = cv2.VideoWriter('chroma.mp4', fourcc, fps, (foreground_width, foreground_height))

while True:
    foreground_ret, foreground_frame = foreground.read()
    background_ret, background_frame = background.read()

    if not foreground_ret or not background_ret:
        break

    foreground_hsv = cv2.cvtColor(foreground_frame, cv2.COLOR_BGR2HSV);

    lower_green = np.uint8([50, 0, 100])
    upper_green = np.uint8([70, 255, 255])

    # capturing the all green area
    foreground_mask = cv2.inRange(foreground_hsv, lower_green, upper_green)
    
    # to ensure that both background and foreground have the same size
    background_reduced = cv2.resize(background_frame, (foreground_width, foreground_height))

    # get the background using the mask obtained considering the green area
    background_frame_content = cv2.bitwise_and(background_reduced, background_reduced, mask=foreground_mask)
    
    # to get the foreground
    foreground_mask_inv = cv2.bitwise_not(foreground_mask)

    foreground_frame_object = cv2.bitwise_and(foreground_frame, foreground_frame, mask=foreground_mask_inv)

    combined_videos = cv2.addWeighted(src1=background_frame_content, alpha=1, src2=foreground_frame_object, beta=1, gamma=0)

    cv2.imshow('Video [Chroma Keying]', combined_videos)

    output.write(combined_videos)
    
    # when any key is pressed, stop video
    if cv2.waitKey(1) >= 0:
        break;


foreground.release()
background.release()
cv2.destroyAllWindows()