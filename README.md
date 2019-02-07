# zTextureReducer

An image processing utility, to plan modifications ahead and then batch execute them, written in Python 3

![screen2](https://user-images.githubusercontent.com/7415076/51749150-acb69500-20bf-11e9-9931-fcbd612e7c3e.png)

## Supported features

 - resizing
 - recoloring
    + 256 colors
    + 16 colors
    + greyscale
 - dithering
 - renaming files on export

## Installation

> **Python 3** should be installed on your system with *pip*

#### Windows

> use the files in **win** directory to avoid using a command prompt
> - install.bat -> install dependancy (still need a proper installation of python 3)
> - launch.bat -> launch the software

#### CLI

Get this repository
Launch command prompt, go to this directory, then

```
$> python -m pip install --user -r requirements.txt
$> python main.py
```
 - Tested on Windows 7 with Python 3.6


## TODO

 - ~~Activate the big export button~~
 - ~~Zoom on preview (by rescaling with NEAREST)~~
 - ~~Add requirements.txt to `pip install` dependency easily~~
 - ~~`win/*.bat` files for windows users to easily install dependency and use it.~~
 - Delete queue after export
 - ~~Export confirmation (success / error)~~
 - ~~Renaming options for export~~
   - ~~1/2 Queue option to rename~~
   - ~~2/2 implementation in export~~
 - ~~Alpha preservation during processing~~
 - **Better alpha support**
   - Bi Level Alpha support
   - Alpha options
    - Discard
    - Bi level
    - 255 level
    - Own resize & dither
 - *Does dithering really work ?*
   - ~~If not, should consider adding `PIL.Image.quantize` function to the stack of operations~~ (wasn't working indeed)
   - ~~*Does the outputted color numbers is correct ?* (dither = duplication of one color)~~ (quantize after dithering)
   - grayscale & dithering support
 - Better quantization support
   - different parameters exposed
   - better alpha handling
 - Support different color format
   - RGBA5551
   - ia16 (8 bits greyscale  8 bits alpha)
   - ...

