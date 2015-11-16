from MalwrAPI import MalwrAPI

# Unauthenticated way, verbose mode ON
api_unauthenticated = MalwrAPI(verbose=True)

print "\nRecent domains"
res = api_unauthenticated.get_recent_domains()
print res

print "\nPublic tags"
res = api_unauthenticated.get_public_tags()
print res

print "\nRecent Analysis"
res = api_unauthenticated.get_recent_analyses()
print res

print "\nLast comments"
res = api_unauthenticated.get_latest_comments()
print res

res = api_unauthenticated.submit_sample('/tmp/test.txt')
print res

# Use the API the authenticated way
api_authenticated = MalwrAPI(verbose=True, username='username', password='password')

res = api_authenticated.submit_sample(filepath='/tmp/waga.exe')
print res

res = api_authenticated.search(search_word='string:kali')
print res
