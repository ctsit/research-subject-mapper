"""
SimpleConfigParser

Simple configuration file parser: Python module to parse configuration files
without sections. Based on ConfigParser from the standard library.

Author: Philippe Lagadec

Project website: http://www.decalage.info/python/configparser

Inspired from an idea posted by Fredrik Lundh:
http://mail.python.org/pipermail/python-dev/2002-November/029987.html

Usage: see end of source code and http://docs.python.org/library/configparser.html
"""

__author__ = 'Philippe Lagadec'
__version__ = '0.02'

#--- LICENSE ------------------------------------------------------------------

# The SimpleConfigParser Python module is copyright (c) Philippe Lagadec 2009-2010
#
# By obtaining, using, and/or copying this software and/or its associated
# documentation, you agree that you have read, understood, and will comply with
# the following terms and conditions:
#
# Permission to use, copy, modify, and distribute this software and its
# associated documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appears in all copies, and that both
# that copyright notice and this permission notice appear in supporting
# documentation, and that the name of the author not be used in advertising or
# publicity pertaining to distribution of the software without specific,
# written prior permission.
#
# THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
# ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
# ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

#-------------------------------------------------------------------------------
# CHANGELOG:
# 2009-02-12 v0.01 PL: - initial version
# 2010-03-15 v0.02 PL: - updated tests and comments

#-------------------------------------------------------------------------------
# TODO:
# - implement read() using the base class code

#=== IMPORTS ==================================================================

import ConfigParser, StringIO

#=== CONSTANTS ================================================================

# section name for options without section:
NOSECTION = 'NOSECTION'


#=== CLASSES ==================================================================

class SimpleConfigParser(ConfigParser.RawConfigParser):
    """
    Simple configuration file parser: based on ConfigParser from the standard
    library, slightly modified to parse configuration files without sections.

    Inspired from an idea posted by Fredrik Lundh:
    http://mail.python.org/pipermail/python-dev/2002-November/029987.html
    """

    def read(self, filename):
        try:
            text = open(filename).read()
            f = StringIO.StringIO("[%s]\n" % NOSECTION + text)
            self.readfp(f, filename)
        except IOError:
            raise Exception('Error reading file ' + filename)

    def getoption(self, option):
        'get the value of an option'
        return self.get(NOSECTION, option)

    def getoptionslist(self):
        'get a list of available options'
        return self.options(NOSECTION)


    def hasoption(self, option):
        """
        return True if an option is available, False otherwise.
        (NOTE: do not confuse with the original has_option)
        """
        return self.has_option(NOSECTION, option)

    def get_list(self, option):
        return self.getoption(option).replace(',','').split()

    def get_dict(self, section):
        temp_dict = {}
        for option in self.options(section):
            value = self.get(section, option)
            if ',' in value:
                value = value.replace(',', '')
                temp_dict[option] = value.split()
            else:
                temp_dict[option] = value
        return temp_dict

    def set_attributes(self):
        for section in self.sections():
            for option in self.options(section):
                setattr(self, option, self.get(section, option))

#=== MAIN =====================================================================

if __name__ == '__main__':
    # simple tests when launched as a script instead of imported as module:

    ##cp = ConfigParser.ConfigParser()
    ### this raises an exception:
    ### ConfigParser.MissingSectionHeaderError: File contains no section headers.
    ##cp.read('config_without_section.ini')

    print 'SimpleConfigParser tests:'

    filename = 'sample_config_file.ini'
    cp = SimpleConfigParser()
    print 'Parsing %s...' % filename
    cp.read(filename)

    print 'Sections:', cp.sections()
    #print cp.items(NOSECTION)
    print 'getoptionslist():', cp.getoptionslist()
    for option in cp.getoptionslist():
        print "getoption('%s') = '%s'" % (option, cp.getoption(option))
    print "hasoption('wrongname') =", cp.hasoption('wrongname')

    # print
    # print "Print out options by attribute instead of recursing the list"
    cp.set_attributes()
    # print cp.option1
    # print cp.option2
    # print cp.get_dict('RULES')
    # print cp.get_list('receiver_email')