import numpy as np
from subprocess import call 
import sys
from PIL import Image
import cv2

#TODO: Make these user input
IM_MAX_H = 1080
IM_MAX_W = 1920
IM_RES_1080_PROD = IM_MAX_H * IM_MAX_W



def file2hex(fname):
  #Hexdump the file, convert to rgb, save to an np array
  #split filename
  print("Processing file...")
  txt_fname = fname.split('.')[0] + '.txt'
  #Use subprocess.call to call hexdump and pipe to text file
  #TODO: seems jank, find a better way to do this?
  f = open(txt_fname, "w")
  call(['hexdump', fname], stdout=f)
  rgb_arr = []
  with open(txt_fname, 'rb') as hdump:
    i = 0
    for line in hdump:
      #Remove the offset
      if i % 5000 == 0:
        print("Processed {} lines".format(i))
      line = line.decode().split(' ')[1:]
      for hex_val in line:
        if hex_val and hex_val != '\n':
          rgb_arr.append(int(hex_val, 16))
      i = i + 1
  #Remove created text file
  call(['rm', txt_fname])
  return np.asarray(rgb_arr).astype(np.uint8)


def shape_rgbarr(rgb_arr):
  #Shape the hex array into the proper shape
  #TODO: implement downsampling, right now it just truncates hexdumps that are too big
  print("Reshaping array...")
  curr_len = rgb_arr.shape[0] // 3
  end_lim = curr_len * 3
  rgb_arr = rgb_arr[:end_lim]
  rgb_arr = rgb_arr.reshape(curr_len, 3)
  div_factor = get_div_factor(curr_len)
  h_lim = IM_MAX_H // div_factor
  w_lim = IM_MAX_W // div_factor
  prod_lim = h_lim*w_lim
  rgb_arr = rgb_arr[:prod_lim]
  rgb_arr = rgb_arr.reshape(h_lim, w_lim, 3)
  print(rgb_arr.shape)
  return rgb_arr


def get_div_factor(size_prod):
  if size_prod > IM_RES_1080_PROD:
    return 1
  curr_lim = 2
  curr_prod = IM_RES_1080_PROD // (curr_lim**2)
  while size_prod < curr_prod:
    curr_lim = curr_lim + 1
    curr_prod = IM_RES_1080_PROD // (curr_lim**2)
  return curr_lim



def imfromrgb_arr(rgb_arr, fname):
  #Create an image from an rgb array
  print("Writing image...")
  img = Image.fromarray(rgb_arr)
  fname = fname.split('.')[0] + '.png'
  img.save(fname)
  print("Done!")


# Check if user passed in a file
if len(sys.argv) < 2:
  print("Please pass in a file to visualize!")
else:
  fname = sys.argv[-1]
  rgb_arr = file2hex(fname)
  shaped_rgb_arr = shape_rgbarr(rgb_arr)
  imfromrgb_arr(shaped_rgb_arr, fname)