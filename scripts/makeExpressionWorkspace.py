#!/usr/bin/env python
"""
Thomas Klijnsma
"""

########################################
# Imports
########################################

import os
from os.path import *
from glob import glob
from shutil import copyfile

import ROOT

# Load some libraries                                                                                                                                                          
ROOT.gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ")
ROOT.gSystem.Load("$CMSSW_BASE/lib/$SCRAM_ARCH/libHiggsAnalysisCombinedLimit.so")
ROOT.gSystem.AddIncludePath("-I$ROOFITSYS/include")
ROOT.gSystem.AddIncludePath("-Iinclude/")


# ======================================
# Import the SMXS and efficiencies from a common file

from Numbers import Numbers
numbers = Numbers()

Fine_Binning = numbers.Fine_Binning
Hgg_Binning  = numbers.Hgg_Binning
HZZ_Binning  = numbers.HZZ_Binning
HWW_Binning  = numbers.HWW_Binning
Fine_nBins   = len(Fine_Binning)-1
Hgg_nBins    = len(Hgg_Binning)-1
HZZ_nBins    = len(HZZ_Binning)-1
HWW_nBins    = len(HWW_Binning)-1

HZZ_EffNumbers = {
    '4e'     : numbers.GetEff( 'HZZ_4e'    ),
    '4mu'    : numbers.GetEff( 'HZZ_4mu'   ),
    '2e2mu'  : numbers.GetEff( 'HZZ_2e2mu' ),
    }

HZZ_SMXSNumbers = {
    '4e'     : numbers.GetXS(  'HZZ_4e'    ),
    '4mu'    : numbers.GetXS(  'HZZ_4mu'   ),
    '2e2mu'  : numbers.GetXS(  'HZZ_2e2mu' ),
    }

Hgg_SMXSNumbers = numbers.GetXS( 'Hgg' )
HWW_SMXSNumbers = numbers.GetXS( 'HWW' )
Hgg_EffNumbers = numbers.GetEff( 'Hgg' )
HWW_EffNumbers = numbers.GetEff( 'HWW' )

HggMergemap = numbers.HggMergemap
HZZMergemap = numbers.HZZMergemap
HWWMergemap = numbers.HWWMergemap


########################################
# Main
########################################

inputDir = join( os.environ['STARTDIR'], 'input' )


def main():


    # ########################################
    # # Get SM fractions from any HZZ input workspace
    # ########################################

    # smFractions4e, smFractions4mu = GetSMFractions( join( inputDir, 'HZZ_orig/hzz4l_2e2muS_8TeV_xs_SM_125_pT4l_v3.Databin0.root' ) )


    outRootFile = join( inputDir, 'expressions.root' )
    fout = ROOT.TFile( outRootFile, 'recreate' )

    wout = ROOT.RooWorkspace( 'w', 'w' )

    smFractions4e, smFractions4mu = GetSMFractions( join( inputDir, 'HZZ_orig/hzz4l_2e2muS_8TeV_xs_SM_125_pT4l_v3.Databin0.root' ) )
    AddSMFractionsToWs( wout, smFractions4e, smFractions4mu )

    WriteMus( wout )

    fout.WriteTObject(wout)
    fout.Close()















def GetSMFractions( smfractionRootFile ):

    smfractionRootFp = ROOT.TFile.Open( smfractionRootFile )
    smfractionWS     = ROOT.gDirectory.Get('w')

    smFractions4e  = [ 0 for i in xrange(HZZ_nBins) ]
    smFractions4mu = [ 0 for i in xrange(HZZ_nBins) ]

    for iBin in xrange(HZZ_nBins):

        fracSM4e  = smfractionWS.var( 'fracSM4eBin{0}'.format(iBin) ).getVal()
        smFractions4e[iBin] = fracSM4e

        fracSM4mu = smfractionWS.var( 'fracSM4muBin{0}'.format(iBin) ).getVal()
        smFractions4mu[iBin] = fracSM4mu

    smfractionRootFp.Close()


    # print smFractions4mu[0]
    # from sys import exit
    # exit()

    return smFractions4e, smFractions4mu


def AddSMFractionsToWs( w, smFractions4e, smFractions4mu ):
    for iBin in xrange(HZZ_nBins):

        smfrac4e = ROOT.RooRealVar(
            'fracSM4eBin{0}'.format(iBin),
            'fracSM4eBin{0}'.format(iBin),
            smFractions4e[iBin]
            )
        getattr( w, 'import' )( smfrac4e )


        smfrac4mu = ROOT.RooRealVar(
            'fracSM4muBin{0}'.format(iBin),
            'fracSM4muBin{0}'.format(iBin),
            smFractions4mu[iBin]
            )
        getattr( w, 'import' )( smfrac4mu )


        K1 = ROOT.RooRealVar(
            'K1Bin{0}'.format(iBin),
            'K1Bin{0}'.format(iBin),
            1.0, 0.0, 1.0/smfrac4e.getVal()
            )
        getattr( w, 'import' )( K1 )

        K2 = ROOT.RooRealVar(
            'K2Bin{0}'.format(iBin),
            'K2Bin{0}'.format(iBin),
            1.0, 0.0, ( 1.0-smfrac4e.getVal() ) / smfrac4mu.getVal()
            )
        getattr( w, 'import' )( K2 )





def WriteMus( wout ):

    ########################################
    # Setting SMXS and Efficiencies as variables in model
    ########################################

    # Open up RooRealVars per channel
    HZZ_SMXSs = {}
    HZZ_Effs = {}

    for channel in [ '4e', '4mu', '2e2mu' ]:

        HZZ_SMXSs[channel] = []

        for iBin in xrange(Fine_nBins):
            SMXS_RooRealVar = ROOT.RooRealVar(
                'HZZ{0}SMXS_FineBin{1}'.format( channel, iBin ), 'HZZ{0}SMXS_FineBin{1}'.format( channel, iBin ),
                HZZ_SMXSNumbers[channel][iBin]
                )
            SMXS_RooRealVar.setConstant(True)
            HZZ_SMXSs[channel].append( SMXS_RooRealVar )

        HZZ_Effs[channel] = []

        for iBin in xrange(Fine_nBins):
            Eff_RooRealVar = ROOT.RooRealVar(
                'HZZ{0}Eff_FineBin{1}'.format( channel, iBin ), 'HZZ{0}Eff_FineBin{1}'.format( channel, iBin ),
                HZZ_EffNumbers[channel][iBin]
                )
            Eff_RooRealVar.setConstant(True)
            HZZ_Effs[channel].append( Eff_RooRealVar )


    # Hgg and HWW are not per-channel
    
    Hgg_SMXSs = []
    HWW_SMXSs = []
    Hgg_Effs = []
    HWW_Effs = []
    Hgg_XSTimesEffs = []
    HWW_XSTimesEffs = []

    for iBin in xrange(Fine_nBins):

        SMXS_RooRealVar = ROOT.RooRealVar(
            'HggSMXS_FineBin{0}'.format(iBin), 'HggSMXS_FineBin{0}'.format(iBin), Hgg_SMXSNumbers[iBin]
            )
        Eff_RooRealVar = ROOT.RooRealVar(
            'HggEff_FineBin{0}'.format(iBin), 'HggEff_FineBin{0}'.format(iBin), Hgg_EffNumbers[iBin]
            )
        Hgg_SMXSs.append( SMXS_RooRealVar )
        Hgg_Effs.append( Eff_RooRealVar )

        Hgg_XSTimesEffs.append(
            ROOT.RooProduct(
                'HggXSTimesEff_FineBin{0}'.format(iBin), 'HggXSTimesEff_FineBin{0}'.format(iBin),
                ROOT.RooArgList( SMXS_RooRealVar, Eff_RooRealVar )
                )
            )

        SMXS_RooRealVar = ROOT.RooRealVar(
            'HWWSMXS_FineBin{0}'.format(iBin), 'HWWSMXS_FineBin{0}'.format(iBin), HWW_SMXSNumbers[iBin]
            )
        Eff_RooRealVar = ROOT.RooRealVar(
            'HWWEff_FineBin{0}'.format(iBin), 'HWWEff_FineBin{0}'.format(iBin), HWW_EffNumbers[iBin]
            )
        HWW_SMXSs.append( SMXS_RooRealVar )
        HWW_Effs.append( Eff_RooRealVar )

        HWW_XSTimesEffs.append(
            ROOT.RooProduct(
                'HWWXSTimesEff_FineBin{0}'.format(iBin), 'HWWXSTimesEff_FineBin{0}'.format(iBin),
                ROOT.RooArgList( SMXS_RooRealVar, Eff_RooRealVar )
                )
            )




    ########################################
    # Fine Mus
    ########################################

    fineMus = []

    for iBin in xrange(Fine_nBins):

        muName = 'FineBin{0}_Mu'.format(iBin)
        print 'Building expressions for {0}'.format( muName )

        muPar  = ROOT.RooRealVar( muName, muName, 1.0 )
        muPar.setRange( -1.0, 3.0 )
        muPar.setConstant(False)

        if iBin == Fine_nBins-1:
            muPar.removeRange()
            muPar.setVal(1)
            muPar.setConstant(True)

        fineMus.append( muPar )


    ########################################
    # Hgg
    ########################################

    Hgg_Mus = []

    for iBin in xrange(Hgg_nBins):

        muName = 'HggBin{0}_Mu'.format(iBin)
        print 'Building expressions for {0}'.format( muName )

        mergeFineBins = HggMergemap[iBin]

        if len(mergeFineBins) < 1:
            raise RuntimeError, 'Invalid bin mapping'
        
        elif len(mergeFineBins) == 1:
            muPar = ROOT.RooFormulaVar(
                muName, muName,
                '(@0)', ROOT.RooArgList( fineMus[mergeFineBins[0]] )
                )

        elif len(mergeFineBins) > 1:

            totalXS_input = ROOT.RooArgList()
            for iBinFine in mergeFineBins:
                totalXS_input.add( Hgg_XSTimesEffs[iBinFine] )

            # Compute total cross section over the merged bins
            totalXS = ROOT.RooAddition(
                'totalXS_HggBin{0}'.format(iBin), 'totalXS_HggBin{0}'.format(iBin), totalXS_input
                )

            # Compute weighted Mus and their sum
            weightedMus = []
            for iBinFine in mergeFineBins:
                varname = 'weightedFineMu{0}_HggBin{1}'.format( iBinFine, iBin )
                weightedMu = ROOT.RooFormulaVar(
                    varname, varname,
                    '( @0/@1 * @2 )',
                    ROOT.RooArgList(
                        Hgg_XSTimesEffs[iBinFine], totalXS, fineMus[iBinFine]
                        )
                    )
                weightedMus.append( weightedMu )

            ROOT.RooArgList( *weightedMus )

            muPar = ROOT.RooAddition(
                muName, muName,
                ROOT.RooArgList( *weightedMus )
                )

        Hgg_Mus.append( muPar )
        getattr(wout,'import')( muPar )


    ########################################
    # HWW
    ########################################

    HWW_Mus = []

    for iBin in xrange(HWW_nBins):

        muName = 'HWWBin{0}_Mu'.format(iBin)
        print 'Building expressions for {0}'.format( muName )

        mergeFineBins = HWWMergemap[iBin]

        if len(mergeFineBins) < 1:
            raise RuntimeError, 'Invalid bin mapping'
        
        elif len(mergeFineBins) == 1:
            muPar = ROOT.RooFormulaVar(
                muName, muName,
                '(@0)', ROOT.RooArgList( fineMus[mergeFineBins[0]] )
                )

        elif len(mergeFineBins) > 1:

            totalXS_input = ROOT.RooArgList()
            for iBinFine in mergeFineBins:
                totalXS_input.add( HWW_XSTimesEffs[iBinFine] )

            # Compute total cross section over the merged bins
            totalXS = ROOT.RooAddition(
                'totalXS_HWWBin{0}'.format(iBin), 'totalXS_HWWBin{0}'.format(iBin), totalXS_input
                )

            # Compute weighted Mus and their sum
            weightedMus = []
            for iBinFine in mergeFineBins:
                varname = 'weightedFineMu{0}_HWWBin{1}'.format( iBinFine, iBin )
                weightedMu = ROOT.RooFormulaVar(
                    varname, varname,
                    '( @0/@1 * @2 )',
                    ROOT.RooArgList(
                        HWW_XSTimesEffs[iBinFine], totalXS, fineMus[iBinFine]
                        )
                    )
                weightedMus.append( weightedMu )

            ROOT.RooArgList( *weightedMus )

            muPar = ROOT.RooAddition(
                muName, muName,
                ROOT.RooArgList( *weightedMus )
                )

        HWW_Mus.append( muPar )
        getattr(wout,'import')( muPar )


    ########################################
    # HZZ
    # Requires special bin merging because of the separate channels
    ########################################

    HZZBinStr   = lambda binNumber: 'HZZBin{0}_Mu'.format(binNumber)

    HZZ_Mus = []
    SigmaBinXs  = []

    for iBin in xrange(HZZ_nBins):

        muName = 'HZZBin{0}_Mu'.format(iBin)
        print 'Building expressions for {0}'.format( muName )

        mergeFineBins = HZZMergemap[iBin]


        if len(mergeFineBins) < 1:
            raise RuntimeError, 'Invalid bin mapping'
        
        elif len(mergeFineBins) == 1:
            muPar = ROOT.RooFormulaVar(
                muName, muName,
                '(@0)', ROOT.RooArgList( fineMus[mergeFineBins[0]] )
                )

        elif len(mergeFineBins) > 1:

            # ======================================
            # Make the summed reco Eff*SMXS

            summedXSs = []
            for iBinFine in mergeFineBins:

                varname = 'summedXSFineBin{0}_HZZBin{1}'.format( iBinFine, iBin )

                summedXS = ROOT.RooFormulaVar(
                    varname, varname,
                    '( @0*@3 + @1*@4 + @2*@5 )',
                    ROOT.RooArgList(
                        HZZ_SMXSs['4e'][    iBinFine ],
                        HZZ_SMXSs['4mu'][   iBinFine ],
                        HZZ_SMXSs['2e2mu'][ iBinFine ],
                        HZZ_Effs['4e'][     iBinFine ],
                        HZZ_Effs['4mu'][    iBinFine ],
                        HZZ_Effs['2e2mu'][  iBinFine ],
                        ),
                    )
                summedXSs.append( summedXS )


            # ======================================
            # Create variables for the weighted Mus and their sum

            totalXS = ROOT.RooAddition(
                'totalXS_HZZBin{0}'.format( iBin ), 'totalXS_HZZBin{0}'.format( iBin ),
                ROOT.RooArgList( *summedXSs )
                )

            weightedMus = []
            for iBinFine, summedXS in zip( mergeFineBins, summedXSs ):

                varname = 'weightedFineMu{0}_HZZBin{1}'.format( iBinFine, iBin )

                weightedMu = ROOT.RooFormulaVar(
                    varname, varname,
                    '(  @0/@1 * @2 )',
                    ROOT.RooArgList( summedXS, totalXS, fineMus[iBinFine] )
                    )
                weightedMus.append( weightedMu )


            muPar = ROOT.RooAddition(
                muName, muName,
                ROOT.RooArgList( *weightedMus ),
                )



        else:
            raise RuntimeError, 'more elaborate bin merging needs to be created in the model'

        HZZ_Mus.append( muPar )


        # ======================================
        # Final step: (over)write the variables SigmaBinX

        SigmaBinX = ROOT.RooFormulaVar(
            'SigmaBin{0}'.format(iBin), 'SigmaBin{0}'.format(iBin),
            '(@0)', ROOT.RooArgList( muPar )
            )
        SigmaBinXs.append( SigmaBinX )

 
        getattr(wout,'import')( SigmaBinX )












########################################
# End of Main
########################################
if __name__ == "__main__":
    main()