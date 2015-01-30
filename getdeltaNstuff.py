import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

def getNFliq(NIce,Nbar,Nstar,Nmono,phi):
    NFliq = Nbar+Nstar*np.sin(NIce/Nmono*2*np.pi-phi)
    return NFliq


def getdeltaN(NIcep,NFliqp,Nbar,Nstar,Nmono,phi):
    deltaN = 0.0
    for i in range(8):
        deltaN = getNFliq(NIcep-deltaN,Nbar,Nstar,Nmono,phi)-NFliqp
    deltaN
    return deltaN


def getdeltaN2(NIcep,NFliqp,Nbar,Nstar,Nmono,phi):
    Ntotp = NIcep+NFliqp
    Ntotref, Niceref, Fliqref = getresponsecurve(Nbar,Nstar,Nmono,phi)
    NFliq = np.interp(Ntotp,Ntotref,Fliqref)
    deltaN = NFliq - NFliqp
    return deltaN


def getresponsecurveinterp(NIcep,NFliqp,Nbar,Nstar,Nmono,phi):
    Ntotp = NIcep+NFliqp
    Ntottest, Nicetest, Fliqtest = getresponsecurve(Nbar,Nstar,Nmono,phi)
    NFliq = np.interp(Ntotp,Ntottest,Fliqtest)
    NIce = np.interp(Ntotp,Ntottest,Nicetest)
    return NFliq, NIce


def getresponsecurve(Nbar=None,Nstar=None,Nmono=None,phi=None):
    # This lays out an x-axis that spans one step
    Nicetest = np.linspace(0,1)
    Fliqtest = getNFliq(Nicetest,Nbar,Nstar,Nmono,phi)
    Ntottest = Nicetest + Fliqtest
    return Ntottest, Nicetest, Fliqtest
    
    
def getNiceoffset(Nbar=None,Nstar=None,Nmono=None,phi=None):

    # Get the unit response curve
    Ntottest, Nicetest, Fliqtest = getresponsecurve(Nbar,Nstar,Nmono,phi)

    # This is for the iterative scheme with a "typical" displacement
    Fliqlast = Fliqtest + 0.03
    deltaN = getdeltaN(Nicetest,Fliqlast,Nbar,Nstar,Nmono,phi)
    Fliqapprox = Fliqlast + deltaN
    Niceapprox = Nicetest - deltaN
    Ntotapprox = Nicetest+Fliqlast
    #deltaN = getdeltaN2(Nicetest,Fliqlast,Nbar,Nstar,Nmono,phi)
    #Fliqinterp = Fliqlast + deltaN
    #Niceinterp = Nicetest - deltaN
    #Ntotinterp = Fliqinterp + Niceinterp

    # Get the point at which Fliq is a minumum
    Imin = np.argmin(Fliqtest)
    Niceoffset = Nicetest[Imin]; #print Imin, Niceoffset
    test  = (Nicetest-Niceoffset+1).astype(int)
    dtestdt = np.diff(test)
    IedgeP = mlab.find(dtestdt > 0); #print IedgeP
    IedgeN = mlab.find(dtestdt < 0)+1; #print IedgeN

    # Graphing
    plt.figure(4)
    plt.clf()
    plt.plot(Ntottest,Nicetest,'b',Ntottest,Fliqtest,'g')
    plt.plot(Ntotapprox,Niceapprox,'b:',Ntotapprox,Fliqapprox,'g:')
    #plt.plot(Ntotinterp,Niceinterp,'+',Ntotinterp,Fliqinterp,'g+')
    plt.plot(Ntottest[IedgeP],Nicetest[IedgeP],'o')
    plt.plot(Ntottest[IedgeN],Nicetest[IedgeN],'x')
    plt.plot(Ntottest[IedgeP],Fliqtest[IedgeP],'o')
    plt.plot(Ntottest[IedgeN],Fliqtest[IedgeN],'x')
    plt.grid('on')    
    return Niceoffset



# NIcep = 0.0
# print "exact result:", NIcep, getNFliq(NIcep,Nbar,Nstar,Nmono,phi)
# NFliqp = getNFliq(NIcep,Nbar,Nstar,Nmono,phi)-.05; print "Starting with:", NIcep, NFliqp
# deltaN = getdeltaN(NIcep,NFliqp,Nbar,Nstar,Nmono,phi)
# NFliq_new = NFliqp + deltaN
# NIce_new = NIcep - deltaN
# print NFliq_new, getNFliq(NIce_new,Nbar,Nstar,Nmono,phi), 
# (NFliq_new - getNFliq(NIce_new,Nbar,Nstar,Nmono,phi))/NFliq_new*100