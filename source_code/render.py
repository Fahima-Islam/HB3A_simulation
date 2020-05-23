from instrument.geometry.pml.Renderer import Renderer as base
from instrument.geometry.pml import weave
import os, sys

class File_inc_Renderer(base):
    """A class to include header, footer in the xml file of the geometry of the object
      """
    def _renderDocument(self, body):
        """     rendering the geometry
                      Parameters
                      ----------
                      body: object
                         geometry of the object

                      """
        self.onGeometry(body)
        return
    def header(self):
        return []
    def footer(self):
        return []
    def end(self):
        return

def renderin_the_file (objectGeo, fileNameTosave, patheNameTOSave, scad_flag):
    """
                  creating the xml file of the object geometry based on if the xml file will be
                  rendering to cad file or will be using to run the simulation
                  using mcvine

                  Parameters
                  ----------
                  objectGeo: object
                     the geometry of the body
                  fileNameTosave: string
                        name of the xml geometry file to be saved
                  patheNameTOSave: string
                        name of the path where the xml geometry file will be saved
                  scad_flag: boolen
                        to indicate if the xml file will be used to render cad file

                  Returns: object
                  -------
                  xml file of the object geometry
                  """
    filename_withExtension = '%s.xml' % (fileNameTosave,)
    outputfile = os.path.join(patheNameTOSave, filename_withExtension)
    with open(outputfile, 'wt') as file_h:
        if scad_flag:
            weave(objectGeo, file_h, print_docs=False)
        else:
            weave(objectGeo, file_h, print_docs=False, renderer=File_inc_Renderer(), author='')
