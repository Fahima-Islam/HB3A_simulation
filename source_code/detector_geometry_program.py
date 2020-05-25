import os
template = """<instrument
    xmlns="http://www.mantidproject.org/IDF/1.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.mantidproject.org/IDF/1.0 http://schema.mantidproject.org/IDF/1.0/IDFSchema.xsd"
    name="{name_of_instrument}"
    valid-from="{starting_date}"
    valid-to="{ending_date}"
    >

<defaults>
    <length unit="metre"/>
    <angle unit="degree"/>
    <reference-frame>
      <along-beam axis="z"/>
      <pointing-up axis="y"/>
      <handedness val="right"/>
    </reference-frame>
  </defaults>

<!-- SOURCE -->
  {source_blocks}
  
<!-- SAMPLE -->
    <component type="sample-position">
    <location y="0.0" x="0.0" z="0.0"/>
  </component>
  <type name="sample-position" is="SamplePos"/>
  
<!-- Detector Independent position -->
  {detector_orientation_block}
  
<!-- Detector position with respect to sample -->
  {detector_relative_position_block}
  
<!-- Detector's number of  pixels, height, width, resolution -->
  {detector_size_block}
  
<!-- Detector's pixel shape and size -->
  {pixel_shape_block}

</instrument>

"""
def _source_block(source_to_sample_distance):
    """

    Parameters
    ----------
    source_to_sample_distance : float
        the distance between source and sample in m

    Returns
    -------

    """

    return """    <component type="moderator">
    <location z="-{source_to_sample_distance}"/>
  </component>
  <type name="moderator" is="Source"/>
        """.format(source_to_sample_distance=source_to_sample_distance)

def _detector_orientation_block(r_position, t_position,
                                p_position, rot_x, rot_y,
                                rot_z ):
    """

    Parameters
    ----------
    r_position : float
        the distance between source and sample in m
    t_position : float
        theta position of the detector in m
    p_position : float
        radial position of the detector in m
    rot_x : float
        rotation wrt x_axis in degree
    rot_y : float
        rotation wrt y axis in degree
    rot_z : float
        roation wrt z in degree
    Returns
    -------

    """

    return """ <component type="DetectorArm1">
    <location>
      <parameter name="r-position">
        <value val="{r_position}"/>
      </parameter>
      <parameter name="t-position">
        <value val="{t_position}"/>
      </parameter>
      <parameter name="p-position">
        <value val="{p_position}"/>
      </parameter>
      <parameter name="rotx">
        <value val="{rot_x}"/>
      </parameter>
      <parameter name="roty">
        <value val="{rot_y}"/>
      </parameter>
      <parameter name="rotz">
        <value val="{rot_z}"/>
      </parameter>
    </location>
  </component>
        """.format(r_position=r_position, t_position=t_position, p_position=p_position,
                   rot_x=rot_x, rot_y=rot_y, rot_z=rot_z )

def _detector_relative_position_block(sampleTodetector_z):
    """

        Parameters
        ----------
        sampleTodetector_z : float
            the distance between detector and sample in m

        Returns
        -------

        """

    return """  <type name="DetectorArm1">
    <component type="panel1" idstart="0" idfillbyfirst="y">
      <location name="detector1">
        <parameter name="z">
        <!--  <logfile id="sampleTodetector_z" eq="value"/>-->
        <value val="{sampleTodetector_z}"/>
        </parameter>
      </location>
    </component>
  </type> """.format(sampleTodetector_z=sampleTodetector_z)

def _detector_size_block(number_pixels_x, number_pixels_y,
                         xwidth, yheight):
    """

        Parameters
        ----------
        number_pixels_x : int
            number of pixels in x_width
        number_pixels_y: int
            number of pixels in y_height
        xwidth : float
            detector width
        yheight : float
            detector height

        Returns
        -------

        """
    x_start = xwidth/2.
    y_start = yheight/2.
    x_step = xwidth/number_pixels_x
    y_step = yheight/number_pixels_y


    return """  <type name="panel1" is="RectangularDetector" type="pixel"
      xpixels="{number_pixels_x}" xstart="-{x_start}" xstep="+{x_step}"
      ypixels="{number_pixels_y}" ystart="-{y_start}" ystep="+{y_step}" >
</type> """.format(number_pixels_x=number_pixels_x, number_pixels_y=number_pixels_y, x_start=x_start,
                   y_start=y_start, x_step=x_step, y_step= y_step )


def _pixel_shape_block(number_pixels_x, number_pixels_y, xwidth, yheight):
    """

        Parameters
        ----------
       number_pixels_x : int
            number of pixels in x_width
        number_pixels_y: int
            number of pixels in y_height
        xwidth : float
            detector width
        yheight : float
            detector height

        Returns
        -------

        """
    x_step = xwidth / number_pixels_x
    y_step = yheight / number_pixels_y

    p_x_start = x_step/2.
    p_y_start = y_step/2.

    return """ <type is="detector" name="pixel">
  <cuboid id="pixel-shape">
    <left-front-bottom-point y="-{p_y_start}" x="-{p_x_start}" z="0.0"/>
    <left-front-top-point y="{p_y_start}" x="-{p_x_start}" z="0.0"/>
    <left-back-bottom-point y="-{p_y_start}" x="-{p_x_start}" z="-0.0002"/>
    <right-front-bottom-point y="-{p_y_start}" x="{p_x_start}" z="0.0"/>
  </cuboid>
  <algebra val="pixel-shape"/>
</type> """.format( p_x_start=p_x_start, p_y_start=p_y_start)

def makeDetXML(path_ToSave, file_name, name_of_instrument, source_to_sample_distance,
              r_position, t_position, p_position, rot_x, rot_y, rot_z,sampleTodetector_z,
              number_pixels_x, number_pixels_y, xwidth, yheight,
              starting_date="2020-05-23 00:00:00",
              ending_date= "2021-05-23 00:00:00" ):
   """
   making scattering kernel xml file

                      Parameters
                      ----------
                        source_to_sample_distance : float
                            the distance between source and sample
                        r_position : float
                            the distance between source and sample in m
                        t_position : float
                            theta position of the detector in m
                        p_position : float
                            radial position of the detector in m
                        rot_x : float
                            rotation wrt x_axis in degree
                        rot_y : float
                            rotation wrt y axis in degree
                        rot_z : float
                            roation wrt z in degree
                        sampleTodetector_z : float
                            the distance between detector and sample in m
                        number_pixels_x : int
                            number of pixels in x_width
                        number_pixels_y: int
                            number of pixels in y_height
                        xwidth : float
                            detector width
                        yheight : float
                            detector height
                      """
   source_blocks =_source_block (source_to_sample_distance)
   detector_orientation_block = _detector_orientation_block(r_position, t_position,
                                p_position, rot_x, rot_y,
                                rot_z)

   detector_relative_position_block = _detector_relative_position_block(sampleTodetector_z)
   detector_size_block = _detector_size_block(number_pixels_x, number_pixels_y,
                        xwidth, yheight)
   pixel_shape_block = _pixel_shape_block(number_pixels_x, number_pixels_y, xwidth, yheight)


   text = template.format(name_of_instrument=name_of_instrument, starting_date=starting_date,
                          ending_date=ending_date, source_blocks= source_blocks,
                          detector_orientation_block= detector_orientation_block,
                          detector_relative_position_block= detector_relative_position_block,
                          detector_size_block= detector_size_block,
                          pixel_shape_block= pixel_shape_block)
   with open( os.path.join('{}','{}.xml').format(path_ToSave, file_name), "w") as sam_new:
       sam_new.write(text)







