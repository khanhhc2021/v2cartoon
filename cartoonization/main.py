

import sys
import os
from glob import glob
import datetime





# print(my_parameter[-1])




image_extenstion="png"#@param ["jpg","png"]
frames_image = []

from os.path import join
import shutil
try:
    os.mkdir("test_images")
except:
    pass
test_image=[]
if len(glob(f"./test_images/*.{image_extenstion}"))!=0:
    for i in glob(f"./test_images/*.{image_extenstion}"):
        test_image.append(i)
    for i in test_image:
       os.remove(i)
else:
    pass
try:
    os.mkdir("cartoonized_images")
except:
    pass
try:
   if len(glob(f"./cartoonized_images/*.{image_extenstion}")) != 0:
       cartoonized_images = []
       for i in glob(f"./cartoonized_images/*.{image_extenstion}"):
          cartoonized_images.append(i)
       for i in cartoonized_images:
          os.remove(i)
   else:
       pass
except Exception as e:
   print(str(e))

files = []
extensions = ['*.mp4', '*.mkv']
for ext in extensions:
   files.extend(glob(join("", ext)))

print(files)
video_title=files[0]
video_extenstion=""
if files[0].endswith(".mp4"):
   video_extenstion=".mp4"
   os.rename(files[0],"input_video.mp4")
elif files[0].endswith(".mkv"):
   video_extenstion=".mkv"
   os.rename(files[0],"input_video.mkv")
try:
   var=os.system(f'ffmpeg -i "./input_video{video_extenstion}" "test_images/%03d.{image_extenstion}"')
   if var==0:
      print("Frame extract successful")
   else:
      print("Can't extract any frame")
except Exception as e:
   print(str(e))

root_path=os.getcwd()
var1=os.system("python cartoonize.py")
if var1==0:
   print("cartoonized complete")
else:
   print("cartoonize failed")


os.system("python upscale.py")
   
   
os.chdir("./cartoonized_images")
#print(os.getcwd())
var3=os.system(f"ffmpeg -framerate 30 -i %03d.{image_extenstion} cartoon{video_extenstion}")
if var3==0:
    print("We successfully make the cartoonized video.")
else:
    print("We can't make the cartoonized video.")
path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)
#print(os.getcwd())
try:
    os.mkdir("input_video")
except:
    pass
remove_list=["./input_video/input_video.mp4","./input_video/cartoon.mp4","./input_video/input_video.mkv","./input_video/cartoon.mkv"]
for i in remove_list:
      try:
         os.remove(i)
      except:
         pass

shutil.move(f"input_video{video_extenstion}","./input_video/")
shutil.move(f"./cartoonized_images/cartoon{video_extenstion}","./input_video/")


os.chdir("./input_video")
if video_title.endswith(".mp4"):
    extension=".mp4"
elif video_title.endswith(".mkv"):
    extension = ".mkv"

var4=os.system(f"ffmpeg -i input_video{extension} audio.wav")
if var4==0:
    print("Successfully export audio")
else:
    print("Failed to export audio")
var5=os.system(f"ffmpeg -i cartoon{video_extenstion} -i audio.wav -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 cartoon_audio{video_extenstion}")
if var5==0:
    print("Successfully replace audio in output file")
else:
    print("Failed to replace audio in output file")
path_parent1 = os.path.dirname(os.getcwd())
os.chdir(path_parent1)
