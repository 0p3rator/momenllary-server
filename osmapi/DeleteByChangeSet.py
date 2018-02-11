import osmapi.api.query_changeset as queryAll
import osmapi.utils.XMLHandler as xmlHandler
import osmapi.api.delete_element as deleteEle
import trans.file.OSMFile as osmFile
import os
getcwd = os.getcwd()
split = getcwd.split("map_osmid_api")
cwd = split[0]
def delete(changeSetNum,isDeleteNode=True,isDeleteWay=True,isDeleteRelation=True):
    content = queryAll.queryChangeSet(changeSetNum)
    node = xmlHandler.loadXMLstr(content)
    lis = []
    if isDeleteNode: lis.append("node")
    if isDeleteWay: lis.append("way")
    if isDeleteRelation: lis.append("relation")
    for type in lis:
        eles = xmlHandler.findAllByXPath(node, "create/{}".format(type))
        for ele in eles:
            id = xmlHandler.getNodeAttribValue(ele,"id")
            elestr = xmlHandler.toString(ele)
            deleteEle.delete(type,id,elestr)

def deleteByOsmChange(changeSetNum,isDeleteNode=True,isDeleteWay=True,isDeleteRelation=True):
    content = queryAll.queryChangeSet(changeSetNum)
    node = xmlHandler.loadXMLstr(content)
    lis = []
    if isDeleteWay: lis.append("way")
    if isDeleteNode: lis.append("node")
    if isDeleteRelation: lis.append("relation")
    for type in lis:
        fileOsm = osmFile.OSMFileAccess("./tmp/osm.osm")
        fileOsm.writeHead()
        eles = xmlHandler.findAllByXPath(node, "create/{}".format(type))
        for ele in eles:
            id = xmlHandler.getNodeAttribValue(ele,"id")
            xmlHandler.addAttrib(ele,"action","delete")
            elestr = xmlHandler.toString(ele)
            # print(elestr)
            # deleteEle.delete(type,id,elestr)
            fileOsm.writeLine(elestr)
            fileOsm.flush()
        fileOsm.writeFoot()
        fileOsm.close()
        os.system('python {}map_osmid_api/osmapi/utils/bulk_upload_sax.py -i ./tmp/osm.osm -u jingwei@momenta.ai -p zuojingwei -c "test commit"'.format(cwd))

# def deleteNode(fileCallback):
#     fileOsm = osmFile.OSMFileAccess("./tmp/osm.osm")
#     fileOsm.writeHead()
#     fileCallback(fileOsm)
#     fileOsm.flush()
#     fileOsm.writeFoot()
#     fileOsm.close()
#     os.system('python {}map_osmid_api/osmapi/utils/bulk_upload_sax.py -i ./tmp/osm.osm -u jingwei@momenta.ai -p zuojingwei -c "test commit"'.format(cwd))

if __name__ == "__main__":
    for i in range(549,576):
        try:
            deleteByOsmChange(i)
        except:
            print("error ",i)

    # delete(192)