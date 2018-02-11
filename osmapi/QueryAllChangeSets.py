import osmapi.api.get_changesets as queryApi
import osmapi.utils.XMLHandler as xmlHandler

def query(attrs=[],tagKeys=[],filter=None):
    result = queryApi.query()
    out = {}
    osmNode = xmlHandler.loadXMLstr(result)
    results = xmlHandler.findAllByXPath(osmNode, "changeset", filter)
    for onechange in results:
        id =  xmlHandler.getNodeAttribValue(onechange,"id")
        oneout = {}
        for att in attrs:
            oneout[att] = xmlHandler.getNodeAttribValue(onechange,att)
        for tagKey in tagKeys:
            oneout[tagKey] = xmlHandler.getTagNodeAttribValue(onechange,tagKey)
        out[id] = oneout
    return out

if __name__ == "__main__":
    def filter(node):
        return True #xmlHandler.getNodeAttribValue(node,"open")=="true"

    query(attrs=["id","user","created_at"],tagKeys=["acomment"],filter=filter)
    print(query(attrs=["id"],filter=filter))