# -*- coding: utf-8 -*-
import arcpy

#対象GDB
arcpy.env.workspace = "C:\ArcPySample\Map.gdb"

#ShapeをMap.gdbにコピー
arcpy.CopyFeatures_management("WorldMap", "WorldMap2")