from . import db
from .models import MEDIA_LIBRARY

def load_image_default():
    new_file_1 = MEDIA_LIBRARY(filename='DPL_CATI.jpg', checksum='8f8c5d272ad69ae5a4664fcd28e8f7d8')
    new_file_2 = MEDIA_LIBRARY(filename='DPL_PRAW.jpg', checksum='1e81300aaa6bb7e1637119ba6f9cb336')
    new_file_3 = MEDIA_LIBRARY(filename='DPL_PRIW.jpg', checksum='083a1b2cb2ffeee83bc28f78c90c8d7a')
    new_file_4 = MEDIA_LIBRARY(filename='DPL_PRMW.jpg', checksum='e686dbbfd1e11ad36d851e6c79c00517')
    new_file_5 = MEDIA_LIBRARY(filename='DPL_PRSW.jpg', checksum='307e7a7482a7c11bb4dbc15c0958cd34')
    new_file_6 = MEDIA_LIBRARY(filename='DPL_THUM.jpg', checksum='d358bb394e2e7a11912305e29f16c3dd')
    new_file_7 = MEDIA_LIBRARY(filename='FinestHours_182x98.jpg', checksum='e9e23717c0b20f6af34ffbbf6b83add2')
    new_file_8 = MEDIA_LIBRARY(filename='FinestHours_182x243.jpg', checksum='43a1883f263a9bbae1b5944f24645430')
    new_file_9 = MEDIA_LIBRARY(filename='FinestHours_262x349.jpg', checksum='300343d46b52bbe7b191d9055d12b364')
    new_file_10 = MEDIA_LIBRARY(filename='FinestHours_456x257.jpg', checksum='3396a3ff9fc6e09ae94068011556d0e5')

    db.session.add(new_file_1)
    db.session.add(new_file_2)
    db.session.add(new_file_3)
    db.session.add(new_file_4)
    db.session.add(new_file_5)
    db.session.add(new_file_6)
    db.session.add(new_file_7)
    db.session.add(new_file_8)
    db.session.add(new_file_9)
    db.session.add(new_file_10)

    db.session.commit()

    return 'Successfully loaded default image data..'