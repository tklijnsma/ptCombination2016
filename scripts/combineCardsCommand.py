#!/usr/bin/env python
"""
Thomas Klijnsma
"""

########################################
# Imports
########################################

import os, sys


########################################
# Main
########################################


class Datacard():

    def __init__(self, name, card, prefix, ):
        self.name   = name
        self.card   = os.path.abspath( card )
        self.prefix = prefix

        

inputDir = os.path.join( os.environ['STARTDIR'], 'input' )


def main():

    Hgg_orig = Datacard(
        'Hgg_orig',
        card   = os.path.join( inputDir, 'Hgg_orig/cms_hgg_datacard_pToMscaled.txt' ),
        prefix ='Hgg',
        )

    HZZ_orig = Datacard(
        'HZZ_orig',
        card   = os.path.join( inputDir, 'HZZ_orig/hzz4l_all_8TeV_xs_pT4l_bin_v3.txt' ),
        prefix ='HZZ',
        )

    HWW_orig = Datacard(
        'HWW_orig',
        card   = os.path.join( inputDir, 'HWW_orig/hww-19.47fb.mH125.of_pthincl_shape.txt' ),
        prefix ='HWW',
        )


    Hgg_edit = Datacard(
        'Hgg',
        card   = os.path.join( inputDir, 'Hgg_edit/cms_hgg_datacard_pToMscaled.txt' ),
        prefix ='Hgg',
        )

    HZZ_edit = Datacard(
        'HZZ',
        card   = os.path.join( inputDir, 'HZZ_edit/hzz4l_all_8TeV_xs_pT4l_bin_v3.txt' ),
        prefix ='HZZ',
        )

    HWW_edit = Datacard(
        'HWW',
        card   = os.path.join( inputDir, 'HWW_edit/hww-19.47fb.mH125.of_pthincl_shape.txt' ),
        prefix ='HWW',
        )


    # combine( 'CARD_All', cards=[ Hgg_orig, HZZ_orig, HWW_orig ] )
    # combine( 'CARD_ggZZ', cards=[ Hgg_orig, HZZ_orig ] )
    # combine( 'CARD_ggWW', cards=[ Hgg_orig, HWW_orig ] )
    # combine( 'CARD_gg', cards=[ Hgg_orig ] )
    # combine( 'CARD_ZZ', cards=[ HZZ_orig ] )

    # combine( 'CARD_Hgg_preModeled', cards=[ Hgg_edit ] )
    # combine( 'CARD_HZZ_preModeled', cards=[ HZZ_edit ] )
    # combine( 'CARD_HWW_preModeled', cards=[ HWW_orig ] )
    # combine( 'CARD_HggHZZ_preModeled', cards=[ Hgg_edit, HZZ_edit ] )
    # combine( 'CARD_all_preModeled', cards=[ Hgg_edit, HZZ_edit, HWW_orig ] )


    combine( 'CARD_all_orig', cards=[ Hgg_orig, HZZ_orig, HWW_orig ] )

    combine( 'CARD_Hgg', cards=[ Hgg_orig ] )
    combine( 'CARD_HZZ', cards=[ HZZ_orig ] )
    combine( 'CARD_HWW', cards=[ HWW_orig ] )



def combine( outname, cards ):

    cmd = 'combineCards.py '

    for card in cards:

        cmd += ' {0}={1} '.format( card.prefix, card.card )


    if not outname.endswith('.txt'): outname += '.txt'
    outname = os.path.join( inputDir, outname )


    cmd += ' > ' + outname

    print cmd

    os.system( cmd )








########################################
# End of Main
########################################
if __name__ == "__main__":
    main()