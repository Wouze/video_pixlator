from PIL import Image, ImageEnhance
import cv2
import time
import threading as th
from moviepy.editor import *

#MoviePy==1.0.3
start_time = time.time()
#top -F -R -o cpu
#threaded gave 116.4 seconds, not threaded gave 225.7 seconds
threaded = True

#NOT WORKING
with_sound = False

def pixellize(input_path, output_path, saturation = 1.25, contrast = 1.2, n_colors = 10, superpixel_size = 5):

    # load image
    #img_name = "test.jpg"
    #img_name = "./examples/original/test.jpg"

    img = Image.open(input_path)
    img_size = img.size

    # boost saturation of image
    sat_booster = ImageEnhance.Color(img)
    img = sat_booster.enhance(float(saturation))

    # increase contrast of image
    contr_booster = ImageEnhance.Contrast(img)
    img = contr_booster.enhance(float(contrast))

    # reduce the number of colors used in picture
    img = img.convert('P', palette=Image.Palette.ADAPTIVE, colors=int(n_colors))

    # reduce image size
    reduced_size = (img_size[0] // superpixel_size, img_size[1] // superpixel_size)
    img = img.resize(reduced_size, Image.Resampling.BICUBIC)

    # resize to original shape to give pixelated look
    img = img.resize(img_size, Image.Resampling.BICUBIC)

    # plot result
    img.save(output_path)


vidcap = cv2.VideoCapture('input.mp4')

fps = vidcap.get(cv2.CAP_PROP_FPS) #to know the frame rate

success,image = vidcap.read()
count = 0


while success:

    cv2.imwrite("frames/frame%d.jpg" % count, image)     # save frame as JPG file

    success,image = vidcap.read()
    print('Read a new frame: ', success)
    if threaded:
        th.Thread(target=pixellize, args=["frames/frame%d.jpg" % count, "pixframes/frame%d.png" % count]).start()
        print('Done working on the frame: ', count)
    else:
        pixellize("frames/frame%d.jpg" % count, "pixframes/frame%d.png" % count)
        print('Done coloring the frame: ', count)

    count += 1
    print("Active threads are: ", th.activeCount())

threads = th.activeCount()
while threads > 1:
    time.sleep(0.5)
    threads = th.activeCount()
    print("Active threads are: ", threads)


print("--- %s seconds ---" % (time.time() - start_time))

# Done breaking down video to pictures and making them pixeled, now making it videos back.

path = 'pixframes/'
out_path = ""
video_name = 'video.mp4'


pre_imgs = os.listdir(path)
img = []

for i in range(len(pre_imgs)):
    img.append(path+"frame"+str(i)+".png")
    #print(path+"frame"+str(i)+".png")


cv2_fourcc = cv2.VideoWriter_fourcc(*"mp4v")

frame = cv2.imread(img[0])
height, width, layers = frame.shape


print("FPS is ", fps)
video = cv2.VideoWriter(video_name, cv2_fourcc, int(fps), (width,height))


for i in range(len(img)):
    video.write(cv2.imread(img[i]))
    print(f"count = {i}")

cv2.destroyAllWindows()
video.release()

#adding sound  ##NOT WORKING RN
if with_sound:
    

    clip = VideoFileClip("input.mp4")
    clip.audio.write_audiofile(r"input_sound.mp3")

    clip = VideoFileClip("video.mp4")
    audioclip = AudioFileClip("input_sound.mp3")

    clip_w_sound = clip.set_audio(audioclip)

    clip_w_sound.write_videofile("video with sound.mp4")

print("--- %s seconds ---" % (time.time() - start_time))
print("---------- DONE! ----------")
