#!/usr/bin/env python
from __future__ import division

__author__ = "Giorgio Casaburi and Greg Caporaso"
__copyright__ = "Copyright 2013, The meta-miRNA project"
__credits__ = "Giorgio Casaburi", "Greg Caporaso"
__license__ = "GPL"
__version__ = "0.0.0-dev"
__maintainer__ = "Giorgio Casaburi"
__email__ = "casaburi@ceinge.unina.it"

from pyqi.core.command import Command, Parameter, ParameterCollection

from os import walk

from pyqi.util import pyqi_system_call

class SraToQiime(Command):
    BriefDescription = "post split libraries format: This script allows to convert .sra miRNA sequence data into a QIIME compatible format"
    LongDescription = "A script for converting SRA miRNA sequence data into a format that can be used with QIIME's closed reference OTU picking workflows. THIS CODE IS CURRENTLY UNTESTED. YOU SHOULD NOT USE THIS VERSION OF THE CODE. THIS MESSAGE WILL BE REMOVED WHEN TESTS ARE ADDED."
    Parameters = ParameterCollection([
        Parameter(Name='input_sra', DataType=str,
                  Description='your input should be a list of .sra formatted strings', Required=True),
        Parameter(Name='output', DataType=str,
                  Description='the output is a fasta string', Required=True)
    ])

# sratoolkit and SCHIRMP are required to be installed by the User so that the tools sra_dumo and fastq_to_fasta can be called in the command line within the User $HOME.

    sra_dump_path = "/Users/giorgiocasaburi/Downloads/sratoolkit.2.3.1-mac64/bin/fastq-dump.2.3.1"
    fastq_to_fasta = "/Users/giorgiocasaburi/SHRiMP_2_2_2/utils/fastq_to_fasta"

    def run(self, **kwargs):
            
        input_sra_folder = kwargs['input_sra']
        if input_sra_folder[-1:] != "/":	
            input_sra_folder = input_sra_folder + "/"  
        input_filepaths = [] 
        
        for (dirpath, dirnames, filenames) in walk(input_sra_folder):
            input_filepaths.extend(filenames)
            break
        create_dir = kwargs['output']
    
        output_dir_1 = kwargs['output']


        for input_filepath in input_filepaths:
            print input_filepath
            output_filepath = output_dir_1 + input_filepath + ".fastq"
            command = "%s %s -O %s" % (self.sra_dump_path, input_sra_folder + input_filepath, output_filepath)

            stdout, stderr, ret_val = pyqi_system_call(command)
            print stdout, stderr, ret_val
            command = "rm %s" % (input_filepath)

            stdout, stderr, ret_val = pyqi_system_call(command)

            command = "%s %s/*.fastq > %s.fast" % (self.fastq_to_fasta, output_filepath, output_filepath)

            stdout, stderr, ret_val = pyqi_system_call(command)
            command = "rm -r %s" % (output_filepath)

            stdout, stderr, ret_val = pyqi_system_call(command)
            command = "sed 's/\./_/g;s/ .*$//g' %s*.fast > %s.fasta" % (output_filepath, output_filepath)

            stdout, stderr, ret_val = pyqi_system_call(command)
            command = "rm %s*.fast" % (input_filepath)

            stdout, stderr, ret_val = pyqi_system_call(command)
        
        return {'result': "sra file converted in fasta"}

CommandConstructor = SraToQiime


