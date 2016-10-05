Python API for malwr.com 
========


Usage 
========

You can check ```API_example.py``` for advanced usage.

Import the class: 

```python
from MalwrAPI import MalwrAPI
```

Then, here are the different features: 

Submit a sample
=======

```python
res = MalwrAPI(True).submit_sample('/tmp/test.txt')
print res
```

Submit an entire folder
=======

```python
res = api_unauthenticated.submit_folder('/tmp/malware/')
print res
```

Get recent domains
=======

```python
res = MalwrAPI(True).get_recent_domains()
print res 
```

Get public tags
=======

```python
res = MalwrAPI(True).get_public_tags()
print res 
```

Get recent analyses
=======

```python
res = MalwrAPI(True).get_recent_analyses()
print res 
```

Get latest comments
=======

```python
res = MalwrAPI(True).get_latest_comments()
print res 
```

Get search results
=======

```python
res = MalwrAPI(True, "LOGIN_TO_MALWR.COM","PASSWORD_TO_MALWR.COM").search("STRING_TO_SEARCH")
print res 
```

Get Sample report
=======

```python
api = MalwrAPI(True, "LOGIN_TO_MALWR.COM","PASSWORD_TO_MALWR.COM")
report = api.getReport("/analysis/path/")
print(report)
>>> {"IP": ["192.168.1.1"], "Domain":["google.com"]}
```

This can be used with the `search` function to provide a nice little search-and-retrieve.

```python
api = MalwrAPI(True, "LOGIN_TO_MALWR.COM","PASSWORD_TO_MALWR.COM")
search = api.search("google.com")
for search_result in search:
    this_report = api.getReport(search_result["submission_url"])
```

Improvements
=======

So far, the API is pretty basic and submit files anonymously (not linked to your account). 
Next steps are: authentication on malwr.com, add search feature. 


Contributing
=======

Code was just a quick and dirty PoC, feel free to open issues, contribute and submit your Pull Requests. 
You can also ping me on Twitter (@PaulWebSec)
