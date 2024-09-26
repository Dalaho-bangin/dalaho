from core.utils import requester
import re

ce=0
def check_response(request):
    c+=1
    print(ce)
    response = requester(request)
    if type(response) != str and response.status_code in (400, 413, 418, 429, 503):
        return False
    if type(response) ==str:
        return False

    value='dalaho'
    if value in response.text and re.search(r'[\'"\s]%s[\'"\s]' % value, response.text):
        return True

        
