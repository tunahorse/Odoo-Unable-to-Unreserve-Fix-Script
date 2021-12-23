import xmlrpc.client
import ssl
from pprint import pprint


### Begin Handle SSL issues with self hosting. 
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context
    
### End handle SSL issues with self hosting    


### Begin color coding for issues
class issues:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
#### End color coding for issues 


#### Begin Login 

url = "your ip"
db = "your db"
username = "youe email"
password = "your password"



models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

### End Login 


### Begin comparing qty RSV vs moves


def compare_rsv_vs_moves():
    
   
    ### Place name of products to run the compare process. 
    
    components = ['#product','#1product']
    
    
    
    moves_to_unreserve = []
    
    
    ### Begin get all active locations 
    location_trying_unreserve =  models.execute_kw(db, uid, password,
                'stock.location', 'search',
                [[['active', '=', True]]]
    )
    ### End get all active locations 
    
    
    
    ### Begin Loop each product in each location. 


    for component_product in components:
        print(f"{issues.WARNING}" +'Checking:',component_product + f"{issues.ENDC}")
        for locations in location_trying_unreserve:

            on_hand_data = models.execute_kw(db, uid, password,
                                            'stock.quant', 'search_read',
                                            [[['product_id', '=', component_product],
                                            ['location_id', '=', locations]
                                            ]])
            if not on_hand_data:
                pass

            else:

                rsv_qty = on_hand_data[0]['reserved_quantity']
                

                stock_moves = models.execute_kw(db, uid, password,
                                                        'stock.move.line', 'search_read',
                                                        [[['product_id', '=',component_product],['location_id','=',locations],'!',['state', '=', "done"],'!',['state', '=', 'cancel']]],
                                            )



                reserved_quant_moves = []

                for i in stock_moves:
                    reserved_quant_moves.append(i['product_qty'])
                    
                moves_summed = sum(reserved_quant_moves)
                    
                    
                print(f"{issues.OKBLUE}Location ID:"+ str(locations) +f"{issues.OKBLUE}")
                print(f"{issues.OKBLUE}QTY RSVD:" + str(rsv_qty)+ f"{issues.OKBLUE}")
                print(f"{issues.OKBLUE}MOVES SUMMED:"+ str(moves_summed) +f"{issues.OKBLUE}")
               
           







                if rsv_qty <= sum(reserved_quant_moves):

                    pass 
                   

                else:
                    stock_moves_grt_than_rsv = models.execute_kw(db, uid, password,
                                                    'stock.move.line', 'search_read',
                                                    [[['product_id', '=', component_product],
                                                    ['location_id', '=', locations],['product_qty','>=',rsv_qty],'!', ['state', '=', "done"], '!',
                                                    ['state', '=', 'cancel']]],
                                                    )

                    if not stock_moves_grt_than_rsv:
                        pass
                    else:
                        for moves_to_checkk in stock_moves_grt_than_rsv:
                            moves_to_unreserve.append(moves_to_checkk)
        ### End Loop each product in each location. 


                  
    ### Begin Print Moves to unreserve/ that require unreservation.

    if not moves_to_unreserve:
        print(f"{issues.OKBLUE}No single move has more reserved than reserved QTY{issues.OKBLUE}")

    else:
        print(f"{issues.FAIL}These moves are greater than reserved QTY, need to unreserve if you can or brute force to close them{issues.ENDC}")
        print(f"{issues.FAIL}ALERT{issues.ENDC}")
        for i in moves_to_unreserve:
            print(i['reference'])
            print(i['product_qty'])
            print(i['location_id'][1])
            print(i['product_id'][1])
            print('Always check the product and location before running this script')
            print('-------------')
            
            if input("Attempt brute force fix on "+i['reference']+"(y/n)?") != "y":
                pass
            else:
                print(f"{issues.OKBLUE}Setting reserved to match bugged records{issues.ENDC}")

                try:
                    print('Just joshing')
                    
                    on_hand_data = models.execute_kw(db, uid, password,
                                                     'stock.quant', 'search_read',
                                                     [[['product_id', '=', i['product_id'][0]],
                                                       ['location_id', '=', i['location_id'][0]]
                                                       ]])

                    ### Onhand VS RSV
                    print('On hand quantity')
                    print(on_hand_data[0]['quantity'])
                    print('Reserved Quantity')
                    print(on_hand_data[0]['reserved_quantity'])
                    
                    print(f"{issues.OKBLUE}Begin brute force fix{issues.ENDC}")
                    
                    on_hand_qty = models.execute_kw(db, uid, password, 'stock.quant', 'write',
                                            [i['location_id'][0], {
                                                'quantity': i['product_qty']
                                            }])
                    
                    
                    rsv_hand_qty = models.execute_kw(db, uid, password, 'stock.quant', 'write',
                                            [i['location_id'][0], {
                                                'reserved_quantity': i['product_qty']
                                            }])
                    
                    print(f"{issues.OKBLUE}Brute force fix worked, you should be able to unreserve or cancel the record now. {issues.ENDC}")
                    
                    
                except:
                    print(f"{issues.FAIL}Something went wrong{issues.ENDC}")
     
        ### End Print Moves to unreserve/ that require unreservation.

                
                
                    
       
        
        
    
    
compare_rsv_vs_moves()


