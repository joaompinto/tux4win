#!/usr/bin/pyhon
# -*- coding: utf-8 -*-

"""
  This module provides functions to generate the static components of
  the site: (.html and screenshot thumbnails).
  The data is read from the data/products/*.xml files, the html files
  are generated from templates/*.html, which are "Tempita" templates.
  The screenshot thumbnails (public_html/thumbs) are generated
  from data/media/screenshots/*.png .
"""

import os
import sys
import re
from PIL import Image
from lxml import etree
from os.path import dirname, join, exists, basename
from glob import glob


def current_path():
    return os.path.dirname(os.path.abspath(__file__))

path = join(current_path(), '..')
if path not in sys.path:
    sys.path.append(path)

from tempita import HTMLTemplate


def dict_from_element(element):
    """
    Returns a dict from an XML structure: dict[element.tag] = element.text
    When a child element contains childs elements, set it to a list
    of dics of the child elements
    """
    element_dict = {}
    for child in element:
        if list(child): # contains childs elements
            child_dict = dict_from_element(child)
            if not child.tag in element_dict:
                element_dict[child.tag] = [child_dict]
            else:
                element_dict[child.tag].append(child_dict)
        else:
            element_dict[child.tag] = child.text
    return element_dict

def load_products_data():
    """
    Load products data from products/*.xml files
    Return a list of dicts containing the corresponding xml data
    """
    data_path = join(current_path(), '..', 'data')
    product_files = glob(join(data_path, 'products', '*.xml'))
    products_list = []
    for product_filename in product_files:
        tree = etree.parse(product_filename)
        product_dict = dict_from_element(tree.getroot())
        if not re.match('^[0-9a-z.]+$', product_dict['index_name']):
            raise Exception('Invalid index name %s at %s, must match [a-z.]+' %
                    (product_dict['index_name'] , basename(product_filename)))
        products_list.append(product_dict)
    return products_list

def create_thumb(source_fame, target_fame, target_w = 260, target_h=205):
    """
    Create a resized image from source_fname into target_fname
    """
    size = target_w, target_h
    im = Image.open(source_fame)
    width = im.size[0]
    height = im.size[1]
    newwidth = int(size[0])
    newheight = int(height*(newwidth/float(width)))
    if newheight > int(size[1]):
        newheight = int(size[1])
        newwidth = int(width*(newheight/float(height)))
    size = newwidth, newheight
    # Resize and save the image
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(target_fame)

def update_thumbs():
    """
    Update thumbnails for images which don't have one or which have been
    modified after the corresponding thumbnail file.
    """
    screens_path = public_html_path = join(current_path(),
                                           '..', 'data', 'media', 'screens')
    thumbs_path = join(current_path(), '..', 'public_html', 'thumbs')
    if not exists(thumbs_path):
        os.mkdir(thumbs_path)
    for screen_filename in glob(join(screens_path, '*.png')):
        filename = basename(screen_filename)
        screen_mtime = os.path.getmtime(screen_filename)
        thumb_filename = join(thumbs_path, filename)
        try:
            thumb_mtime = os.path.getmtime(thumb_filename)
        except OSError:
            thumb_mtime = 0
        if thumb_mtime < screen_mtime:
            try:
                os.unlink(thumb_filename)
            except OSError:
                pass
            create_thumb(screen_filename, thumb_filename)


def rebuild_static_files():
    """
    Rebuilds static files
    """
    public_html_path = join(current_path(), '..', 'public_html')
    if not exists(public_html_path):
        os.mkdir(public_html_path)

    # Create index.html
    template = HTMLTemplate.from_filename(join(current_path(), '..',
                                               'templates' , 'index.html'))
    products_data = load_products_data()
    all_products = sorted(products_data,
           key=lambda product: product['version'][0]['publish_time'])
    all_products.reverse()

    # Build index html files
    # First remove any existing files
    html_files_list = glob(join(public_html_path, 'index.html.*'))
    for html_filename in html_files_list:
        os.unlink(html_filename)
    # Create per page files
    for i in xrange(0, len(all_products), 5):
        products = all_products[i:i+5]
        page_nr = (i/5)+1
        next_page_nr = page_nr + 1 if len(all_products) > i+5 else 0
        prev_page_nr = page_nr - 1 if page_nr > 1 else 0
        index_fname = join(public_html_path, 'index.html.%d' % page_nr)
        with open(index_fname, 'w') as index_html_file:
            index_html_file.write(template.substitute(locals()))

    # Build per product files
    template = HTMLTemplate.from_filename(join(current_path(), '..',
                                               'templates' , 'product.html'))

    products_path = join(public_html_path, 'products')
    if not exists(products_path):
        os.mkdir(products_path)
    html_files_list = glob(join(products_path, '*.html'))
    # First remove any existing files
    for html_filename in html_files_list:
        os.unlink(html_filename)
    for product in all_products:
        index_name = basename(product['index_name'])
        product_fname = join(products_path, '%s.html' % index_name)
        with open(product_fname, 'w') as html_file:
           html_file.write(template.substitute(locals()))

    # Create/update screenshot thumbnails
    update_thumbs()


if __name__ == "__main__":
    rebuild_static_files()