# -*- coding: utf-8 -*-
import arcpy

arcpy.env.workspace = "C:\ArcPySample\ArcPyJapan.gdb"
arcpy.AddField_management("Japan", "P_NUM", "Long")
arcpy.AddField_management("Japan", "H_NUM", "Long")