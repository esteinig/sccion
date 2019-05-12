# SCCion <a href='https://github.com/esteinig'><img src='docs/img/sccion.png' align="right" height="210" /></a>

![](https://img.shields.io/badge/version-0.1-blue.svg)
![](https://img.shields.io/badge/docs-none-green.svg)
![](https://img.shields.io/badge/lifecycle-experimental-orange.svg)

## Overview

`SCCion` is a bioinformatics toolkit for genotypiong *Staphylococcus aureus* seqeunce data. It provides three streams for analysis: fast whole genome typing from assemblies, parallelized read-to-assembly and read-genotyping pipeline in `Nextflow` and real-time `MinHash` typing of uncorrected nanopore reads with `Sketchy`. It combines a variety of databases constructed during previous efforts to develop genoem typing programs specific to MRSA. As such, `SCCion` is an agglomerate beast that sources from many different open-source projects. Please make sure to have a look at the `Citations` section to figure out who to pay honor and respect to, for their efforts in creating some of the underlying databases used in this program.

Pre-print available on BioRxiv.

### Docs
---

[sccion.readthedocs.io](https://sccion.readthedocs.io/)

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
