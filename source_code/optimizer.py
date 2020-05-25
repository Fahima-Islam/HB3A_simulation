import os,numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import differential_evolution
from mcvine import run_script
from mantid2mcvine.nxs import template as nxs_template

import convert2nxs as det2nxs
import reduce_nexasdata_using_mantid as red
import rotate_detector_for_reduction_mantid as rot
import masking_nexus_givenKernel as mask
import conf
from peak import Peak
from create_collimator_geometry_HB3A import create as create_collimator_geometry

PARENT_DIR = os.path.abspath(os.pardir)

class Parameter_error(Exception):
    pass

def _safe_path_join(*args):
    """
    join the path and check if the path exist, if path does not exist, raising the error
    Parameters
    ----------
    args: strings
        any path to be joined

    Returns
    -------
        path : string
            path of any file

    """
    path = os.path.join(*args)
    if os.path.exists(os.path.dirname(path)) is False:
        raise IOError('{} does not exist'.format(path))
    return path


DEFAULT_BEAM_PATH=_safe_path_join(PARENT_DIR, 'beam')  # directory for possible mcvine neutron sources
DEFAULT_NEXUS_PATH=_safe_path_join(PARENT_DIR, 'nexus') # directory to save the nexus files
DEFAULT_RESULT_PATH=_safe_path_join(PARENT_DIR, 'results') # directory to save the resulted diffraction 1D curve
DEFAULT_SAMPLE_PATH = _safe_path_join(PARENT_DIR, 'sample') # directory to save the scattering and geometry files for simulation
DEFAULT_COLLIMATOR_GEOMETRY_FILENAME= 'coll_geometry' # default collimator geometry file name
DEFAULT_COLLIMATOR_GEOMETRY_SAVED_PATH = os.path.join(DEFAULT_SAMPLE_PATH, DEFAULT_COLLIMATOR_GEOMETRY_FILENAME) # default file name with path to save collimator geometry
DEFAULT_INSTRUMENT_PATH = os.path.join(PARENT_DIR, 'instruments/myinstrument_multipleDetectors.py') # default instrument script path on which simulation will run


#### DEFAULT peaks for components of clamp cell #################
Si_111_peak = Peak(label='Si 111', d_spacing=3.345, d_min=3., d_max=3.5)
Al_111_peak = Peak(label='Al 111', d_spacing=2.3, d_min=2.2, d_max=2.5)
Cu_111_peak = Peak(label='Cu 111', d_spacing=2.08, d_min=2., d_max=2.1)
Si_220_peak = Peak(label='Si 220', d_spacing=1.9, d_min=1.86, d_max=2)
Cu_200_peak = Peak(label='Cu 200', d_spacing=1.8, d_min=1.78, d_max=1.85)

class Optimizer(object):
    """
    class to create essential steps for optimization of collimator and performing optimization
    """
    @staticmethod ## allows to call this function as it is bound method
    def _validate_names(param_names):
        """
        cheking if the given param names is in the argument of create_collimator _geometry function

        Parameters
        ----------
        param_names: list
            list of string for the collimator geometry to be optimized

        Returns
        -------
        list
            input parameter names if valid

        Raises
        ------
        ValueError
            when the param names is not in the argument list of the create_collimator_geometry.py function
        """
        valid_arguments= {'coll_front_end_from_center', 'max_coll_len', 'detector_width',
                          'detector_height', 'min_channel_wall_thickness', 'min_channel_size' }
        if set(param_names).issubset(valid_arguments) is False:
            raise ValueError("params name is not valid, provide the params name from " + str(valid_arguments))
        return param_names


    def parameters( self, Snap_angle = False, coll_sim = False  ,
                   source_file = 'clampcellSi_scattered-neutrons_1e9_det-50_105_new',
                    beam_path=DEFAULT_BEAM_PATH,
                    sample_path = None,
                    nexus_path = DEFAULT_NEXUS_PATH,
                    result_path=DEFAULT_RESULT_PATH,
                    param_names = None,
                    template =None,
                    instrument_definition_file =None,
                    nodes=20,
                    sampleassembly_fileName = 'collimator_plastic',
                    path_tosave_collimator_geometry = DEFAULT_COLLIMATOR_GEOMETRY_SAVED_PATH,
                    collimator_detector_width = 160,
                    collimator_detector_height = 65.,
                    min_channel_wall_thickness = 1,
                    min_channel_size = 3.,
                    coll_front_end_from_center =17.,
                    channel_length = 298 ,
                    vertical_number_channels =5,
                    wall_thickness = 2,
                    horizontal_number_channels = 26,
                    multiple_collimator = False,
                    collimator_Nosupport = True,
                    scad_flag = False,
                    ncount=1e3, sourceTosample_x = 0.0,
                    sourceTosample_y = 0.0, sourceTosample_z = 0.0, moderatorTosample_z=-42.254,
                    angleMons = [-50, 105] ,
                    angleMon1=45, angleMon2=135,
                    collimator_angles=[-45],
                    max_coll_len = 165,
                    wall_size =1.,
                    sampleTodetector_z=[0.5, 0.5], detector_width=[0.5,0.5], detector_height=[0.5, 0.5],
                    number_pixels_in_height=[256, 256],
                    number_pixels_in_width=[256, 256], number_of_box_in_height=[3,3],
                    number_of_box_in_width=[3,3], masking = False,
                    masked_template = 'coll_plastic_SCAT_masked.nxs',
                    binning=[0.5, 0.01, 4.],number_of_detectors= 1,
                    peaks={'sample':[Si_111_peak,Si_220_peak ], 'cell' : [Al_111_peak,Cu_111_peak,Cu_200_peak]}):

        """
        Defining the parameters to run the simulation and to create the geometry of the collimator
        Parameters
        ----------
        Snap_angle : Boolean
            if the conventional SNAP detector angle is used
        coll_sim: Boolean
            if simulating the collimator
        source_file: string
            the incoming beam file to the sample
        beam_path: string
            path to get the incoming beam file to the sample
        nexus_path: string
            path to save nexus files
        result_path: string
            path to save the diffraction results
        template: string
            path to the nexus template of instrument definition file
        instrument_definition_file: string
            path to the instrument definition file
        nodes: int
            number of nodes to run the simulation
        sampleassembly_fileName: string
            name of the file to save the materials scattering information
        ncount: int
            number of neutrons used for simulation
        sourceTosample_x: float
            source to sample distance along X in m
        sourceTosample_y: float
            source to sample distance along Y in m
        sourceTosample_z: float
            source to sample distance along Z in m
        moderatorTosample_z: float
            moderator to sample distance in m
        angleMons: list
            monitors angular position in degree with respect to beam axis (Z axis)
        collimator_angles: list
            collimator angular position in degree with respect to beam axis (Z axis)
        sampleTodetector_z: list
            sample detector distances in  m
        detector_width: list
            width of the detectors in m
        detector_height: list
            height of the detectors in m
        number_pixels_in_height: int
            number of pixels per bank along height
        number_pixels_in_width: int
            number of pixels per bank along width
        number_of_box_in_height: int
            number of bank along height
        number_of_box_in_width: int
            number of box along width
        masking: bool
            if masking is added or not
        masked_template: string
            the path of the mask
        binning: list
            list of first value, spacing and last value
        number_of_detectors: int
            number of detectors
        peaks: object
            class of the peaks of peaks label, d-spacing value, d minimum and d maximum

        Returns
        -------

        """
        self.beam_path = beam_path
        self.sample_path = sample_path
        self.nexus_path = nexus_path
        self.result_path = result_path
        self.Snap_angle = Snap_angle
        self.coll_sim = coll_sim
        self.source_file = source_file
        self.template = template
        self.instrument_definition_file = instrument_definition_file
        self.sampleassembly_fileName = sampleassembly_fileName
        self.ncount = ncount
        self.sourceTosample_x = sourceTosample_x
        self.sourceTosample_y = sourceTosample_y
        self.sourceTosample_z = sourceTosample_z
        self.angleMons = angleMons
        self.detector_width = detector_width
        self.detector_height = detector_height
        self.sampleTodetector_z = sampleTodetector_z
        self.number_pixels_in_height = number_pixels_in_height
        self.number_of_box_in_height = number_of_box_in_height
        self.number_pixels_in_width = number_pixels_in_width
        self.number_of_box_in_width = number_of_box_in_width
        self.masking = masking
        self.masked_template = masked_template
        self.peaks = peaks
        self.moderatorTosample_z = moderatorTosample_z
        self.number_of_detectors = number_of_detectors
        self.number_of_total_DetectorPixels = 0
        self.binning= binning
        self.collimator_angles = collimator_angles
        self.nodes = nodes
        self.path_tosave_collimator_geometry = path_tosave_collimator_geometry
        self.collimator_detector_width = collimator_detector_width
        self.collimator_detector_height = collimator_detector_height
        self.min_channel_wall_thickness = min_channel_wall_thickness
        self.coll_front_end_from_center = coll_front_end_from_center
        self.min_channel_size = min_channel_size
        self.channel_length = channel_length
        self.vertical_number_channels = vertical_number_channels
        self.wall_thickness = wall_thickness
        self.horizontal_number_channels = horizontal_number_channels
        self.multiple_collimator = multiple_collimator
        self.collimator_Nosupport = collimator_Nosupport
        self.scad_flag = scad_flag
        self.param_names= param_names
        self.max_coll_len = max_coll_len
        self.wall_size = wall_size
        self.angleMon1 = angleMon1
        self.angleMon2 = angleMon2

        for i in range(self.number_of_detectors):
            self.number_of_total_DetectorPixels += self.number_pixels_in_height[i]\
                                              *self.number_of_box_in_height[i]\
                                              *self.number_pixels_in_width[i]\
                                              *self.number_of_box_in_width[i]

    def source_neutrons(self):
        """
        creating the path for the source neutrons to be fed to sample assembly
        Returns
        -------
            scattered neutrons: string
                the path of the scattered neutron to be fed to sample assembly
        """
        scattered = _safe_path_join( self.beam_path, self.source_file )
        return(scattered)

    def create_collimator_geometry(self, params, optimization):
        """
        creating collimator geometry to be optimized
        Parameters
        ----------
        params: class parameters

        Returns
        -------
        output directory name of the simulation: string

        """
        if self.coll_sim:
            kwargs = dict(coll_front_end_from_center=self.coll_front_end_from_center,
                    max_coll_len=self.max_coll_len,
                    chanel_length =self.channel_length,
                    vertical_number_channels = self.vertical_number_channels,
                    wall_thickness = self.wall_thickness,
                    horizontal_number_channels = self.horizontal_number_channels,
                    detector_width=self.collimator_detector_width,
                    detector_height=self.collimator_detector_height,
                    min_channel_wall_thickness=self.wall_size,
                    min_channel_size=self.min_channel_size,
                    detector_angles=self.collimator_angles,
                    multiple_collimator=self.multiple_collimator,
                    collimator_Nosupport=self.collimator_Nosupport,
                    scad_flag=self.scad_flag,
                    outputfile=self.path_tosave_collimator_geometry

                          )
            if optimization:
                ## creating parameter dictionary with parameters name and values to be optimized
                params_to_update = {key: value for key, value in zip(self.param_names, params) }
                ##updating the arguments of create_collimator_geometry.py function with parameters to be optimizd
                kwargs.update(params_to_update)
            create_collimator_geometry(**kwargs)

            name = "length_{}-dist_{}".format(*params)

        else:
            name = self.sampleassembly_fileName
        return name


    def diffraction_pattern_calculation(self, params=[20, 20], instr=DEFAULT_INSTRUMENT_PATH, optimization=False, simdir=None):
        """
        calculated the diffracted neutrons by the object. running the simulation. producing 1D and 2D plot

        Parameters
        ----------
        params: list
            list geometrical parameters to be optimized
        instr: string
            path of the instrument file on which mcvine simulation will run
        simdir: string
            path of the simulation output file

        Returns:
            diffracted intensities, d-spacing, error: tuple
                output result
        -------

        """
        name = self.create_collimator_geometry(params, optimization)

        if simdir is None:
            simdir = os.path.join(
                PARENT_DIR,
                "out/%s" %
                (name))


        run_script.run1_mpi(instr, simdir,
        beam = self.source_neutrons(), ncount = self.ncount,
        nodes = self.nodes,
        angleMons=self. angleMons,
        sample_path = self.sample_path,
        sample = self.sampleassembly_fileName,
        sourceTosample_x = self.sourceTosample_x,
        sourceTosample_y = self.sourceTosample_y,
        sourceTosample_z = self.sourceTosample_z,
        sampleTodetector_z = self.sampleTodetector_z,
        number_detectors = self.number_of_detectors,
        detector_width = self.detector_width,
        detector_height = self.detector_height,
        number_pixels_in_height = self.number_pixels_in_height,
        number_of_box_in_height = self.number_of_box_in_height,
        number_pixels_in_width = self.number_pixels_in_width,
        number_of_box_in_width = self.number_of_box_in_width,
        overwrite_datafiles = True)


        if self.instrument_definition_file is None:
            # calling the existing instrument defition file
            self.instrument_definition_file = _safe_path_join(self.nexus_path, 'SNAP_virtual_Definition.xml')


        if self.template is None:
            # the path where template output will be saved
            self.template=os.path.join(self.nexus_path, 'template.nxs')
            # creating template file
            nxs_template.create(
                self.instrument_definition_file,
                ntotpixels=self.number_of_total_DetectorPixels, outpath=self.template, pulse_time_end=1e5
            )

        # the path where nexus file of simulation will be save
        nexus_file_path = os.path.join(self.nexus_path, '{}.nxs'.format(name))
        # creating the nexus file of the simulation
        det2nxs.create_nexus(simdir, nexus_file_path, self.template, 
                             numberOfPixels=self.number_of_total_DetectorPixels)

        # the path where the nexus file for updated instrument definition file will be saved
        nexus_file_correctDet_path = os.path.join(self.nexus_path, '{}_correctDet.nxs'.format(name))

        #updating the nexus file with proper configuration of instrument detector geometry
        rot.detector_position_for_reduction(nexus_file_path, conf,
                                            self.instrument_definition_file, nexus_file_correctDet_path)

        if self.masking :
            # the path where the masked file will be saved
            masked_file_path = os.path.join(self.nexus_path, '{}_masked.nxs'.format(name))
            mask.masking(nexus_file_correctDet_path, self.masked_template, masked_file_path)

        else:
            masked_file_path = nexus_file_correctDet_path

        binning = self.binning
        # reduction from nexus event file
        d_sim, I_sim, error = red.mantid_reduction(masked_file_path, binning)

        plt.figure()
        plt.errorbar (d_sim, I_sim, error)
        plt.xlabel('d_spacing ()')
        plt.show()

        np.save(os.path.join(self.result_path, 'I_d_{sample}.npy'.format(sample=name)), [d_sim, I_sim, error])

        return (d_sim, I_sim, error)


    def collimator_inefficiency(self, params):
        """
        calculating collimator inefficiency

        Parameters
        ----------
        params: list
            list geometrical parameters to be optimized
        Returns
        -------
        collimator inefficiency: float
            the inverse of the perforamce of the collimator
        """
        dcs, I_d, error = self.diffraction_pattern_calculation (params)
        sample_peaks = self.peaks['sample']
        cell_peaks = self.peaks['cell']
        sample_peak_int=0.0
        cell_peak_int =0.0
        for sample_peak in sample_peaks:
            sample_peak_int += I_d[ (dcs<sample_peak.dmax) & (dcs>sample_peak.dmin)].sum() #I_d[ (dcs<3.5) & (dcs>3)].sum()
        for cell_peak in cell_peaks:
            cell_peak_int +=  I_d[ (dcs<cell_peak.dmax) & (dcs>cell_peak.dmin)].sum()  #I_d[np.logical_and(dcs<2.2, dcs>2)].sum()
        collimator_ineff = (cell_peak_int / sample_peak_int)  # new objective function suggested by Garrett
        print ('coll_len,:', params[0] , 'focal_distance,:', params[1]  ,'collimator_performance: ', (sample_peak_int/cell_peak_int))
        return (collimator_ineff)

    def collimator_performance (self, params):
        """
        calculating collimator performance

        Parameters
        ----------
        params: list
            list geometrical parameters to be optimized
        Returns
        -------
        collimator performance: float
            the inverse of the inefficiency of the collimator

        """
        return (1/self.collimator_inefficiency(params))


    def objective_func(self,params):
        """
        objective function for the optimization of collimator geometry

        Parameters
        ----------
        params: list
            list geometrical parameters to be optimized

        Returns
        -------
            collimator inefficiency to be minimized: float

        """
        try:
            return (self.collimator_inefficiency(params))

        except Parameter_error as e:
            return (1e10)

    def optimize(self, param_names, params_bounds = [(2.0, 8.0), (17.0, 50.0)], population_size=4, maximum_iteration =5):
        """
        optimizing collimator geometry to minimize collimator inefficiency

        Parameters
        ----------
        param_names : list
            list of string of the colimator geometrical parameters to be optimized
        params_bounds: list
            list of the geometrical parameters to be optimized
        population_size: int
            number of population for simulation
        maximum_iteration: int
            maximum iteration per simulation

        Returns
        -------
        optimized values: list of floats
        """

        self.param_names = self._validate_names(param_names)
        result = differential_evolution(self.objective_func, params_bounds,popsize=population_size,maxiter=maximum_iteration)
        with open(os.path.join(self.result_path, 'optimized_Collimator_Dimension.dat'), "w") as res:
            res.write(result.x)
        return(result.x)
