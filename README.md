miMAP: A tool for ecological analysis and meta-analysis of micro-interference RNA profiles
==========================================================================================


miMAP is a tool for allowing microRNA meta analysis. Users can download public dataset (e.g., from the [Sequence Read Archive (SRA)](http://www.ncbi.nlm.nih.gov/sra) directly processable in the tool or provide their own data.
Once the sequences are extracted from the .sra archive they are made compatibale to work in [QIIME](www.qiime.org), then the following steps occur:

1. Performing a closed-reference miRNAs picking against a modified version of the [Human Ensemble non-coding RNA database](ftp://ftp.ensembl.org/pub/release-73/fasta/homo_sapiens/ncrna/) without the miRNAs annotation.


2. Filtering from the original sequences file all the sequences that did not hit the Human Ensemble non-coding RNA database.


3. Performing another closed-reference miRNAs picking with the filtered sequences from step 2. against the [miRBASE mature miRNAs database](http://www.mirbase.org/ftp.shtml)


4. Making a miRNA table from step 3.


5. Computing principal coordinate analysis with Bray Curtis



miMAP installation guide
========================

miMAP consists of  pyqi and python code and use some external applications. 



