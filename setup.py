from cx_Freeze import setup, Executable

base = None

executables = [Executable("auto_180iq_lib.py", base=base)]

packages = []
options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name = "auto180iq",
    options = options,
    version = "1",
    description = 'good',
    executables = executables
)