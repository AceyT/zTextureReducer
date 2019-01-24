# zTextureReducer

An image processing utility, to plan modifications ahead and then batch execute them, written in Python 3

![screen1](https://user-images.githubusercontent.com/7415076/51576429-3b13f680-1ec7-11e9-8797-f5a44c7c6421.png)

## Supported features

 - resizing
 - recoloring
    + 256 colors
    + 16 colors
    + greyscale
 - dithering

## Installation

> **Python 3** should be installed on your system

Get this repository
Use a command prompt, go to this directory, then

```
$> python -m pip install --user -r requirements.txt
$> python main.py
```
 - Tested on Windows 7 with Python 3.6

#### Windows

> use the files in **win** directory to avoid using a command prompt
> - install.bat -> install dependancy (still need a proper installation of python 3)
> - launch.bat -> launch the software

## TODO

 - ~~Activate the big export button~~
 - ~~Zoom on preview (by rescaling with NEAREST)~~
 - ~~Add requirements.txt to `pip install` dependency easily~~
 - ~~`win/*.bat` files for windows users to easily install dependency and use it.~~
 - Delete queue after export
 - ~~Alpha preservation during processing~~
 - *Does dithering really work ?*
   - ~~If not, should consider adding `PIL.Image.quantize` function to the stack of operations~~ (wasn't working indeed)
   - Does the outputted color numbers is correct ?
 - How to support different color format
   - RGBA5551
   - ia16 (8 bits greyscale  8 bits alpha)
   - ...

