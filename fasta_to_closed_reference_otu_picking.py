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
from tempfile import gettempdir
from pyqi.util import pyqi_system_call, remove_files
from pyqi.core.command import Command, CommandIn,CommandOut,ParameterCollection


class FastaToParallelPickOtusUclustRef(Command):
    BriefDescription = "This command allows to run a parallel closed-reference otu picking in Qiime using a fasta file containing mirna sequences (i.e. output from sra_to_qiime.py script)"
    LongDescription = "A command for running parallel closed-reference otu picking in Qiime in order to obtain a final biom table with the mirnas annotation that can be used for further analysis. THIS CODE IS CURRENTLY UNTESTED. YOU SHOULD NOT USE THIS VERSION OF THE CODE. THIS MESSAGE WILL BE REMOVED WHEN TESTS ARE ADDED."
    
    CommandIns = ParameterCollection([
        CommandIn(Name='input_file', DataType=str,
                  Description='directory containing the input mirnas fasta file', Required=True),
        CommandIn(Name='output_dir', DataType=str,
                  Description='the path where the output biom table with the mirnas annotation should be written', Required=True),
        CommandIn(Name='ncRNAdb_file', DataType=str,
                  Description='the path to the non coding rna database file', Required=True),
        CommandIn(Name='jobs_to_start', DataType=int,
                  Description='the number of jobs you want to run in parallel', Default=1),
        CommandIn(Name='mature_miRNAs_database_file', DataType=str,
                  Description='the path to the miRbase mature mirna database file', Required=True)
    
        ])
     
    CommandOuts = ParameterCollection([
        CommandOut(Name='status', DataType=str,
                  Description='the final result'),
        CommandOut(Name='error', DataType=str,
                  Description='the error result')
       
    ])

# Qiime is required to be installed by the User so that every scripts can be called in the command line within the User $HOME.
# The modified version of the Ensemble 'all non coding except mirnas (nc_ex_mirna)' database needs to be downloaded by the User.
# The human miRBase database needs to be downloaded by the user.

    # Scripts included in Qiime 
    parallel_pick_otus_uclust_ref_path = "parallel_pick_otus_uclust_ref.py"
    filter_fasta = "filter_fasta.py"
    make_otu_table = "make_otu_table.py"
    
    
    
    # Temporary folder to store the files:
    temp_dir = gettempdir()
    verbose = True

    def run(self, **kwargs):
        
        input_fp = kwargs['input_file']
       
        
        output_dir = kwargs['output_dir']
        
        ncrnadb_fp = kwargs['ncRNAdb_file']
        input_all_ncrna_except_mirna_database_pattern = ncrnadb_fp
        
        maturemirnadb_fp = kwargs['mature_miRNAs_database_file']
        input_human_mature_mirna_database_pattern = maturemirnadb_fp
         
         
        temp_files_to_remove = []
        temp_dirs_to_remove = []
        input_filename = split(input_fp)[1]
        input_basename = splitext(input_filename)[0]
            
        #Create and call the parallel_pick_otus_uclust_ref.py command and run it against Ensemble nc_ex_mirna database
        command = "%s -i %s -r %s -o %s -O %s --enable_rev_strand_match --max_accepts 1 --max_rejects 8 --stepwords 8 --word_length 8" % (self.parallel_pick_otus_uclust_ref_path, input_fp, input_all_ncrna_except_mirna_database_pattern, self.temp_dir, int(kwargs["jobs_to_start"]))
        if self.verbose:
                print command
        stdout, stderr, ret_val = pyqi_system_call(command)
        if ret_val != 0:
            raise Exception(stderr)


        # Filter all the sequences from the previous closed-reference picking otu that didn't hit the database (i.e. standard output from parallel_pick_otus_uclust_ref.py = *_failures.txt) using the script 'filter_fasta.py -f input_fasta -s index_list -o output) 
        temp_fasta_index_list_failing_to_hit_database_fp = join(self.temp_dir, '%s_failures.txt' % input_basename)
        temp_fasta_filtered_fp = join(self.temp_dir, '%s_filtered.fasta' % input_basename)

        command = "%s -f %s -s %s  -o %s" % (self.filter_fasta, input_fp, temp_fasta_index_list_failing_to_hit_database_fp, temp_fasta_filtered_fp)
        if self.verbose:
                print command
        stdout, stderr, ret_val = pyqi_system_call(command)
        if ret_val != 0:
            raise Exception(stderr)


        # Create and call the parallel_pick_otus_uclust_ref.py command against mirBase - human mature mirna database
            
        temp_index_of_otus_hitting_miRbase_fp= join(self.temp_dir, '%s_otus.txt' % input_basename)
        stdout, stderr, ret_val = pyqi_system_call(command)
        command = "%s -i %s -r %s -o %s --enable_rev_strand_match --max_accepts 1 --max_rejects 8 --stepwords 8 --word_length 8" % (self.parallel_pick_otus_uclust_ref_path, temp_fasta_filtered_fp, input_human_mature_mirna_database_pattern, self.temp_dir)
        if self.verbose:
                print command
        stdout, stderr, ret_val = pyqi_system_call(command)
        if ret_val != 0:
            raise Exception(stderr)

            
        # Create an otu_table using the outuput otu_map from the previous step:
            
            
        mirna_final_biom_table = join(output_dir, '%s.biom' % input_basename)
        command = "%s -i %s -o %s"  % (self.make_otu_table, temp_index_of_otus_hitting_miRbase_fp, mirna_final_biom_table)
        stdout, stderr, ret_val = pyqi_system_call(command)
        if self.verbose:
                print command
        stdout, stderr, ret_val = pyqi_system_call(command)
        if ret_val != 0:
            raise Exception(stderr)
            
        return {"status": "is ok",
                "error":None}
            # clean up (to do)
            

CommandConstructor = FastaToParallelPickOtusUclustRef