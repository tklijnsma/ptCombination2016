#!/usr/bin/env python
"""
Thomas Klijnsma
"""

########################################
# Imports
########################################

import os


########################################
# Main
########################################

def main():
    
    numbers = Numbers()

    print len(numbers.Fine_Binning)-1, len(numbers.Hgg_Binning)-1, len(numbers.HZZ_Binning)-1, len(numbers.HWW_Binning)-1



class Numbers():

    def __init__(self):

        self.channels = [ 'Fine', 'Hgg', 'HZZ', 'HWW' ]

        self.Fine_Binning  = [ 0, 15, 30, 45, 85, 125, 165, 200, 300 ]
        self.Hgg_Binning   = [ 0, 15, 30, 45, 85, 125, 200, 300 ]
        self.HZZ_Binning   = [ 0, 15, 30, 85, 200, 300 ]
        self.HWW_Binning   = [ 0, 15, 45, 85, 125, 165, 300 ]

        self.Fine_nBins    = len( self.Fine_Binning ) - 1
        self.Hgg_nBins     = len( self.Hgg_Binning ) - 1
        self.HZZ_nBins     = len( self.HZZ_Binning ) - 1
        self.HWW_nBins     = len( self.HWW_Binning ) - 1


        self.HggMergemap   = self.determineMergeMap( self.Fine_Binning, self.Hgg_Binning )
        self.HZZMergemap   = self.determineMergeMap( self.Fine_Binning, self.HZZ_Binning )
        self.HWWMergemap   = self.determineMergeMap( self.Fine_Binning, self.HWW_Binning )


        # ======================================
        # Cross sections and efficiencies in fine binning

        self.SMXS_FineBinning = {

            'Hgg' : [
                0.4337,          # 0 - 15
                0.4697,          # 15 - 30
                0.2860,          # 30 - 45
                0.1232,          # 45 - 85
                0.0376,          # 85 - 125
                0.0110*8./15.,   # 125 - 165
                0.0110*7./15.,   # 165 - 200
                0.3157,          # 200 - 13000
                ],

            'HZZ' : [
                0.28330705405589995,        # 0 - 15
                0.2827145731139,            # 15 - 30
                0.1749759087399,            # 30 - 45
                0.2366889062789,            # 45 - 85
                0.0959907248256,            # 85 - 125
                0.06296804788919999*8./15., # 125 - 165
                0.06296804788919999*7./15., # 165 - 200
                0.024635112567909997,       # 200 - 13000
                ],


            'HZZ_4e' : [
                0.0708253178238,            # 0 - 15
                0.0725692875204,            # 15 - 30
                0.0446390688887,            # 30 - 45
                0.0605045829914,            # 45 - 85
                0.0242267591396,            # 85 - 125
                0.0159373534927*8./15.,     # 125 - 165
                0.0159373534927*7./15.,     # 165 - 200
                0.0059655598938,            # 200 - 13000
                ],

            'HZZ_4mu' : [
                0.0805713648401,            # 0 - 15
                0.0794293472885,            # 15 - 30
                0.048485692192,             # 30 - 45
                0.0665107495195,            # 45 - 85
                0.0268843477724,            # 85 - 125
                0.0175912312341*8./15.,     # 125 - 165
                0.0175912312341*7./15.,     # 165 - 200
                0.00668824203941,           # 200 - 13000
                ],

            'HZZ_2e2mu' : [
                0.131910371392,             # 0 - 15
                0.130715938305,             # 15 - 30
                0.0818511476592,            # 30 - 45
                0.109673573768,             # 45 - 85
                0.0448796179136,            # 85 - 125
                0.0294394631624*8./15.,     # 125 - 165
                0.0294394631624*7./15.,     # 165 - 200
                0.0119813106347,            # 200 - 13000
                ],


            'HWW' : [
                0.132106,       # 0 - 15
                0.127684,       # 15 - 30
                0.0758239,      # 30 - 45
                0.0916542,      # 45 - 85
                0.0315076,      # 85 - 125
                0.0126234,      # 125 - 165
                0.0117063*0.6,  # 165 - 200
                0.0117063*0.4,  # 200 - 13000
                ],

            }


        self.Eff_FineBinning = {

            'Hgg' : [
                1.0,   # 0 - 15
                1.0,   # 15 - 30
                1.0,   # 30 - 45
                1.0,   # 45 - 85
                1.0,   # 85 - 125
                1.0,   # 125 - 165
                1.0,   # 165 - 200
                1.0,   # 200 - 13000
                ],

            'HZZ' : [
                0.642557154267,       # 0 - 15
                0.641977055267,       # 15 - 30
                0.630331261101,       # 30 - 45
                0.6427573624746666,   # 45 - 85
                0.6530151732593333,   # 85 - 125
                0.6832155872226666,   # 125 - 165
                0.6832155872226666,   # 165 - 200
                0.675051714188,       # 200 - 13000
                ],

            'HZZ_4e' : [
                0.0708253178238,      # 0 - 15
                0.0725692875204,      # 15 - 30
                0.0446390688887,      # 30 - 45
                0.0605045829914,      # 45 - 85
                0.0242267591396,      # 85 - 125
                0.0159373534927,      # 125 - 165
                0.0159373534927,      # 165 - 200
                0.0059655598938,      # 200 - 13000
                ],

            'HZZ_4mu' : [
                0.0805713648401,      # 0 - 15
                0.0794293472885,      # 15 - 30
                0.048485692192,       # 30 - 45
                0.0665107495195,      # 45 - 85
                0.0268843477724,      # 85 - 125
                0.0175912312341,      # 125 - 165
                0.0175912312341,      # 165 - 200
                0.00668824203941,     # 200 - 13000
                ],

            'HZZ_2e2mu' : [
                0.131910371392,       # 0 - 15
                0.130715938305,       # 15 - 30
                0.0818511476592,      # 30 - 45
                0.109673573768,       # 45 - 85
                0.0448796179136,      # 85 - 125
                0.0294394631624,      # 125 - 165
                0.0294394631624,      # 165 - 200
                0.0119813106347,      # 200 - 13000
                ],



            'HWW' : [
                0.102843,     # 0 - 15
                0.100349,     # 15 - 30
                0.0956815,    # 30 - 45
                0.0949129,    # 45 - 85
                0.0980958,    # 85 - 125
                0.0987143,    # 125 - 165
                0.103491,     # 165 - 200
                0.103491,     # 200 - 13000
                ],




            }


        # Will frequently need cross section times efficiency as well
        self.XSTimesEff_FineBinning = {}
        for key in self.SMXS_FineBinning.keys():
            self.XSTimesEff_FineBinning[key] = (
                [ xs*eff for xs, eff in zip( self.SMXS_FineBinning[key], self.Eff_FineBinning[key] ) ]
                )




        # ======================================
        # Cross sections and efficiencies in Hgg binning

        self.SMXS_HggBinning = {

            'Hgg' : [
                0.4337, 0.4697, 0.2860, 0.1232, 0.0376, 0.0110, 0.3157
                ],

            'HZZ_4e' : [
                0.0708253178238, 0.0725692875204, 0.0446390688887, 0.0605045829914, 0.0242267591396, 0.0159373534927, 0.0059655598938
                ],

            'HZZ_4mu' : [
                0.0805713648401, 0.0794293472885, 0.048485692192, 0.0665107495195, 0.0268843477724, 0.0175912312341, 0.00668824203941
                ],

            'HZZ_2e2mu' : [
                0.131910371392, 0.130715938305, 0.0818511476592, 0.109673573768, 0.0448796179136, 0.0294394631624, 0.0119813106347
                ],

            }

        self.SMXS_HggBinning['HZZ'] = [ i+j+k for i,j,k in zip(
            self.SMXS_HggBinning['HZZ_4e'], self.SMXS_HggBinning['HZZ_4mu'], self.SMXS_HggBinning['HZZ_2e2mu'] ) ]


        self.Eff_HggBinning = {

            # 'Hgg' : [
                
            #     ],

            'HZZ_4e' : [
                0.467989691456, 0.468957695823, 0.454304079204, 0.460849924288, 0.484995481856, 0.520122774252, 0.499953284016,
                ],

            'HZZ_4mu' : [
                0.832133782583, 0.83369201827, 0.809706542204, 0.839046212191, 0.829209415272, 0.850592570452, 0.824898832682, 
                ],

            'HZZ_2e2mu' : [
                0.627547988762, 0.623281451708, 0.626983161895, 0.628375950945, 0.64484062265, 0.678931416964, 0.700303025866,             
                ],

            }

        self.Eff_HggBinning['HZZ'] = [ (i+j+k)/3.0 for i,j,k in zip(
            self.Eff_HggBinning['HZZ_4e'], self.Eff_HggBinning['HZZ_4mu'], self.Eff_HggBinning['HZZ_2e2mu'] ) ]


        # ======================================
        # Cross sections and efficiencies in HZZ binning

        self.SMXS_HZZBinning = {

            'HZZ_4e' : [
                0.0708253178238, 0.0725692875204, 0.10514365188, 0.0401641126322, 0.0059655598938,            
                ],

            'HZZ_4mu' : [
                0.0805713648401, 0.0794293472885, 0.114996441712, 0.0444755790065, 0.00668824203941,
                ],

            'HZZ_2e2mu' : [
                0.131910371392, 0.130715938305, 0.191524721427, 0.0743190810761, 0.0119813106347, 
                ],

            }

        self.SMXS_HZZBinning['HZZ'] = [ i+j+k for i,j,k in zip(
            self.SMXS_HZZBinning['HZZ_4e'], self.SMXS_HZZBinning['HZZ_4mu'], self.SMXS_HZZBinning['HZZ_2e2mu'] ) ]


        self.Eff_HZZBinning = {

            'HZZ_4e' : [
                0.467989691456, 0.468957695823, 0.458070865121, 0.498934195784, 0.499953284016,             
                ],

            'HZZ_4mu' : [
                0.832133782583, 0.83369201827, 0.826675792839, 0.837667001113, 0.824898832682,             
                ],

            'HZZ_2e2mu' : [
                0.627547988762, 0.623281451708, 0.627780720307, 0.658344754682, 0.700303025866,             
                ],

            }

        self.Eff_HZZBinning['HZZ'] = [ (i+j+k)/3.0 for i,j,k in zip(
            self.Eff_HZZBinning['HZZ_4e'], self.Eff_HZZBinning['HZZ_4mu'], self.Eff_HZZBinning['HZZ_2e2mu'] ) ]



        # ======================================
        # Cross sections and efficiencies in HWW binning


        self.SMXS_HWWBinning = {

            'HWW' : [
                132.106, 203.508, 91.6542, 31.5076, 12.6234, 11.7063
                ],

            }


        self.Eff_HWWBinning = {

            'HWW' : [
                0.102843, 0.0986098, 0.0949129, 0.0980958, 0.0987143, 0.103491
                ],

            }




    def Get(
        self,
        channel,
        binning,
        SMXS_or_Eff,
        ):
        return getattr( self, '{0}_{1}Binning'.format( SMXS_or_Eff, binning ) )[channel]

    def GetXS( self, channel, binning = 'Fine' ):
        return self.Get( channel, binning, 'SMXS' )

    def GetEff( self, channel, binning = 'Fine' ):
        return self.Get( channel, binning, 'Eff' )


    def GetXSTimesEff( self, channel, binning = 'Fine' ):

        if channel != 'HZZ':
            ret = self.Get( channel, binning, 'XSTimesEff' )
        else:
            l_4e    = self.Get( 'HZZ_4e', binning, 'XSTimesEff' )
            l_4mu   = self.Get( 'HZZ_4mu', binning, 'XSTimesEff' )
            l_2e2mu = self.Get( 'HZZ_2e2mu', binning, 'XSTimesEff' )
            ret = [ i+j+k for i,j,k in zip( l_4e, l_4mu, l_2e2mu ) ]

        return ret



    def determineMergeMap( self, fine, coarse ):

        nBinsCoarse = len(coarse) - 1
        nBinsFine   = len(fine) - 1

        mergemap = {}

        for iBinCoarse in xrange(nBinsCoarse):

            coarseLeft  = coarse[iBinCoarse]
            coarseRight = coarse[iBinCoarse+1]

            if not coarseLeft in fine or not coarseRight in fine:
                print 'Can not merge bins; disagreement in bin boundaries'
                return

            iBinFine_Left  = fine.index(coarseLeft)
            iBinFine_Right = fine.index(coarseRight)

            mergemap[iBinCoarse] = range( iBinFine_Left, iBinFine_Right )

        return mergemap



        # ======================================
        # HZZ

        # HZZ bins
        # 4e    pT4l0to15       smxs = 0.0708253178238   smeff = 0.467989691456
        # 4e    pT4l15to30      smxs = 0.0725692875204   smeff = 0.468957695823
        # 4e    pT4l30to85      smxs = 0.10514365188     smeff = 0.458070865121
        # 4e    pT4l85to200     smxs = 0.0401641126322   smeff = 0.498934195784
        # 4e    pT4l200to13000  smxs = 0.0059655598938   smeff = 0.499953284016
        # 4mu   pT4l0to15       smxs = 0.0805713648401   smeff = 0.832133782583
        # 4mu   pT4l15to30      smxs = 0.0794293472885   smeff = 0.83369201827
        # 4mu   pT4l30to85      smxs = 0.114996441712    smeff = 0.826675792839
        # 4mu   pT4l85to200     smxs = 0.0444755790065   smeff = 0.837667001113
        # 4mu   pT4l200to13000  smxs = 0.00668824203941  smeff = 0.824898832682
        # 2e2mu pT4l0to15       smxs = 0.131910371392    smeff = 0.627547988762
        # 2e2mu pT4l15to30      smxs = 0.130715938305    smeff = 0.623281451708
        # 2e2mu pT4l30to85      smxs = 0.191524721427    smeff = 0.627780720307
        # 2e2mu pT4l85to200     smxs = 0.0743190810761   smeff = 0.658344754682
        # 2e2mu pT4l200to13000  smxs = 0.0119813106347   smeff = 0.700303025866

        # Hgg Bins
        # 4e    pT4l0to15       smxs = 0.0708253178238   smeff = 0.467989691456
        # 4e    pT4l15to30      smxs = 0.0725692875204   smeff = 0.468957695823
        # 4e    pT4l30to45      smxs = 0.0446390688887   smeff = 0.454304079204
        # 4e    pT4l45to85      smxs = 0.0605045829914   smeff = 0.460849924288
        # 4e    pT4l85to125     smxs = 0.0242267591396   smeff = 0.484995481856
        # 4e    pT4l125to200    smxs = 0.0159373534927   smeff = 0.520122774252
        # 4e    pT4l200to13000  smxs = 0.0059655598938   smeff = 0.499953284016
        # 4mu   pT4l0to15       smxs = 0.0805713648401   smeff = 0.832133782583
        # 4mu   pT4l15to30      smxs = 0.0794293472885   smeff = 0.83369201827
        # 4mu   pT4l30to45      smxs = 0.048485692192    smeff = 0.809706542204
        # 4mu   pT4l45to85      smxs = 0.0665107495195   smeff = 0.839046212191
        # 4mu   pT4l85to125     smxs = 0.0268843477724   smeff = 0.829209415272
        # 4mu   pT4l125to200    smxs = 0.0175912312341   smeff = 0.850592570452
        # 4mu   pT4l200to13000  smxs = 0.00668824203941  smeff = 0.824898832682
        # 2e2mu pT4l0to15       smxs = 0.131910371392    smeff = 0.627547988762
        # 2e2mu pT4l15to30      smxs = 0.130715938305    smeff = 0.623281451708
        # 2e2mu pT4l30to45      smxs = 0.0818511476592   smeff = 0.626983161895
        # 2e2mu pT4l45to85      smxs = 0.109673573768    smeff = 0.628375950945
        # 2e2mu pT4l85to125     smxs = 0.0448796179136   smeff = 0.64484062265
        # 2e2mu pT4l125to200    smxs = 0.0294394631624   smeff = 0.678931416964
        # 2e2mu pT4l200to13000  smxs = 0.0119813106347   smeff = 0.700303025866



        # ======================================
        # HWW

        # below you can find the SM cross sections and efficiencies (actually acceptances) for HWW.
        # The binning scheme is: [0-15] GeV, [15-45] GeV, [45-85] GeV, [85-125] GeV, [125-165] GeV, >165 GeV

        # SM xsec bin 1 = 132.106 fb
        # SM xsec bin 2 = 203.508 fb
        # SM xsec bin 3 = 91.6542 fb
        # SM xsec bin 4 = 31.5076 fb
        # SM xsec bin 5 = 12.6234 fb
        # SM xsec bin 6 = 11.7063 fb

        # SM acceptance bin 1 = 0.102843
        # SM acceptance bin 2 = 0.0986098
        # SM acceptance bin 3 = 0.0949129
        # SM acceptance bin 4 = 0.0980958
        # SM acceptance bin 5 = 0.0987143
        # SM acceptance bin 6 = 0.103491


    def GetChannelMusFromFineMus( self, channel, iBin, fineMus ):

        # Get fineBins
        fineBins = getattr( self, '{0}Mergemap'.format(channel) )[iBin]

        # User can give a list of all Mu's or just the Mu's that need to be merged
        if   len(fineMus) == self.Fine_nBins:
            fineMus = fineMus[ fineBins[0] : fineBins[-1]+1 ]
        elif len(fineMus) == len(fineBins):
            pass
        else:
            print 'ERROR: Length of the passed list of fineMus makes no sense'
            print '    {0} bins are to be merged, bins '.format(len(fineBins)), fineBins
            print '    but passed list of fineMus has {0} entries'.format(len(fineMus))
            return

        # If there is nothing to merge, return simply the fineMu
        if len(fineBins) == 1:
            return fineMus[0]


        # ======================================
        # Calculate the merged Mu

        summedXStimesEff = sum( self.GetXSTimesEff(channel)[ fineBins[0]:fineBins[-1]+1 ] )

        # Calculate and up the weighted parts
        mergedMu = 0.
        for iBinFine, fineMu in zip( fineBins, fineMus ):
            weightedPartMu = (
                fineMu *
                self.GetXSTimesEff(channel)[iBinFine] / summedXStimesEff
                )
            mergedMu += weightedPartMu

        return mergedMu
















########################################
# End of Main
########################################
if __name__ == "__main__":
    main()