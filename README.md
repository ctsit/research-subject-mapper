#Research Subject Mapper

Research Subject Mapper is a tool designed to serve the needs of multi-center studies to prevent exposure of medical record identifiers to the data coordination center while allowing the data coordination center to specify data collection periods for the research subjects.  The intended usage of this tool is to combine authoritative data from a research subject data store with identifiable data at a data collection site to generate inputs for queries of an Electronic Health Record (EHR).

This tool has 2 components. The first component, generate_subject_map_input.py, allows data aggregators to access and transform data from a REDCap instance to generate an input file for site administrators.  

The second component, generate_subject_map.py, extracts a mapping of EHR identifiers to research subject identifiers from a local Person Index and combines it with the data from generate_subject_map_input.py.  The resulting data file indicates which patient records should be queried, the applicable date ranges for each patient, and the research subject ID that should be attached to those records when they are returned to study staff. 

The Person Index is a small REDCap instance operating as the data collection site.  Refer to the data dictionary (personIndex_DataDictionary.csv) in the doc directory to see the fields used in the person index REDCap project.

## generate_subject_map_input.py

generate_subject_map_input.py is a tool used to generate patient-to-research subject ID mapping files based on inputs from REDCap projects.
This tool reads inputs from the REDCap for the fields listed in the source_data_schema.xml and processes the data to generate an input file for subject mapping. This file smi.xml will be uploaded to the secure FTP location listed in site-catalog.xml.

Steps to use generate_subject_map_input.py:

All files and input paramters required to run generate_subject_map_input.py can be found in the config-example-gsm-input folder.

1) Modify files in config-example-gsm-input with your implementation specific details (for example: site details, sftp credentials, source_data details).
2) Rename config-example-gsm-input to config.
3) Run generate_subject_map_input.py.



## generate_subject_map.py
generate_subject_map.py reads the smi.xml from the site FTP listed in the site-catalog.xml. It also reads inputs from the person index for the fields listed in the source_data_schema.xml. This tool maps the subjects in the smi.xml to the subjects in person index based on research subject id and year of birth. All successfully mapped subjects are written to subject_map.csv and all failed mappings are written to subject_map_exceptions.csv.

Steps to use generate_subject_map.py:

All files and input parameters required to run generate_subject_map.py can be found in the config-example-gsm folder.

1) Modify files in config-example-gsm with your implementation specific details (for example: site details, SFTP details, source_data details)
2) Rename config-example-gsm to config
3) Run generate_subject_map.py

