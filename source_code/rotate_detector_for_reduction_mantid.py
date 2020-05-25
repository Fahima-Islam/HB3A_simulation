from mantid.simpleapi import *



def detector_position_for_reduction(path, conf, SNAP_definition_file, saved_file_path):
    """

    Parameters
    ----------
    path
    conf
    SNAP_definition_file
    saved_file_path

    Returns
    -------

    """
    sim=Load(path)

    AddSampleLog(sim, LogName='det_arc1', LogText= '{}'.format(conf.mon1), LogType='Number Series', NumberType='Double')
    AddSampleLog(sim, LogName='det_arc2', LogText= '{}'.format(conf.mon2), LogType='Number Series', NumberType='Double')
    LoadInstrument(sim, Filename=SNAP_definition_file, RewriteSpectraMap='True')
    SaveNexus(sim, saved_file_path)



