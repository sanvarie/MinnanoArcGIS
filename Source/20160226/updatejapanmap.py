# -*- coding: utf-8 -*-
import arcpy
import pandas as pd

#日本地図のShape
inFeatures = "D:\python\soccer\japan_ver80.shp"

#更新するフィーチャクラスがあるgdb
arcpy.env.workspace = "C:\ArcPySample\ArcPyJapan.gdb"

field_list = []
for field in arcpy.ListFields(inFeatures):
    if field.type != "Geometry":
        field_list.append(field.name)

df = pd.DataFrame(arcpy.da.FeatureClassToNumPyArray(inFeatures,field_list,null_value=-9999))

#グルーピング
df_group = df.groupby('KEN')['P_NUM','H_NUM'].sum()

for key,row in df_group.iterrows():
    cursorJ = arcpy.UpdateCursor("Japan")
    for rowJ in cursorJ:
        if key == rowJ.KEN:
            rowJ.setValue("P_NUM", row.P_NUM)
            rowJ.setValue("H_NUM", row.H_NUM)
            cursorJ.updateRow(rowJ)