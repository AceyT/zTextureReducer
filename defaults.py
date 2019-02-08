
class zDefault:

    zoom = (1, 2, 4)
    sizes = (128, 64, 32, 16, 8)
    sampling_modes = (
        "Nearest",
        "Box",
        "Bilinear",
        "Hamming",
        "Bicubic",
        "Lanczos"
    )
    color_modes = (
        "Greyscale",
        "16 Colors Palette",
        "256 Colors Palette"
    )
    order_modes = ("Resize first", "Recolor first")
    
    config = {
        "preview" : 1,
        "resize" : 1,
        "width": sizes[1],
        "height" : sizes[1],
        "sampling" : sampling_modes[-1],
        "recolor" : 1,
        "colors" : color_modes[-1],
        "dither" : 1,
        "alpha_keep" : 1,
        "order" : order_modes[0],
        "zoom" : zoom[0]
    }


