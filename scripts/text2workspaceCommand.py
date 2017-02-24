#!/usr/bin/env python
"""
Thomas Klijnsma
"""

########################################
# Imports
########################################

import os, sys, shutil

from Numbers import Numbers



########################################
# Main
########################################

shutil.copyfile(
    os.path.join( os.environ['STARTDIR'], 'TestModel.py' ),
    os.path.join( os.environ['STARTDIR'], '../../bin/slc6_amd64_gcc481/TestModel.py' )
    )

inputDir = os.path.join( os.environ['STARTDIR'], 'input' )

numbers = Numbers()


def main():

    text2workspace( os.path.join( inputDir, 'CARD_all_orig.txt' ), importMuExpressions=True )
    text2workspace( os.path.join( inputDir, 'CARD_HWW.txt' ),      importMuExpressions=False )
    text2workspace( os.path.join( inputDir, 'CARD_Hgg.txt' ),      importMuExpressions=False )
    
    text2workspace(
        os.path.join( inputDir, 'CARD_HZZ.txt' ),
        importMuExpressions=False,
        isHZZ=True
        )

    

def text2workspace( datacard, importMuExpressions, isHZZ=False ):

    cmd = 'text2workspace.py '

    cmd += os.path.abspath( datacard ) + ' '
    cmd += ' -o ' + os.path.abspath( datacard ).replace('.txt','.root') + ' '

    cmd += ' -P TestModel:testModel '    

    if importMuExpressions:
        cmd += '--PO importMuExpressions=True '
    else:
        cmd += '--PO importMuExpressions=False '

    if isHZZ:
        cmd += '--PO isHZZ=True '
    else:
        cmd += '--PO isHZZ=False '


    cmd += '--PO higgsMassRange=122,128 '
    cmd += '--PO Fine_nBins={0} '.format( numbers.Fine_nBins )
    cmd += '--PO Hgg_nBins={0} '.format( numbers.Hgg_nBins + 1 ) # actually breaks without +1 (OOA bin)
    cmd += '--PO HZZ_nBins={0} '.format( numbers.HZZ_nBins )
    cmd += '--PO HWW_nBins={0} '.format( numbers.HWW_nBins )
    cmd += '--PO range=-1.00:4.00 '

    print 'Executing: ', cmd
    os.system(cmd)


########################################
# End of Main
########################################
if __name__ == "__main__":
    main()