# SCCion

SCC*mec* typing for MRSA

This is a simple program to determine staphylococcal cassette chromosome mec (SCC*mec*) types and subtypes/payloads for methicillin resistant *Staphylococcus aureus*  (MRSA) from whole genome sequencing data. The current version can distinguish main types (I - XII) from single-end and paired-end Illumina reads and from high-quality assembled genomes. Results include common payloads and assemblies can be typed for MLST.

### Usage
---

[sccion.readthedocs.io](https://sccion.readthedocs.io/)

### Install
---

`conda install -c conda-forge -c bioconda -c esteinig sccion`

### Quick Start
---

```
# From paired-end reads:
sccion type R1.fastq.gz R2.fastq.gz > results.json

# From assembly:
sccion type DAR4145.fasta > results.json

# From assembly with MLST:
sccion type DAR4145.fasta --mlst > results.json

# Assemble with Shovill and type from assembly:
sccion assemble --threads 8 --assembler shovill --outdir assembly R1.fastq.gz R2.fastq.gz |
sccion type - > results.json

```
