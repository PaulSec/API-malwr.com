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
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0'
}

class MalwrAPI(object):

    """
        MalwrAPI Main Handler
    """
    session = None
    logged = False
    verbose = False

    def __init__(self, verbose=False, username=None, password=None):
        self.verbose = verbose
        # Authenticate and store the session
        self.session = requests.session()
        if (username and password):
            s = self.session
            req = s.get("https://malwr.com/account/login/", headers=headers)
            soup = BeautifulSoup(req.content)
            csrf_input = soup.find(attrs = dict(name = 'csrfmiddlewaretoken'))
            csrf_token = csrf_input['value']
            payload = {'csrfmiddlewaretoken': csrf_token, 'username' : u'{0}'.format(username), 'password': u'{0}'.format(password)}
            login_request = s.post("https://malwr.com/account/login/",data=payload,headers=headers)
            if (login_request.status_code == 200):
                self.logged = True
            else:
                self.logged = False
                print "Not being able to log you"

    def display_message(self, s):
        if (self.verbose):
            print '[verbose] %s' % s

    def get_latest_comments(self):
        res = []
        req = self.session.get(url, headers=headers)
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
        req = self.session.get(url, headers=headers)
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
        req = self.session.get(url, headers=headers)
        soup = BeautifulSoup(req.content, "html.parser")

        tags = soup.findAll('div', {'class': 'span6'})[2]
        for tag in tags.findAll('a', {'class': 'tag-label'}):
            res.append(tag.string)
        return res

    def get_recent_analyses(self):
        res = []
        req = self.session.get(url, headers=headers)
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

    def submit_sample(self, filepath, analyze=True, share=True, private=True):
        s = self.session
        req = s.get(url + '/submission/', headers=headers)
        
        soup = BeautifulSoup(req.content, "html.parser")
        math_captcha_question = soup.find('input', {'name': 'math_captcha_question'})['value']

        pattern = '(\d [-+*] \d) ='
        data = {
            'math_captcha_field': eval(re.findall(pattern, req.content)[0]),
            'math_captcha_question': soup.find('input', {'name': 'math_captcha_question'})['value'],
            'csrfmiddlewaretoken': soup.find('input', {'name': 'csrfmiddlewaretoken'})['value'],
            'share': 'on' if share else 'off', # share by default
            'analyze': 'on' if analyze else 'off', # analyze by default
            'private': 'on' if private else 'off' # private by default
        }

        req = s.post(url + '/submission/', data=data, headers=headers, files={'sample': open(filepath, 'rb')})
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
            elif ('file like this waiting for processing, submission aborted.' in req.content):
                self.display_message('File already submitted, check on the site')
                return None
            else:
                self.display_message('Error with the file %s' % filepath)
                return None
        return res

    def search(self, search_word):
        res = []
        if (self.logged):
            s = self.session
            search_url = url + '/analysis/search/'
            cnt = s.get(search_url,data="",headers=headers)
            c = BeautifulSoup(cnt.content)
            csrf_input = c.find(attrs = dict(name = 'csrfmiddlewaretoken'))
            csrf_token = csrf_input['value']
            payload = {'csrfmiddlewaretoken': csrf_token, 'search':u'{}'.format(search_word)}
            sc = s.post(search_url,data=payload,headers=headers)
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
