#!/usr/bin/env python

# Guides_Save_Load Rel 1
# Created by Tin Tran http://bakon.ca/gimplearn/
# Comments directed to http://gimpchat.com or http://gimpscripts.com
#
# License: GPLv3
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY# without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# To view a copy of the GNU General Public License
# visit: http://www.gnu.org/licenses/gpl.html
#
#
# ------------
#| Change Log |
# ------------
# Rel 1: Initial release.


# All guides will be saved and loaded from "[userfolder]/.gimp-2.8/guides/guides.txt" 
# each line in the text file will have the format for example "Guide:Cross|6000,4000|2000|3000"
# where every line starts with "Guide:" then the guides name in this case "Cross"
# followed by a pipe (|) then width, then a comma then height
# followed by a pipe (|) then followed by list (comma separated) of horizontal guides (in pixels), in this case there's just one guide at 2000(y position)
# followed by a pipe (|) then followed by list (comma separated) of vertical guies (in pixels), in this case there's just one guide at 3000(x position)
import math
from gimpfu import *
#from array import array
import os, string, sys

RELATIVE_METHOD = 0          #use percentages relative based on image width and height
ABSOLUTE_METHOD = 1          #use absolute pixel positions
RELATIVE_METHOD_DESCRIPTION = "RELATIVE (percentage)"
ABSOLUTE_METHOD_DESCRIPTION = "ABSOLUTE (pixels)"

#resolve directories and filenames
directory = os.path.join("~",".gimp-2.8","guides")
directory = os.path.expanduser(directory)
filename = os.path.join("~",".gimp-2.8","guides","guides.txt") #as suggested by dinasset to not hardcode slashes.
filename = os.path.expanduser(filename)


#This is called once before main() when we start up GIMP to create a default guide.txt file if it doesn't already exist
def tt_create_file_if_not_exist():
	if not os.path.exists(directory):
		os.makedirs(directory)
	if not os.path.isfile(filename):
		newfile = open( u''+filename,'w' )
		newfile.write("Guide:Cross|6000,4000|2000|3000\n")
		newfile.write("Guide:10% border|6000,4000|400,3600|600,5400\n")
		newfile.close()
		
def tt_key_of_guide(guide):
	return guide[0][1]
	
def tt_sort_guides_alphabetically(guides):
	return sorted(guides,key=tt_key_of_guide) #sort alphabetically based on guide's names
	
def tt_load_guides():
	guides = []
	file = open(u''+filename,'r')
	lines = file.readlines()
	for line in lines: #for each line see if it's a Guide definition.
		if line.find("Guide:") > -1: #guide definition found
		    
			data = line.split('|')  #break it up using pipe
			
			#break up with ":" to get strings "Guide" and guide name
			data[0] = data[0].split(":")
			
			#break up with comma to get width and height
			data[1] = map(float,data[1].split(",")) 
			
			#break up with comma to get horizontal guide positions	
			data[2] = map(float,data[2].split(",")) 
			
			#break up with comma to get vertical guide positions	
			data[3] = map(float,data[3].split(",")) 
			
			guides.append(data)
	file.close()
	guides = tt_sort_guides_alphabetically(guides)
	return guides


def tt_get_guide_names():
	guides = tt_load_guides()
	guide_names = []
	for guide in guides:
		guide_names.append(guide[0][1])
	return guide_names
	
def tt_guides_to_guide_data(image,guide_name):
	guide_detail = ["Guide",guide_name]
	guide_width_and_height = [image.width,image.height]
	horizontal_guides = []
	vertical_guides = []
	
	#read guide info into arrays 
	guide_id = pdb.gimp_image_find_next_guide(image,0)
	while guide_id > 0:
		if pdb.gimp_image_get_guide_orientation(image,guide_id) == ORIENTATION_HORIZONTAL:
			horizontal_guides.append(pdb.gimp_image_get_guide_position(image,guide_id))
		else:
			vertical_guides.append(pdb.gimp_image_get_guide_position(image,guide_id))
		guide_id = pdb.gimp_image_find_next_guide(image,guide_id)
		
	#if empty add some place holders so we don't have to deal with empty list
	if len(horizontal_guides) == 0:
		horizontal_guides = [100000]
	if len(vertical_guides) == 0:
		vertical_guides = [100000]
	return [guide_detail,guide_width_and_height,horizontal_guides,vertical_guides]
	
def tt_guides_replace_or_add(guides,newguide):

	for guide in guides:
		if guide[0][1] == newguide[0][1]: #if we find the same name remove it and break
			guides.remove(guide)
			break
	guides.append(newguide)
	return tt_sort_guides_alphabetically(guides)
	
def tt_save_guides(guides):

	savefile = open( u''+filename,'w' )
	for guide in guides:
		guide_str_data = "|".join([":".join(map(str,guide[0])),",".join(map(str,guide[1])),",".join(map(str,guide[2])),",".join(map(str,guide[3]))])
		savefile.write(guide_str_data + "\n")
		
	savefile.close()

def tt_remove_all_guides(image):
	guides = []
	
	#read guide ids
	guide_id = pdb.gimp_image_find_next_guide(image,0)
	while guide_id > 0:
		guides.append(guide_id)
		guide_id = pdb.gimp_image_find_next_guide(image,guide_id)
		
	#remove it in reverse order
	guides = guides[::-1] #reverse the list
	for guide_id in guides:
		pdb.gimp_image_delete_guide(image,guide_id)
		
	
def python_tt_guides_load(image, layer, guide_index, remove_existing, method) :
	pdb.gimp_image_undo_group_start(image)
	pdb.gimp_context_push()
	
	#PUT YOUR CODE HERE 
	if remove_existing > 0:
		tt_remove_all_guides(image)
		
	guides = tt_load_guides()
	guide = guides[guide_index] #load that guide at chosen index
	
	if method == RELATIVE_METHOD: #load based on percentage
		guide_width = guide[1][0]
		guide_height = guide[1][1]
		for horizontal in guide[2]:
			add_at = float(horizontal)/guide_height * image.height
			if add_at >= 0 and add_at <= image.height:
				pdb.gimp_image_add_hguide(image,add_at)
		for vertical in guide[3]:
			add_at = float(vertical)/guide_width * image.width
			if  add_at >= 0 and add_at <= image.width:
				pdb.gimp_image_add_vguide(image,add_at)
	else: # ABSOLUTE_METHOD - load based on absolute pixel
		for horizontal in guide[2]:
			if horizontal >= 0 and horizontal <= image.height:
				pdb.gimp_image_add_hguide(image,horizontal)
		for vertical in guide[3]:
			if vertical >= 0 and vertical <= image.width:
				pdb.gimp_image_add_vguide(image,vertical)
		
		
		
	
	pdb.gimp_context_pop()
	pdb.gimp_image_undo_group_end(image)
	pdb.gimp_displays_flush()
    #return

def python_tt_guides_save(image, layer, guide_name) :
	pdb.gimp_image_undo_group_start(image)
	pdb.gimp_context_push()
	
	#PUT YOUR CODE HERE 
	guides = tt_load_guides()
	guide = tt_guides_to_guide_data(image,guide_name)
	guides = tt_guides_replace_or_add(guides,guide)
	tt_save_guides(guides)
	
	pdb.gimp_context_pop()
	pdb.gimp_image_undo_group_end(image)
	pdb.gimp_displays_flush()
    #return
	
tt_create_file_if_not_exist()

register(
	"python_fu_tt_guides_load",                           
	"Loads a set of guides",
	"Loads a set of guides...",
	"Tin Tran",
	"Tin Tran",
	"2014",
	"<Image>/Image/Guides/Load...",             #Menu path
	"*",
	[
	(PF_OPTION,"guide_index",   "Guide:", 0, tt_get_guide_names()),
	(PF_TOGGLE, "remove_existing",   "Remove Existing Guides:", 1),
	(PF_OPTION,"method",   "Load Method:", 0, [RELATIVE_METHOD_DESCRIPTION,ABSOLUTE_METHOD_DESCRIPTION]),
	],
	[],
	python_tt_guides_load)

register(
	"python_fu_tt_guides_save",                           
	"Saves a set of guides",
	"Saves a set of guides...",
	"Tin Tran",
	"Tin Tran",
	"2014",
	"<Image>/Image/Guides/Save...",             #Menu path
	"*",
	[
	(PF_STRING, "guide_name", "Guides Name:", "My Guides 1"),
	],
	[],
	python_tt_guides_save)	
	
#make this call to create a guide file if it doesn't exist.


main()
