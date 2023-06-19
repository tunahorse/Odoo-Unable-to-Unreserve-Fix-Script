import xmlrpc.client
import ssl
from pprint import pprint

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

url = 
db =
username = 
password = 


def get_model_fields(url, db, username, password, model_name):
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

    # Get the model's metadata
    model_fields = models.execute_kw(db, uid, password,
                                     'ir.model.fields', 'search_read',
                                     [[['model', '=', model_name]]],
                                     {'fields': ['name']})

    # Extract the field names
    field_names = [field['name'] for field in model_fields]
    return field_names


model_name = 'product.product'

fields = get_model_fields(url, db, username, password, model_name)
pprint(fields)