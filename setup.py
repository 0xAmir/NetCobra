from distutils.core import setup
import py2exe

setup(
    console=['nc.py'],
    windows = [{
            "script":"nc.py",
            "dest_base":"NetCobra"
                }]
    )
