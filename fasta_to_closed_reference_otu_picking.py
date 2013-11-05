#!/usr/bin/env python
from __future__ import division

__author__ = "Giorgio Casaburi and Greg Caporaso"
__copyright__ = "Copyright 2013, The miMAP project"
__credits__ = "Giorgio Casaburi", "Greg Caporaso"
__license__ = "GPL"
__version__ = "0.0.0-dev"
__maintainer__ = "Giorgio Casaburi"
__email__ = "casaburi@ceinge.unina.it"

from shutil import rmtree
from os.path import join, split, splitext, exists
from glob import glob

from pyqi.util import pyqi_system_call, remove_files
from pyqi.core.command import Command, Parameter, ParameterCollection

class FastaToParallelPickOtusUclustRef(Command):
    BriefDescription = "This script allows to run a parallel closed-reference otu picking in Qiime using a fasta file containing miRNA sequences (i.e. output from sra_to_qiime.py script)"
    LongDescription = "A script for running parallel closed-reference otu picking in Qiime in order to obtain a final biom table with the miRNas annotation that can be used for further analysis. THIS CODE IS CURRENTLY UNTESTED. YOU SHOULD NOT USE THIS VERSION OF THE CODE. THIS MESSAGE WILL BE REMOVED WHEN TESTS ARE ADDED."
    Parameters = ParameterCollection([
        Parameter(Name='input_dir', DataType=str,
                  Description='directory containing the input miRNAs fasta file', Required=True),
        Parameter(Name='output_fp', DataType=str,
                  Description='the path where the output biom table with the miRNAs annotation should be written', Required=True)
    ])

# Qiime is required to be installed by the User so that every scripts can be called in the command line within the User $HOME.
# The modified version of the Ensemble 'all non coding except miRNAs (nc_ex_miRNA)' database needs to be downloaded by the User.
# The human miRBase database needs to be downloaded by the user.

    # Scripts included in Qiime 
    parallel_pick_otus_uclust_ref_path = "parallel_pick_otus_uclust_ref.py"
    filter_fasta = "filter_fasta.py"
    make_otu_table = "make_otu_table.py"
    
    # Database
    all_ncrna_except_miRNA_database_dir = "/Users/giorgiocasaburi/Desktop/rna_data_base/all_ncrna_except_mirna/all_ncrna_nomirna.fasta"
    mirBase = "/Users/giorgiocasaburi/Desktop/rna_data_base/mirBase_13_6/miRbase_13_6_2013_human.fasta"
    
    # Temporary folder to store the files:
    temp_dir = "/tmp/"
    verbose = True

    def run(self, **kwargs):
        
        input_dir = kwargs['input_dir']
        input_fasta_file = join(input_dir,'*.fasta')
        input_filepaths = glob(input_fasta_file)
        output_fp = kwargs['output_fp']

        for input_filepath in input_filepaths:
            temp_files_to_remove = []
            temp_dirs_to_remove = []
            input_filename = split(input_filepath)[1]
            input_basename = splitext(input_filename)[0]
            
            # Create and call the parallel_pick_otus_uclust_ref.py command and run it against Ensemble nc_ex_miRNA database
            command = "%s -i %s -r %s -o %s --enable_rev_strand_match --max_accepts 1 --max_rejects 8 --stepwords 8 --word_length 8" % (self.parallel_pick_otus_uclust_ref_path, input_filepath, self.all_ncrna_except_miRNA_database_dir, self.temp_dir)
            if self.verbose:
                print command
            stdout, stderr, ret_val = pyqi_system_call(command)

		    
			
			# Filter all the sequences from the previous closed-reference picking otu that didn't hit the database (i.e. standard output from parallel_pick_otus_uclust_ref.py = *_failures.txt) using the script 'filter_fasta.py -f input_fasta -s index_list -o output) 
            temp_fasta_index_list_failing_to_hit_database_fp = join(self.temp_dir, '%s_failures.txt' % input_basename)
            temp_fasta_filtered_fp = join(self.temp_dir, '%s.fasta' % input_basename)

            command = "%s -f %s -s %  -o %s" % (self.filter_fasta, input_filepath, temp_fasta_index_list_failing_to_hit_database_fp, temp_fasta_filtered_fp)
            stdout, stderr, ret_val = pyqi_system_call(command)
            if self.verbose:
                print command

			# Create and call the parallel_pick_otus_uclust_ref.py command against mirBase - human mature miRNA database
            
            temp_index_of_otus_hitting_miRbase_fp= join(self.temp_dir, '%s_otus.txt' % input_basename)
            stdout, stderr, ret_val = pyqi_system_call(command)
            command = "%s -i %s -r %s -o %s --enable_rev_strand_match --max_accepts 1 --max_rejects 8 --stepwords 8 --word_length 8" % (self.parallel_pick_otus_uclust_ref_path, temp_fasta_filtered_fp, mirBase, temp_index_of_otus_hitting_miRbase_fp)
            stdout, stderr, ret_val = pyqi_system_call(command)
            if self.verbose:
                print command
            
            
            # Create an otu_table using the output otu list file from the previous step:
            
            stdout, stderr, ret_val = pyqi_system_call(command)
            command = "%s -i %s -o %s"  % (self.make_otu_table, temp_index_of_otus_hitting_miRbase_fp, output_fp)
            stdout, stderr, ret_val = pyqi_system_call(command)
            if self.verbose:
                print command
            
            
            # clean up to do
            

CommandConstructor = FastaToParallelPickOtusUclustRef

