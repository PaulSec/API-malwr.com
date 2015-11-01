"""
This is the (unofficial) Python API for malwr.com Website.
Using this code, you can retrieve recent analyses, domains, tags but also latest comments.
You can also submit files

"""
import requests
import re
from bs4 import BeautifulSoup
import hashlib

url = "https://malwr.com"

class MalwrAPI(object):

    """
        MalwrAPI Main Handler
    """

    _instance = None
    _verbose = False

    def __init__(self, arg=None):
        pass

    def __new__(cls, *args, **kwargs):
        """
            __new__ builtin
        """
        if not cls._instance:
            cls._instance = super(MalwrAPI, cls).__new__(
                cls, *args, **kwargs)
            if (args and args[0] and args[0]['verbose']):
                cls._verbose = True
        return cls._instance

    def display_message(self, s):
        if (self._verbose):
            print '[verbose] %s' % s

    def get_latest_comments(self):
        res = []
        req = requests.get(url)
        soup = BeautifulSoup(req.content, "html.parser")

        comments = soup.findAll('div', {'class': 'span6'})[3]
        for comment in comments.findAll('tr'):
            infos = comment.findAll('td')

            infos_to_add = {}
            infos_to_add['comment'] = infos[0].string
            infos_to_add['comment_url'] = infos[1].find('a')['href']
            res.append(infos_to_add)
        return res

    def get_recent_domains(self):
        res = []
        req = requests.get(url)
        soup = BeautifulSoup(req.content, "html.parser")

        domains = soup.findAll('div', {'class': 'span6'})[1]
        for domain in domains.findAll('tr'):
            infos = domain.findAll('td')

            infos_to_add = {}
            infos_to_add['domain_name'] = infos[0].find('span').string
            infos_to_add['url_analysis'] = infos[1].find('a')['href']
            res.append(infos_to_add)
        return res

    def get_public_tags(self):
        res = []
        req = requests.get(url)
        soup = BeautifulSoup(req.content, "html.parser")

        tags = soup.findAll('div', {'class': 'span6'})[2]
        for tag in tags.findAll('a', {'class': 'tag-label'}):
            res.append(tag.string)
        return res

    def get_recent_analyses(self):
        res = []
        req = requests.get(url)
        soup = BeautifulSoup(req.content, "html.parser")

        submissions = soup.findAll('div', {'class': 'span6'})[0]
        for submission in submissions.findAll('tr'):
            infos = submission.findAll('td')

            infos_to_add = {}
            infos_to_add['submission_time'] = infos[0].string
            infos_to_add['hash'] = infos[1].find('a').string
            infos_to_add['submission_url'] = infos[1].find('a')['href']
            res.append(infos_to_add)
        return res

    def submit_sample(self, filepath):
        s = requests.session()
        req = s.get(url + '/submission/')
        
        soup = BeautifulSoup(req.content, "html.parser")
        math_captcha_question = soup.find('input', {'name': 'math_captcha_question'})['value']

        pattern = '(\d [-+*] \d) ='
        data = {
            'math_captcha_field': eval(re.findall(pattern, req.content)[0]),
            'math_captcha_question': soup.find('input', {'name': 'math_captcha_question'})['value'],
            'csrfmiddlewaretoken': soup.find('input', {'name': 'csrfmiddlewaretoken'})['value'],
            'share': 'on', # share by default
            'analyze': 'on', # analyze by default
        }

        req = s.post(url + '/submission/', data=data, files={'sample': open(filepath, 'rb')})
        soup = BeautifulSoup(req.content, "html.parser")

        # regex to check if the file was already submitted before
        pattern = '(\/analysis\/[a-zA-Z0-9]{12,}\/)'
        submission_links = re.findall(pattern, req.content)

        res = {}
        res['md5'] = hashlib.md5(open(filepath, 'rb').read()).hexdigest()
        res['file'] = filepath

        if (len(submission_links) > 0):
            self.display_message('File %s was already submitted, taking last analysis' % filepath)
            res['analysis_link'] = submission_links[0]
        else:
            pattern = '(\/submission\/status\/[a-zA-Z0-9]{12,}\/)'
            submission_status = re.findall(pattern, req.content)
            if (len(submission_status) > 0):
                res['analysis_link'] = submission_status[0]
            else:
                self.display_message('Error with the file %s' % filepath)
                return None
        return res

    def search(self,login,password,search_word):
        res = []
        s = requests.Session()
        req = s.get("https://malwr.com/account/login/")
        soup = BeautifulSoup(req.content)
        csrf_input = soup.find(attrs = dict(name = 'csrfmiddlewaretoken'))
        csrf_token = csrf_input['value']
        payload = {'csrfmiddlewaretoken': csrf_token, 'username' : u'{0}'.format(login), 'password': u'{0}'.format(password)}
        logged = s.post("https://malwr.com/account/login/",data=payload,headers=dict(Referer="https://malwr.com/account/login/"))
        l=""
        cnt = s.get("https://malwr.com/analysis/search/",data=l,headers=dict(Referer="https://malwr.com/account/login/"))
        c = BeautifulSoup(cnt.content)
        csrf_input = c.find(attrs = dict(name = 'csrfmiddlewaretoken'))
        csrf_token = csrf_input['value']
        payload = {'csrfmiddlewaretoken': csrf_token, 'search':u'{}'.format(search_word)}
        sc = s.post("https://malwr.com/analysis/search/",data=payload,headers=dict(Referer="https://malwr.com/analysis/search"))
        ssc = BeautifulSoup(sc.content)
        res=[]
        submissions = ssc.findAll('div', {'class': 'box-content'})[0]
        sub = submissions.findAll('tbody')[0]
        for submission in sub.findAll('tr'):
            infos = submission.findAll('td')
            infos_to_add = {}
            infos_to_add['submission_time'] = infos[0].string
            infos_to_add['hash'] = infos[1].find('a').string
            infos_to_add['submission_url'] = infos[1].find('a')['href']
            infos_to_add['file_name'] = infos[2].string
            res.append(infos_to_add)
        return res
