from setuptools import setup, find_packages

# Research Subject Mapper
#
# Can be installed from the tgz file in two steps:
#
#   tar xvzf rsm.a.b.c.tar.gz
#   python setup.py install
#
# Note: the OS needs to have
#   apt-get install setuptools python-dev libxml2 libxslt1-dev

setup(
    name='rsm',
    version='0.10.2',
    author='Christopher P Barnes, Philip Chase, Nicholas Rejack',
    author_email='cpb@ufl.edu, pbc@ufl.edu, nrejack@ufl.edu',
    packages=find_packages(),
    include_package_data=True,
    package_data={'rsm': ['utils/*.xsl'],'config-example-gsm': ['*'],'config-example-gsm-input': ['*']},
    data_files={
            'README.md'
        },
    url='http://it.ctsi.ufl.edu/about/',
    license='BSD 3-Clause',
    description='A suite of tools to curate and manage the people identifiers in a multi-site clinical research project.',
    long_description=open('README.md').read(),
    install_requires=["requests >= 2.2.1","lxml >= 3.3.5","pysftp >= 0.2.8", "appdirs"],
    entry_points={
            'console_scripts': [
                'gsmi = rsm.generate_subject_map_input:main',
                'gsm = rsm.generate_subject_map:main'
                ],
            },
    classifiers=[
        "License :: OSI Approved :: BSD License",
    ],
)
