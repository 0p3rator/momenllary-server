import os
os.sys.path.append(os.getcwd())
print os.getcwd()

import osmapi.utils.dataHandler as handler



def queryBasicInfo(basic_info_id):
    return handler.getBasic_Info(basic_info_id,{})


if __name__ =="__main__":
    print queryBasicInfo("B5_1512113412799.jpg")