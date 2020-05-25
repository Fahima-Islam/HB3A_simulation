import mcvine, mcvine.components
import numpy as np
import os, sys
thisdir = os.path.abspath(os.path.dirname(__file__))


def instrument(beam=None, sample_path=None, sample='', angleMons= [45,135], detector_width=[0.5,0.5],
               detector_height = [0.5,0.5], sourceTosample_x=0., sourceTosample_y=0.,
               sourceTosample_z=0., sampleTodetector_z = [0.5,0.5], number_detectors=2,
               number_pixels_in_height=[256,256], number_pixels_in_width=[256,256],
               number_of_box_in_height=[3,3], number_of_box_in_width=[3,3]):
    """

    Parameters
    ----------
    beam
    sample_path:
    sample
    angleMons
    detector_width
    detector_height
    sourceTosample_x
    sourceTosample_y
    sourceTosample_z
    sampleTodetector_z
    number_detectors
    number_pixels_in_height
    number_pixels_in_width
    number_of_box_in_height
    number_of_box_in_width

    Returns
    -------

    """
    if beam is None:
        beam = os.path.join(thisdir, '../../beam/Neutrons_mcvine.dat')
    instrument = mcvine.instrument()
    a_source = mcvine.components.sources.NeutronFromStorage('source', beam)
    instrument.append(a_source, position=(0, 0, 0))

    samplename = sample

    if sample_path is None:
        samplexml = os.path.join(thisdir, '../../sample/sampleassembly_%s.xml' % samplename)
    else:
        samplexml = os.path.join(sample_path, 'sampleassembly_%s.xml' % samplename)

    sample = mcvine.components.samples.SampleAssemblyFromXml('sample', samplexml)
    instrument.append(sample, position=(sourceTosample_x, sourceTosample_y,
                                        sourceTosample_z), relativeTo=a_source)

    save = mcvine.components.monitors.NeutronToStorage('save', '{}.mcvine'.format(samplename))
    instrument.append(save, position=(0,0,0), relativeTo=sample)

    from detector import Detector

    width = detector_width
    height = detector_height

    NpixelsPerPanel = 0
    for i in range(number_detectors):
        angle = np.deg2rad(angleMons[i])
        print ('detector_angle: ', angleMons[i])
        pixel_width = detector_width[i] / number_pixels_in_width[i] / number_of_box_in_width[i]  # *1.00000001
        pixel_height = height[i] / number_pixels_in_height[i] / number_of_box_in_height[i]
        NpixelsPerPanel += number_pixels_in_height[i]\
                           *number_of_box_in_height[i]\
                           *number_pixels_in_width[i]\
                           *number_of_box_in_width[i]

        instrument.append(
            Detector('detector{}'.format(i+1), width[i], height[i], pixel_width,
                     pixel_height,
                     'detector{}'.format(i+1), start_index=NpixelsPerPanel*i),
            position=(sampleTodetector_z[i] * np.sin(angle), 0,
                      sampleTodetector_z[i] * np.cos(angle)),
            orientation=(0, np.rad2deg(angle), 0),
            relativeTo=sample
        )

    return instrument


