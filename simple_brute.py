
#!/usr/bin/env python3


import xmlrpc.client
import ssl
from pprint import pprint



# Begin Login to Odoo#
import requests
from Tools.scripts.objgraph import ignore


from datetime import datetime

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

url = "http://localhost:8069"
db = "demo_"
username = "demo_user"
password = "demo_pw"

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})


#Note you can use regular names or ids 
#Search for stock.quant ID 


product_to_unres = "product_x"
location_to_unres = 'location_x'




on_hand_data = models.execute_kw(db, uid, password,
'stock.quant', 'search_read',
[[['product_id', '=', product_to_unres],['location_id', '=', location_to_unres]]]

)

rsv_qty = on_hand_data[0]['reserved_quantity']
room_id = on_hand_data[0]['id']
location_id = on_hand_data[0]['location_id'][1]
real_qty = on_hand_data[0]['quantity']
product_id = on_hand_data[0]['product_id'][1]



print('Reserved Quantity: %s' % rsv_qty, 'Real Quantity: %s' % real_qty, 'Room ID: %s' % room_id, 'Product ID: %s' % product_id, 'Location ID: %s' % location_id)


### Begin overwrite process 

answer = input("Overwrite? (y/n)")

if answer.lower() in ["y","yes"]:
    print("Overwriting")
    
    answer.lower() == "y"
    overwrite_number = int(input("Please enter number by how much to overwrite(ENTER ENOUGH TO CANCEL THE BUGGED MOVE): "))
    
    print("Overwriting by %s" % overwrite_number)
    
    rsv_qty = models.execute_kw(db, uid, password, 'stock.quant', 'write',
                            [room_id, {
                                'reserved_quantity': overwrite_number, 
                            }])
    print("Reserved Overwrite Successful")
    
    rsv_qty = models.execute_kw(db, uid, password, 'stock.quant', 'write',
                            [room_id, {
                                'quantity': overwrite_number, 
                            }])
    print("Real Overwrite Successful")
    
    print("Overwrite Complete, you can now cancel the move that is bugged")
    
### End overwrite process 
    
    
  

elif answer.lower() in ["n","no"]:
    print('Exiting')
    

else:
    print("Invalid input")
     # Handle "wrong" input




