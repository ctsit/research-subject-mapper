from setuptools import setup, find_packages

setup(
    name='Research Subject Mapper',
    version='0.7.1',
    author='Christopher P Barnes, Philip Chase, Nicolas Rejack',
    author_email='cpb@ufl.edu, pbc@ufl.edu, nrejack@ufl.edu',
    packages=find_packages(),
    url='',
    license='BSD 3-Clause',
    description='A suite of tools to curate and manage the people identifiers in a multi-site clinical research project.',
    long_description=open('README.md').read(),
    install_requires=[
        "requests >= 2.2.1",
        "lxml >= 3.2.4",
        "pysftp >= 0.2.2",
    ],
    classifiers=[
        "License :: OSI Approved :: BSD License",
    ],
)
