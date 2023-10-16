from array import array

import bpy
import numpy as np

selfie = bpy.data.scenes["Scene"].socket_props_per_UD.collection[0]
m_str = "int_1d"

min_int_np = np.int64(1)
max_int_np = np.int64(3)

print("min_int_np = ", min_int_np)

min_int_blender = int(min_int_np)
print("min_int_blender = ", min_int_blender)

# min_array = getattr(self, "min_" + m_str)
# max_array = getattr(self, "max_" + m_str)
min_array = np.array(getattr(selfie, "min_" + m_str))
max_array = np.array(getattr(selfie, "max_" + m_str))

# print("MIN CLOSURE min_array ", type(min_array))
# MAX RECURSION DEPTH EXCEEDED WHILE CALLING A PYTHON OBJECT
# print("MIN CLOSURE max_array ", type(max_array))

# min_array = ast.literal_eval(str(min_array))
# max_array = ast.literal_eval(str(max_array))
# min_array = np.array(min_array)
# max_array = np.array(max_array)

# min_array = [pyt_int.item() for pyt_int in min_array]
# max_array = [pyt_int.item() for pyt_int in max_array]

# print("MIN CLOSURE min_array FIRST", type(min_array[0]))
# print("MIN CLOSURE max_array FIRST", type(max_array[0]))

# min_array = np.asarray(min_array,dtype="int")
# max_array = np.asarray(max_array,dtype="int")
min_array = array("i", min_array)
max_array = array("i", max_array)
# min_array = np.array(min_array)
# max_array = np.array(max_array)

# print("MIN CLOSURE min_array ", type(min_array))
# print("MIN CLOSURE max_array ", type(max_array))

# print("MIN CLOSURE min_array FIRST", type(min_array[0]))
# print("MIN CLOSURE max_array FIRST", type(max_array[0]))
print(min_array > max_array)

cond_min = [min > max for min, max in zip(min_array, max_array)]
# if (min_array > max_array).all():
if any(cond_min):
    cond = np.where(cond_min, max_array, min_array)
# print('np.where result = ', cond)
# print('np.where type = ', type(cond))
