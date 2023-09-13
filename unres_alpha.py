import xmlrpc.client
import ssl

# Initialize SSL context
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Connection settings
db = 'demo'
url = 'http://localhost:8069'
username = 'admin'
password = 'pw'

# Connect to the server
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Accept stock picking name from CLI
stock_picking_name = input("Enter stock picking name: ")

# Check if stock picking exists and is not closed or done
stock_picking_data = models.execute_kw(db, uid, password,
    'stock.picking', 'search_read', [[['name', '=', stock_picking_name], ['state', 'not in', ['done', 'cancel']]]])

if not stock_picking_data:
    print("Stock picking does not exist or is closed/done.")
else:
    stock_picking_id = stock_picking_data[0]['id']

    # Fetch stock moves for this stock picking
    stock_moves_data = models.execute_kw(db, uid, password,
        'stock.move.line', 'search_read', [[['picking_id', '=', stock_picking_id]]])

    for move in stock_moves_data:
        
        product_id = move['product_id'][0]
        reserved_qty = move['product_uom_qty']
        location_id = move['location_id'][0]
        
        print(f"Checking product {move['product_id'][1]} at location {move['location_id'][1]}...")
        print(f"Product ID: {product_id}")
        print(f"Reserved quantity: {reserved_qty}")
        print(f"Location ID: {location_id}")
        
        # Fetch actual inventory details for the specific location
        on_hand_data = models.execute_kw(db, uid, password,
            'stock.quant', 'search_read', [[['product_id', '=', product_id], ['location_id', '=', location_id]]])
        
        
        if not on_hand_data:
            print(f"No product {move['product_id'][1]} found at location {move['location_id'][1]}.")

            # Prompt to add product
            answer = input("Would you like to add product to this location? (y/n): ")

            if answer.lower() in ["y", "yes"]:
                add_qty = int(input("Please enter the quantity to add: "))
                
                # Adding the product to the location using 'create' operation on 'stock.quant'
                models.execute_kw(db, uid, password, 'stock.quant', 'create', [{
                    'product_id': product_id,
                    'location_id': location_id,
                    'quantity': add_qty,
                }])

                print(f"Added {add_qty} of {move['product_id'][1]} to location {move['location_id'][1]}.")

            elif answer.lower() in ["n", "no"]:
                print("Skipping.")

            else:
                print("Invalid input.")

        else:
            
            for quant in on_hand_data:
                
                rsv_qty = quant['reserved_quantity']
                quant_id = quant['id']
                print(f"Quant ID: {quant_id}")
                print(f"Real quantity: {rsv_qty}")
                
                # Compare each individual reserved quantity with actual inventory
                if reserved_qty > rsv_qty:
                    print(f"Discrepancy found for product {move['product_id'][1]} in quant ID {quant_id}. Reserved: {rsv_qty}, Move RSV: {rsv_qty}.")
                                
                    # Prompt for overwrite
                    answer = input("Overwrite? (y/n)")

                    if answer.lower() in ["y", "yes"]:
                        overwrite_number = int(input("Please enter number by how much to overwrite: "))
                                    
                        # Overwrite reserved and real quantities
                        models.execute_kw(db, uid, password, 'stock.quant', 'write',
                                        [quant_id, {'reserved_quantity': overwrite_number}])
                        models.execute_kw(db, uid, password, 'stock.quant', 'write',
                                        [quant_id, {'quantity': overwrite_number}])
                        print("Overwrite successful.")
                                    
                    elif answer.lower() in ["n", "no"]:
                        print("Skipping.")
                                    
                    else:
                        print("Invalid input.")
