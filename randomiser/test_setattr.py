import bpy

bpy.data.scenes["Scene"].socket_props_per_UD.collection[0].min_int_1d[0]
selfie = bpy.data.scenes["Scene"].socket_props_per_UD.collection[0]
min_blend = selfie.min_int_1d[0]

m_str = "int_1d"
print("min_blend value", min_blend)
print("min_blend type ==== ", type(min_blend))

getattr_val = getattr(selfie, "min_" + m_str)
print(getattr_val)
print("gettr_val type ==== ", type(getattr_val))
print(getattr_val[0])
print("getattr_val[0] type ===== ", type(getattr_val[0]))


# try:
#     setattr(
#         selfie,
#         "min_" + m_str,
#         min_blend,
#     )
#     print("min_blend WORKING!!!!!!! type = ", type(min_blend))
# except:
#     print("min_blend NOT WORKING--- type = ", type(min_blend))
# try:
#     setattr(
#         selfie,
#         "min_" + m_str,
#         getattr_val,
#     )
#     print("getattr_val WORKING!!!!!!!!!!!! type = ", type(getattr_val))
# except:
#     print("getattr_val NOT WORKING--- type = ", type(getattr_val))


# try:
#     setattr(
#         selfie,
#         "min_" + m_str,
#         getattr_val[0],
#     )
#     print("getattr_val[0] WORKING!!!!!!! type = ", type(getattr_val[0]))
# except:
#     print("getattr_val[0] NOT WORKING--- type = ", type(getattr_val[0]))
