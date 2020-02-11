from PIL import Image
from resizeimage import resizeimage
from . import movie_config, main, create_tar
import os
IMAGE_FETCH_DIRECTORY = movie_config.omdb_image_dir
IMAGE_UPLOAD_DIRECTORY = movie_config.premium_upload_dir+'/'


def omdb_image_create(title):
    title = title.replace(' ', '')
    with open(IMAGE_FETCH_DIRECTORY+'OMDB_base.jpg', 'r+b') as f:
        with Image.open(f) as image:
            cover = resizeimage.resize_cover(image, [182, 98], validate=False)
            filename_182x98 = title+'_182x98.jpg'
            cover.save(IMAGE_UPLOAD_DIRECTORY+filename_182x98, image.format)
            checksum = main.checksum_creator(os.path.join(IMAGE_UPLOAD_DIRECTORY, filename_182x98))
            create_tar.add_supporting_files_to_db(filename_182x98, checksum, title)
            cover = resizeimage.resize_cover(image, [182, 243], validate=False)
            filename_182x243 = title + '_182x243.jpg'
            cover.save(IMAGE_UPLOAD_DIRECTORY + filename_182x243, image.format)
            checksum = main.checksum_creator(os.path.join(IMAGE_UPLOAD_DIRECTORY, filename_182x243))
            create_tar.add_supporting_files_to_db(filename_182x243, checksum, title)
            cover = resizeimage.resize_cover(image, [800, 600], validate=False)
            filename_800x600 = title + '_800x600.jpg'
            cover.save(IMAGE_UPLOAD_DIRECTORY + filename_800x600, image.format)
            checksum = main.checksum_creator(os.path.join(IMAGE_UPLOAD_DIRECTORY, filename_800x600))
            create_tar.add_supporting_files_to_db(filename_800x600, checksum, title)
            cover = resizeimage.resize_cover(image, [1920, 1080], validate=False)
            filename_1920x1080 = title + '_1920x1080.jpg'
            cover.save(IMAGE_UPLOAD_DIRECTORY + filename_1920x1080, image.format)
            checksum = main.checksum_creator(os.path.join(IMAGE_UPLOAD_DIRECTORY, filename_1920x1080))
            create_tar.add_supporting_files_to_db(filename_1920x1080, checksum, title)
            cover = resizeimage.resize_cover(image, [262, 349], validate=False)
            filename_262x349 = title + '_262x349.jpg'
            cover.save(IMAGE_UPLOAD_DIRECTORY + filename_262x349, image.format)
            checksum = main.checksum_creator(os.path.join(IMAGE_UPLOAD_DIRECTORY, filename_262x349))
            create_tar.add_supporting_files_to_db(filename_262x349, checksum, title)
            cover = resizeimage.resize_cover(image, [456, 257], validate=False)
            filename_456x257 = title + '_456x257.jpg'
            cover.save(IMAGE_UPLOAD_DIRECTORY + filename_456x257, image.format)
            checksum = main.checksum_creator(os.path.join(IMAGE_UPLOAD_DIRECTORY, filename_456x257))
            create_tar.add_supporting_files_to_db(filename_456x257, checksum, title)

    return main.list_files()
