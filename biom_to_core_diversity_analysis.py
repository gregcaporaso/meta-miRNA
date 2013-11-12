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

class biomtocorediversityanalysis(Command):
    BriefDescription = "This command allows to run core diversity analysis using as input a biom table (i.e. output from fasta_to_closed_reference_otu_picking.py script)"
    LongDescription = "A command for running core diversity analysis using in Qiime in order to obtain alpha and beta diversity using a miRNAs biom table. Alpha diversity id performed with obsrved specied metric while the beta diversity with bray-curtis. THIS CODE IS CURRENTLY UNTESTED. YOU SHOULD NOT USE THIS VERSION OF THE CODE. THIS MESSAGE WILL BE REMOVED WHEN TESTS ARE ADDED."
    Parameters = ParameterCollection([
        Parameter(Name='input_dir', DataType=str,
                  Description='directory containing the input biom table', Required=True),
        Parameter(Name='output_dir', DataType=str,
                  Description='the path where the output of core diversity analysis should be written', Required=True),
        Parameter(Name='sampling_depth', DataType=int,
                  Description='Sequencing depth to use for even sub-sampling and maximum rarefaction depth. You should review the output of print_biom_table_summary.py on the miRNAs biom table to decide on this value', Required=True),
        Parameter(Name='mapping_file', DataType=str,
                  Description='the path to the mapping file associated with your samples', Required=True)
    
        ])

# Qiime is required to be installed by the User so that every scripts can be called in the command line within the User $HOME.

    # Scripts included in Qiime 
    core_diversity_anlysis_path = "core_diversity_analyses.py"
    
    
    
    # Temporary folder to store the files:
    temp_dir = "/tmp/miMAP"
    verbose = True

    def run(self, **kwargs):
        
        input_dir = kwargs['input_dir']
        input_biom_table_pattern = join(input_dir,'*.biom')
        input_filepath = glob(input_biom_table_pattern)
        
        output_dir = kwargs['output_dir']
        
        sampling_depth = kwargs['sampling_depth']
        
        
        
        mapping_file = kwargs['mapping_file']
        input_mapping_file_pattern = (mapping_file + 'mapping_file.txt')
        

        for input_filepath in input_filepath:
            temp_files_to_remove = []
            temp_dirs_to_remove = []
            input_filename = split(input_filepath)[1]
            input_basename = splitext(input_filename)[0]
            
            #Create and call the core_diversity_analysis.py command and run it using a miRNAs biom table
            command = "%s -i %s -m %s -e %s -o %s  --suppress_otu_category_significance --nonphylogenetic_diversity" % (self.core_diversity_anlysis_path, input_filepath,  mapping_file, sampling_depth, output_dir)
            if self.verbose:
                print command
            stdout, stderr, ret_val = pyqi_system_call(command)
            if ret_val != 0:
            
                return {"status":ret_val,
                        "error":stderr}
            


            
            
            # clean up (to do)
            

CommandConstructor = biomtocorediversityanalysis

