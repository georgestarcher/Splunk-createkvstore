# Splunk Create KV Store Collection


Author: George Starcher (starcher)
Email: george@georgestarcher.com

This code is presented **AS IS** under MIT license.

##Summary:

This Python script helps you create Splunk KV Store collections and the field definitions via the REST API.

##Requirements:

* Decide the Splunk app context the Collection will be made under.

* Decide the Collection name.

* Decide the needed fields and their types.

##Usage:

1. Edit the template.csv file.
    - The header row are the desired field names. 
    - The second row specifies the data type for each field. 
    -- Use the types: string, bool, time or number.

2. Edit the target splunk server in kvstore.conf

    splunk_server = localhost

3. Execute the script

    python makekvstore.py app collection

    - Example: python makekvstore.py search mycollection

