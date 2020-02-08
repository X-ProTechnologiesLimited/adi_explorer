from . import db
from .models import MEDIA_LIBRARY, MEDIA_DEFAULT

def load_default_media():
    dpl_image_1 = MEDIA_LIBRARY(filename='DPL_CATI.jpg', checksum='8f8c5d272ad69ae5a4664fcd28e8f7d8')
    dpl_image_2 = MEDIA_LIBRARY(filename='DPL_PRAW.jpg', checksum='1e81300aaa6bb7e1637119ba6f9cb336')
    dpl_image_3 = MEDIA_LIBRARY(filename='DPL_PRIW.jpg', checksum='083a1b2cb2ffeee83bc28f78c90c8d7a')
    dpl_image_4 = MEDIA_LIBRARY(filename='DPL_PRMW.jpg', checksum='e686dbbfd1e11ad36d851e6c79c00517')
    dpl_image_5 = MEDIA_LIBRARY(filename='DPL_PRSW.jpg', checksum='307e7a7482a7c11bb4dbc15c0958cd34')
    dpl_image_6 = MEDIA_LIBRARY(filename='DPL_THUM.jpg', checksum='d358bb394e2e7a11912305e29f16c3dd')
    standard_image_1 = MEDIA_LIBRARY(filename='FinestHours_182x98.jpg', checksum='e9e23717c0b20f6af34ffbbf6b83add2')
    standard_image_2 = MEDIA_LIBRARY(filename='FinestHours_182x243.jpg', checksum='43a1883f263a9bbae1b5944f24645430')
    standard_image_3 = MEDIA_LIBRARY(filename='FinestHours_262x349.jpg', checksum='300343d46b52bbe7b191d9055d12b364')
    standard_image_4 = MEDIA_LIBRARY(filename='FinestHours_456x257.jpg', checksum='3396a3ff9fc6e09ae94068011556d0e5')
    sdr_movie = MEDIA_LIBRARY(filename='4K_SDR_MOVIE.ts', checksum='806761c26916f9a26abb547188c62cf6')
    hd_movie = MEDIA_LIBRARY(filename='HD_MOVIE.ts', checksum='2e78cb32788e099db6a3118a074bc9a9')
    hdr_movie = MEDIA_LIBRARY(filename='HDR_MOVIE.ts', checksum='cb6a578d7551d7908c7ee88c3bdf9deb')
    sd_movie = MEDIA_LIBRARY(filename='SD_2_min.ts', checksum='8e003a54635310a6da4d7bdff4f96c46')
    dpl_video_file = MEDIA_LIBRARY(filename='DPL_VIDEO_FILE.ts', checksum='2e78cb32788e099db6a3118a074bc9a9')
    trailer_file = MEDIA_LIBRARY(filename='FinestHours_Trailer.ts', checksum='f4ee486d734bb812498b31624354f248')

    default_config = MEDIA_DEFAULT(default_video_path='Providers/BSS/Content/Distribution/TestFiles/',
                                   default_image_path='Images/adi_t/', hdr_movie_file='HDR_MOVIE.ts',
                                   sdr_movie_file='4K_SDR_MOVIE.ts', hd_movie_file='HD_MOVIE.ts',
                                   est_movie_file='HD_MOVIE.ts', title_movie_file='SD_2_min.ts',
                                   dpl_movie_file='DPL_VIDEO_FILE.ts', trailer_file='FinestHours_Trailer.ts',
                                   standard_image_file_prefix='FinestHours_',
                                   dpl_image_file_prefix='DPL_')


    db.session.add_all([dpl_image_1, dpl_image_2, dpl_image_3, dpl_image_4, dpl_image_5, dpl_image_6, standard_image_1,
                       standard_image_2, standard_image_3, standard_image_4, sdr_movie, hd_movie, hdr_movie, sd_movie,
                       dpl_video_file, trailer_file, default_config])

    db.session.commit()

    return 'Successfully loaded default image data..'