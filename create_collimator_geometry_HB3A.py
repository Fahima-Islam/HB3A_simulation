from collimator_geometry import Collimator_geom
import os
DEFAULT_PARENT_DIR = os.path.abspath(os.pardir)
DEFAULT_SAMPLE_PATH = os.path.join (DEFAULT_PARENT_DIR, 'sample')

DEFAULT_COLLIMATOR_GEOMETRY_FILE_NAME = 'coll_geometry'
DEFAULT_COLLIMATOR_GEOMETRY_FILE = os.path.join(DEFAULT_SAMPLE_PATH,
                                                DEFAULT_COLLIMATOR_GEOMETRY_FILE_NAME)

def create (detector_width= 126 , detector_height = 340,
            coll_front_end_from_center=20,max_coll_len=298,
            chanel_length=298 ,  vertical_number_channels=5,
            min_channel_size=3.,
            min_channel_wall_thickness=2.0,
            wall_thickness =2.0,
            horizontal_number_channels=26,
            detector_angles=[-45],multiple_collimator=False,
            collimator_Nosupport=True, scad_flag=False,
            outputfile=DEFAULT_COLLIMATOR_GEOMETRY_FILE):
    """
    creating the collimator geometry with specific parameters
    Parameters
    ----------
    coll_front_end_from_center: float
        the distance between the collimator front end and sample center in mm
    max_coll_len: float
        the maximum length of the collimator in mm
    Snap_angle: Bool
        if the detector position of SNAP is used
    detector_width: float
        the width of the collimator at the detector side in mm
    detector_height: float
        the height of the collimator at the detector side in mm
    min_channel_wall_thickness:float
        the minimum thickness of the channel wall in mm
    min_channel_size=float
        minimum size of the channel in mm
    detector_angles:list
        the angular position of collimator with respect to the beam axis in mm
    multiple_collimator: Bool
        if there is more than one collimator then it is True
    collimator_Nosupport: Bool
        if there is no support for the collimator to mount then it is True
    scad_flag: Bool
        if the file will be converted to .scad, then it will be true
    outputfile: string
        file path to save the geometry of the collimator

    Returns
    -------

    """
    coll = Collimator_geom()
    detector_dist_fr_sample_center =coll_front_end_from_center+max_coll_len
    coll.set_constraints(max_coll_height_detector=detector_height,
                          max_coll_width_detector=detector_width,
                          min_channel_wall_thickness=min_channel_wall_thickness,
                          max_coll_length=max_coll_len,
                          min_channel_size=min_channel_size,
                          wall_thickness=wall_thickness,
                          collimator_front_end_from_center=coll_front_end_from_center,
                          detector_dist_fr_sample_center=detector_dist_fr_sample_center,
                          detector_size=detector_width,

                          )

    coll.set_parameters(vertical_number_channels=vertical_number_channels,
                        horizontal_number_channels=horizontal_number_channels,
                         channel_length=chanel_length)

    coll.gen_collimators_xml( detector_angles=detector_angles,multiple_collimator=multiple_collimator,
                              collimator_Nosupport=collimator_Nosupport,
                              scad_flag=scad_flag, coll_file=outputfile)





