#INTRODUCTION
This document describes the need for creating a research subject map to use with the RED-I software project and details a method for creating this manually. 

* The most recent version of this document can be found at: [https://github.com/ctsit/research-subject-mapper/blob/develop/doc/manual_research_subject_mapping/README_create_research_subject_map.md]

#REQUIREMENTS
This document is intended to be used along with the file [example_subject_map.csv](https://github.com/ctsit/research-subject-mapper/raw/develop/doc/manual_research_subject_mapping/example_subject_map.csv)

#USAGE
When transforming and loading patient data from the electronic health record (EHR) to a REDCap system it is important to protect the patient's confidentiality by hiding potentially identifiable information such as medical record numbers (MRN) from the RED-I software and anyone running it. 

[Research subject mapper](https://github.com/ctsit/research-subject-mapper) software can automatically create the mapping file. It uses a REDCap project that site coordinators can enter MRNs, date of birth, and research subject IDs into generate the mapping file.

Site coordinators may instead choose to manually create a mapping file, using the [example_subject_map.csv](https://github.com/ctsit/research-subject-mapper/raw/develop/doc/manual_research_subject_mapping/example_subject_map.csv). Use a text editor such as TextEdit on Mac or Notepad on Windows to avoid formatting problems. 

Format the data following these guidelines:

1. All fields must be surrounded by double quotes
2. All fields must be separated by commas, except at the end of a line.

The fields in the file are:

1. "research_subject_id" is the subject number for the patient 
2. "start_date" and "end_date" must be formatted YYYY-MM-DD. This specifies the date range to pull records, according to your protocol. start_date is consent date minus 180 days, end_date is the end of treatment plus 180 days.
3. "mrn" is the medical record number in the local EHR. 
4. "facility_code"" is an optional code that corresponds to a hospital in the EHR. 


#MAINTAINERS
This document is created and maintained by members of CTS-IT, including:

Nicholas Rejack - nrejack@ufl.edu

Chris Barnes - cpb@ufl.edu

Philip Chase - pbc@ufl.edu


