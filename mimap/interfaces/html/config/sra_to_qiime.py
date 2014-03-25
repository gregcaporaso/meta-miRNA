#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__author__ = "Evan Bolyen"
__copyright__ = "Copyright 2013, The pyqi project"
__credits__ = ["Evan Bolyen"]
__license__ = "BSD"
__version__ = "0.2.0-dev"
__maintainer__ = "Evan Bolyen"
__email__ = "ebolyen@gmail.com"

from pyqi.core.interfaces.html import (HTMLInputOption, HTMLDownload, HTMLPage)
from pyqi.core.interfaces.html.output_handler import newline_list_of_strings
from pyqi.core.command import (make_command_in_collection_lookup_f,
    make_command_out_collection_lookup_f)
from miMAP.commands.sra_to_qiiime import CommandConstructor


def open_file_for_download(result_key, data, value=None):
	with open(data, "U") as f:
		return f.read()
		
		
cmd_in_lookup = make_command_in_collection_lookup_f(CommandConstructor)
cmd_out_lookup = make_command_out_collection_lookup_f(CommandConstructor)

inputs = [
    HTMLInputOption(Parameter=cmd_in_lookup('input_dir'), Required=True, Help ='define your input'),
    HTMLInputOption(Parameter=cmd_in_lookup('output_fp'), Required=True, Help ='your output file'),
    HTMLInputOption(Parameter=None, Name="download-file", Required=True, Help = 'download file name')
                   
]

outputs = [HTMLDownload(Parameter=cmd_out_lookup('result'),
                   Handler=open_file_for_download,
                   FilenameLookup='download-file',
                   FileExtension='.fasta')]

#Comment out the above and uncomment the below for an example of a page.

#     HTMLPage(Parameter=cmd_out_lookup('result'),
#              Handler=newline_list_of_strings) 
    

