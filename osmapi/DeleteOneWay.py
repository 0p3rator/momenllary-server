import osmapi.api.query_changeset as queryAll
import osmapi.utils.XMLHandler as xmlHandler

def __queryNodeIds(node, wayId):
    eles = xmlHandler.findAllByXPath(node, "create/way[@id='{}']".format(wayId))
    nodeIds = {}
    wayStr = ""
    for el in eles:
	xmlHandler.addAttrib(el, "action", "delete")
        wayStr += xmlHandler.toString(el)
        nds =  xmlHandler.findAllByXPath(el,"nd")
        for nd in nds:
            value = xmlHandler.getNodeAttribValue(nd, "ref")
            nodeIds[value] = value
    return nodeIds,wayStr

def __filterByNodeID(nodeIds):
    def filter(node):
        id = xmlHandler.getNodeAttribValue(node, "id")
        if id in nodeIds:
            return True
        return False
    return filter

def deleteNodeElement(changeSetNum,nodeId):
    content = queryAll.queryChangeSet(changeSetNum)
    node = xmlHandler.loadXMLstr(content)
    result = ""
    nodeIds = {}
    nodeIds[nodeId] = nodeId
    wayNodes = xmlHandler.findAllByXPath(node, "create/node", filter=__filterByNodeID(nodeIds))
    for ele in wayNodes:
        xmlHandler.addAttrib(ele, "action", "delete")
        elestr = xmlHandler.toString(ele)
        result += elestr
        # print(elestr)
        # deleteEle.delete(type,id,elestr)
    try:
        xmlHandler.loadXMLstr("<osm>"+result+"</osm>")
        # print("result ",result)
    except:
        print("parse error delete way id:{}  changeSet:{}".format(wayId,changeSet))
        result = ""
    return result

def deleteWayNode(changeSetNum,wayId):
    content = queryAll.queryChangeSet(changeSetNum)
    node = xmlHandler.loadXMLstr(content)
    result = ""
    nodeIDs,wayStr = __queryNodeIds(node, wayId)
    result += wayStr
    wayNodes = xmlHandler.findAllByXPath(node, "create/node", filter=__filterByNodeID(nodeIDs))
    for ele in wayNodes:
        xmlHandler.addAttrib(ele, "action", "delete")
        elestr = xmlHandler.toString(ele)
        result += elestr
        # print(elestr)
        # deleteEle.delete(type,id,elestr)
    try:
        xmlHandler.loadXMLstr("<osm>"+result+"</osm>")
    except:
        print("parse error delete way id:{}  changeSet:{}".format(wayId,changeSet))
        result = ""
    return result


if __name__ == "__main__":
    print deleteWayNode(1498,"6318")
