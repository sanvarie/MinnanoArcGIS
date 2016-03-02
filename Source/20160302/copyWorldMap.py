# -*- coding: utf-8 -*-
import arcpy

#対象GDB
arcpy.env.workspace = "C:\ArcPySample\Map.gdb"

#コピーするフィーチャクラス名
inFeature = "WorldMap"

#ShapeをMap.gdbにコピー
arcpy.CopyFeatures_management(r"D:\python\WorldMap\ne_10m_admin_0_countries.shp", inFeature)

#コードブロック
codeblock = """
def UpdateColumn(FORMAL_EN,NAME_LONG):
    if FORMAL_EN == " ":
        return NAME_LONG
    else:
        return FORMAL_EN
"""

# 条件式を設定
expression = "UpdateColumn(!FORMAL_EN!,!NAME_LONG!)"

#フィールド演算(正式名称が半角スペースになっているものをNAME_LONGに置き換える)
arcpy.CalculateField_management(inFeature, "FORMAL_EN", expression, "PYTHON_9.3", codeblock)

#カラム追加
arcpy.AddField_management(inFeature, "NAME_EN", "Text",field_length = 60,field_alias="英語名")

#フィールド演算(FORMAL_ENをNAME_ENに置き換える)
arcpy.CalculateField_management(inFeature, "NAME_EN", "!FORMAL_EN!", "PYTHON_9.3")

field_list = []
fields = arcpy.ListFields(inFeature)
for field in fields:
    if field.type != "Geometry":
        if field.name != "NAME_EN" and field.name != "OBJECTID" and field.name != "Shape_Length" and field.name != "Shape_Area":
            field_list.append(field.name)

#不要なフィールドを削除
arcpy.DeleteField_management(inFeature,
                             field_list)