from mantid.simpleapi import *

def mantid_reduction(nexus_file, binning):
    """

    Parameters
    ----------
    nexus_file
    binning

    Returns
    -------

    """
    sim=Load(nexus_file)
    I_d=ConvertUnits(sim, Target='dSpacing', AlignBins=True)

    sum_I_d=SumSpectra(I_d)
    hist=Rebin(sum_I_d, Params=binning)


    x_sim = hist.readX(0)
    d_sim = (x_sim[1:] + x_sim[:-1]) / 2
    I_sim = hist.readY(0)
    error=hist.readE(0)
    return(d_sim, I_sim.copy(), error.copy())




