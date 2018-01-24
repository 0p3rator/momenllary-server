
from datetime import datetime 

time1Num = 1512115213007

local_str_time = datetime.fromtimestamp(time1Num / 1000.0).strftime('%Y-%m-%d-%H-%M-%S')
location = 'B9-' + local_str_time + '/keyframes/' + str(time1Num) + '.jpg'
print location 
