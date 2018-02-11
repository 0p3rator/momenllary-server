import osmapi.utils.http as http

import conf.conf as config

head = '<?xml version="1.0" encoding="UTF-8"?>'
def queryChangeSet(changeSetNum):
    (resp, content) = http.doHttpRequest("query changeset data", config.api_host+config.api_query_changeset.format(changeSetNum),"GET")
    content = content.replace(head,"")
    return content


if __name__ == "__main__":
    queryChangeSet(2)