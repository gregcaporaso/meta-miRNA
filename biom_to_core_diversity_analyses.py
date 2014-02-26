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
from pyqi.core.command import (Command, CommandIn, CommandOut,
    ParameterCollection)

class biomtocorediversityanalyses(Command):
    BriefDescription = "This command allows to run core diversity analysis using as input a biom table (i.e. output from fasta_to_closed_reference_otu_picking.py script)"
    LongDescription = "A command for running core diversity analysis using in Qiime in order to obtain alpha and beta diversity using a miRNAs biom table. Alpha diversity id performed with obsrved specied metric while the beta diversity with bray-curtis. THIS CODE IS CURRENTLY UNTESTED. YOU SHOULD NOT USE THIS VERSION OF THE CODE. THIS MESSAGE WILL BE REMOVED WHEN TESTS ARE ADDED."
    
    CommandIns = ParameterCollection([
        CommandIn(Name='input_file', DataType=str,
                  Description='directory containing the input biom table', Required=True),
        CommandIn(Name='output_dir', DataType=str,
                  Description='the path where the output of core diversity analysis should be written', Required=True),
        CommandIn(Name='sampling_depth', DataType=int,
                  Description='Sequencing depth to use for even sub-sampling and maximum rarefaction depth. You should review the output of print_biom_table_summary.py on the miRNAs biom table to decide on this value', Required=True),
        CommandIn(Name='jobs_to_start', DataType=int,
                  Description='the number of jobs you want to run in parallel', Default=1)
    
        ])

    CommandOuts = ParameterCollection([
        CommandOut(Name='status', DataType=str,
                  Description='the final result'),
        CommandOut(Name='error', DataType=str,
                  Description='the error result')
       
    ])

# Qiime is required to be installed by the User so that every scripts can be called in the command line within the User $HOME.

    # Scripts included in Qiime
    core_diversity_analyses_path = "core_diversity_analyses.py"
    
    
    
    # Temporary folder to store the files:
    temp_dir = gettempdir()
    verbose = True

    def run(self, **kwargs):
        
        input_fp = kwargs['input_file']
      
        output_dir = kwargs['output_dir']
        
                
        #Mapping file
        mapping_file_fp = kwargs['mapping_file_fp']
        input_mapping_file_pattern = join(mapping_file_fp,'mapping_file.txt')
        

        temp_files_to_remove = []
        temp_dirs_to_remove = []
        input_filename = split(input_fp)[1]
        input_basename = splitext(input_filename)[0]
            
        #Create and call the core_diversity_analysis.py command and run it using a miRNAs biom table
        command = "%s -i %s -m %s -e %s -o %s -O %s --suppress_otu_category_significance --nonphylogenetic_diversity" % (self.core_diversity_analyses_path, input_fp, mapping_file_fp, int(kwargs["sampling_depth"]), output_dir, int(kwargs["jobs_to_start"]))
        if self.verbose:
                print command
        stdout, stderr, ret_val = pyqi_system_call(command)
        if ret_val != 0:
            
                return {"status":ret_val,
                        "error":stderr}
            


            
            
            # clean up (to do)
            

CommandConstructor = biomtocorediversityanalyses