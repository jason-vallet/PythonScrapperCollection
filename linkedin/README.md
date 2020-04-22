# PythonScrapperCollection

## LinkedIn Scrapper

Python class implementing a scrapper fetching data from LinkedIn. The class uses `selenium` to manage a remote window.

## Dependency requirements:

* selenium (tested with 3.141.0)

Selenium needs a webdriver to work; more information, proper installation instructions and documentation are available [here](https://selenium-python.readthedocs.io/installation.html) and [here](https://pythonspot.com/selenium-webdriver/).

## Example

Import the class, set up your parameters, create an instance, declare your driver and connection information, then fetch and print information about a company:

```python
from LinkedInScrapper import LinkedInScrapper
p = {}
p['email'] = "MyEmail"
p['password'] = "MyPassword"
p['driver'] = 'firefox'
ls = LinkedInScrapper(p)
ls.signIn()
info = ls.getCompany('facebook')
print(info)
ls.signOut()
```

Result:

```
{
    'id': 'facebook', 
    'url': 'https://www.linkedin.com/company/facebook', 
    'name': 'Facebook', 
    'specialty': 'Internet', 
    'address': 'Menlo Park, CA', 
    'followers': '5,694,808 followers', 
    'short bio': '', 
    'overview': 'Founded in 2004, Facebook’s mission is to give people the power to build community and bring the world closer together. [...]',
    'website': 'http://www.facebook.com/careers', 
    'phone': '', 
    'industry': 'Internet', 
    'company size': '10,001+ employees;63,242 on LinkedIn\nIncludes members with current employer listed as Facebook, including part-time roles. Also includes employees from subsidiaries: WhatsApp Inc.,Oculus VR,Instagram and 2 more.',
    'headquarters': 'Menlo Park, CA', 
    'type': 'Public Company', 
    'founded': '2004', 
    'specialties': 'Connectivity, Artificial Intelligence, Virtual Reality, Machine Learning, Social Media, Augmented Reality, Marketing Science, Mobile Connectivity, and Open Compute'
}
```

## Class documentation

### Parameters

#### _wait_

The parameter `wait` is defined to avoid performing a lot of successive requests in a small amount of time. Its default value is set to 3 seconds.

#### _email_

The email address you use to connect to LinkedIn.

#### _password_

Your password to connect to LinkedIn.

#### _driver_

The driver to use with `selenium`; choose one of the following values: chrome, firefox, edge, ie, opera, safari.


### Changing parameters values

The parameters can be initialised when creating the class instance (example with `wait` set up to 10 seconds):

```python
ls = LinkedInScrapper({'wait': 10 })
```

or reconfigured during the class lifecycle (for instance setting it to 5 seconds):

```python
parameters = ls.getParams()
parameters['wait'] = 5
ls.setParams(parameters)
```

### Methods

#### _getParams_

Get the class parameters

###### return
obj: the class parameters


#### _setParams_

Set the class parameters

###### param 
* obj *params*: the new values for the class parameters


#### _signIn_

Initialise the driver and sign in using the credentials provided to the class

###### return
bool: the success of the driver initialisation


#### _signOut_

Log out of LinkedIn and close the driver


#### _getCompany_

Get company info

###### param
* string *name*: name of the company

###### return
obj: the company info


#### _getPeople_

Get list of people linked to a company

###### param
* string *name*: name of the company

###### return
list: the users' info


