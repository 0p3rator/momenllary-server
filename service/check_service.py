# -*- coding: UTF-8 -*-
import time
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
sys.path.append("..")
from mycolorlog import UseStyle
from sql.postgresql import PostgreSql
import jwt

def check_login(request):
    auth_token = request.cookies.get("M_Auth_Token")
    user = None
    if auth_token is None:
        raise Exception('No cookie')
    try:
        payload = jwt.decode(auth_token, 'ucenter', algorithms=['HS512'])
        if not payload:
            raise Exception('Illegel User')
        else:
            user = payload['sub']
    except:
        raise
    return user

class CheckService():
    def __init__(self):
        self.__psql = PostgreSql()

    def __extract_loc(self, position):
        indexstart = position.find('(')
        indexend = position.find(')')
        loc = position[indexstart+1:indexend]
        loc = loc.split(' ')[:2]
        return loc

    def upload_check_result(self,request):
        user = None
        try:
            user = check_login(request)
            print user
        except Exception as e:
            print 'Exception', e
            return {'result': 'Login Fail'} 
        finally:
            if user is None:
                return {'result': 'Login Fail'}      
        requestValues = request.values
        frameId = requestValues.get('image_key')
        packetName = requestValues.get('packetName')
        photoResult = requestValues.get('photoResult')
        detectionResult = requestValues.get('detectionResult')
        spslamResult = requestValues.get('spslamResult')
        commentResult =  requestValues.get('commentResult')
        check_time = time .strftime('%Y-%m-%d %H:%M:%S')

        sql = """insert into human_check (keyframe_id, packet_name, photo_result, detection_result, spslam_result, \
            check_time, user_name, work_order, comment ) values ({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', \
            '{}') returning id""".format(frameId, packetName, photoResult, detectionResult,
            spslamResult, check_time, user, 'test', commentResult)
        print sql
        self.__psql.execute(sql)
        return {'result' : 'OK'}

    def get_check_result(self, packetName, request):
        user = None

        try:
            user = check_login(request)
        except Exception as e:
            print e
            return {'result': 'Login Fail'} 
        finally:
            if user is None:
                return {'result': 'Login Fail'} 
        packetName = packetName
        sql = """select human_check.keyframe_id, human_check.photo_result, human_check.detection_result, \
        human_check.spslam_result, human_check.comment, ST_AsText(keyframes.geom) \
        from human_check left join keyframes on (human_check.keyframe_id = keyframes.id) \
            where human_check.packet_name = '{}' and human_check.user_name = '{}'""".format(packetName, user)
        print sql
        rows = None
        try:
            rows = self.__psql.execute(sql)
        except Exception as e:  
            raise
        result = {}
        for row in rows:
            result[row[0]] = {
                'commentResult': row[4],
                'photoResult' : row[1],
                'detectionResult': row[2],
                'spslamResult': row[3],
                'loc' : self.__extract_loc(row[5])
            }
        return result


if __name__ == '__main__':
    checkService = CheckService()
    print checkService.get_check_result('B6-2018-02-24-13-30-05','')