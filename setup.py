from distutils.core import setup

setup(
    name='Research Subject Mapper',
    version='0.1.0',
    author='Christopher P Barnes, Philip Chase, Nicolas Rejack',
    author_email='cpb@ufl.edu, pbc@ufl.edu, nrejack@ufl.edu',
    packages=['bin/'],
    scripts=['bin/generate_subject_map_input.py'],
    url='',
    license='LICENSE',
    description='Subject map input generator',
    long_description=open('README.md').read(),
    install_requires=[
        "requests >= 2.2.1",
        "lxml >= 3.2.4",
        "pysftp >= 0.2.2",
    ],
)
