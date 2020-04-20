import requests
import lxml.html
from lxml import etree
import time

class GithubScrapper:
    params = {'wait': 3}
    request_base = 'https://github.com/'

    def __init__(self, params = {}):
        self.setParams(params)

## Private methods
    def __cleanString(self, s): 
        cont = True
        while cont:
            cont = False
            if s.startswith(' ') or s.startswith('\n'):
                cont = True
                s = s[1:]
            if s.startswith('\\n'):
                cont = True
                s = s[2:]
        cont = True
        while cont:
            cont = False
            if s.endswith(' ') or s.endswith('\n'):
                cont = True
                s = s[:-1]
            if s.endswith('\\n'):
                cont = True
                s = s[:-2]
        return s

    def __buildRepositoryInfo(self, li_elem):
        repo = {}
        page = li_elem
        # get name & id
        val = page.xpath('.//h3[@class="wb-break-all"]/a')
        if len(val) > 0:
            repo['name'] = self.__cleanString(val[0].text or '')
            repo['id'] = self.__cleanString(val[0].get('href', ' ')[1:])
        # get description
        val = page.xpath('.//p[@itemprop="description"]')
        if len(val) > 0:
            repo['profile'] = self.__cleanString(val[0].text or '')
        # get list of topics
        val = page.xpath('.//a[contains(@class, "topic-tag-link")]')
        list_topics = []
        for v in val:
            if v.text not in list_topics:
                list_topics.append(self.__cleanString(v.text))
        repo['topics'] = list_topics
        # get fork origin
        val = page.xpath('.//span/a[contains(@class, "muted-link")]')
        if len(val) > 0:
            repo['fork_origin'] = self.__cleanString(val[0].get('href', ' ')[1:])
        # get main coding language
        val = page.xpath('.//span[@itemprop="programmingLanguage"]')
        if len(val) > 0:
            repo['language'] = self.__cleanString(val[0].text or '')
        # get licence
        val = page.xpath('.//span/svg[contains(@class, "octicon-law")]/..')
        if len(val) > 0:
            tmp = str(etree.tostring(val[0][0]))[2:-1].split('</svg>')
            if len(tmp) > 1:
                tmp = tmp[1]
            else:
                tmp = tmp[0] 
            repo['licence'] = self.__cleanString(tmp)
        # get number of forks
        val = page.xpath('.//a[@href="/'+repo['id']+'/network/members"]')
        if len(val) > 0:
            tmp = str(etree.tostring(val[0][0]))[2:-1].split('</svg>')
            if len(tmp) > 1:
                tmp = tmp[1]
            else:
                tmp = tmp[0] 
            repo['forks'] = self.__cleanString(tmp)
        # get number of stars
        val = page.xpath('.//a[@href="/'+repo['id']+'/stargazers"]')
        if len(val) > 0:
            tmp = str(etree.tostring(val[0][0]))[2:-1].split('</svg>')
            if len(tmp) > 1:
                tmp = tmp[1]
            else:
                tmp = tmp[0] 
            repo['stars'] = self.__cleanString(tmp)
        # get number of issues
        #val = page.xpath('.//a[@href="/'+repo['id']+'/issues"]')
        val = page.xpath('.//a/svg[contains(@class, "octicon-issue-opened")]/..')
        if len(val) > 0:
            tmp = str(etree.tostring(val[0][0]))[2:-1].split('</svg>')
            if len(tmp) > 1:
                tmp = tmp[1]
            else:
                tmp = tmp[0] 
            repo['issues'] = self.__cleanString(tmp)
        # get number of pulls
        val = page.xpath('.//a[@href="/'+repo['id']+'/pulls"]')
        if len(val) > 0:
            tmp = str(etree.tostring(val[0][0]))[2:-1].split('</svg>')
            if len(tmp) > 1:
                tmp = tmp[1]
            else:
                tmp = tmp[0] 
            repo['pulls'] = self.__cleanString(tmp)
        # get latest version date
        val = page.xpath('.//relative-time')
        if len(val) > 0:
            repo['update'] = self.__cleanString(val[0].get('datetime', ''))
        return repo
        
    def __fetchEntity(self, name):
        response = requests.get(self.request_base + name)
        page = lxml.html.fromstring(response.content)
        sp = page.xpath('.//span[contains(@class, "p-name")]')
        if len(sp) > 0:
            # page is user
            return page, 'user'
        else:
            # page is organisation
            return page, 'organisation'

    def __fetchPeople(self, name, index):
        response = requests.get(self.request_base + 'orgs/' + str(name) + '/people?page=' + str(index))
        page = lxml.html.fromstring(response.content)
        val = page.xpath('.//div[@class="blankslate"]/h3')
        if len(val) > 0:
            return None
        return page

    def __fetchRepositories(self, name, page = ''):
        url = ''
        # fetch first page
        if page == '':
            response = requests.get(self.request_base + str(name) + '?tab=repositories&page=1')
            page = lxml.html.fromstring(response.content)
            return page
        # fetch the following page based on the current one
        # is organisation        
        val = page.xpath('.//div[@id="org-repositories"]') #exists
        if len(val) > 0:
            val = page.xpath('.//a[@class="next_page"]') #none if nothing after
            if len(val) > 0:
                url = self.request_base + val[0].get('href', ' ')[1:]
        # is user
        val = page.xpath('.//div[@id="user-repositories-list"]') #exists
        if len(val) > 0:
            val = page.xpath('.//div[@id="user-repositories-list"]//div[@class="paginate-container"]/div[@data-test-selector="pagination"]/a') #none if nothing after
            for v in val:
                if v.text == 'Next':
                    url = v.get('href', '')
        # fetch next
        if url == '':
            return None
        response = requests.get(url)
        page = lxml.html.fromstring(response.content)
        return page

    def __fetchTopicRepositories(self, topic, index, seed):
        response = requests.get(self.request_base + '/topics/' + topic + '?page=' + str(index) + '&q=' + seed) 
        page = lxml.html.fromstring(response.content)
        return page

## Public methods
    '''
      Get the class parameters
      @return obj: the class parameters
    '''
    def getParams(self):
        return self.params

    '''
      Set the class parameters
      @param obj params: the new values for the class parameters
    '''
    def setParams(self, params = {}):
        for i in params:
            self.params[i] = params[i]

    '''
      Get entity, whether it's an user or an organisation
      @param string name: name of the entity to request
      @return obj: the entity info
    '''
    def getEntity(self, name):
        page, type_entity = self.__fetchEntity(name)
        if type_entity == 'user':
            # page is user
            return self.getUser(name, page)
        if type_entity == 'organisation':
            # page is organisation
            return self.getOrganisation(name, page)

    '''
      Get user info
      @param string name: name of the user
      @param xmltree page (optional): use the page passed as a parameter
      @return obj: the user info
    '''
    def getUser(self, name, page = ''):
        if page == '':
            page, type_entity = self.__fetchEntity(name)
            if page == None or type_entity != 'user':
                return None
        new_user = {'type': 'user'}
        # print('Querying ' + name + '...')
        # get name
        val = page.xpath('.//h1[contains(@class, "vcard-names")]/span[@itemprop="name"]')
        if len(val) > 0:
            new_user['name'] = val[0].text or ''
        # get id
        val = page.xpath('.//h1[contains(@class, "vcard-names")]/span[@itemprop="additionalName"]')
        if len(val) > 0:
            new_user['id'] = val[0].text or ''
        # get description
        val = page.xpath('.//div[contains(@class, "user-profile-bio")]/div')
        if len(val) > 0:
            new_user['profile'] = val[0].text or ''
        # get work
        val = page.xpath('.//li[@itemprop="worksFor"]/span[@class="p-org"]/div')
        if len(val) > 0:
            if val[0].text != '':
                new_user['works'] = val[0].text or ''
            elif val[0][0].get('href') != None:
                new_user['works'] = val[0][0].text or ''
        # get location 
        val = page.xpath('.//li[@itemprop="homeLocation"]/span[@class="p-label"]')
        if len(val) > 0:
            new_user['location'] = val[0].text or ''
        # get url
        val = page.xpath('.//li[@itemprop="url"]/a')
        if len(val) > 0:
            new_user['url'] = val[0].text or ''
        # get organizations
        val = page.xpath('.//a[@itemprop="follows"]')
        tab = []
        for itm in val:
            tab.append(itm.get('href')[1:])
        new_user['organisations'] = tab
        return new_user

    '''
      Get organisation info
      @param string name: name of the organisation
      @param xmltree page (optional): use the page passed as a parameter
      @return obj: the organisation info
    '''
    def getOrganisation(self, name, page = ''):
        if page == '':
            page, type_entity = self.__fetchEntity(name)
            if page == None or type_entity != 'organisation':
                return None
        new_org = {'type': 'organisation'}
        # get name
        val = page.xpath('.//meta[@property="og:title"]')
        if len(val) > 0:
            new_org['name'] = val[0].get('content', '')
        # get id
        val = page.xpath('.//meta[@property="profile:username"]')
        if len(val) > 0:
            new_org['id'] = val[0].get('content', '')
        # get description
        val = page.xpath('.//div[contains(@class, "TableObject-item")]/span/div')
        if len(val) > 0:
            new_org['profile'] = val[0].text or ''
        # get location 
        val = page.xpath('.//ul[contains(@class, "has-location")]/li/span[@itemprop="location"]')
        if len(val) > 0:
            new_org['location'] = val[0].text or ''
        # get url
        val = page.xpath('.//ul[contains(@class, "has-blog")]/li/a[@itemprop="url"]')
        if len(val) > 0:
            new_org['url'] = val[0].get('href', '')
        return new_org

    '''
      Get list of people linked to an organisation
      @param string name: name of the organisation
      @return list: the users' handles
    '''
    def getPeople(self, name):
        # get users
        i = 1
        list_people_tmp = []
        cont = True
        while cont:
            time.sleep(self.params['wait'])
            page = self.__fetchPeople(name, i)
            if page == None:
                cont = False
                break
            val = page.xpath('.//div/a[@data-hovercard-type="user"]')
            if len(val) > 0:
                for v in val: 
                    tmp = v.get('href', ' ')[1:]
                    if tmp not in list_people_tmp:
                        list_people_tmp.append(tmp)
            else:
                cont = False
            i += 1
        return list_people_tmp

    '''
      Get list of repositories for a given user or organisation
      @param string name: name of the user/organisation
      @return list: objects containing informations concerning the repositories
    '''
    def getRepositories(self, name):
        list_repo = []
        cont = True
        page = ''
        while cont:
            time.sleep(self.params['wait'])
            page = self.__fetchRepositories(name, page)
            if page == None:
                cont = False
                break
            # tries for organisation first
            val = page.xpath('.//div[@id="org-repositories"]//li[@itemprop="owns"]')
            if len(val) == 0:
                # if failed, tries for user
                val = page.xpath('.//div[@id="user-repositories-list"]//li[@itemprop="owns"]')
            for v in val:
                list_repo.append(self.__buildRepositoryInfo(v))
            if len(val) == 0:
                cont = False
        return list_repo

    '''
      Get list of repositories for a given topic
      @param string name: name of the user
      @param xmltree page (optional): use the page passed as a parameter
      @return obj: the user info
    '''
    def getRepositoriesFromTopic(self, topic):
        index = 1
        cnt = 0
        cont = True
        start = 'a'
        end = 'z'
        seed = [start]
        list_repo = []
        index_repo = []
        while cont:
            cont = False
            time.sleep(self.params['wait'])
            # print(seed, cnt)
            page = self.__fetchTopicRepositories(topic, index, str.join('', seed))
            val = page.xpath('.//button[contains(@data-disable-with, "Loading")]')
            if len(val) > 0:
                # 'Loading more' button exists
                cont = True
            val = page.xpath('.//h2[contains(@class, "h3-mktg")]')
            n = ''
            if len(val) > 0:
                for c in val[0].text:
                    if c >= '0' and c <= '9':
                        n += c
            if n != '':
                n = int(n)
            else:
                n = 0
            if n > 1000:
            # github limits the lists to the first 1020 elements, thus subdivide if more results
            # ex: tries querying with 'a', then 'aa', then 'aaa'...
                seed.append(start)
                continue
            else:
                elements = page.xpath('.//article')
                for elem in elements:
                    repo = {}
                    # get author id
                    val = elem.xpath('.//h1/a[contains(@data-ga-click, "Explore, go to repository owner")]')
                    if len(val) > 0:
                        repo['author'] = val[0].get('href', ' ')[1:]
                    # get repository id
                    val = elem.xpath('.//h1/a[contains(@data-ga-click, "Explore, go to repository, location")]')
                    if len(val) > 0:
                        repo['repository'] = val[0].get('href', ' ')[1:]
                    # get stars
                    val = elem.xpath('.//a[contains(@class, "social-count")]')
                    if len(val) > 0:
                        repo['stars'] = self.__cleanString(val[0].text)
                    # get update time
                    val = elem.xpath('.//relative-time')
                    if len(val) > 0:
                        repo['update'] = self.__cleanString(val[0].get('datetime',''))
                    # ignore if repo is already accounted for
                    if repo.get('repository', '') not in index_repo:
                        list_repo.append(repo)
                        index_repo.append(repo.get('repository', ''))
                        cnt += 1

                if not cont:
                    # flush end seed once it reached "end"
                    while seed[-1] == end:
                        seed = seed[:-1]
                        if len(seed) == 0:
                            cont = False
                            break
                    # increment last letter of seed
                    if len(seed) > 0:
                        seed[-1] = chr(ord(seed[-1]) +1)
                        index = 0
                        cont = True
                else:
                    # get next page
                    index += 1
        return list_repo       

## Aliases
    def getRepositoriesFromEntity(self, name):
        return self.getRepositories(name)

    def getRepositoriesFromUser(self, name):
        return self.getRepositories(name)

    def getRepositoriesFromOrganisation(self, name):
        return self.getRepositories(name)

if __name__ == "__main__":
    gs = GithubScrapper()
    #print(gs.getPeople('facebook'))
    l = gs.getRepositoriesFromTopic('image-generation')
    print(l)
    print(len(l))
    
