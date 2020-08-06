# PythonScrapperCollection

## Crunchbase Scrapper

Python class implementing a scrapper fetching data from Crunchbase. The class uses `selenium` with Firefox in its headless configuration to handle the webpage.

## Dependency requirements:

* selenium (tested with 3.141.0)

Selenium needs a webdriver to work; more information, proper installation instructions and documentation are available [here](https://selenium-python.readthedocs.io/installation.html) and [here](https://pythonspot.com/selenium-webdriver/).

## Example

Import the class, create an instance, then fetch and print information about an organisation, and close the driver instance:

```python
from CrunchbaseScrapper import CrunchbaseScrapper
cs = CrunchbaseScrapper()
e = cs.getOrganisation('facebook')
print(e)
cs.done()
```

Result (edited and shortened):

```
{
    'name': 'Facebook', 
    'short bio': 'Facebook is an online social networking service that enables its users to connect with friends and family.', 
    'location': 'Menlo Park, California, United States', 
    'industries': ['Messaging', 'Mobile', 'Mobile Apps', 'Social', 'Social Media', 'Social Network'], 
    'headquarters regions': 'San Francisco Bay Area, Silicon Valley, West Coast', 
    'founded date': 'Feb 4, 2004', 
    'founders': ['Andrew McCollum', 'Chris Hughes', 'Dustin Moskovitz', 'Eduardo Saverin', 'Mark Zuckerberg'], 
    'ipo status': 'Public', 
    'stock symbol': 'NASDAQ:FB', 
    'company type': 'For Profit', 
    'website': 'http://www.facebook.com/', 
    'facebook': 'https://www.facebook.com/facebook/', 
    'linkedin': 'http://www.linkedin.com/company/facebook', 
    'twitter': 'https://twitter.com/facebook',
    [...]
}
```

## Class documentation

### Parameters

#### _wait_

The parameter `wait` defined to avoid performing a lot of successive requests in a small amount of time. Its default value is set to 3 seconds, but you can be initialised as follows (set up to 10 seconds):

```python
gs = GithubScrapper({'wait': 10 })
```

or reconfigured during the class lifecycle (for instance setting it to 5 seconds):

```python
parameters = gs.getParams()
parameters['wait'] = 5
gs.setParams(parameters)
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


#### _getOrganisation_

Get organisation info

###### param
* string *name*: name of the organisation

###### return
obj: the organisation info


#### _getFundingRounds_ (TBSL)

Get funding rounds info of the organisation

###### param
* string *name*: name of the organisation

###### return
obj: the funding rounds info


#### _getInvestors_ (TBSL)

Get investors info for the organisation

###### param
* string *name*: name of the organisation

###### return
obj: the investors info


#### _getInvestments_ (TBSL)

Get investments info for the organisation

###### param
* string *name*: name of the organisation

###### return
obj: the investments info


#### _getAcquisitions_ (TBSL)

Get acquisitions info for the organisation

###### param
* string *name*: name of the organisation

###### return
obj: the acquisitions info

