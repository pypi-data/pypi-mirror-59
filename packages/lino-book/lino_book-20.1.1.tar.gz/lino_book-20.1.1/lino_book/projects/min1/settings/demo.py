from lino_book.projects.min1.settings import *
from lino.utils import i2d

class Site(Site):
    languages = "en de fr"
    the_demo_date = i2d(20141023)

SITE = Site(globals())
DEBUG = True
