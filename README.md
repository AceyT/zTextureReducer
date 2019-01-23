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

## TODO

 - ~~Activate the big export button~~
 - ~~Zoom on preview (by rescaling with NEAREST)~~
 - Add requirements.txt to `pip install` dependency easily
 - Delete queue after export
 - Does dithering really work ?
   - If not, should consider adding `PIL.Image.quantize` function to the stack of operation
 - How to support different color format
   - RGBA5551
   - ia16 (8 bits greyscale  8 bits alpha)
   - ...

