import cv2
import os
import time

start_time = time.time()

path = 'pixframes/'
out_path = ""
video_name = 'video.mp4'


pre_imgs = os.listdir(path)
img = []

for i in range(len(pre_imgs)):
    img.append(path+"frame"+str(i)+".png")
    #print(path+"frame"+str(i)+".png")

#print(img)

cv2_fourcc = cv2.VideoWriter_fourcc(*"mp4v")

frame = cv2.imread(img[0])
height, width, layers = frame.shape


video = cv2.VideoWriter(video_name, cv2_fourcc, 30, (width,height))


for i in range(len(img)):
    video.write(cv2.imread(img[i]))
    print(f"count = {i}")

cv2.destroyAllWindows()
video.release()

print("--- %s seconds ---" % (time.time() - start_time))