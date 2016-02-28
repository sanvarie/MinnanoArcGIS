# -*- coding: utf-8 -*-
import arcpy
import pandas as pd

arcpy.env.workspace = "C:\ArcPySample\Soccer.gdb"

field_list = []
fields = arcpy.ListFields("HighShcool")
for field in fields:
    if field.type != "Geometry":
        field_list.append(field.name)

#属性テーブルをPandasに格納
column = arcpy.da.FeatureClassToNumPyArray("HighShcool",field_list,null_value=-9999)
df = pd.DataFrame(column)

#ポイントの集計
df_group = df.groupby('Name')['Point'].sum()

#ポイントの降順でソート
df_group.sort("Point",ascending=False)

cursor = arcpy.InsertCursor("HighSchool_Record")

#集計値を「HighSchool_Record」に格納
for i in df_group.index:
    row = cursor.newRow()
    row.setValue("Name", i)
    row.setValue("Point", df_group.ix[i])
    cursor.insertRow(row)
del cursor