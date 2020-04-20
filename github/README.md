# PythonScrapperCollection

## Github Scrapper

Simple python class implementing a scrapper fetching data directly from Github. 

## Dependency requirements:

* requests (tested with 2.18.4)
* lxml (tested with 4.4.2)

## Example

Import the class, create an instance, then fetch and print information about an organisation:

```python
from GithubScrapper import GithubScrapper
gs = GithubScrapper()
info = gs.getOrganisation('facebook')
print(info)
```

Result:

```
{
  'id': 'facebook',
  'type': 'organisation', 
  'name': 'Facebook', 
  'profile': 'We are working to build community through open source technology. NB: members must have two-factor auth.', 
  'location': 'Menlo Park, California', 
  'url': 'https://opensource.fb.com'
}
```

## Class documentation

### Parameters

#### wait

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

#### getParams

Get the class parameters

**return** obj: the class parameters


#### setParams

Set the class parameters

**param** 
* obj params: the new values for the class parameters


#### getEntity

Get entity, whether it's an user or an organisation

**param**
* string name: name of the entity to request

**return** obj: the entity info


#### getUser

Get user info

**param**
* string name: name of the user
* xmltree page (optional): use the page passed as a parameter

**return** obj: the user info


#### getOrganisation

Get organisation info

**param**
* string name: name of the organisation
* param xmltree page (optional): use the page passed as a parameter

**return** obj: the organisation info


#### getPeople

Get list of people linked to an organisation

**param**
* string name: name of the organisation

**return** list: the users' handles


#### getRepositories

Get list of repositories for a given user or organisation

**param**
* string name: name of the user/organisation

**return** list: objects containing informations concerning the repositories

**alias** 
* getRepositoriesFromEntity
* getRepositoriesFromUser
* getRepositoriesFromOrganisation


#### getRepositoriesFromTopic

Get list of repositories for a given topic

**param**
* string name: name of the user
* xmltree page (optional): use the page passed as a parameter

**return** obj: the user info

