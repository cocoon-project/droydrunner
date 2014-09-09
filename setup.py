
import os

from distutils.core import setup

from droydrunner.__init__ import __version__ as version

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='DroydRunner',
    version=version,
    packages=[
              'droydrunner', 'droydrunner.api', 'droydrunner.lib', 'droydrunner.lib.facets', 'droydrunner.apps',
              'droydrunner.phone', 'droydrunner.phone.hub', 'droydrunner.phone.hub.server', 'droydrunner.utils',
              'droydrunner.scrutinizer'],
    url='',
    license='orange',
    author='cocoon',
    author_email='tordjman.laurent@gmail.com',
    description='test automation tool for android phones',
    long_description=read('README.md'),
    entry_points = {
        'console_scripts': ['droydrun=droydrunner.droydrun:main',],
    },
    #include_package_data=True,
    #data_files=[('','requirements.txt'),],
    #package_data= {'doc':['*.htm*','*.yaml']},
    #install_requires=[
    #]
)
