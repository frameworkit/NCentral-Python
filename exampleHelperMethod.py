import zeep

# This file is intended to be used in tandem with the exampleRunner.py

# Place your NC Server FQDN into this variable
nc_Server_URL = 'MUST CHANGE'

# Your server organization ID in NC is a key bit of info you will need to identify. 
# This is considered your "root" organization in NC, and any customers you have will point to this as their parent,
# similar to how each site points at their customer ID for their parent.
# This should be an int, not a string
nc_SOID = 150 # <<<< MUST CHANGE

# Simply returns a prepared zeep client for use
def ncentralClient() -> zeep.Client:

   client = zeep.Client(f'http://{nc_Server_URL}/dms2/services2/ServerEI2?wsdl')
   return client

# Helper method for .customerList() method in the N-Central API.
# The .customerList() call does not just return customers, it returns customers and sites for each customer
# It seems to place sites and customers at the same "level". All of them have a key:value pair for 'customer.parentid' though
# Using the parentid, you can identify if it's a site, or if it's a customer
def getNCCustomerList(userName,passWord,client=ncentralClient()) -> list:

    response = client.service.customerList(userName,passWord)
    fullCustomerList = []

    
    for customer in response:
        customerDict = {}
        for items in customer['items']:
            customerDict[items['key']] = items['value']
        fullCustomerList.append(customerDict)

    return fullCustomerList

def getNCCustDeviceList(userName,passWord,ncId,client=ncentralClient()) -> list:

    custId = {
        'key': 'customerID',
        'value': ncId,
    }

    settingsList = [custId]
    response = client.service.deviceList(userName,passWord,settingsList)
    fullDeviceList = []

    for device in response:
        deviceDict = {}
        for items in device['items']:
            deviceDict[items['key']] = items['value']
        fullDeviceList.append(deviceDict)

    return fullDeviceList

def getNCDeviceInfo(userName,passWord,ncDeviceId,client=ncentralClient()) -> list:

    deviceId = {
        'key': 'TargetByDeviceID',
        'value': ncDeviceId
    }

    include = {
        'key': 'InformationCategoriesInclusion',
        'value': "asset.computersystem"
    }

    settingsList = [deviceId,include]
    response = client.service.deviceAssetInfoExportDeviceWithSettings("0.0",userName,passWord,settingsList)
    deviceDict = {}

    for item in response[0]['items']:
        deviceDict[item['key']] = item['value']

    return deviceDict

def getNCDeviceCustomerInfo(userName,passWord,ncDeviceId,client=ncentralClient()) -> list:

    deviceId = {
        'key': 'TargetByDeviceID',
        'value': ncDeviceId
    }

    include = {
        'key': 'InformationCategoriesInclusion',
        'value': "asset.customer"
    }

    settingsList = [deviceId,include]
    response = client.service.deviceAssetInfoExportDeviceWithSettings("0.0",userName,passWord,settingsList)
    deviceDict = {}

    for item in response[0]['items']:
        deviceDict[item['key']] = item['value']

    return deviceDict

# Helper method to format call to .customerAdd()
# Requires specific formatting of data payload to complete successfully
# This helper method handles that formatting for you.
def addNewNCCustomer(userName,passWord,customerName,extId,client=ncentralClient()) -> int:

    newCustomerNameDict = {
    'key': 'customername',
    'value': customerName,

    }
    # The parent id of 143 is hard coded, this is the root level of our organization in NCentral
    newCustomerIDDict = {
    'key': 'parentid',
    'value': 143
    }

    newCustomerExtIdDict = {
    'key': 'externalid',
    'value': extId
    }

    newCustomerLicTypeDict = {
    'key': 'licensetype',
    'value': "Professional"
    }

    settingsList = [newCustomerNameDict,newCustomerIDDict,newCustomerExtIdDict,newCustomerLicTypeDict]
    addResponse = client.service.customerAdd(userName,passWord,settingsList)

    return addResponse


# This is almost identical to the addNewCustomer() helper method above, but key difference of requiring the parentID as a param
def addNewNCSite(userName,passWord,siteName,parentID,extId,client=ncentralClient()) -> int:

    newSiteNameDict = {
    'key': 'customername',
    'value': siteName
    }
    # The parent id is crucial, that is what makes this new record a site under the correct customer
    newSiteIDDict = {
    'key': 'parentid',
    'value': parentID
    }

    newSiteExtIdDict = {
    'key': 'externalid',
    'value': extId
    }

    newSiteLicTypeDict = {
    'key': 'licensetype',
    'value': "Professional"
    }

    settingsList = [newSiteNameDict,newSiteIDDict,newSiteExtIdDict,newSiteLicTypeDict]
    addResponse = client.service.customerAdd(userName,passWord,settingsList)

    return addResponse

# Changing custom properties is a little strange, the parameters the API wants are formatted a little differently as they are nested
def changeNCDeviceProperty(userName,passWord,deviceID,propertyID,newValue,client=ncentralClient()):

    deviceProp = [{
            'deviceID': int(deviceID),
            'properties': [{
                'devicePropertyID': propertyID,
                'value': newValue
            }]
        }
    ]
    deviceResponse = client.service.devicePropertyModify(userName,passWord,deviceProp)
    return deviceResponse

# Changing custom properties is a little strange, the parameters the API wants are formatted a little differently as they are nested
def changeNCOrganizationProperty(userName,passWord,orgID,propertyID,newValue,client=ncentralClient()):

    orgProp = [{
            'customerId': int(orgID),
            'properties': [{
                'propertyId': propertyID,
                'value': newValue
            }]
        }
    ]
    orgResponse = client.service.organizationPropertyModify(userName,passWord,orgProp)
    return orgResponse

# Returns a list of customer organization properties. Method takes optional customerIDList params to filter down results as needed, otherwise will return all of the org lists.
def getNCOrgPropertyList(userName,passWord,customerIDList: list[int] = None,client=ncentralClient()) -> list:

    if customerIDList == None:
        orgPropList = client.service.organizationPropertyList(userName,passWord,[],False)
    else:
        orgPropList = client.service.organizationPropertyList(userName,passWord,customerIDList,False)

    fullPropList = []        

    for org in orgPropList:
        orgName = ''
        orgID = org['customerId']
        orgProps = []
        for props in org['properties']:
            propEntry = {
                'propertyId': props['propertyId'],
                'propertyName': props['label'],
                'propertyValue': props['value'],
            }
            orgProps.append(propEntry)
        orgEntry = {
            'customerName': orgName,
            'customerId': orgID,
            'properties': orgProps
        }
        fullPropList.append(orgEntry)

    return fullPropList

# Returns a list of device custom properties. Method takes optional deviceID param to filter down results as needed, otherwise will return all of the device custom properties
def getNCDevicePropertyList(userName,passWord,deviceID=None,client=ncentralClient()):

    deviceIDs = [deviceID]
    deviceNames = ['']
    filterIDs = []
    filterNames = ['']

    settingsDict = {
        'key': 'customerID',
        'value': nc_SOID,
    }

    if not deviceID==None:
        listResponse = client.service.devicePropertyList(userName,passWord,deviceIDs,reverseOrder=False)
        deviceList = []
        for device in listResponse:
            serverProps = []
            for props in device['properties']:
                propEntry = {
                    'propertyID': props['devicePropertyID'],
                    'propertyName': props['label'],
                    'propertyValue': props['value'],
                }
                serverProps.append(propEntry)
            serverEntry = {
                'deviceID': device['deviceID'],
                'deviceName': device['deviceName'],
                'properties': serverProps
            }
            deviceList.append(serverEntry)
    else:
        listResponse = client.service.deviceList(userName,passWord,settingsDict)
        deviceList = []
        for device in listResponse:
            deviceDict = {}
            for items in device['items']:
                deviceDict[items['key']] = items['value']
            deviceList.append(deviceDict)

    return deviceList