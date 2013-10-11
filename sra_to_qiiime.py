#!/usr/bin/env python
from __future__ import division

__author__ = "Giorgio Casaburi and Greg Caporaso"
__copyright__ = "Copyright 2013, The QIIME project"
__credits__ = ["Giorgio Casaburi and Greg Caporaso"]
__license__ = "GPL"
__version__ = "0.0.0-dev"
__maintainer__ = "Giorgio Casaburi and Greg Caporaso"
__email__ = "casaburi@ceinge.unina.it"

from pyqi.core.command import Command, Parameter, ParameterCollection

class sra_to_qiime(Command):
    BriefDescription = "A script for converting SRA miRNA sequence data into a format compatible with QIIME"
    LongDescription = "A script for converting SRA miRNA sequence data into a format that can be used with QIIME's closed reference OTU picking workflows. THIS CODE IS CURRENTLY UNTESTED. YOU SHOULD NOT USE THIS VERSION OF THE CODE. THIS MESSAGE WILL BE REMOVED WHEN TESTS ARE ADDED."
    Parameters = ParameterCollection([
        Parameter(Name='-i', DataType=str,
                  Description='your input .sra file', Required=True),
        Parameter(Name='-o', DataType=str,
                  Description='the output directory', Required=True,
                  Default=True)
    ])


sra_dump_path = "/Users/giorgiocasaburi/Downloads/sratoolkit.2.3.1-mac64/bin/fastq-dump.2.3.1"
fastq_to_fasta = "/Users/giorgiocasaburi/SHRiMP_2_2_2/utils/fastq_to_fasta"

    def run(self, **kwargs):
        option_parser, opts, args =\
       parse_command_line_parameters(**script_info)
    input_filepaths = glob(opts.input_glob)
    create_dir(opts.output_dir)
    output_dir = opts.output_dir
    print input_filepaths
    
    for input_filepath in input_filepaths:
        output_filepath = join(output_dir, input_filepath + ".fastq")
      command = "%s %s -O %s" % (sra_dump_path, input_filepath, output_filepath)
    	print command
    	stdout, stderr, ret_val = qiime_system_call(command)
    	command = "rm %s" % (input_filepath)
    	print command
    	stdout, stderr, ret_val = qiime_system_call(command)
    	print ""
    	command = "%s %s/*.fastq > %s.fast" % (fastq_to_fasta, output_filepath, output_filepath)
        print command
    	stdout, stderr, ret_val = qiime_system_call(command)
    	command = "rm %s/*.fastq" % (output_filepath)
    	print command
    	stdout, stderr, ret_val = qiime_system_call(command)
    	command = "sed 's/\./_/g;s/ .*$//g' %s*.fast > %s.fasta" % (output_filepath, output_filepath)
    	print command
    	stdout, stderr, ret_val = qiime_system_call(command)
        command = "rm %s*.fast" % (input_filepath)
    	print command
    	stdout, stderr, ret_val = qiime_system_call(command)
    	
if __name__ == "__main__":
    main()
CommandConstructor = sra_to_qiime
