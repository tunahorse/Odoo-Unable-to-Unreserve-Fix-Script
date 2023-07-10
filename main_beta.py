import PySimpleGUI as sg
import yaml
from odoo_logic import test_login, fetch_products, fetch_product_quantities, update_product_quantities

def load_config():
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config

config = load_config()

url = config['odoo']['url']
db = config['odoo']['db']
username = config['odoo']['username']
password = config['odoo']['password']

is_logged_in, uid = test_login(url, db, username, password)
if is_logged_in:
    products = fetch_products(url, db, uid, password)
else:
    products = []

sg.theme('DarkBlue')

new_quantity_input = sg.Input(key='-NEWQTY-', size=(20, 1), disabled=False)



submit_button = sg.Button('Submit', key='-SUBMIT-', disabled=True)
cancel_button = sg.Button('Cancel', key='-CANCEL-', disabled=True)
quantities_text = sg.Text('', key='-QUANTITIES-', size=(30, 10))

layout = [
    [sg.Text('Product:', size=(10, 1)), sg.Combo(products, size=(60, 10), key='-PRODUCT-', enable_events=True, readonly=True), quantities_text],
    [sg.Text('Locations:', size=(10, 1)), sg.Listbox(values=[], size=(60, 20), key='-LOCATIONS-', enable_events=True, pad=(0, (10, 0)))],
    [sg.Button('Unreserve', pad=(0, 20)), sg.Button('Exit')],
    [sg.Text('Enter the new quantity:', key='-NEWQTYTEXT-', visible=True), new_quantity_input],
    
    [submit_button, cancel_button]
]

window = sg.Window('Unreserve Products', layout, size=(1200, 800))


selected_product = None
selected_location = None

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    elif event == '-PRODUCT-':
        selected_product = values['-PRODUCT-']
        quantities = fetch_product_quantities(url, db, uid, password, selected_product)
        locations = [f"{location}: {quantity}" for location, quantity, _ in quantities if 'virtual' not in location.lower()]
        window['-LOCATIONS-'].update(locations)
    elif event == '-LOCATIONS-':
        if values['-LOCATIONS-']:
            selected_location = values['-LOCATIONS-'][0].split(':')[0]
            print(f"Location selected: {selected_location}")  # Existing print statement
            quantities = fetch_product_quantities(url, db, uid, password, selected_product)
            print("Quantities fetched")  # New print statement
            quantities_at_location = [(quantity, record) for location, quantity, record in quantities if location == selected_location]
            print("Quantities at location determined")  # New print statement
            quantities_at_location = [(q, {k: v for k, v in rec.items() if 'quantity' in k}) for q, rec in quantities_at_location]
            print("Filtered quantities at location")  # New print statement
            user_friendly_data = "\n".join([f"{k}: {v}" for data in quantities_at_location for k, v in data[1].items()])
            window['-QUANTITIES-'].update(user_friendly_data)
            print("Quantities text updated")  # New print statement
            new_quantity_input.update(disabled=False)
            print("New quantity input enabled")  # New print statement
            submit_button.update(disabled=False)
            cancel_button.update(disabled=False)
            print("Submit and cancel buttons enabled")  # New print statement
            window.refresh()  # Force the window to redraw
            print("Window refreshed")  # New print statement
        else:
            selected_location = None

    elif event == '-SUBMIT-':
        new_quantity = values['-NEWQTY-']
        if new_quantity.isdigit():
            new_quantity = int(new_quantity)
            for _, record in quantities_at_location:
                update_product_quantities(url, db, uid, password, record['id'], new_quantity)
            quantities = fetch_product_quantities(url, db, uid, password, selected_product)
            locations = [f"{location}: {quantity}" for location, quantity, _ in quantities if 'virtual' not in location.lower()]
            window['-LOCATIONS-'].update(locations)
            new_quantity_input.update(disabled=True)
            submit_button.update(disabled=True)
            cancel_button.update(disabled=True)
    elif event == '-CANCEL-':
        new_quantity_input.update(disabled=True)
        submit_button.update(disabled=True)
        cancel_button.update(disabled=True)
    elif event == 'Unreserve':
        print(f"Unreserve event triggered. Product: {selected_product}, Location: {selected_location}, New Quantity: {values['-NEWQTY-']}")
        print(selected_location,'selected')
        
        print(selected_product,'selected')
        if selected_product is None or selected_location is None or values['-NEWQTY-'] == '':
            sg.popup('Please select a product and a location, and enter a new quantity.')
        else:
            print('Unreserve')
            new_quantity = values['-NEWQTY-']
            if new_quantity.isdigit():
                new_quantity = int(new_quantity)
                for _, record in quantities_at_location:
                    update_product_quantities(url, db, uid, password, record['id'], new_quantity)
                quantities = fetch_product_quantities(url, db, uid, password, selected_product)
                locations = [f"{location}: {quantity}" for location, quantity, _ in quantities if 'virtual' not in location.lower()]
                window['-LOCATIONS-'].update(locations)

window.close()
