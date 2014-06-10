#Research Subject Mapper

Research Subject Mapper is a tool designed to serve the needs of multi-center studies to prevent exposure of medical record identifiers to the data coordination center while allowing the data coordination center to specify data collection periods for the research subjects.  The intended usage of this tool is to combine authoritative data from a research subject data store with identifiable data at a data collection site to generate inputs for queries of an Electronic Health Record (EHR).

## Working with research-subject-mapper executable(egg file):
### Requirements:
To successfully run the Research Subject Mapper tool on the target machine please install the software below before going any further.
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

#### Files Description:
The files that need to be modified with your implementation details in config directory are `site-catalog.xml` and `source_data_schema.xml`.

##### site-catalog.xml
This xml file follows below structure

```
<sites_list>
	<site>
        <site_name>source</site_name>
        <site_URI>sftp.source_site.edu</site_URI>
        <site_uname>source_user</site_uname>
        <site_password>source_password</site_password>
        <site_remotepath>ftp/smi.xml</site_remotepath>
        <site_contact_email>contact@source_site.edu</site_contact_email>
    </site>
</sites_list>
```

##### source_data_schema.xml
This xml file follows below structure

```
<source>
	<redcap_uri>Your_RedCap_Instance_URI</redcap_uri>
	<apitoken>API_TOKEN</apitoken>
	<fields>
		<field>Field_Name</field>
		<field>Field_Name</field>
		<field>Field_Name</field>
	</fields>
</source>
```

### Running the generate_subject_mapper tools
#### Input Requirements:
1) Edit the source_data_schema.xml file to specify the Person Index fields before running gsm. You will need to specify the study subject number, a field to verify the study subject (typically year of birth), and the subject's corresponding MRN.

2) If this tool is being run on the central site you need to run `gsmi` tool as shown below and put generated files in the ftp of the site. Client sites typically only need to run the generate_subject_mapper tool.

##### To generate input at the central site location
Run `gsmi -c <FULL_PATH_TO_CONFIG_DIRECTORY> -k <YES_OR_NO_TO_KEEP_GENERATED_FILES>` (if a directory named config is already setup in the parent directory of generate_subject_map_input.py, one need not provide the path to config directory in -c option)

If this tool is being run at the site, one can just provide site ftp details in the `site-catalog.xml` use the `gsm` tool.


#### To run generate_subject_map.py tool:
Run `gsm -c <FULL_PATH_TO_CONFIG_DIRECTORY> -k <YES_OR_NO_TO_KEEP_GENERATED_FILES>` (if a directory named config is already setup in the parent directory of generate_subject_map_input.py, one need not provide the path to config directory in -c option)

