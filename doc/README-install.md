# Installation and Deployment Plan for Generate Subject Map Input (GSMI) and Generate Subject Map (GSM)

## Prequisities

GSMI and GSM require Python 2.7, several python libraries, access via sftp and REDCap API to the data sources and targets it needs.  In addition, the code repository is accessed with git so git must be installed locally as well.

These libraries are required:

    lxml
    requests
    pysftp

On a mac, run these commands to install the required libraries and related utilities

    sudo easy_install lxml
    sudo easy_install requests
    sudo easy_install pysftp

In Debian Wheezy, execute these commands

    sudo apt-get install python-lxml
    sudo apt-get install python-requests
    sudo apt-get install python-libssh2

To install git, visit [Git Downloads](http://git-scm.com/downloads) for installation instructions for your operating system. Most linux distributions can install git using their package manager, as in Debian:

    sudo apt-get install git

Note to Mac Users: the deployment scripts below assume the use of GNU Utilities.  The default command line utilities that ship with Mac OSX behave differently.  If you want to use these procedures on a Mac please follow the installation procedures at [GNU Utilities](http://www.topbug.net/blog/2013/04/14/install-and-use-gnu-command-line-tools-in-mac-os-x/) to install the GNU Utilities

## Configuration

GSMI and GSM are configured via files that appear in ./config/  Once configured these files should be curated with a source control manager like git or mercurial.  

## Deployment to a new installation

GSMI and GSM are components of the Research Subject Mapper (RSM) project.  Checkout the version of the Research Subject Mapper required for this installation

    # set some variables
    rsm_git_repository_uri=<rsm_git_repository_uri>
    rsm_instance_name=<rsm_instance_name>

    MYTEMP=`mktemp -d`
    cd $MYTEMP

    git clone $rsm_git_repository_uri $rsm_instance_name
    cd $rsm_instance_name
    git checkout develop
    sudo mkdir /var/lib/$rsm_instance_name.archive/
    sudo mkdir /var/lib/$rsm_instance_name/
    sudo cp -r $MYTEMP/$rsm_instance_name/* /var/lib/$rsm_instance_name/
    cd /var/lib/$rsm_instance_name

    # clean up the mess
    rm -rf $MYTEMP

Copy the example configuration to your home directory for editing and commiting changes.  After editing, this config data needs to be deployed to the production location.

    # set some variables
    rsm_instance_configuration_uri=<configuration_URI>

    mkdir ~/$rsm_instance_name
    cp -r /var/lib/$rsm_instance_name/config-example/* ~/<local_config_folder_name>
    cd ~/$rsm_instance_name
    # edit config as needed
    git init 
    git remote add origin $rsm_instance_configuration_uri
    git push -u origin master

Deploy config to the RSM instance 

    sudo rm -rf /var/lib/$rsm_instance_name/config
    sudo cp -r ~/$rsm_instance_name /var/lib/$rsm_instance_name/config


## Redeployment to an existing RSM installation

Back up existing installation

    # set some variables
    rsm_git_repository_uri=<rsm_git_repository_uri>
    rsm_instance_name=<rsm_instance_name>

    date=`date +"%Y%m%d-%H%M"`
    if [ -e /var/lib/$rsm_instance_name ];  then
        cd /var/lib/
        sudo -E tar czvf /var/lib/$rsm_instance_name.archive/$rsm_instance_name.archive.$date.tgz $rsm_instance_name
    fi

Remove the existing installation and redeploy code.
Checkout the version of RSM required for this installation

    # clone the master branch into some scratch space
    MYTEMP=`mktemp -d`
    cd $MYTEMP
    # Now checkout the head of master
    git clone $rsm_git_repository_uri $rsm_instance_name
    cd $rsm_instance_name
    git checkout develop

    # delete the old code
    if [ -e /var/lib/$rsm_instance_name ];  then
        sudo rm -rf /var/lib/$rsm_instance_name
    fi

    # deploy the new code
    sudo mkdir /var/lib/$rsm_instance_name
    sudo cp -r $MYTEMP/$rsm_instance_name/* /var/lib/$rsm_instance_name
    cd /var/lib/$rsm_instance_name
    sudo rm -rf .git

    # Clean up the mess
    rm -rf $MYTEMP

Install the production configuration

    # set some variables
    rsm_instance_configuration_uri=<configuration_URI>

    # Clone the config repo to some scratch space
    MYTEMP=`mktemp -d`
    cd $MYTEMP
    git clone $rsm_instance_configuration_uri config
    cd config
    rm -rf .git
    cd ..
    
    # Deploy config to the RSM instance
    sudo rm -rf /var/lib/$rsm_instance_name/config
    cd $MYTEMP
    sudo cp -r config /var/lib/$rsm_instance_name/config

    # Clean up the mess
    cd ~/
    rm -rf $MYTEMP

## Manually run RSM

    # Run RSM
    sudo python /var/lib/$rsm_instance_name/bin/generate_subject_map_input.py

or 

    # Run RSM
    sudo python /var/lib/$rsm_instance_name/bin/generate_subject_map.py

## Configure this RSM instance to run via cron
