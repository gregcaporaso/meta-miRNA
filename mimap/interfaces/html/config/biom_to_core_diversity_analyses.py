#!/usr/bin/env python
from __future__ import division

__author__ = "Giorgio Casaburi and Greg Caporaso"
__copyright__ = "Copyright 2013, The miMAP project"
__credits__ = "Giorgio Casaburi", "Greg Caporaso"
__license__ = "GPL"
__version__ = "0.0.0-dev"
__maintainer__ = "Giorgio Casaburi"
__email__ = "casaburi@ceinge.unina.it"

from pyqi.core.interfaces.html import (HTMLInputOption, HTMLDownload, HTMLPage)
from pyqi.core.interfaces.html.output_handler import newline_list_of_strings
from pyqi.core.command import (make_command_in_collection_lookup_f,
    make_command_out_collection_lookup_f)
from miMAP.commands.biom_to_core_diversity_analyses import CommandConstructor
from tempfile import gettempdir
import string
import random


cmd_in_lookup = make_command_in_collection_lookup_f(CommandConstructor)
cmd_out_lookup = make_command_out_collection_lookup_f(CommandConstructor)

inputs = [
    HTMLInputOption(Parameter=cmd_in_lookup('input_file'), Required=True, Help ='define your input'),
    HTMLInputOption(Parameter=cmd_in_lookup('output_dir'), Required=True, Help ='your output file'),
    HTMLInputOption(Parameter=cmd_in_lookup('mapping_file'), Type="str", Required=True, Help ='your mapping file path'),
    HTMLInputOption(Parameter=cmd_in_lookup('sampling_depth'), Type="int", Required=True, Help ='the sampling depth to run core diversity analysis'),
    HTMLInputOption(Parameter=cmd_in_lookup('jobs_to_start'), Type="int", Required=True, Help = 'the number of jobs to start in parallel'),
    HTMLInputOption(Parameter=cmd_in_lookup('category'), Type="str", Required=False, Help = 'The metadata category or categories to compare (i.e.,column headers in the mapping file)')              
]

outputs = [HTMLPage(Parameter=cmd_out_lookup('status'))]
    
