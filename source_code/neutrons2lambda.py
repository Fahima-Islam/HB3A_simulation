import numpy as np
from mcni.utils import conversion
from mcni.neutron_storage import readneutrons_asnpyarr as rdn

def process(neutronspath,neutron_properties_flag =False):
    r"""
        calculating d spacing from the scattering events
       ----------
       neutronspath : str
           the path where the scattered neutron events are saved.

       Returns
       -------
       tuple
        Three float numbers:
        ``(lambda in angstrom, d spacing in angstrom, probability of the scattered neutrons)``

        """

    narr = rdn(neutronspath) # neutron events
    vx = narr[:,3]; vy = narr[:,4]; vz = narr[:,5]
    p = narr[:,9]
    v = (vx*vx + vy*vy +vz*vz)**.5 ## calculating velocity vector
    cos2theta = vz/v # calculating the scattering angle
    lamda = 2 * np.pi / conversion.V2K / v # calculating the wavelength
    sintheta = np.sqrt((1 - cos2theta) / 2)
    d = lamda / (2 * sintheta) # calculating the d-spacing
    if neutron_properties_flag:
        return (narr)
    else:
        return lamda, d, p

def convert2histogram(x_values, y_values, bins):
    r"""
        Converting the data to histogram
       ----------
       x_values : array_like
           Input data. The histogram is computed over the flattened array.
       y_values:  array_like,
            An array of the same shape as a.
            Each value in a only contributes its associated weight towards the bin count (instead of 1).
       bins : int or sequence of scalars or str, optional.
            If bins is an int, it defines the number of equal-width bins in the given range (10, by default).
            If bins is a sequence, it defines a monotonically increasing array of bin edges,
            including the rightmost edge, allowing for non-uniform bin widths.

       Returns
       -------
       tuple
        Three float numbers:
        ``(x in bins, y in bins, associated error)``

        """

    I_d, dbb = np.histogram(x_values, bins=bins, weights=y_values)
    errorbar_sqr_I_d, edgesS = np.histogram(x_values, bins=bins, weights=y_values * y_values)
    error = np.sqrt(errorbar_sqr_I_d )
    dcs = (dbb[1:] + dbb[:-1]) / 2
    return(dcs, I_d, error)
