import os
template = """<?xml version="1.0"?>

<!DOCTYPE scatterer>

<!-- weights: absorption, scattering, transmission -->
<homogeneous_scatterer mcweights="{absorption}, {scattering}, {transmission}">

  {kernel_blocks}

</homogeneous_scatterer>

"""
def _kernel_block(kernel_type, Dd_over_d= None, DebyeWaller_factor=None, scatterer=None, E=None, S_Q_E=None,Qmin=None, Qmax=None):
    """

    Parameters
    ----------
    kernel_type
    Dd_over_d
    DebyeWaller_factor
    scatterer
    E
    S_Q_E
    Qmin
    Qmax

    Returns
    -------

    """
    if kernel_type == "elastic":
        return """  <SimplePowderDiffractionKernel Dd_over_d="{Dd_over_d}" DebyeWaller_factor="{DebyeWaller_factor}" peaks-py-path="{scatterer}_peaks.py">
  </SimplePowderDiffractionKernel>
        """.format(Dd_over_d=Dd_over_d, DebyeWaller_factor=DebyeWaller_factor, scatterer=scatterer)

    elif kernel_type == "inelastic":
        return """
  <E_Q_Kernel
  E_Q="{E}"
  S_Q="{S_Q_E}"
  Qmin="{Qmin}"
  Qmax="{Qmax}"
   />
              """.format(E=E, S_Q_E=S_Q_E, Qmin=Qmin, Qmax=Qmax)
    else:
        raise NameError('"elastic" or "inelastic" type is required')


def makeSKXML(kernel_type, path_ToSave_ScatteringKernel, scatterer_type_name,scatterer=None,absorption=0,scattering=1,transmission=3,
              Dd_over_d=1e-5, DebyeWaller_factor=1, E=None, S_Q_E=None,Qmin=None, Qmax=None ):
   """
   making scattering kernel xml file

                      Parameters
                      ----------
                      kernel_type: string
                        if the 'elastic or inelastic' kernel to specify
                      scatterer: string
                         peaks location of the scatterer
                      path_ToSave_ScatteringKernel : string
                            path where the scattering kernel file would be saved
                      scatterer_type_name: string
                          name of the scatterer type (sample/ cell)
                      absorption: int
                            weight for absorption
                      transmission: int
                            weight for transmission
                      Dd_over_d: float
                            d spacing resolution in Angstrom
                      DebyeWaller_factor: int
                            Debye Waller factor
                      """

   kernel_blocks = _kernel_block(kernel_type, Dd_over_d= Dd_over_d, DebyeWaller_factor=DebyeWaller_factor,
                                 scatterer=scatterer, E=E,
                                 S_Q_E=S_Q_E,Qmin=Qmin, Qmax=Qmax)
   # kernel_blocks = '\n'.join(kernel_blocks)

   text = template.format(absorption=absorption, scattering=scattering,transmission=transmission, kernel_blocks= kernel_blocks)
   with open( os.path.join('{}','{}-scatterer.xml').format(path_ToSave_ScatteringKernel, scatterer_type_name), "w") as sam_new:
       sam_new.write(text)







