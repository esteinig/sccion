# SCCion <a href='https://github.com/esteinig'><img src='docs/img/sccion.png' align="right" height="210" /></a>

![](https://img.shields.io/badge/version-0.1-blue.svg)
![](https://img.shields.io/badge/docs-none-green.svg)
![](https://img.shields.io/badge/lifecycle-experimental-orange.svg)

## Overview

`SCCion` is a bioinformatics toolkit for genotyping of *Staphylococcus aureus* sequence data. It provides three streams for analysis of MRSA genome data: 

1. fast whole genome typing from assemblies similar to programs like `Kleborate`
2. parallelized read-to-assembly and read-genotyping pipeline in `Nextflow` 
3. real-time `MinHash` typing of uncorrected nanopore reads with `Sketchy`

`SCCion` combines a variety of databases constructed during previous efforts to develop genome typing programs specific to MRSA. As such, it is an agglomerate beast that sources from many different open-source projects. Please make sure to have a look at the `Citations` section to figure out who to pay honor and respect to, for their efforts in creating some of the underlying databases used in this program.

Pre-print available on BioRxiv.

### Install
---

`conda install -c conda-forge -c bioconda -c esteinig sccion`

### Usage
---

From assembly:

```
sccion type reference.fasta
```

From assemblies:

```
sccion type path/to/assemblies/*.fasta
```

From uncorrected nanopore reads

```
sccion type reads.fastq --limit 1000
```

From uncorrected nanopore reads, live watching directory

```
sccion type path/to/basecalled/fastq
```

Nextflow set of paired end reads on default `PBS` cluster configuration:

```
nextflow pf-core/pf-sccion -profile cluster --fastq path/to/fastq/*.fq.gz
```

### Docs
---

[sccion.readthedocs.io](https://sccion.readthedocs.io/)

### Citations
---

`sccion type default`:

* Mash
* SCC*mec*-Finder
* Mykrobe
* Ridom spa typing scheme
* mlst
* Abricate
* Resfinder
* VFDB
* Plasmidfinder
* Nanopath @np-core
