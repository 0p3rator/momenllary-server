from transforms3d.euler import quat2euler
from transforms3d.quaternions import quat2mat
from transforms3d.euler import mat2euler
import numpy as np

if __name__ == '__main__':
    quanternion = [0.691628016517772, -0.0121321190746634, 0.00552576806824856, 0.722130849875357] 
    matTemp = quat2mat(quanternion)
    eulerTemp = mat2euler(matTemp,"sxyz")
    ca = eulerTemp[2] * 57.3
    ca1 = quat2euler(quanternion, 'sxyz')
    print 'ca1:', ca1[2] * 57.3
    print ca

