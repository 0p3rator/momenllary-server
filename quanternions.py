from transforms3d import euler 
from transforms3d.quaternions import quat2mat
import numpy as np
q = [-0.471996167401817, -0.480949615504513, -0.520430258417663, 0.524461086666478] # 180 degree rotation around axis 0
#q = [ 0.530519,0.483431, -0.493598, 0.491127]

matConvert = np.array([1, 0, 0, 0, 0, 1, 0, -1, 0]).reshape(3,3)

matTemp = quat2mat(q)
matTemp = matConvert.dot(matTemp)
print matTemp
# euler1 = euler.mat2euler(mat_temp,"sxyz")
# print mat_temp
# print euler1[2] * 57.3

# angle = euler.quat2euler(q,'szyx')
# # mat = quat2mat(q)
# # print mat
# # print angle
# print angle[2] * 57.3