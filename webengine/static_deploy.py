import os
import sys
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
    element_dict = {}
    for child in element:
        if list(child): # contains sub elements
            child_dict = dict_from_element(child)
            if not child.tag in element_dict:
                element_dict[child.tag] = [child_dict]
            else:
                element_dict[child.tag].append(child_dict)
        else:
            element_dict[child.tag] = child.text
    return element_dict

def load_products_data():
    data_path = join(current_path(), '..', 'data')
    products = glob(join(data_path, 'products', '*.xml'))
    print "Processing %d product file(s)" % len(products)
    products_list = []
    for product_xml in products:
        tree = etree.parse(product_xml)
        product_dict = dict_from_element(tree.getroot())
        products_list.append(product_dict)
    return products_list

def create_thumb(source_filename, target_filename):
    size = 260, 205
    im = Image.open(source_filename)
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
    im.save(target_filename)
            
def update_thumbs():
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
    """ Rebuilds static htmtl files from the dynamics data """
    public_html_path = join(current_path(), '..', 'public_html')
    if not exists(public_html_path):
        os.mkdir(public_html_path)
    template = HTMLTemplate.from_filename(join(current_path(), '..',
                                               'templates' , 'index.html'))
    products_data = load_products_data()
    with open(join(public_html_path, 'index.html'), 'w') as index_html_file:
        index_html_file.write(template.substitute(locals()) )
        
    update_thumbs() 
        

if __name__ == "__main__":
    rebuild_static_files()