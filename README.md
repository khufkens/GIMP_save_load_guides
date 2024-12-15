# Saves guides in GIMP for use with the weahtr ML workflow

This GIMP plug-in complements the weahtr python package and workflow for automated climate data recovery. When creating a template the plug-in allows you to export the boundaries of rows and columns, or regions of interest.

## Install

You will need a recent (2.10) GIMP version, and the flatpak version of GIMP when using linux.

1. Copy the python file to the any folder.
2. Make the script executable (`chmod +x ` in unix based OS)
3. Add the folder to the GIMP preferences in the plug-in menu

## Use

Create guides in GIMP by clicking in the side or top margins, and [dragging the cursor into an open image](https://docs.gimp.org/2.10/en/gimp-concepts-image-guides.html). To save the guides go to `Image - Guides - weahtr save guides ...`

Select an output directory and filename.

To clear the guides use `Image - Guides - Remove all Guides`


##
