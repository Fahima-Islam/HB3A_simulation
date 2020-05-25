from mcni import neutron_storage as ns
import numpy as np


def mcstas2mcvine(inpath, outpath):
    """
     converting mcstas neutron events file to mcvine neutron events file
    Parameters
    ----------
    inpath: string
        path where mcstas event file exist
    outpath:string
        path where mcvine event file will be saved

    Returns
    -------

    """
    arr = np.loadtxt(inpath)
    N = len(arr)
    newarr = np.zeros((N, 10), dtype=float)
    newarr[:, list(range(10))] = arr[:, [1,2,3, 4,5,6, 8,9, 7, 0]]
    neutrons = ns.neutrons_from_npyarr(newarr)
    ns.dump(neutrons, outpath)

