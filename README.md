# SCCion

SCC*mec* typing for MRSA

This is a simple program to determine staphylococcal cassette chromosome mec (SCC*mec*) types and subtypes/payloads for methicillin resistant *Staphylococcus aureus* from whole genome sequencing data. Current version can distinguish main types (I - XII) from single-end and paired-end Illumina reads and from high-quality assembled genomes.

### Usage

[sccion.readthedocs.io](https://sccion.readthedocs.io/)

### Install:

`conda install -c conda-forge -c bioconda -c esteinig sccion`

### Quick Start:

```
sccion type R1.fastq.gz R2.fastq.gz > results.json

sccion type DAR4145.fasta > results.json

sccion assemble --threads 8 --assembler shovill --outdir assembly R1.fastq.gz R2.fastq.gz |
sccion type - > results.json

sccion type DAR4145.fasta --mlst > results.json

```
