import os
os.sys.path.append(os.getcwd())
print os.getcwd()

import osmapi.utils.dataHandler as handler


def queryFrame(basic_info_id,timestamp):
    return handler.getFrameInfo(basic_info_id,timestamp,{})

def queryFrames(basic_info_id,timestamps):
    result = []
    for timestamp in timestamps:
        result.append(queryFrame(basic_info_id,timestamp))
    return result