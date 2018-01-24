from transforms3d.euler import quat2euler
import numpy as np
q = [0.519896071194186, 0.490301370069116, -0.507149687341035, 0.481779862899114] # 180 degree rotation around axis 0
angle = quat2euler(q)

print angle