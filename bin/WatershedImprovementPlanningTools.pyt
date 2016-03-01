import os, sys, shutil, arcpy
import traceback, time

def log(message):
    arcpy.AddMessage(message)
    with file(sys.argv[0]+".log", 'a') as logFile:
        logFile.write("%s:\t%s\n" % (time.asctime(), message))
    
class Toolbox(object):
    def __init__(self):
        self.label = "WIP tools"
        self.alias = ""
        self.tools = [TopoHydro, ImpCov, Runoff]
        
class TopoHydro(object):
    def __init__(self):
        self.label = "Topography and Hydrology Analysis"
        self.description = "Establishes the watershed and stream network"
        self.canRunInBackground = False
        
        arcpy.env.Workspace = self.Workspace = os.path.split(__file__)[0]
        log("Workspace = " + arcpy.env.Workspace)
        arcpy.env.overwriteOutput = True       

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Input Digital Elevation Model",
            name="DEM",
            datatype="DERasterDataset",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
            
        param1 = arcpy.Parameter(
            displayName="Analysis Mask",
            name="Mask",
            datatype="DEFeatureClass",
            parameterType="Optional",
            direction="Input",
            multiValue=False)  
        
        param2 = arcpy.Parameter(
            displayName="Threshold accumulation for Stream formation (acres)",
            name="StreamFormation",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
        
        params = [ param0, param1, param2 ]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return
            
    def execute(self, parameters, messages):
        try:
            log("Parameters are %s, %s, %s" % (parameters[0].valueAsText, parameters[1].valueAsText, parameters[2].valueAsText))
        except Exception as err:
            log(traceback.format_exc())
            log(err)
            raise err
        return

class ImpCov(object):
    def __init__(self):
        self.label = "Imperviousness Analysis"
        self.description = "Impervious area contributions"
        self.canRunInBackground = False
        
        arcpy.env.Workspace = self.Workspace = os.path.split(__file__)[0]
        log("Workspace = " + arcpy.env.Workspace)
        arcpy.env.overwriteOutput = True       

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Impervious Areas",
            name="ImperviousAreas",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
            
        param1 = arcpy.Parameter(
            displayName="Lakes",
            name="Lakes",
            datatype="DEFeatureClass",
            parameterType="Optional",
            direction="Input",
            multiValue=False)  
        
        params = [ param0, param1 ]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return
            
    def execute(self, parameters, messages):
        try:
            log("Parameters are %s, %s" % (parameters[0].valueAsText, parameters[1].valueAsText))
        except Exception as err:
            log(traceback.format_exc())
            log(err)
            raise err
        return
        
class Runoff(object):
    def __init__(self):
        self.label = "Runoff Calculations"
        self.description = "Calculation of standard storm flows via USGS regression equations"
        self.canRunInBackground = False
        
        arcpy.env.Workspace = self.Workspace = os.path.split(__file__)[0]
        log("Workspace = " + arcpy.env.Workspace)
        arcpy.env.overwriteOutput = True       

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Curve Number",
            name="Landuse",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
        
        params = [ param0 ]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return
            
    def execute(self, parameters, messages):
        try:
            log("Parameter is %s" % (parameters[0].valueAsText))
			# -*- coding: utf-8 -*-
			# ---------------------------------------------------------------------------
			# Stream_Lab6.py
			# Created on: 2016-03-01 18:19:03.00000
			#   (generated by ArcGIS/ModelBuilder)
			# Description: 
			# ---------------------------------------------------------------------------

			# Import arcpy module
			import arcpy


			# Local variables:
			DEM = "DEM"
			DEM_Fill = "E:\\Senior Year\\Spring 2016\\ERE693\\Lab6\\Lab06Data.gdb\\DEM_Fill"
			AnalysisMask = "E:\\Senior Year\\Spring 2016\\ERE693\\Lab6\\Lab06Data.gdb\\AnalysisMask"
			AnalysisRas = "E:\\Senior Year\\Spring 2016\\ERE693\\Lab6\\Lab06Data.gdb\\AnalysisRas"
			Output_drop_raster = ""
			DEM_fd = "E:\\Senior Year\\Spring 2016\\ERE693\\Lab6\\Lab06Data.gdb\\DEM_fd"
			DEM_fa = "E:\\Senior Year\\Spring 2016\\ERE693\\Lab6\\Lab06Data.gdb\\DEM_fa"
			Accum_acres = "E:\\Senior Year\\Spring 2016\\ERE693\\Lab6\\Lab06Data.gdb\\Accum_acres"
			Stream_Ras = "E:\\Senior Year\\Spring 2016\\ERE693\\Lab6\\Lab06Data.gdb\\Stream_Ras"
			Stream_Feat = "E:\\Senior Year\\Spring 2016\\ERE693\\Lab6\\Lab06Data.gdb\\Stream_Feat"

			# Process: Fill
			tempEnvironment0 = arcpy.env.extent
			arcpy.env.extent = "2008480.2410905 751026.288687245 2056480.2410905 811226.288687245"
			arcpy.gp.Fill_sa(DEM, DEM_Fill, "")
			arcpy.env.extent = tempEnvironment0

			# Process: Polygon to Raster
			arcpy.PolygonToRaster_conversion(AnalysisMask, "OBJECTID", AnalysisRas, "CELL_CENTER", "NONE", "190")

			# Process: Flow Direction
			tempEnvironment0 = arcpy.env.snapRaster
			arcpy.env.snapRaster = ""
			tempEnvironment1 = arcpy.env.extent
			arcpy.env.extent = "2008480.2410905 751026.288687245 2056480.2410905 811226.288687245"
			tempEnvironment2 = arcpy.env.mask
			arcpy.env.mask = AnalysisRas
			arcpy.gp.FlowDirection_sa(DEM_Fill, DEM_fd, "NORMAL", Output_drop_raster)
			arcpy.env.snapRaster = tempEnvironment0
			arcpy.env.extent = tempEnvironment1
			arcpy.env.mask = tempEnvironment2

			# Process: Flow Accumulation
			tempEnvironment0 = arcpy.env.snapRaster
			arcpy.env.snapRaster = ""
			tempEnvironment1 = arcpy.env.extent
			arcpy.env.extent = "2008480.2410905 751026.288687245 2056480.2410905 811226.288687245"
			arcpy.gp.FlowAccumulation_sa(DEM_fd, DEM_fa, "", "FLOAT")
			arcpy.env.snapRaster = tempEnvironment0
			arcpy.env.extent = tempEnvironment1

			# Process: Raster Calculator
			tempEnvironment0 = arcpy.env.snapRaster
			arcpy.env.snapRaster = ""
			tempEnvironment1 = arcpy.env.extent
			arcpy.env.extent = DEM_fa
			arcpy.gp.RasterCalculator_sa("(\"%DEM_fa%\"*1600)/43560", Accum_acres)
			arcpy.env.snapRaster = tempEnvironment0
			arcpy.env.extent = tempEnvironment1

			# Process: Reclassify
			arcpy.gp.Reclassify_sa(Accum_acres, "Value", "0 776 NODATA;776 22536.638671875 1", Stream_Ras, "DATA")

			# Process: Stream to Feature
			arcpy.gp.StreamToFeature_sa(Stream_Ras, DEM_fd, Stream_Feat, "SIMPLIFY")


        except Exception as err:
            log(traceback.format_exc())
            log(err)
            raise err
        return
		
