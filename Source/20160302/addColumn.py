# -*- coding: utf-8 -*-
import arcpy

#対象GDB
arcpy.env.workspace = "C:\ArcPySample\Map.gdb"

#コピーするフィーチャクラス名
inFeature = "WorldMap"

#カラム追加
arcpy.AddField_management(inFeature, "NAME", "Text",field_length = 50,field_alias="国名")
arcpy.AddField_management(inFeature, "CAPITAL", "Text",field_length = 50,field_alias="首都")
#arcpy.AddField_management(inFeature, "INDE_YEAR", "Text",field_length = 50,field_alias="独立年")
arcpy.AddField_management(inFeature, "LANGUAGE", "Text",field_length = 50,field_alias="主要言語")
arcpy.AddField_management(inFeature, "AREASQUARE", "Double",field_length = 50,field_alias="面積（1,000平方キロ）")
arcpy.AddField_management(inFeature, "POPULATION", "Double",field_length = 50,field_alias="人口（100万人）")
arcpy.AddField_management(inFeature, "CURRENCY", "Text",field_length = 50,field_alias="通貨単位")