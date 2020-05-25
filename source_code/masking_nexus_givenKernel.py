from mantid.simpleapi import *

def masking(path, Masked_detector_path, saved_file_path):
    """

    Parameters
    ----------
    path
    Masked_detector_path
    saved_file_path

    Returns
    -------

    """
    nxs=Load(path)
    masked_detector=Load(Masked_detector_path)
    MaskDetectors(nxs, MaskedWorkspace=masked_detector)
    SaveNexus(nxs, saved_file_path)












