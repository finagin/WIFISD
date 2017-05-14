'''
py2app/py2exe build script for WIFISD.

Will automatically ensure that all build prerequisites are available
via ez_setup

Usage (Mac OS X):
 python setup.py py2app

Usage (Windows):
python setup.py py2exe
'''
try:
    import ez_setup

    ez_setup.use_setuptools()
except Exception:
    pass

import sys

from setuptools import setup

mainscript = "src/main.py"

if sys.platform == "darwin":
    extra_options = dict(
        setup_requires=["py2app"],
        app=[mainscript],
        data_files=["app"],
        options=dict(
            py2app=dict(
                optimize=True,
                argv_emulation=True,
                iconfile="app/images/icon.icns"
            )
        ),
    )
elif sys.platform == "win32":
    extra_options = dict(
        setup_requires=["py2exe"],
        app=[mainscript],
    )
else:
    extra_options = dict(
        scripts=[mainscript],
    )

setup(
    name="WIFISD",
    version="0.0.1",
    **extra_options
)
