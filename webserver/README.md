Requirement  
https://pypi.org/project/python-a2s/

Note: webserver seems to be blocking multiple connection access and is maybe not multithreaded. Observation from the JavaScript side/browser client.


Latest: webserver-fetch-rewrite.py  
Bug/issue: The in-browser time simulation does not work here, as the fetches are very constant and overwrite the ticking.
