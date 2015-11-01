from MalwrAPI import MalwrAPI

res = MalwrAPI({'verbose': True}).get_recent_domains()
print res 

res = MalwrAPI({'verbose': True}).get_public_tags()
print res 

res = MalwrAPI({'verbose': True}).get_recent_analyses()
print res 

res = MalwrAPI({'verbose': True}).get_latest_comments()
print res 

res = MalwrAPI({'verbose': True}).submit_sample('/tmp/test.txt')
print res

res=MalwrAPI({'verbose': True}).search(LOGIN_MALWR,PASSWORD_MALWR,WORD_TO_SEARCH)
print res
