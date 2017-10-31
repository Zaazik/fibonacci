import os

from cx_Freeze import setup, Executable

base = "Win32GUI"


executables = [Executable("some.py", base=base)]
os.environ['TCL_LIBRARY'] = r'C:\Program Files (x86)\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Program Files (x86)\Python36-32\tcl\tk8.6'
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))


packages = ["idna"]
options = {
    'build_exe': {

        'packages':packages,
        'include_files':[
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
         ],
    },

}

setup(
    name="PDF_Reader",
    options = options,
    version = "2",
    description = '<any description>',
    executables = executables,
)