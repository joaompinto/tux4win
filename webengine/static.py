import os
from lxml import etree
from os.path import dirname, join, exists
from glob import glob
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
    current_path = os.path.dirname(os.path.abspath(__file__))
    data_path = join(current_path, '..', 'data')
    products = glob(join(data_path, 'products', '*.xml'))
    print "Processing %d product file(s)" % len(products)
    products_list = []
    for product_xml in products:
        tree = etree.parse(product_xml)
        product_dict = dict_from_element(tree.getroot())
        products_list.append(product_dict)
    return products_list


def rebuild_static_files():
    """ Rebuilds static htmtl files from the dynamics data """
    current_path = os.path.dirname(os.path.abspath(__file__))
    public_html_path = join(current_path, '..', 'public_html')
    if not exists(public_html_path):
        os.mkdir(public_html_path)
    template = HTMLTemplate.from_filename('../templates/index.html')
    products_data = load_products_data()
    with open(join(public_html_path, 'index.html'), 'w') as index_html_file:
        print template.substitute(locals())
        index_html_file.write(template.substitute(locals()) ) 


if __name__ == "__main__":
    rebuild_static_files()