# -*- coding: utf-8 -*-
import arcpy

#ディゾルブ
arcpy.Dissolve_management("D:\python\soccer\japan_ver80.shp", "C:\ArcPySample\ArcPyJapan.gdb\Japan",
                           "KEN", "", "MULTI_PART",
                           "DISSOLVE_LINES")