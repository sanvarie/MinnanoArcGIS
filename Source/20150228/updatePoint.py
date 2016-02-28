# -*- coding: utf-8 -*-
import arcpy
import pandas as pd

arcpy.env.workspace = "C:\ArcPySample\Soccer.gdb"

#インターセクト
highShcool = arcpy.Intersect_analysis(["HighShcool", "Japan"],"HighShcool_Japan" ,"", "", "")

field_list = []
fields = arcpy.ListFields(highShcool)
for field in fields:
    if field.type != "Geometry":
        field_list.append(field.name)

#属性テーブルをPandasに格納
column = arcpy.da.FeatureClassToNumPyArray(highShcool,field_list,null_value=-9999)
df = pd.DataFrame(column)

#ポイントの集計
df_group = df.groupby('KEN')['Point'].sum()

#集計値をJapanに格納
for i in df_group.index:
    cursor = arcpy.UpdateCursor("Japan")
    for row in cursor:
        if i == row.KEN:
            row.setValue("Point", df_group.ix[i])
            cursor.updateRow(row)
    del cursor


#コードブロック
codeblock = """
def UpdatePoint(Point):
    if Point is None:
        return 0
    else:
        return Point
"""

# 条件式を設定
expression = "UpdatePoint(!Point!)"

#ポイントが0の県に対してフィールド演算
arcpy.CalculateField_management("Japan", "Point", expression, "PYTHON_9.3", codeblock)
