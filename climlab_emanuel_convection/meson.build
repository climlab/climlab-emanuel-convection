python_sources = [
  '__init__.py',
]

py.install_sources(
  python_sources,
  pure: false,
  subdir: 'climlab_emanuel_convection'
)

incdir_numpy = run_command(py,
  ['-c', 'import os; os.chdir(".."); import numpy; print(numpy.get_include())'],
  check : true
).stdout().strip()

incdir_f2py = run_command(py,
    ['-c', 'import os; os.chdir(".."); import numpy.f2py; print(numpy.f2py.get_include())'],
    check : true
).stdout().strip()

mysource = custom_target('_emanuel_convection.c',
  input : ['Driver.f90', 'convect.f', 'dry_adjustment.f'],  
  output : ['_emanuel_convectionmodule.c', 
            '_emanuel_convection-f2pywrappers.f'],
  command : [py, '-m', 'numpy.f2py', '@INPUT@', 
             '-m', '_emanuel_convection', '--lower', 
             '--build-dir', '@OUTDIR@']
)

inc_np = include_directories(incdir_numpy, incdir_f2py)

py.extension_module('_emanuel_convection',
  ['Driver.f90', mysource],
  incdir_f2py / 'fortranobject.c',
  include_directories: inc_np,
  dependencies : py_dep,
  install : true,
  subdir: 'climlab_emanuel_convection'
)

subdir('tests')