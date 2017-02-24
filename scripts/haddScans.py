#!/usr/bin/env python
"""
Thomas Klijnsma
"""

########################################
# Imports
########################################

import os, sys, shutil, re
from time import strftime
from glob import glob

from os.path import join, abspath, basename, isdir, isfile
from Numbers import Numbers

import argparse

########################################
# Main
########################################


datestr = strftime( '%b%d' )

inputDir = join( os.environ['STARTDIR'], 'input' )
startDir = os.environ['STARTDIR']


# ======================================
# Load numbers

numbers = Numbers()
channels = numbers.channels




def main():

    parser = argparse.ArgumentParser()
    parser.add_argument( 'jobdirs', metavar='N', type=str, nargs='+', help='list of strings' )
    args = parser.parse_args()


    for jobdir in args.jobdirs:

        # ======================================
        # Determine to what channel the job corresponds

        foundChannel = False
        for channel in channels:
            if channel in jobdir:
                foundChannel = True
                break

        if not foundChannel:
            print 'ERROR: unable to determine channel'
            return




        print
        print 'Hadding rootfiles in', jobdir

        jobdir = abspath( jobdir )

        outputdir = 'HADDED_' + basename(jobdir)
        outputdir = outputdir.replace( '_'+channel, '' )
        outputdir = join( startDir, outputdir )
        if not isdir(outputdir): os.makedirs(outputdir)


        for iBin in xrange(getattr( numbers, channel+'_nBins' )):
            rootfiles = glob( join( jobdir, 'higgsCombineSCAN_{0}_Bin{1}.POINTS.*.MultiDimFit.mH125.root'.format( channel, iBin ) ) )
            outputfile = 'Hadded_{0}_Bin{1}.root'.format( channel, iBin )
            outputfile = join( outputdir, outputfile )

            print
            print 'Hadding Bin', iBin, 'input rootfiles:'
            for i in rootfiles:
                print '    ' + basename(i)
            print '    into', basename(outputdir) + '/' + basename(outputfile)


            cmd = 'hadd -f '
            cmd += outputfile + ' '
            cmd += ' '.join( rootfiles )

            print cmd

            os.system(cmd)




########################################
# End of Main
########################################
if __name__ == "__main__":
    main()