
# Odoo Unreserve Fix

A quick and dirty script to deal with the 
"It is not possible to unreserve more products of ... than you have in stock." bug. 

# Test locally before running!!! 


### UPDATE 6/10/2022

I have received multiple messages asking me for help or an easier solution. While I would love to help, I don't have the time to asses each DB and set up. In the interest of helping people out, I have made an updated version of the script, simple_brute.py. 

This version of the script is much more simple, and basically takes in your login info, product and locatin ID's and overwrites it with enough QTY to close the bugged move. 

If you are still having issues after running this updated version, feel free to email me. 


Set up you info the same as below, then run 


    ```python3 simple_brute.py 
    ```   
Follow the CLI, overwrite your QTY's and you are now able to cancel the bugged move. 







## Set up 

 - Insert your login info on line 35 -38 
    ```python3 
    url = "your ip"
    db = "your db"
    username = "youe email"
    password = "your password"
    ```   
- Insert products to check on line 57
    ```python3 
    components = ['#product','#1product']
    ```   
    
## Logic

Basically something went wrong with QTY's or pickings and now Odoo will not let you close the record. Even attempting to delete from the API will not work. This should be used as a last resort, the script sets the QTY of the location to what is needed to close the move. 

IE.

- Record N has product N 3000 units UOM and is unable to close. 
- Location of the record N has a UOM LESS than 3000 units UOM reserved.
- No matter what configs you make, the record will never close due to the QTY reserved being less than the move. 
- For example for Record N, product N 3000 units is reserved at location n, but the location N has a reserved QTY of 1000 units(regardless of UOM)

- This script set the QTYS (both on hand and reserved) to 'product_qty' to get the move to be able to close. 
- Note: Keep track of the QTYs if you want to keep inventory in synch. I will add logic for this further down the road.
## Usage/Examples

```python3
python3 unres_fix.py


```


## Screenshots

![Screenshot](https://i2.paste.pics/76df673157642ff1748b7f6bcc6afe77.png)

