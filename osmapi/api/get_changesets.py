import osmapi.utils.http as http
import conf.conf as config

api_url=config.api_get_changesets

headers = config.api_headers

head = '<?xml version="1.0" encoding="UTF-8"?>'

def query():
    resp, content = http.doHttpRequest("get changesets :", config.api_host+api_url, "GET", headers=headers)
    content = content.replace(head,"")
    return content

if __name__ == "__main__":
    print(query())