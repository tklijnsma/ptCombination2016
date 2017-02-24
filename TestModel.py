
from HiggsAnalysis.CombinedLimit.PhysicsModel import *

import re
import ROOT

class TestModel( PhysicsModel ):
    ''' Model used to unfold differential distributions '''

    def __init__(self):
        PhysicsModel.__init__(self)
        self.Range=[0.,4]
        self.mHRange=[]
        self.debug=1
        self.mass=0

        self.importMuExpressions = True
        self.isHZZ               = False

        # ======================================
        # HZZ parameters

        # self.Range=[0.,10]
        self.fracRange=[0.,0.5]                
        # self.mHRange=[20,1000]
        # self.mass=125.0
        # self.debug=1

        # All of these should already be included



    def chapter( self, text ):
        print
        print '='*70
        print text
        print '='*70
        print



    def setPhysicsOptions(self,physOptions):

        # Interpreting the passed physics options to text2workspace.py


        # ======================================
        # From Thomas

        self.chapter( 'Setting physics options' )

        # Function that can read "--PO Hgg_nBins=8" kind of physics options (lists have to be done manually)
        def readOption( physOption, parName, type=float ):
            if physOption.startswith(parName):
                if type==bool :
                    parValue = eval(physOption.replace(parName,'').replace('=',''))
                else:
                    parValue = type( physOption.replace(parName,'').replace('=','') )
                setattr( self, parName, parValue )
                print 'Registered physics option: model.{0} = {1}'.format( parName, parValue )
                return True
            return False


        for physOption in physOptions:

            # All the simple options
            if   readOption( physOption, 'Fine_nBins', type=int ): continue
            elif readOption( physOption, 'Hgg_nBins', type=int ): continue
            elif readOption( physOption, 'HZZ_nBins', type=int ): continue
            elif readOption( physOption, 'HWW_nBins', type=int ): continue
            elif readOption( physOption, 'importMuExpressions', type=bool ): continue
            elif readOption( physOption, 'isHZZ', type=bool ): continue
            elif readOption( physOption, 'mass' ): continue


            # main POI scan range; should be relatively small HZZ
            elif physOption.startswith("range="):

                self.Range=physOption.replace("range=","").split(":")

                if len(self.Range)!=2: 
                    raise RunTimeError, "Range require minimal and maximal values: range=min:max"

                print "POI scan range is set to ", self.Range


            # Higgs mass range to fit
            elif physOption.startswith("higgsMassRange="):

                print "setting higgs mass range floating:",physOption.replace("higgsMassRange=","").split(":")
                
                self.mHRange=physOption.replace("higgsMassRange=","").split(",")

                #checks
                if len(self.mHRange) != 2:
                    raise RuntimeError, "Higgs mass range definition requires two extrema"
                elif float(self.mHRange[0]) >= float(self.mHRange[1]):
                    raise RuntimeError, "Extrema for Higgs mass range defined with inverterd order. Second must be larger the first"

            else:
                print 'WARNING: physics option "{0}" is not known and thus not saved as an attribute in the model'.format(physOption)


    def factoryHZZfunctions( self ):

        for iBin in xrange(self.HZZ_nBins):

            self.modelBuilder.factory_((
                'expr::Sigma_trueH4eBin{0}('
                '"@0*@3*@1*@2", '
                'SigmaBin{0}, fracSM4eBin{0}, K1Bin{0}, SigmaSMBin{0} )'
                ).format( iBin ) )

            self.modelBuilder.factory_((
                'expr::Sigma_trueH4muBin{0}('
                '"@0*@5*(1.0-@1*@2)*@3*@4/(1.0-@1)", '
                'SigmaBin{0}, fracSM4eBin{0}, K1Bin{0}, K2Bin{0}, fracSM4muBin{0}, SigmaSMBin{0} )'
                ).format( iBin ) )

            self.modelBuilder.factory_((
                'expr::Sigma_trueH2e2muBin{0}('
                '"@0*@5*(1.0-@1*@2)*(1.0-@3*@4/(1.0-@1))", '
                'SigmaBin{0}, fracSM4eBin{0}, K1Bin{0}, K2Bin{0}, fracSM4muBin{0}, SigmaSMBin{0} )'
                ).format( iBin ) )



    def doParametersOfInterest(self):

        self.chapter( 'Setting parameters of interest' )

        # Central list of POInames that will be passed to the modelBuilder
        POInames = []


        # ======================================
        # Manually import objects from the input workspaces
        # This is STRONGLY against the designed workflow

        # Get the filled input workspace
        filledWsPath = '/afs/cern.ch/work/t/tklijnsm/Combinations/CMSSW_7_1_5/src/combination3/input/expressions.root'
        filledWsFp = ROOT.TFile.Open( filledWsPath )
        filledWs = filledWsFp.Get('w')

        if self.importMuExpressions:

            print 'Importing premade expressions from ' + filledWsPath

            getattr( self.modelBuilder.out ,'import')(
                filledWs.components(), ROOT.RooFit.RecycleConflictNodes(), ROOT.RooFit.Silence()
                )

            # This part is still needed
            self.factoryHZZfunctions()

            for iBinFine in xrange(self.Fine_nBins):
                POInames.append( 'FineBin{0}_Mu'.format(iBinFine) )


        elif self.isHZZ:

            print 'Creating all variables and expressions necessary for HZZ'

            for iBin in xrange(self.HZZ_nBins):

                fracSM4e = self.modelBuilder.out.var("fracSM4eBin{0}".format(iBin)).getVal()
                fracSM4mu = self.modelBuilder.out.var("fracSM4muBin{0}".format(iBin)).getVal()

                if self.modelBuilder.out.var("SigmaBin{0}".format(iBin)):
                    self.modelBuilder.out.var("SigmaBin{0}".format(iBin)).setRange( float(self.Range[0]), float(self.Range[1]) )
                    self.modelBuilder.out.var("SigmaBin{0}".format(iBin)).setConstant(False)
                else :
                    self.modelBuilder.doVar("SigmaBin%d[1, %s,%s]" % (iBin, self.Range[0],self.Range[1]))

                if self.modelBuilder.out.var("K1Bin{0}".format(iBin)):
                    self.modelBuilder.out.var("K1Bin{0}".format(iBin)).setRange(0.0, 1.0/fracSM4e)
                    self.modelBuilder.out.var("K1Bin{0}".format(iBin)).setConstant(False)
                else :
                    self.modelBuilder.doVar("K1Bin%d[1.0,%s,%s]" % (iBin, 0.0, 1.0/fracSM4e))

                if self.modelBuilder.out.var("K2Bin{0}".format(iBin)):
                    self.modelBuilder.out.var("K2Bin{0}".format(iBin)).setRange(0.0, (1.0-fracSM4e)/fracSM4mu)
                    self.modelBuilder.out.var("K2Bin{0}".format(iBin)).setConstant(False)
                else :
                    self.modelBuilder.doVar("K2Bin%d[1.0,%s,%s]" % (iBin, 0.0, (1.0-fracSM4e)/fracSM4mu))

                if iBin>=0:
                    POInames.append( "SigmaBin%d,"%iBin )
                    POInames.append( "K1Bin%d,"%iBin )
                    POInames.append( "K2Bin%d,"%iBin )

                # print 'Creating the Sigma_trueH(channel)Bin{0} expressions'.format(iBin)
                self.factoryHZZfunctions()

                # Create HZZBinX_Mu for consistency with other channels;
                # --> Fitted parameter is still SigmaBinX, since only a RooRealVar can be the fitted par
                self.modelBuilder.factory_((
                    'expr::HZZBin{0}_Mu('
                    '"(@0)", '
                    'SigmaBin{0} )'
                    ).format( iBin ) )

        else:

            print 'Creating simple RooRealVars for the yieldScales'

            for iBin in xrange(self.Hgg_nBins):

                if  self.modelBuilder.out.var( "HggBin{0}_Mu".format(iBin)):
                    self.modelBuilder.out.var( "HggBin{0}_Mu".format(iBin)).setRange( float(self.Range[0]), float(self.Range[1]) )
                    self.modelBuilder.out.var( "HggBin{0}_Mu".format(iBin)).setConstant(False)
                else:
                    self.modelBuilder.doVar(   "HggBin{0}_Mu[ 1, {1}, {2}]".format( iBin, self.Range[0],self.Range[1] ) )

                POInames.append( "HggBin{0}_Mu".format(iBin) )


            for iBin in xrange(self.HWW_nBins):

                if  self.modelBuilder.out.var( "HWWBin{0}_Mu".format(iBin)):
                    self.modelBuilder.out.var( "HWWBin{0}_Mu".format(iBin)).setRange( float(self.Range[0]), float(self.Range[1]) )
                    self.modelBuilder.out.var( "HWWBin{0}_Mu".format(iBin)).setConstant(False)
                else:
                    self.modelBuilder.doVar(   "HWWBin{0}_Mu[ 1, {1}, {2}]".format( iBin, self.Range[0],self.Range[1] ) )

                POInames.append( "HWWBin{0}_Mu".format(iBin) )


        filledWsFp.Close()


        # # ======================================
        # # Define the HZZ bins

        # self.chapter( 'Creating the HZZBinX_Mu expression' )

        # for iBin in xrange( self.HZZ_nBins ):


        #     ########################################
        #     # Build the per channel Mus only for HZZ workspaces
        #     ########################################

        #     if self.modelBuilder.out.function( 'SigmaBin{0}'.format(iBin) ):


        #     else:
        #         print 'Not creating the Sigma_trueH(channel)Bin{0} expressions'.format(iBin)



        # ======================================
        # Wrap up


        self.modelBuilder.doSet( 'POI', ','.join(POInames) )


        
        self.chapter( 'Doing getYieldScale' )



    def getYieldScale( self, bin, process ):

        yieldScale = 1

        def p( yieldScale ):
            print 'Getting yield scale: bin: {0:30} | process: {1:16} | yieldScale: {2}'.format( bin, process, yieldScale )


        if not self.DC.isSignal[process]:
            p( 1 )
            return 1
        
        # Set processes with certain strings to 1.0
        yieldOneProcesses = [ 'bkg', 'fakeH', 'out_trueH' ]

        for yieldOneProces in yieldOneProcesses:
            if yieldOneProces in process:
                p( 1 )
                return 1


        # ======================================
        # Passing all these selections, assume the process is a bin

        isBin = re.search( r'Bin(\d)', process )
        if not isBin: raise RuntimeError, 'Unknown bin/process combination: bin = {0}, process = {1}'.format( bin, process )
        iBin = int(isBin.group(1))


        if bin.startswith( 'Hgg' ):

            if iBin == self.Hgg_nBins-1:
                # This is the overflow bin
                p( 1 )
                return 1
            else:
                p( 'HggBin{0}_Mu'.format(iBin) )
                return 'HggBin{0}_Mu'.format(iBin)


        elif bin.startswith( 'HWW' ):

            if iBin == self.HWW_nBins-1:
                # This is the overflow bin
                p( 1 )
                return 1
            else:
                p( 'HWWBin{0}_Mu'.format(iBin) )
                return 'HWWBin{0}_Mu'.format(iBin)


        elif bin.startswith( 'HZZ' ):

            Processes = []
            for Boson in ['H', 'Z']:
                for iBin in xrange(self.HZZ_nBins):
                    for channel in ['4e', '4mu', '2e2mu']:       
                        Processes += ['true'+Boson+channel+'Bin'+str(iBin)]
            
            if process in Processes:
                p( 'Sigma_'+process )
                return 'Sigma_'+process
            else:
                print 'WARNING: unknown HZZ process: ', process
                p( 1 )
                return 1


        else:
            p( 1 )
            return 1



testModel=TestModel()

