import FWCore.ParameterSet.Config as cms

hgcaltbrechits = cms.EDProducer("HGCalTBRecHitProducer",
                              OutputCollectionName = cms.string(''),
                              digiCollection = cms.InputTag('hgcaltbdigis'),
                                pedestalLow = cms.string(''),
#                                pedestalHigh = cms.string('CondObjects/data/Ped_HighGain_8272_Mean.txt'),  
                                pedestalHigh = cms.string(''),
                                gainLow = cms.string(''),
                                gainHigh = cms.string(''),
                              )

hgcaltbsimrechits = cms.EDProducer("HGCalTBSimRecHitProducer",
                              OutputCollectionName = cms.string(''),
                              digiCollection = cms.InputTag("source","","HGC"),
                                pedestalLow = cms.string(''),
                                pedestalHigh = cms.string(''),
                                gainLow = cms.string(''),
                                gainHigh = cms.string(''),
                              )

