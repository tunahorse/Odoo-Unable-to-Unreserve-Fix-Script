
# Odoo Stock Management Script

## Overview

This Python script connects to an Odoo server to perform various stock management operations. It allows you to:

- Authenticate and connect to the Odoo server using XML-RPC.
- Check if a given stock picking exists and whether it's in an operable state (not done or closed).
- List the stock moves related to the stock picking.
- Check and compare the reserved quantities of products against actual quantities in specific locations.
- Add products to a location if they are not found.
- Overwrite quantities to resolve discrepancies.

## Prerequisites

- Python 3.x installed.
- No additional Python packages are required as this script uses Python's standard libraries.

## How to Run

1. Clone the repository or download the script to your local machine.
2. Open the script in your favorite text editor to configure the Odoo server details:

   ```python
   db = 'your_database_name'
   url = 'your_server_url'
   username = 'your_username'
   password = 'your_password'
   ```

3. Save your changes.
4. Open a terminal window and navigate to the folder containing the script.
5. Run the script using Python:

   ```bash
   python your_script_name.py
   ```

6. When prompted, enter the stock picking name.

## Additional Notes

- The script uses an unverified SSL context. This is not recommended for production use. Make sure to use verified SSL certificates for secure connections.
  
- The Odoo server must have XML-RPC enabled, and you must have the necessary permissions to perform stock-related operations.


## Demo Video

Click on the image below to watch the demo video:

[![Watch the video](https://img.youtube.com/vi/VIDEO_ID/0.jpg)](https://www.canva.com/design/DAFuXHRlYpE/jdzRp0QYo9fuyW4giVfbrA/watch?utm_content=DAFuXHRlYpE&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink)

> Note: Replace `https://img.youtube.com/vi/VIDEO_ID/0.jpg` with a screenshot of your video.
