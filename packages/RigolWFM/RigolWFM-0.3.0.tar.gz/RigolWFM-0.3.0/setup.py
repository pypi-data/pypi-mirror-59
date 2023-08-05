from setuptools import setup

# use README as the long description
# make sure to use the syntax that works in both ReST and markdown
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='RigolWFM',
    packages=['RigolWFM'],
    version='0.3.0',
    description='Read and parse Rigol Oscilloscope WFM files',
    url='https://github.com/scottprahl/RigolWFM.git',  
    author='Scott Prahl',
    author_email='scott.prahl@oit.edu',
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
    ],
    keywords=['Rigol', 'wfm', 'DS1052E', 'DS1102E', 'DS1054Z'],
    install_requires=['numpy','matplotlib'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)