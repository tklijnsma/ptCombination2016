#!/usr/bin/env python
"""
Thomas Klijnsma
"""

########################################
# Imports
########################################

import os, sys, shutil, re
from time import strftime

from os.path import join, abspath, basename, isdir, isfile
from Numbers import Numbers

########################################
# Main
########################################


datestr = strftime( '%b%d' )

inputDir = join( os.environ['STARTDIR'], 'input' )
startDir = os.getcwd()


# ======================================
# Load numbers

numbers = Numbers()
channels = numbers.channels


# class Scan():

#     def __init__(self, name, win ):
#         self.name   = name
#         self.win    = win




def main():

    scan(
        abspath( join( inputDir, 'CARD_all_orig.root' ) ),
        'Fine',
        )

    scan(
        abspath( join( inputDir, 'CARD_HZZ.root' ) ),
        'HZZ',
        )

    scan(
        abspath( join( inputDir, 'CARD_Hgg.root' ) ),
        'Hgg',
        )

    scan(
        abspath( join( inputDir, 'CARD_HWW.root' ) ),
        'HWW',
        )






def makeJobdir( name ):
    jobdir = join( os.environ['STARTDIR'], 'jobs_' + datestr + '_' + name )
    if isdir(jobdir): shutil.rmtree( jobdir )
    os.makedirs(jobdir)
    return jobdir



def scan( inputrootfile, channel, selectbins='*' ):

    # Determine number of bins
    if not channel in channels:
        print 'ERROR: Channel {0} is not implemented'.format(channel)
        return

    jobdir = makeJobdir( channel )
    rootfile = join( basename(inputrootfile), join( jobdir, basename(inputrootfile) ) )
    shutil.copyfile( inputrootfile, rootfile )


    os.chdir(jobdir)


    # Some parameters related to fitting
    Range         = [ -1.00, 4.00 ]
    nPoints       = 48
    
    if channel == 'HZZ' or channel == 'HWW':
        nPointsPerJob = 12
    elif channel == 'Hgg':
        nPointsPerJob = 4
    else:
        nPointsPerJob = 3


    # Other variables that should be saved in the workspace
    saveFunctionsList = []

    if channel == 'Fine':
        for iterchannel in channels:
            for iBin in xrange(getattr( numbers, iterchannel+'_nBins' )):
                saveFunctionsList.append( '{0}Bin{1}_Mu'.format( iterchannel, iBin ) )
        saveFunctions = ','.join( saveFunctionsList )
    else:
        for iBin in xrange(getattr( numbers, channel+'_nBins' )):
            saveFunctionsList.append( '{0}Bin{1}_Mu'.format( channel, iBin ) )
        saveFunctions = ','.join( saveFunctionsList )


    sp = lambda text: ' {0} '.format(text)

    if selectbins == '*':
        bins = range(getattr( numbers, channel+'_nBins' ))
    else:
        bins = selectbins

    for iBin in bins:

        POI = '{0}Bin{1}_Mu'.format( channel, iBin )
        if channel == 'HZZ':
            POI = 'SigmaBin{0}'.format(iBin)

        scanName = 'SCAN_{0}_Bin{1}'.format( channel, iBin )

        cmd = 'combineTool.py '
        cmd += sp( rootfile )
        cmd += sp( '-n {0}'.format(scanName) )

        cmd += sp( '-M MultiDimFit ' )
        cmd += sp( '--cminDefaultMinimizerType Minuit2 ' )
        cmd += sp( '--cminDefaultMinimizerAlgo migrad ' )
        cmd += sp( '--algo=grid  ' )
        cmd += sp( '--floatOtherPOIs=1 ' )
        cmd += sp( '-P "{0}" '.format(POI) )
        cmd += sp( '--setPhysicsModelParameterRanges "{0}"={1:.3f},{2:.3f} '.format( POI, Range[0], Range[1]) )
        cmd += sp( '-m 125.00 ' )
        cmd += sp( '--squareDistPoi ' )
        cmd += sp( '--saveNLL ' )
        cmd += sp( '--saveInactivePOI 1 ' )
        cmd += sp( '--saveSpecifiedFunc {0} '.format(saveFunctions) )
        cmd += sp( '--points={0} '.format(nPoints) )
        cmd += sp( '--split-points {0} '.format(nPointsPerJob) )
        cmd += sp( '--job-mode lxbatch --task-name {0} --sub-opts=\'-q 1nh\''.format(scanName) )


        try:
            print
            print cmd
            os.system( cmd )
        except:
            print 'COMMAND FAILED!'
            print




    # combineTool.py \
    #     "$(basename $WORKSPACE)" \
    #     -n "$SCANNAME" \
    #     -M MultiDimFit \
    #     --cminDefaultMinimizerType Minuit2 \
    #     --cminDefaultMinimizerAlgo migrad \
    #     --algo=grid  \
    #     --floatOtherPOIs=1 \
    #     -P "FineBin${BIN}_Mu" \
    #     --setPhysicsModelParameterRanges "FineBin${BIN}_Mu"=-1.00,4.00  \
    #     -m 125.00 \
    #     --squareDistPoi \
    #     --saveNLL \
    #     --saveInactivePOI 1 \
    #     --saveSpecifiedFunc "$(SaveVariablesCommaSepList)" \
    #     --points=48 \
    #     --split-points 3 \
    #     --job-mode lxbatch --task-name "$SCANNAME" --sub-opts='-q 1nh'














########################################
# End of Main
########################################
if __name__ == "__main__":
    main()