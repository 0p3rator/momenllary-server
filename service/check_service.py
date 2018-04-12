# -*- coding: UTF-8 -*-

import time
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
sys.path.append("..")
from mycolorlog import UseStyle
from sql.postgresql import PostgreSql

class CheckService():
    def __init__(self):
        self.__psql = PostgreSql()

    def upload_check_result(self, request):
        requestValues = request.values
        frameId = requestValues.get('image_key')
        packetName = requestValues.get('packetName')
        photoResult = requestValues.get('photoResult')
        detectionResult = requestValues.get('detectionResult')
        spslamResult = requestValues.get('spslamResult')
        commentResult = requestValues.get('commentResult')
        check_time = time .strftime('%Y-%m-%d %H:%M:%S')

        sql = """insert into human_check (keyframe_id, packet_name, photo_result, detection_result, spslam_result, \
            check_time, user_name, work_order, comment ) values ({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', \
            '{}') returning id""".format(frameId, packetName, photoResult, detectionResult, 
            spslamResult, check_time, 'changyu', 'test', commentResult)
        print sql
        # checkResult = {
        # 'keyframe_id' : requestValues.get('id'),
        # 'photo_result' : requestValues.get('photoResult'),
        # 'detection_result' : requestValues.get('detectionResult'),
        # 'spslam_result' : requestValues.get('spslamResult'),
        # 'comment' : requestValues.get('commentResult'),
        # 'check_time' : time.strftime('%Y-%m-%d %H:%M:%S'),
        # }
        self.__psql.execute(sql)
        return {'result' : 'OK'}


if __name__ == '__main__':
    checkService = CheckService()
    checkService.upload_check_result('hello')