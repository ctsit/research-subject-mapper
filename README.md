#Research Subject Mapper

Research Subject Mapper is a tool designed to serve the needs of multi-center studies to prevent exposure of medical record identifiers to the data coordination center while allowing the data coordination center to specify data collection periods for the research subjects.  The intended usage of this tool is to combine authoritative data from a research subject data store with identifiable data at a data collection site to generate inputs for queries of an Electronic Health Record (EHR).

Research Subject Mapper can used by either downloading the source or by downloading and installing the executable
## Working with source code
Source code can be downloaded from [here](ctsit.github.io/research-subject-mapper) in both zip and gzip formats. Copy the downloaded zip file to the desired location and unzip it.

Source code can also be cloned using command `git clone https://github.com/ctsit/research-subject-mapper.git`. Research Subject Mapper source code is now available for usage on the target machine. 

### Requirements:
To successfully run the Research Subject Mapper tool on the target machine please install below softwares before going any further.
#### Install Python:
Run ```sudo apt-get install python2.7``` on target machine
#### Install below python packages
```sudo apt-get install python-setuptools``` (to install setuptools package)

```sudo apt-get install python-dev``` (to install python-dev packages)

```sudo apt-get install libxml2``` (to install libxml2 package)

```sudo apt-get install libxslt1-dev``` (to install libxslt1-dev package)

```sudo easy_install lxml``` (Version >= 3.3.5)

```sudo easy_install requests``` (Version >= 2.2.1)

```sudo easy_install pysftp``` (Version >= 0.2.6)

### Running the generate_subject_mapper tools
Research Subject Mapper tool has 2 components. The first component, generate_subject_map_input.py, allows data aggregators to access and transform data from a REDCap instance to generate an input file for site administrators.  

The second component, generate_subject_map.py, extracts a mapping of EHR identifiers to research subject identifiers from a local Person Index and combines it with the data from generate_subject_map_input.py.  The resulting data file indicates which patient records should be queried, the applicable date ranges for each patient, and the research subject ID that should be attached to those records when they are returned to study staff. 

The Person Index is a small REDCap instance operating as the data collection site.  Refer to the data dictionary (personIndex_DataDictionary.csv) in the doc directory to see the fields used in the person index REDCap project.

#### generate_subject_map_input.py

generate_subject_map_input.py is a tool used to generate patient-to-research subject ID mapping files based on inputs from REDCap projects.
This tool reads inputs from the REDCap for the fields listed in the source_data_schema.xml and processes the data to generate an input file for subject mapping. This file smi.xml will be uploaded to the secure FTP location listed in site-catalog.xml.

Steps to use generate_subject_map_input.py:

All files and input paramters required to run generate_subject_map_input.py can be found in the config-example-gsm-input folder.

1) Setup a config directory on the tagret machine 

2) Add files to config directory with your implementation specific details (for example: site details, sftp credentials, source_data details.For more detailed examples please refer files in config-example-gsm-input).

3) Run ```generate_subject_map_input.py -c <FULL_PATH_TO_CONFIG_DIRECTORy> -k <YES_OR_NO_TO_KEEP_GENERATED_FILES>``` (if a directory named config is already setup in the parent directory of generate_subject_map_input.py, one need not provide the path to config directory in -c option)



#### generate_subject_map.py
generate_subject_map.py reads the smi.xml from the site FTP listed in the site-catalog.xml. It also reads inputs from the person index for the fields listed in the source_data_schema.xml. This tool maps the subjects in the smi.xml to the subjects in person index based on research subject id and year of birth. All successfully mapped subjects are written to subject_map.csv and all failed mappings are written to subject_map_exceptions.csv.

Steps to use generate_subject_map.py:

All files and input parameters required to run generate_subject_map.py can be found in the config-example-gsm folder.


1) Setup a config directory on the tagret machine 

2) Add files to config directory with your implementation specific details (for example: site details, sftp credentials, source_data details.For more detailed examples please refer files in config-example-gsm).

3) Run ```generate_subject_map.py -c <FULL_PATH_TO_CONFIG_DIRECTORy> -k <YES_OR_NO_TO_KEEP_GENERATED_FILES>``` (if a directory named config is already setup in the parent directory of generate_subject_map_input.py, one need not provide the path to config directory in -c option)

## Working with research-subject-mapper executable(egg file):
### Requirements:
To successfully run the Research Subject Mapper tool on the target machine please install below softwares before going any further.
#### Install Python:
Run ```sudo apt-get install python2.7``` on target machine
#### Install below python packages
```sudo apt-get install python-setuptools``` (to install setuptools package)

```sudo apt-get install python-dev``` (to install python-dev packages)

```sudo apt-get install libxml2``` (to install libxml2 package)

```sudo apt-get install libxslt1-dev``` (to install libxslt1-dev package)
### Download .egg file:
Research Subject Mapper Executable can be downloaded from the ctsit.github.io/research-subject-mapper. 

### Installation:
To install research subject mapper run *sudo easy_install rsm_X.X.X.egg* where X's represent version number

###Configuration setup:
Check for config-example-gsm and config-example-gsm-input directories in the rsm installation directory on the target machine and prepare custom config directories with your implementations on the target machine.

### Running the generate_subject_mapper tools

#### To Run generate_subject_map_input.py tool:
Run `gsmi -c <FULL_PATH_TO_CONFIG_DIRECTORY> -k <YES_OR_NO_TO_KEEP_GENERATED_FILES>` (if a directory named config is already setup in the parent directory of generate_subject_map_input.py, one need not provide the path to config directory in -c option)

#### To Run generate_subject_map.py tool:
Run `gsm -c <FULL_PATH_TO_CONFIG_DIRECTORY> -k <YES_OR_NO_TO_KEEP_GENERATED_FILES>` (if a directory named config is already setup in the parent directory of generate_subject_map_input.py, one need not provide the path to config directory in -c option)

