import os

template = """<?xml version="1.0"?>

<!DOCTYPE SampleAssembly[
   {shape_file_entries}
]>
<SampleAssembly name="{sample_assembly_name}"
   max_multiplescattering_loops_among_scatterers="1"
   max_multiplescattering_loops_interactM_path1="1"
   min_neutron_probability="0.01"
 >
    {sample_blocks}

    <LocalGeometer registry-coordinate-system="InstrumentScientist">
        {geom_regs}
    </LocalGeometer>

    <Environment temperature="300*K"/>

</SampleAssembly>
"""
def _shape_file_entry(shape_name, shape_fileName):
  """
    creating the template for shape entry
  Parameters
  ----------
  shape_name: string
            name of the shape
  shape_fileName : string
            name of the geometry file

  Returns
  -------
  template: string
    template for shape file

  """
  return """ <!ENTITY {shape_name} SYSTEM "{shape_fileName}.xml">
""".format(shape_name=shape_name, shape_fileName=shape_fileName)


def _sample_block(name, shape_name, formula, structureFile, strutureFiletype):
  """
    creating the template for sample block
  Parameters
  ----------
  name: string
    name of the scatterer
  shape_name: string
    name of the shape
  formula: string
    chemical formula of the scatterer
  structureFile: string
    structure file path of the scatterer
  strutureFiletype: string
     extension of the structure file (cif or xyz)
  Returns
  -------
  template: string
    template for sample block
  """
  return """  <PowderSample name="{name}" type="sample">
    <Shape>
      &{shape_name};
    </Shape>
    <Phase type="crystal">
      <ChemicalFormula>{formula}</ChemicalFormula>
      <{strutureFiletype}file>{structureFile}</{strutureFiletype}file>
    </Phase>
  </PowderSample>
""".format(name=name, shape_name=shape_name, formula=formula, structureFile=structureFile, strutureFiletype=strutureFiletype)

scatterers = {
     ('outer-body', 'shapeAl', 'outer-body-geom', 'Al', 'Al.xyz', 'xyz'),   # (name, shape_name, geometry file name, formula, structure file, structurefile type)
     ('inner-sleeve', 'shapeCu', 'inner-sleeve-geom', 'Cu',  'Cu.xyz', 'xyz'),
     ('sample', 'shapeSample', 'sample_geom','Si' ,'Si.xyz', 'xyz'),
     ('collimator', 'shapeColl','coll_geometry', 'B4C',  'B4C.cif', 'cif'),
}

def makeSAXML(sampleassembly_fileName, pathTosave, scatterers=scatterers):
   """
    creating the sample assembly file on which mcvine simulation will run
   Parameters
   ----------
   sampleassembly_fileName: string
        file name of the sampleassembly
   pathTosave: string
        the path where the sample assembly file will be saved
   scatterers:set
        the set of scatterer information : scatterer name, shape name, shape file name, chemical formula,
        structure file path, structure file extension


   """

   shape_file_entries = [_shape_file_entry(shape_name, shape_fileName) for name, shape_name, shape_fileName, formula,  structureFile,strutureFiletype  in scatterers]
   shape_file_entries='\n'.join(shape_file_entries)
   sample_blocks = [_sample_block(name, shape_name, formula,structureFile,strutureFiletype) for name, shape_name, shape_fileName, formula, structureFile,strutureFiletype  in scatterers]
   sample_blocks = '\n'.join(sample_blocks)
   lines = ['<Register name="{}" position="(0,0,0)" orientation="(0,0,0)"/>' .format(name) for name, shape_name, shape_fileName, formula, structureFile,strutureFiletype in scatterers]
   geom_regs = '\n '.join(lines)
   text = template.format(shape_file_entries=shape_file_entries, sample_assembly_name=sampleassembly_fileName,
                          sample_blocks=sample_blocks, geom_regs=geom_regs)
   with open(os.path.join('{}', 'sampleassembly_{}.xml').format(pathTosave, sampleassembly_fileName), "w") as sam_new:
       sam_new.write(text)







