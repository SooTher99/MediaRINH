from PIL import Image
import os
from pathlib import Path


def img_to_webp(instance):
    if instance.img:
        image = Image.open(instance.img.path)
        image = image.convert("RGB")
        width, height = image.size
        if width > 300 and height > 300:
            # keep ratio but shrink down
            image.thumbnail((width, height))

        # check which one is smaller
        if height < width:
            # make square by cutting off equal amounts left and right
            left = (width - height) / 2
            right = (width + height) / 2
            top = 0
            bottom = height
            image = image.crop((left, top, right, bottom))

        elif width < height:
            # make square by cutting off bottom
            left = 0
            right = width
            top = 0
            bottom = width
            image = image.crop((left, top, right, bottom))

        if width > 300 and height > 300:
            image.thumbnail((300, 300))
        width, height = image.size  # Get new dimensions
        image.save(instance.img.path, format="webp",
                   quality=70, optimize=True)
        os.rename(instance.img.path,
                  Path(instance.img.path).with_suffix(".webp"))
        instance.img.name = instance.img.name.split(".")[0] + ".webp"
        instance.save()
    return instance
