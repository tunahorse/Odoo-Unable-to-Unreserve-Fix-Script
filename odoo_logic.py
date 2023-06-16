import ssl
import xmlrpc.client
from pprint import pprint
# Handle the SSL certificate
def create_unverified_context():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context

def test_login(url, db, username, password):
    context = create_unverified_context()
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common', context=context)
    uid = common.authenticate(db, username, password, {})
    if uid:
        return True, uid
    else:
        return False, 0

def fetch_products(url, db, uid, password):
    context = create_unverified_context()
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object', context=context)
    product_records = models.execute_kw(db, uid, password,
        'product.product', 'search_read',
        [], {'fields': ['name']})
    return [product['name'] for product in product_records]

def fetch_product_quantities(url, db, uid, password, product_name):
    context = create_unverified_context()
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object', context=context)
    
    # First, we need to get the ID of the product
    product_id = models.execute_kw(db, uid, password,
        'product.product', 'search',
        [[['name', '=', product_name]]])[0]  # Assuming product names are unique
    
    # Then, we fetch all quants for this product
    quant_records = models.execute_kw(db, uid, password,
        'stock.quant', 'search_read',
        [[['product_id', '=', product_id]]],
      )
    pprint(quant_records)
    
    # We return a list of tuples, each containing location name and quantity
    return [(quant['location_id'][1], quant['quantity']) for quant in quant_records]
