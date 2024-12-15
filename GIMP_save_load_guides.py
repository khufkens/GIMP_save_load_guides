#!/usr/bin/env python

import math
from gimpfu import *
import os

def weahtr_save_guides(image, directory_name, filename):
  # open session
  pdb.gimp_context_push()
  
  # create list elements to store guide details
  rows = []
  cols = []

  # collect all guide values
  index = pdb.gimp_image_find_next_guide(image,0)
  while index > 0:
    if pdb.gimp_image_get_guide_orientation(image, index) == ORIENTATION_HORIZONTAL:
      rows.append(pdb.gimp_image_get_guide_position(image, index))
    else:
      cols.append(pdb.gimp_image_get_guide_position(image, index))
    
    # increment guide index
    index = pdb.gimp_image_find_next_guide(image, index)
  
  # sort the values incrementally
  rows = sorted(rows)
  cols = sorted(cols)
  
  # convert to strings
  img_name = '"filename" : "{}"'.format(os.path.basename(image.filename))
  rows = '"rows" : [{}]'.format(','.join(map(str,rows))) 
  cols = '"cols" : [{}]'.format(','.join(map(str,cols)))
  
  # save file as json format, manually formatted
  # to avoid too many libraries
  savefile = open( u'' + os.path.join(directory_name, filename), 'w')
  guide_str_data = "{" + img_name + "," + rows + "," + cols + "}"
  savefile.write(guide_str_data + "\n")
  savefile.close()
  
  # close session
  pdb.gimp_context_pop()
  pdb.gimp_displays_flush()

register(
  "python_fu_weahtr_save_guides",
  "Saves a set of weahtr guides",
  "Saves a set of weahtr guides...",
  "Koen Hufkens",
  "Koen Hufkens",
  "2024",
  "weahtr - Save guides...",
  "*",
  [
  (PF_IMAGE, "image", "takes current image", None),
  (PF_DIRNAME, "directory_name", "Directory:", "/tmp"),
  (PF_STRING, "filename", "Guides Name:", "weahtr.json"),
  ],
  [],
  weahtr_save_guides,
  menu="<Image>/Image/Guides"
)

main()
