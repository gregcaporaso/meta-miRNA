from __future__ import division

__author__ = "Giorgio Casaburi and Greg Caporaso"
__copyright__ = "Copyright 2013, The miMAP project"
__credits__ = "Giorgio Casaburi", "Greg Caporaso"
__license__ = "GPL"
__version__ = "0.0.0-dev"
__maintainer__ = "Giorgio Casaburi"
__email__ = "casaburi@ceinge.unina.it"

from shutil import rmtree
from os import walk
from os.path import join, split, splitext, exists
from glob import glob

from pyqi.util import pyqi_system_call, remove_files
from pyqi.core.command import Command, CommandIn,CommandOut,ParameterCollection

class SraToQiime(Command):
    BriefDescription = "post split libraries format: This script allows to convert .sra miRNA sequence data into a QIIME compatible format"
    LongDescription = "A script for converting SRA miRNA sequence data into a format that can be used with QIIME's closed reference OTU picking workflows. THIS CODE IS CURRENTLY UNTESTED. YOU SHOULD NOT USE THIS VERSION OF THE CODE. THIS MESSAGE WILL BE REMOVED WHEN TESTS ARE ADDED."
    CommandIns = ParameterCollection([
        CommandIn(Name='input_dir', DataType=str,
                  Description='directory containng input .sra files', Required=True),
        CommandIn(Name='output_fp', DataType=str,
                  Description='the path where the output fasta file should be written', Required=True)
    ])

    CommandOuts = ParameterCollection([
        CommandOut(Name='result', DataType=str,
                  Description='the final result')
       
    ])

# sratoolkit and SCHIRMP are required to be installed by the User so that the tools sra_dump and fastq_to_fasta can be called in the command line within the User $HOME.

    sra_dump_path = "fastq-dump.2.3.1"
    fastq_to_fasta = "fastq_to_fasta"
    temp_dir = "/tmp/"
    verbose = True

    def run(self, **kwargs):
        
        input_dir = kwargs['input_dir']
        input_sra_pattern = join(input_dir,'*.sra')
        input_filepaths = glob(input_sra_pattern)
        output_fp = kwargs['output_fp']

        for input_filepath in input_filepaths:
            temp_files_to_remove = []
            temp_dirs_to_remove = []
            input_filename = split(input_filepath)[1]
            input_basename = splitext(input_filename)[0]
            
            # create and call the sra-dump command
            temp_fastq_dir = join(self.temp_dir, '%s_fastq' % input_basename) 
            command = "%s %s -O %s" % (self.sra_dump_path, input_filepath, temp_fastq_dir)
            if self.verbose:
                print command
            stdout, stderr, ret_val = pyqi_system_call(command)
            temp_dirs_to_remove.append(temp_fastq_dir)
            temp_fastq_fp = glob(join(temp_fastq_dir,'*.fastq'))[0]

			# convert fastq to fasta
            temp_fasta_fp = join(self.temp_dir, '%s.fasta' % input_basename)
            command = "%s %s > %s" % (self.fastq_to_fasta, temp_fastq_fp, temp_fasta_fp)
            stdout, stderr, ret_val = pyqi_system_call(command)
            if self.verbose:
                print command
            temp_files_to_remove.append(temp_fasta_fp)

			# convert fasta to qiime-compatible headers
            stdout, stderr, ret_val = pyqi_system_call(command)
            command = "sed 's/\./_/g;s/ .*$//g' %s >> %s" % (temp_fasta_fp, output_fp)
            stdout, stderr, ret_val = pyqi_system_call(command)
            if self.verbose:
                print command
            
            # clean up
            #if self.verbose:
             #   print "Removing files: %s" % " ".join(temp_files_to_remove)
              #  print "Removing directories: %s" % " ".join(temp_dirs_to_remove)
            #remove_files(temp_files_to_remove)
            #for temp_dir_to_remove in temp_dirs_to_remove:
             #   rmtree(temp_dir_to_remove)
        
        return {'result': output_fp}

CommandConstructor = SraToQiime