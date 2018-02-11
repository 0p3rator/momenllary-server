import conf.conf as config
import osmapi.utils.http as http


api_url=config.api_delete_element

headers = config.api_headers


def delete(type,id,elestr):
    elestr = "<osm>"+elestr+"</osm>"
    resp, content = http.doHttpRequest("delete "+type+" "+id+":", config.api_host+api_url.format(type,id), "DELETE",data=elestr, headers=headers)
    # content = content.replace(head,"")
    return content

if __name__ == "__main__":
    delete("node","7143",'''
    <node id="7143" changeset="103" timestamp="2018-01-25T11:48:55Z" version="1" visible="true" user="jingwei" uid="1" lat="39.8732509" lon="116.1809945">
<tag k="ele" v="63.6816170686"/>
<tag k="keypoints" v="(116.180998385 39.8732537349 64.5930167652,116.180990114 39.8732482313 64.5883342065,116.180998905 39.8732534789 62.7735912968,116.180990708 39.8732479685 62.771526006)"/>
<tag k="messageId" v="1516880713-232"/>
<tag k="momenta" v="board"/>
<tag k="tableInfo" v="boards"/>
<tag k="type" v="RECT"/>
</node>
''')