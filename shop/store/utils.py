from uuslug import slugify
from time import time


def gen_slug(obj, cat):
    new_slug = slugify(cat)
    obj = str(obj)
    new_slug2 = slugify(obj)
    return new_slug2 + '-' + new_slug + '-' + str(int(time()))


def size_filter(args):
    size_list = []
    if 'XS' in args:
        size_list.append('XS')
    if 'S' in args:
        size_list.append('S')
    if 'M' in args:
        size_list.append('M')
    if 'L' in args:
        size_list.append('L')
    if 'XL' in args:
        size_list.append('XL')
    if 'XXL' in args:
        size_list.append('XXL')
    return size_list
