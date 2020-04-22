import time
from selenium import webdriver

class LinkedInScrapper:
    params = {'wait': 3, 'email': 'id', 'password': 'pass', 'driver': 'firefox'}

    def __init__(self, params = {}):
        self.setParams(params)
        self.initDriver = False
        self.columns = ['id', 'url', 'name', 'specialty', 'address', 'followers', 'short bio', 'overview', 'website', 'phone', 'industry', 'company size', 'headquarters', 'type', 'founded', 'specialties']

    def __fetchCompany(self, name):
        return self.__fetchUrl('company/' + name + '/about')


    def __fetchUrl(self, url_base):
        if not self.initDriver:
            if not self.signIn():
                return False
        if url_base.startswith('https://www.linkedin.com/'):
            full_url = str(url_base)
        else:
            full_url = 'https://www.linkedin.com/' + str(url_base)
        try:
            self.driver.get(full_url)
        except:
            return False
        # try page availability
        try:
            unavailable = self.driver.find_element_by_xpath("//p[@class='artdeco-empty-state__message']")
        except:
            unavailable = ''
        if unavailable != '':
            return False
        return True

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
      Initialise the driver and sign in using the credentials provided to the class
      @return bool: the success of initialising the driver
    '''
    def signIn(self):
        if self.params['driver'] == 'chrome':
            self.driver = webdriver.chrome()
        elif self.params['driver'] == 'firefox':
            self.driver = webdriver.Firefox()
        elif self.params['driver'] == 'edge':
            self.driver = webdriver.edge()
        elif self.params['driver'] == 'ie':
            self.driver = webdriver.ie()
        elif self.params['driver'] == 'opera':
            self.driver = webdriver.opera()
        elif self.params['driver'] == 'safari':
            self.driver = webdriver.safari()
        else:
            return False    #driver undefined
        self.initDriver = True
        self.driver.get('https://www.linkedin.com/login')

        # signin
        user_field = self.driver.find_element_by_xpath("//input[@id='username']")
        user_field.send_keys(self.params['email'])
        pass_field = self.driver.find_element_by_xpath("//input[@id='password']")
        pass_field.send_keys(self.params['password'])
        self.driver.find_element_by_xpath("//button[@data-litms-control-urn='login-submit']").click()
        return True

    '''
      Log out of LinkedIn and close the driver
    '''
    def signOut(self):
        #signout
        self.driver.get('https://www.linkedin.com/m/logout/')
        self.driver.close()

    '''
      Get company info
      @param string name: name of the company
      @return obj: the company info
    '''
    def getCompany(self, name):
        # get page and set up default values
        if not self.__fetchCompany(name):
            return {}
        entity = {}
        for i in self.columns:
            entity[i] = ''

        entity['id'] = name
        entity['url'] = 'https://www.linkedin.com/company/' + name
        try:
            entity['name'] = self.driver.find_element_by_xpath("//h1[contains(@class,'org-top-card-summary__title')]/span").text
        except:
            entity['name'] = name

        try:
            info_list = self.driver.find_elements_by_xpath("//div[contains(@class,'org-top-card-summary-info-list__info-item')]")
        except:
            info_list = []

        if len(info_list) > 0:
            entity['specialty'] = info_list[0].text
        else:
            entity['specialty'] = ''

        if len(info_list) > 1:
            entity['address'] = info_list[1].text
        else:
            entity['address'] = ''

        if len(info_list) > 2:
            entity['followers'] = info_list[2].text
        else:
            entity['followers'] = ''

        try:
            entity['short bio'] = self.driver.find_element_by_xpath("//div[contains(@class,'org-top-card__primary-content')]/p").text
        except:
            entity['short bio'] = ''

        try:
            entity['overview'] = self.driver.find_element_by_xpath("//div[contains(@class,'org-grid__core-rail--no-margin-left')]/section/p[contains(@class,'break-words')]").text
        except:
            entity['overview'] = ''

        # pick complementary information
        try:
            info_list = self.driver.find_elements_by_xpath("//div[contains(@class,'org-grid__core-rail--no-margin-left')]/section/dl/*")
        except:
            info_list = []
        prev = ''
        for val in info_list:
            if val.text.lower() in self.columns:
                prev = val.text.lower()
                entity[prev] = ''
                continue
            if entity[prev] != '':
                entity[prev] += ';'
            entity[prev] += val.text

        return entity

    '''
      Get list of people linked to a company
      @param string name: name of the company
      @return list: the users' info
    '''
    def getPeople(self, name):
        if not self.__fetchCompany(name):
            return []
        try:
            url_base = self.driver.find_element_by_xpath("//a[@data-control-name='topcard_see_all_employees']").get_attribute('href')
        except:
            url_base = ''
        if url_base == '':
            return []
        n_page = 4
        list_people = []
        cont = True
        while cont:
            time.sleep(self.params['wait'])
            page = self.__fetchUrl(url_base + '&page=' + str(n_page))
            if page == False:
                cont = False
                break
            # init partial list
            list_people_tmp = []
            try:
                tmp_li = self.driver.find_elements_by_xpath("//li[contains(@class,'search-result')]/div/div")
            except:
                tmp_li = []
            if len(tmp_li) == 0:
                cont = False
                break
            list_people_tmp = [{} for i in range(len(tmp_li))]
                
            # name
            try:
                tmp_names = self.driver.find_elements_by_xpath("//li[contains(@class,'search-result')]//span[contains(@class,'actor-name')]")
            except:
                tmp_names = []
            for i in range(len(tmp_names)):
                list_people_tmp[i]['name'] = tmp_names[i].text
            # url
            try:
                tmp_urls = self.driver.find_elements_by_xpath("//li[contains(@class,'search-result')]//div[contains(@class,'search-result__info')]/a[contains(@class,'search-result__result-link')]")
            except:
                tmp_urls = []
            for i in range(len(tmp_names)):
                list_people_tmp[i]['url'] = tmp_urls[i].get_attribute('href')
            # bio
            try:
                tmp_bios = self.driver.find_elements_by_xpath("//li[contains(@class,'search-result')]//p[contains(@class,'subline-level-1')]")
            except:
                tmp_bios = []
            for i in range(len(tmp_bios)):
                list_people_tmp[i]['bio'] = tmp_bios[i].text
            # location
            try:
                tmp_locations = self.driver.find_elements_by_xpath("//li[contains(@class,'search-result')]//p[contains(@class,'subline-level-2')]")
            except:
                tmp_locations = []
            for i in range(len(tmp_locations)):
                list_people_tmp[i]['location'] = tmp_locations[i].text
            while list_people_tmp.count({}):
                list_people_tmp.remove({})
            n_page += 1
            list_people += list_people_tmp
            # next page status
            try:
                tmp_next = self.driver.find_element_by_xpath("//artdeco-pagination/button[contains(@class,'artdeco-pagination__button--next')]").get_attribute('disabled')
            except:
                tmp_next = None
            if tmp_next != None:
                cont = False
        return list_people

if __name__ == "__main__":
    p = {}
    p['email'] = "MyEmail"
    p['password'] = "MyPassword"
    p['driver'] = 'firefox'
    ls = LinkedInScrapper(p)
    ls.signIn()
    l = ls.getCompany('facebook')
    print(l)
    ls.signOut()

