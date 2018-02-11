import osmapi.utils.http as http

import conf.conf as config
def queryBox(left,bottom,right,top):
    (resp, content) = http.doHttpRequest("query box data", config.api_host+config.api_query_box.format(left,bottom,right,top),"GET")
    return content


if __name__ == "__main__":
    queryBox(116.48215,39.90162,116.48571,39.90240)