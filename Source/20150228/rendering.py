# -*- coding: utf-8 -*-
import arcpy

mxd = arcpy.mapping.MapDocument("CURRENT")
for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.symbologyType == "GRADUATED_COLORS":
        if lyr.symbology.valueField == "":
            lyr.symbology.valueField = "Point"
        lyr.symbology.classBreakValues = [0,10,30,50,100,150,200]
        arcpy.RefreshActiveView()