import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

import os,sys

options = VarParsing.VarParsing('standard') # avoid the options: maxEvents, files, secondaryFiles, output, secondaryOutput because they are already defined in 'standard'


options.register('dataFile',
                 '/home/tquast/tb2017/reconstructedFiles/reco_1501.root',
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 'folder containing raw input')

options.register('outputFile',
                 '/home/tquast/tb2017/variable_trees/tree_1501.root',
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 'Output file where analysis output are stored')

options.register('VariablesToPlot',
                 '',
                 VarParsing.VarParsing.multiplicity.list,
                 VarParsing.VarParsing.varType.string,
                 'Indicate which variables are to be added to the tree. The keys here must match the ones as defined in the VariableComputation'
                )

options.register('electronicMap',
                 'map_CERN_Hexaboard_October_17Sensors_5EELayers_6FHLayers_V1.txt',
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 'Name of the electronic map file in HGCal/CondObjects/data/')

options.register('hgcalLayout',
                 'layerGeom_oct2017_h2_17layers.txt',
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 'Name of the hgcal layout file in HGCal/CondObjects/data/')

options.register('layerPositionFile',
                 '/afs/cern.ch/user/t/tquast/CMSSW_9_3_0_/src/HGCal/CondObjects/data/layer_distances_CERN_Hexaboard_September_7EELayers_10FHLayers_V0.txt',
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 'File indicating the layer positions in mm.')

options.register('NHexaBoards',
                17,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 'Number of hexaboards for analysis.'
                )

options.register('NLayers',
                17,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 'Number of layers for analysis.'
                )

options.register('DNNInputFile',
                 '',
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 'File to the trained tensorflow networks for DNN analysis.')


options.register('NColorsInputImage',
                17,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 'Number of colours of input image for DNN analysis.'
                )

                                 
options.register('simulation',
                 0,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 '1=Analysis is run on simulated samples'
                 )

options.register('reportEvery',
                1000,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 'Path to the file from which the DWCs are read.'
                )

options.maxEvents = -1

options.parseArguments()
print options


electronicMap="HGCal/CondObjects/data/%s" % options.electronicMap
hgcalLayout="HGCal/CondObjects/data/%s" % options.hgcalLayout

################################
process = cms.Process("variablecomputation")
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)
####################################
# Reduces the frequency of event count couts
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery
####################################

process.source = cms.Source("PoolSource",
                            fileNames=cms.untracked.vstring("file:%s"%options.dataFile)
)

process.TFileService = cms.Service("TFileService", fileName = cms.string(options.outputFile))


if options.simulation==1:
    rundata_tag = cms.InputTag("source", "FullRunData", "rechitproducer") 
    rechit_tag = cms.InputTag("source", "HGCALTBRECHITS", "rechitproducer")
    dwc_tag = cms.InputTag("source","DelayWireChambers" )
    dwc_track_tag = cms.InputTag("dwctrackproducer","HGCalTBDWCTracks" )
else:
    rundata_tag = cms.InputTag("wirechamberproducer","FullRunData")
    rechit_tag = cms.InputTag("rechitproducer","HGCALTBRECHITS" )
    dwc_tag = cms.InputTag("wirechamberproducer","DelayWireChambers" )
    dwc_track_tag = cms.InputTag("dwctrackproducer","HGCalTBDWCTracks" )

process.variablecomputation = cms.EDProducer("VariableComputation",
                                RUNDATA = rundata_tag,
                                HGCALTBRECHITS = rechit_tag,
                                MWCHAMBERS = dwc_tag,
                                DWCTRACKS = dwc_track_tag,
                                UserRecordCollectionName=cms.untracked.string("VariableUserRecords"),
                                ElectronicMap = cms.untracked.string(electronicMap),
                                DetectorLayout=cms.untracked.string(hgcalLayout),
                                layerPositionFile=cms.string(options.layerPositionFile),
                                NHexaBoards=cms.untracked.int32(options.NHexaBoards),
                                NLayers=cms.untracked.int32(options.NLayers),
                                DNNInputFile = cms.untracked.string(options.DNNInputFile),
                                NColorsInputImage = cms.untracked.int32(options.NColorsInputImage)
                              )

process.ntupelizer = cms.EDAnalyzer("NTupelizer",
                                USERRECORDS = cms.InputTag("variablecomputation","VariableUserRecords" ),
                                UserRecordKeys = cms.vstring(options.VariablesToPlot)
                            )
    

process.p = cms.Path(process.variablecomputation * process.ntupelizer)

