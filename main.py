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
    [sg.Text('Product:', size=(10, 1)), sg.Combo(products, size=(60, 10), key='-PRODUCT-', enable_events=True, readonly=True)],
    [sg.Text('Locations:', size=(10, 1)), sg.Listbox(values=[], size=(60, 20), key='-LOCATIONS-', enable_events=True, pad=(0, (10, 0)))],
    [sg.Button('Unreserve'), sg.Button('Exit')]
]

window = sg.Window('Unreserve Products', layout, size=(800, 600))

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
        selected_location = values['-LOCATIONS-'][0].split(':')[0]  # Save the selected location
        print(f"Selected Location: {selected_location}")
    elif event == 'Unreserve':
        if selected_product and selected_location:
            # Fetch the product quantities for the selected location
            quantities = fetch_product_quantities(url, db, uid, password, selected_product)
            quantities_at_location = [(quantity, record) for location, quantity, record in quantities if location == selected_location]
            sg.popup('Quantities at selected location:', quantities_at_location)
        else:
            sg.popup('Please select a product and a location.')

window.close()
