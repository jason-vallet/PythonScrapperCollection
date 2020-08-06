from selenium import webdriver
import time

class CrunchbaseScrapper:
    params = {'wait': 3}
    url_base = 'https://crunchbase.com/'

    def __init__(self, params = {}):
        self.setParams(params)
        self.__startDriver()

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

    def __startDriver(self):
        opt = webdriver.firefox.options.Options()
        opt.headless = True
        self.driver = webdriver.Firefox(options=opt)

    def __fetchOrganisation(self, name):
        return self.__fetchUrl('organization/' + name)

    def __fetchUrl(self, url_cpl):
        if url_cpl.startswith(self.url_base):
            full_url = str(url_cpl)
        else:
            full_url = self.url_base + str(url_cpl)
        try:
            self.driver.get(full_url)
        except:
            return False
        # try page availability
        return True

## Private methods
    def done(self):
        self.driver.close()

    def proof(self):
        self.driver.save_screenshot('screen.png')

    def __buildOrganisationOverview(self, organisation):
        try:
            overview = self.driver.find_element_by_xpath('.//section-layout[@id="section-overview"]')
        except:
            return organisation
        try:
            organisation['name'] = overview.find_element_by_xpath('.//image-with-text-card//blob-formatter/span').text
        except:
            organisation['name'] = ''
        try:
            organisation['short bio'] = overview.find_element_by_xpath('.//image-with-text-card//field-formatter/span').text
        except:
            organisation['short bio'] = ''
        try:
            organisation['location'] = overview.find_element_by_xpath('.//image-with-text-card//identifier-multi-formatter/span').text
        except:
            organisation['location'] = ''
        # get all the subinfo from table
        info = overview.find_elements_by_xpath('.//fields-card/div/span')
        i = 0
        while i < len(info):
            title = self.__cleanString(info[i].text.lower())
            if title == 'industries' or title == 'founders':
                tmp_list = []
                elems = info[i+1].find_elements_by_xpath('.//a')
                for el in elems:
                    tmp_list.append(self.__cleanString(el.text))
                organisation[title] = tmp_list
            elif title == 'website' or title == 'facebook' or title == 'linkedin' or title == 'twitter':
                try:
                    link = info[i+1].find_element_by_xpath('.//a').get_attribute('href')
                except:
                    link = ''
                organisation[title] = link
            else:
                organisation[title] = self.__cleanString(info[i+1].text)
            i += 2
        return organisation


    def __buildOrganisationInvestors(self, organisation):
        try:
            section = self.driver.find_element_by_xpath('.//section-layout[@id="section-investors"]')
        except:
            return organisation
        investors = {}
        values = section.find_elements_by_xpath('.//big-values-card//field-formatter/a[contains(@class, "field-type-integer")]')
        try:
            investors['nb lead'] = values[0].text
        except:
            investors['nb lead'] = ''
        try:
            investors['nb total'] = values[1].text
        except:
            investors['nb total'] = ''
        # get all the subinfo from table
        table = section.find_element_by_xpath('.//list-card/div/table')
        headers = table.find_elements_by_xpath('.//th//label-with-info//span[contains(@class, "label")]')
        rows = table.find_elements_by_xpath('.//tbody/tr')
        investors_list = []
        for row in rows:
            fields = row.find_elements_by_xpath('.//td')
            i = 0
            invest = {}
            while i < len(fields) and i < len(headers):
                invest[headers[i].text] = fields[i].text
                i += 1
            investors_list.append(invest)
        investors['last'] = investors_list
        organisation['investors'] = investors
        return organisation


    def __buildOrganisationFundingRounds(self, organisation):
        try:
            section = self.driver.find_element_by_xpath('.//section-layout[@id="section-funding-rounds"]')
        except:
            return organisation
        funding = {}
        try:
            funding['nb rounds'] = section.find_element_by_xpath('.//big-values-card//field-formatter/a[contains(@class, "field-type-integer")]').text
        except:
            funding['nb rounds'] = ''
        try:
            funding['amount'] = section.find_element_by_xpath('.//big-values-card//field-formatter/a[contains(@class, "field-type-money")]').text
        except:
            funding['amount'] = ''
        # get all the subinfo from table
        table = section.find_element_by_xpath('.//list-card/div/table')
        headers = table.find_elements_by_xpath('.//th//label-with-info//span[contains(@class, "label")]')
        rows = table.find_elements_by_xpath('.//tbody/tr')
        rounds = []
        for row in rows:
            fields = row.find_elements_by_xpath('.//td')
            i = 0
            rou = {}
            while i < len(fields) and i < len(headers):
                rou[headers[i].text] = fields[i].text
                i += 1
            rounds.append(rou)
        funding['last'] = rounds
        organisation['funding rounds'] = funding
        return organisation


    def __buildOrganisationAcquisitions(self, organisation):
        try:
            section = self.driver.find_element_by_xpath('.//section-layout[@id="section-acquisitions"]')
        except:
            return organisation
        acquisitions = {}
        try:
            acquisitions['nb'] = section.find_element_by_xpath('.//big-values-card//field-formatter/a[contains(@class, "field-type-integer")]').text
        except:
            acquisitions['nb'] = ''
        # get all the subinfo from table
        table = section.find_element_by_xpath('.//list-card/div/table')
        headers = table.find_elements_by_xpath('.//th//label-with-info//span[contains(@class, "label")]')
        rows = table.find_elements_by_xpath('.//tbody/tr')
        acquisitions_list = []
        for row in rows:
            fields = row.find_elements_by_xpath('.//td')
            i = 0
            acqu = {}
            while i < len(fields) and i < len(headers):
                acqu[headers[i].text] = fields[i].text
                i += 1
            acquisitions_list.append(acqu)
        acquisitions['last'] = acquisitions_list
        organisation['acquisitions'] = acquisitions
        return organisation


    def __buildOrganisationInvestments(self, organisation):
        try:
            section = self.driver.find_element_by_xpath('.//section-layout[@id="section-investments"]')
        except:
            return organisation
        investments = {}
        values = section.find_elements_by_xpath('.//big-values-card//field-formatter/a[contains(@class, "field-type-integer")]')
        try:
            investments['nb investments'] = values[0].text
        except:
            investments['nb investments'] = ''
        try:
            investments['nb leads'] = values[1].text
        except:
            investments['nb leads'] = ''
        # get all the subinfo from table
        table = section.find_element_by_xpath('.//list-card/div/table')
        headers = table.find_elements_by_xpath('.//th//label-with-info//span[contains(@class, "label")]')
        rows = table.find_elements_by_xpath('.//tbody/tr')
        investments_list = []
        for row in rows:
            fields = row.find_elements_by_xpath('.//td')
            i = 0
            invest = {}
            while i < len(fields) and i < len(headers):
                invest[headers[i].text] = fields[i].text
                i += 1
            investments_list.append(invest)
        investments['last'] = investments_list
        organisation['investments'] = investments
        return organisation
    
        

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
      Get organisation info
      @param string name: name of the organisation
      @return obj: the organisation info
    '''
    def getOrganisation(self, name):
        page = self.__fetchOrganisation(name)
        if not page:
            return None
        organisation = {}
        tmp = self.__buildOrganisationOverview(organisation)
        tmp = self.__buildOrganisationFundingRounds(tmp)
        tmp = self.__buildOrganisationInvestors(tmp)
        tmp = self.__buildOrganisationAcquisitions(tmp)
        tmp = self.__buildOrganisationInvestments(tmp)
        if tmp != {}:
            organisation = tmp
        return organisation


    def getFundingRounds(self, name):
        # https://www.crunchbase.com/search/funding_rounds/field/organizations/funding_total/facebook
        return None

    def getInvestors(self, name):
        return None

    def getInvestments(self, name):
        return None
        # https://www.crunchbase.com/search/funding_rounds/field/organizations/num_investments/facebook

    def getAcquisitions(self, name):
        # https://www.crunchbase.com/search/acquisitions/field/organizations/num_acquisitions/facebook
        return None

if __name__ == "__main__":
    cs = CrunchbaseScrapper()
    e = cs.getOrganisation('facebook')
    print(e)
    cs.done()
    
