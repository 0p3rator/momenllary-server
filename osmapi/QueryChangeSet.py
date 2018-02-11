import  xml.etree.ElementTree as ET
import osmapi.api.query_changeset as changeset
import osmapi.utils.dataHandler as handler

def queryArea(changeSetNum):
    data = changeset.queryChangeSet(changeSetNum)
    etree = ET.fromstring(data)
    handler.createConnection()
    poles,boards =  handler.dealWithNode(etree.findall("create/node"))
    ways = handler.dealWithWay(etree.findall("create/way"))
    handler.dealWithRelation(etree.findall("create/relation"))
    handler.closeConncetion()
    return {"poles":poles,"boards":boards,"lane_lines":ways}

if __name__ =="__main__":
    queryArea(211)




