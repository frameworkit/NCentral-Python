# NCentral-Python
Repo to house example code for interacting with the N-central SOAP API via Python. Intended to serve as a starting point for an NC Partner who is comfortable with Python, but not familiar with the NC API.

Considered a continual work in progress, be patient with any ugliness or incomplete aspects.

## Must Know Details

#### Aspects of the N-central SOAP API
- Documentation for the SOAP API can be found on each N-central server here: `https://<server address>/dms/`
	- The NCentral server used to build these examples is hosted with N-Able, so for example, our API documentation is found at `https://ncod126.n-able.com/dms`, which is a shared server instance
- The actual useful piece of documentation is the Javadocs, found at `https://<server address>/dms/javadoc_ei2/index.html?com/nable/nobj/ei2/ServerEI2_PortType.html`
	- The methods listed on that page encompass all of the endpoints you can interact with via the API.
- The other aspect of the documentation is the WSDL, found at `https://<server address>/dms2/services2/ServerEI2?wsdl`
	- This is not human readable, but is important for your use of the API as will be explained below
- Common Parameters for the API calls are one of the following:
	- `username` and `password`, these must be passed along in every call.
		- More an authentication below
	- `[List]<[EiKeyValue]> settings` is a little confusing at first, but in python this is just a `dict` formatted a little strangely, here's an example: 
```
  deviceId = {
    'key': 'customerID',
    'value': 150
    }
```
- The data returned from NC can be ugly / cumbersome, so in most of our examples we iterate through the return, parse the data, and place it into a new `list` or `dict` for easier consumption. 

#### Authentication

An API User must be created in your NC server for authentication. Follow N-Able's guide here: https://documentation.n-able.com/N-central/userguide/Content/User_Management/Role%20Based%20Permissions/role_based_permissions_create_APIuser.htm?Highlight=api%20user

Your username for this API account doesn't need to be a real e-mail address, you can make it whatever you want. At the end of the guide, you will have a JSON Web Token (JWT). This is the password for the user that will be used in each API call.

We recommend storing and retrieving the username and password via a key management system, such as Azure Key Vault - https://azure.microsoft.com/en-us/products/key-vault#layout-container-uida0cf . This will provide some best practice security assuming you are executing your API calls in a secure system / environment, such as Azure Functions, as the username and password are only exposed in code during runtime.

#### Zeep Library

We've abstracted away (most) of the ugly part of working with SOAP by using the Zeep Library - https://docs.python-zeep.org/en/master/. Zeep makes working with the NC API much simpler and has very little setup / configuration required. 
