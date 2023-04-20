import zeep

# In this example file, we will do everything needed to get a list of customers from N-central, make that output a bit easier to work with, then create a new customer.

# Place your NC Server FQDN into this variable
nc_Server_URL = 'MUST CHANGE'

# Place your API Username and JSON Web Token into these variables
nc_Username = 'MUST CHANGE'
nc_Password = 'MUST CHANGE'

# Your server organization ID in NC is a key bit of info you will need to identify. 
# This is considered your "root" organization in NC, and any customers you have will point to this as their parent,
# similar to how each site points at their customer ID for their parent.
# This should be an int, not a string
nc_SOID = 150 # <<<< MUST CHANGE

# The link to the WSDL file on your NC Server is ultimately what Zeep interacts with
client = zeep.Client(f'http://{nc_Server_URL}/dms2/services2/ServerEI2?wsdl')

# Using the zeep client is always formatted this way:
# zeepClient.server.API-Method-You-Want-To-Call(params)

# Let's get a list of our customers from NC
# In this example, .customerList() is a method found on the javadocs page, it is written to take a third param (List<EiKeyValue> settings) but it is not required
customerListResponse = client.service.customerList(nc_Username,nc_Password)

# The response for customerList() is a little messy, we recommend parsing it into a new list object
fullCustomerList = []

# Iterate through the response
for customer in customerListResponse:
    # Once we're down one level, create a new dict to store the values
    customerDict = {}
    # We have to manually get into the 'items' list under each customer, that is where the data is actually at
    for items in customer['items']:
        # The data is structured a little strange, but luckily it does have a format included where we can just grab the key and value
        customerDict[items['key']] = items['value']
    # Once all of the items have been added to the dict, add this dict to the response list
    fullCustomerList.append(customerDict)

# Now at this point, fullCustomerList is a list with a format you might expect from other APIs and should be used. 
# You can print(fullCustomerList), or just throw a breakpoint somewhere, debug the file, and look for it to inspect what the data actually looks like
print(fullCustomerList)

# Let's now add a customer to NC
# the .customerAdd() method takes a List<EiKeyValue> settings parameter, which we need to construct first. 
# In python, we build a list of dictionaries to handle all of the required inputs

# Here is the name of our new customer
customerName = 'Test Me Out Corp'

# We start by building a dictionary to house a key-value pair for each property we want to define or pass through

# Required for adding a customer
newCustomerNameDict = {
'key': 'customername',
'value': customerName,
}

# For a new customer, we want their parent ID to be the service organization, or root, of our NC Server. 
# If you wanted to make a new site under an existing customer, you would place that customer's ID here
newCustomerParentIDDict = {
'key': 'parentid',
'value': nc_SOID
}

# This is not necessary, but we recommend it. For example, we place our PSA Company ID's into this field
newCustomerExtIdDict = {
'key': 'externalid',
'value': 1234
}

# Always set to Professional
newCustomerLicTypeDict = {
'key': 'licensetype',
'value': "Professional"
}

# We add all of these above dictionaries into a new list
settingsList = [newCustomerNameDict,newCustomerParentIDDict,newCustomerExtIdDict,newCustomerLicTypeDict]

# We place the list as the last param in the .customerAdd() method
addResponse = client.service.customerAdd(nc_Username,nc_Password,settingsList)

# The response for this call is just an int of the newly created customerID in NC. 
print(f'New Customer Added - ID: {addResponse}')