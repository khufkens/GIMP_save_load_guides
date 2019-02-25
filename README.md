# GIMP save & load guides

A python script to save and load guides in GIMP, written by Tin Tran.

## Install

Copy the python file to the "[userfolder]/.gimp-2.8/plug-ins/" folder and (re)start GIMP.

## Use

Create guides in GIMP by dragging and dropping or [any other method](https://docs.gimp.org/2.6/en/gimp-concepts-image-guides.html). To save the guides go to Image - Guides - Save. Enter a name for the set of guides and click save. All guides will be saved and loaded from "[userfolder]/.gimp-2.8/guides/guides.txt".

The guides.txt text file will have the format for example "Guide:Cross|6000,4000|2000|3000". Every line starts with "Guide:" then the guides name ("Cross") and is pipe (|) delimited. Individual elements within the deliminted sections are comma delimited. The remaining fields describe:

- image width and height (pixels, e.g. 6000 x 4000)
- horizontal guide locations (pixels, e.g. 2000)
- vertical guide locations (pixels, e.g. 3000)
