import  xml.etree.ElementTree as ET


def loadXMLstr(xmlstr):
    return ET.fromstring(xmlstr)

def findAllByXPath(node,xpath,filter=None):
    findall = node.findall(xpath)
    if filter:
        fResult = []
        for one in findall:
            if filter(one):
                fResult.append(one)
        return fResult
    return findall

def findFirstByXpath(node,xpath):
    return findIndexNodeByXpath(node,xpath,0)

def findIndexNodeByXpath(node,xpath,index):
    nodes = findAllByXPath(node, xpath)
    if len(nodes) > index:
        return nodes[index]
    else:
        return None

def getNodeAttribValue(node,key):
    value = node.attrib[key]
    return value

def getTagNodeAttribValue(node,key):
    knode = findFirstByXpath(node, "tag[@k='{}']".format(key))
    if knode!=None:
        return getNodeAttribValue(knode,"v")
    return None
def addAttrib(node,attr,value):
    node.attrib[attr] = value

def toString(node):
    return ET.tostring(node)