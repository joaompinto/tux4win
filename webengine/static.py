import inspect
from lxml import etree
from os.path import dirname, join
from glob import glob

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
    current_path = dirname(inspect.stack()[1][1])
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
    """ Rebuilds static htmtl files from the dynamics datas """
    print load_products_data()


if __name__ == "__main__":
    rebuild_static_files()