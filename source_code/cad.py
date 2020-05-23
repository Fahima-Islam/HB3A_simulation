import SCADGen.Parser as parse

def xmlToOpenScad(filename='collimator_support_ed2.xml'):
    """converting .xml file to .scad file


         Parameters
         ----------
         filename: string
              name of the xml file

         Returns
         -------
         file: string
            scad file
         """
    p=parse.Parser(filename)
    p.createSCAD()
    test = p.rootelems[0]
