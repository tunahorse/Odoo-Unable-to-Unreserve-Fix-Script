import PySimpleGUI as sg
import yaml
from odoo_logic import test_login, fetch_products, fetch_product_quantities

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

layout = [
    [sg.Text('Product:', size=(10, 1)), sg.Combo(products, size=(30, 1), key='-PRODUCT-', enable_events=True, readonly=True)],
    [sg.Text('Locations:', size=(10, 1)), sg.Listbox(values=[], size=(30, 10), key='-LOCATIONS-', enable_events=True, pad=(0, (10, 0)))],
    [sg.Button('Unreserve'), sg.Button('Exit')]
]

window = sg.Window('Unreserve Products', layout, size=(400, 300))

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    elif event == '-PRODUCT-':
        # When a product is selected, fetch its quantities across all locations and display them
        quantities = fetch_product_quantities(url, db, uid, password, values['-PRODUCT-'])
        locations = [f"{location}: {quantity}" for location, quantity in quantities]
        window['-LOCATIONS-'].update(locations)
    elif event == '-LOCATIONS-':
        # When a location is selected, perform desired action
        selected_location = values['-LOCATIONS-'][0]  # Assuming single selection
        # Your logic for handling the selected location
        print(f"Selected Location: {selected_location}")
    elif event == 'Unreserve':
        # Your unreserve logic here
        sg.popup('Unreserve operation completed successfully')

window.close()
