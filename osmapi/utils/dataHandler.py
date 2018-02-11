#coding:utf-8
import  xml.etree.ElementTree as ET
import json as json
import numpy as np
import zlib
from tqdm import tqdm
import osmapi.utils.DBAccess as db
##################-----this file write for query Area------##########################
connection =None
# cur = connection.cursor();
# cur.execute("SELECT gid,adaid,meshid,featcode,length,geom FROM boundary")
big_rang = 10000
base_info_map = {}

def _checkIsBoardNode(node):
    tag = node.find("tag[@v='boards']")
    return tag!=None

def _getNodeAttrib(node,param):
    return node.attrib[param]

def _getTagValue(node,param):
        tag = node.find("tag[@k='" + param + "']")
        if tag == None:
            return None
        return tag.attrib['v']

def _fillTagValues(result,node,tags):
    tags = tags.replace(" ","")
    for tag in tags.split(","):
        result[tag] = _getTagValue(node,tag)

def _queryValue(query):
    cur = connection.cursor()
    cur.execute(query)
    result = cur.fetchone()
    cur.close()
    return result
def _getBaseINFOCar(basic_info_id):
    if not hasattr(base_info_map,basic_info_id):
        query = "select car_id from basic_info WHERE id = '{}'".format(basic_info_id)
        value = _queryValue(query)
        base_info_map[basic_info_id]=value[0]
    return base_info_map[basic_info_id]

def getFrameInfo(basic_info_id,timestamp,result={}):
    try:
        createConnection()
        id = basic_info_id + "_" + timestamp
        fields = "timeStamp_s, basic_info_id, altitude, latitude, longitude, prob, qw, qx, qy, qz "
        query = "select " + fields + " from frames WHERE id='{}'".format(id)
        values = _queryValue(query)
        fields = fields.replace(" ", "")
        index = 0
        for tag in fields.split(","):
            result[tag] = values[index]
            index += 1  # todo 转成json对象
        closeConncetion()
        return result
    except:
        print("sql error")
        exit()
        return {}

def _parseToJson(strvalue):
    value=None
    try:
        strvalue2 = strvalue.replace("'",'"')
        value = json.loads(strvalue2)
    except:
        print("error :: parse2Json  "+strvalue)
    finally:
        return value
# getFrameInfo("B0_1512540710303.jpg","1512541211030")
def _fillOneDBValues(result, fields, table, where):
    query = "select {} from {} where id='{}'".format(fields,table,where)
    values = _queryValue(query)
    if(values==None):
        print(query +" excute error")
        fields = fields.replace(" ", "")
        for tag in fields.split(","):
            result[tag] = None
        return
    # eval(fields+"=values")
    fields = fields.replace(" ", "")
    index =0
    for tag in fields.split(","):
        result[tag] = values[index]
        if tag =="observers" or tag == "feature":
            jsonValue = _parseToJson(values[index])
            if jsonValue:
                result[tag] = jsonValue
        index+=1#todo 转成json对象
    return result


def _doBoardNode(node):
    tags = 'type,tableInfo,messageId,keypoints,ele,merge_count'
    result = {}
    result["id"] = _getNodeAttrib(node,"id")
    result["changeset"] = _getNodeAttrib(node,"changeset")
    result["version"] = _getNodeAttrib(node,"version")
    _fillTagValues(result,node,tags)
    fields = 'basic_info_id,prob,type,complete_number,feature,observers'
    table = "boards"
    where  = _getTagValue(node,"messageId")
    observers = []
    result["observers"] = observers
    observers.append(_fillOneDBValues({}, fields, table, where))
    messageIds = []
    messageIds.append(where)
    for i in np.arange(1, big_rang):
        where = _getTagValue(node, "messageId" + i.__str__())
        if where == None:
            break
        observers.append(_fillOneDBValues({}, fields, table, where))
        messageIds.append(where)
    result["messageIds"]=messageIds
    return result


def _checkIsPoleNode(node):
    tag = node.find("tag[@v='poles']")
    return tag!=None


def _doPoleNode(node):
    tags = 'type,tableInfo,messageId,geom,momenta,ele,merge_count'
    result = {}
    result["id"] = _getNodeAttrib(node,"id")
    result["changeset"] = _getNodeAttrib(node,"changeset")
    result["version"] = _getNodeAttrib(node,"version")
    _fillTagValues(result,node,tags)
    fields = 'basic_info_id,  prob, type, observers'
    table = "poles"
    where  = _getTagValue(node,"messageId")
    messageIds = []
    messageIds.append(where)
    observers = []
    result["observers"] = observers
    observers.append(_fillOneDBValues({}, fields, table, where))
    for i in np.arange(1,big_rang):
        where = _getTagValue(node, "messageId"+i.__str__())
        if where == None:
            break
        messageIds.append(where)
        observers.append(_fillOneDBValues({}, fields, table, where))
    result["messageIds"]=messageIds
    return result


def _checkIsMomenta(node):
    tags = node.find("tag[@k='tableInfo']")
    #todo rm visible=false
    visible = _getNodeAttrib(node,"visible")
    return tags!=None and visible == "true"

def _checkIsMomentaWay(way):
    tags = way.find("tag[@v='lane_lines']")
    return tags!=None

def createConnection():
    global connection
    connection = db.createConnection();

def dealWithNode(nodes):
    poles = []
    boards = []
    for node in nodes:
        if _checkIsMomenta(node):
            if _checkIsBoardNode(node):
                boards.append(_doBoardNode(node))
            elif _checkIsPoleNode(node):
                poles.append(_doPoleNode(node))
    return poles,boards

def _dealWithSegment(value):
    value = value.replace('h','"h"')
    value = value.replace('p','"p"')
    value = value.replace('w','"W"')
    return value

def _fillTagSegs_parameters(result, way, param):
    try:
        arr = []
        for i in np.arange(1,big_rang):
            key = param + i.__str__()
            value = _getTagValue(way, key)
            if value=="split":
                str1 = _getTagValue(way, key+"-part1")
                str2 = _getTagValue(way, key+"-part2")
                value = str1+str2
            if value!=None:
                parasss = _dealWithSegment(value)
                # print(parasss)
                arr.append(_parseToJson(parasss))
                # arr.append(_parseToJson(zlib.decompress(value)))
            else:
                result[param]=arr
                return
    finally:
        return


def _doWayNode(way):

    tags = 'type,tableInfo,messageId,offset,merge_count'
    result = {}
    result["id"] = _getNodeAttrib(way,"id")
    result["changeset"] = _getNodeAttrib(way,"changeset")
    result["version"] = _getNodeAttrib(way,"version")
    _fillTagValues(result,way,tags)
    _fillTagSegs_parameters(result,way,"segs_parameters");

    where  = _getTagValue(way,"messageId")
    messageIds = []
    messageIds.append(where)
    for i in np.arange(1,big_rang):
        where = _getTagValue(way, "messageId"+i.__str__())
        if where == None:
            break
        messageIds.append(where)
    result["messageIds"]=messageIds
    # fields = 'basic_info_id,prob,type,complete_number,feature,observers'
    # table = "boards"
    # where  = _getTagValue(node,"messageId")
    # _fillDBValues(result,fields,table,where)
    return result


def dealWithWay(ways):
    wayresult = []
    for way in ways:
        if _checkIsMomenta(way):
            wayresult.append(_doWayNode(way))
    return wayresult


def dealWithRelation(relations):
    return None

def closeConncetion():
    db.closeConnection(connection)



def getBasic_Info(basic_info_id,result={}):
    try:
        createConnection()
        fields = 'id,car_id,center_altitude,center_latitude,center_longtitude,center_x,center_y,center_z,fx,fy,cx,cy,start_timeStamp_s'
        query = "select " + fields + " from basic_info WHERE id='{}'".format(basic_info_id)
        values = _queryValue(query)
        fields = fields.replace(" ", "")
        index = 0
        for tag in fields.split(","):
            result[tag] = values[index]
            index += 1  # todo 转成json对象
        closeConncetion()
        return result
    except:
        print("sql error")
        return {}