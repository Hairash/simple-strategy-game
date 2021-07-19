def create_images(x):
    class IMAGES:
        EMPTY = x

    return IMAGES()


images = create_images(67)
print(images.EMPTY)
