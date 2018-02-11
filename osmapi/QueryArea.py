import os
os.sys.path.append(os.getcwd())
print os.getcwd()
import json

import  xml.etree.ElementTree as ET
import osmapi.api.query_box as querybox
import osmapi.utils.dataHandler as handler


def queryArea(left,bottom,right,top):
    data = querybox.queryBox(left,bottom,right,top)
    etree = ET.fromstring(data)
    handler.createConnection()
    poles,boards =  handler.dealWithNode(etree.findall("node"))
    ways = handler.dealWithWay(etree.findall("way"))
    handler.dealWithRelation(etree.findall("relation"))
    handler.closeConncetion()
    return {"boards":boards}
    return {"poles":poles, "boards":boards, "lane_lines":ways}


if __name__ =="__main__":
    print json.dumps(queryArea(116.630, 40.273, 116.635, 40.275))




