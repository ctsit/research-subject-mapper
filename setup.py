from setuptools import setup

# Research Subject Mapper
#
# Can be installed from the tgz file in two steps:
#   
#   tar xvzf rsm.a.b.c.tar.gz
#   python setup.py install
# 
# Note: the OS needs to have 
#   apt-get install python-dev libxml2 libxslt1-dev

setup(
    name='rsm',
    version='0.7.1',
    author='Christopher P Barnes, Philip Chase, Nicolas Rejack',
    author_email='cpb@ufl.edu, pbc@ufl.edu, nrejack@ufl.edu',
    packages=['bin'],
    url='http://it.ctsi.ufl.edu/about/',
    license='BSD 3-Clause',
    description='A suite of tools to curate and manage the people identifiers in a multi-site clinical research project.',
    long_description=open('README.md').read(),
    requires=[
        "requests   (>= 2.2.1)",
        "lxml       (>= 3.3.5)",
        "pysftp     (>= 0.2.6)",
    ],
    classifiers=[
        "License :: OSI Approved :: BSD License",
    ],
)
