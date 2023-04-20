import exampleHelperMethod as helper

# This file is intended to just show how we build / format things to keep certain actions abstracted away in a helper file. 
# 

ncUsername = 'MUST CHANGE'
ncPassword = 'MUST CHANGE'

ncClient = helper.ncentralClient()

# Example of a client import

newClientList = [
    {
    'customerName': 'New Test Client 1',
    'psaID': 10
    },
    {
    'customerName': 'New Test Client 2',
    'psaID': 11
    },
    {
    'customerName': 'New Test Client 3',
    'psaID': 12
    },
    {
    'customerName': 'New Test Client 4',
    'psaID': 13
    },
]

for client in newClientList:

    newCustName = client['customerName']
    psaID = client['psaID']

    newCustID = helper.addNewNCCustomer(userName=ncUsername,passWord=ncPassword,customerName=newCustName,extId=psaID,client=ncClient)

# Fleshing out this example file, you can build a recurring client sync from your PSA by running it on a platform like Azure Functions or AWS Lambda. 