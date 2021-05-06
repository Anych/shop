from uuslug import slugify
from time import time


def gen_slug(obj, cat):
    new_slug = slugify(cat)
    obj = str(obj)
    new_slug2 = slugify(obj)
    return new_slug2 + '-' + new_slug + '-' + str(int(time()))
