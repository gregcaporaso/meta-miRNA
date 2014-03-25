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
from miMAP.commands.fasta_to_closed_reference_otu_picking import CommandConstructor
from tempfile import gettempdir
import string
import random


cmd_in_lookup = make_command_in_collection_lookup_f(CommandConstructor)
cmd_out_lookup = make_command_out_collection_lookup_f(CommandConstructor)

inputs = [
    HTMLInputOption(Parameter=cmd_in_lookup('input_file'), Type="str", Required=True, Help ='define your input'),
    HTMLInputOption(Parameter=cmd_in_lookup('output_dir'), Required=True, Help ='your output file'),
    HTMLInputOption(Parameter=cmd_in_lookup('ncRNAdb_file'), Type="str", Required=True, Help ='your ncRNA data base path'),
    HTMLInputOption(Parameter=cmd_in_lookup('mature_miRNAs_database_file'), Type="str", Required=True, Help ='your matur miRNAs data base path'),
    HTMLInputOption(Parameter=cmd_in_lookup('jobs_to_start'), Type="int", Required=True, Help = 'the number of jobs to start in parallel'),
    HTMLInputOption(Parameter=None, Name="download-file", Required=True, Help = 'download file name')
                   
]

outputs = [HTMLPage(Parameter=cmd_out_lookup('status'))]
    

