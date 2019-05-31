# SCCion <a href='https://github.com/esteinig'><img src='docs/img/sccion.png' align="right" height="210" /></a>

![](https://img.shields.io/badge/version-0.1-blue.svg)
![](https://img.shields.io/badge/docs-none-green.svg)
![](https://img.shields.io/badge/lifecycle-experimental-orange.svg)

## Overview

`SCCion` is a genotyping toolkit for *Staphylococcus aureus* sequence data. It provides three analysis methods:

1. fast whole genome typing from assemblies similar to `Kleborate`
2. parallelized read-to-assembly and read-genotyping pipeline in `Nextflow` 
3. real-time `MinHash` typing of uncorrected nanopore reads with `Sketchy`

The last component is somewhat experimental, and should be considered a pre-release for now until `Sketchy` is more mature and has tests and stuff. However, in the few bootstrap analyses we have run on data from *S. aureus* it performed reasonably well, specifically because we have generated an extensive index of *S. aureus* genomes from the European Nucleotide Archive for `Sketchy`. Do not rely on it for more serious matters, like clinical diagnostics. All in all, `SCCion` combines a variety of databases sourced from many different open-source projects. Please make sure to have a look at the `Citations` section to see who to pay respect to for their valiant efforts in creating the databases used by `SCCion`.

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

From uncorrected nanopore reads:

```
sccion type reads.fq.gz --limit 1000
```

From uncorrected nanopore reads, live run, watching directory:

```
sccion type path/to/basecalled/fastq
```

Nextflow set of paired end reads on default `PBS` cluster configuration:

```
nextflow pf-core/pf-sccion -profile cluster --fastq path/to/fastq/*.fq.gz
```

### Modules 
---

* Genome assembly typing
* Real-time nanopore typing with `Sketchy`
* Illumina and ONT read-to-assembly pipelines in `Nextflow`

### Limitations
---

Most importantly, `SCCion` expects input that is definitely *S. aureus* or at least a Staphylococcal species (but then SCC*mec* typing and other genotypes might be off). This is also true for the real-time nanopore typing component, which will break and do all sorts of funky things if input is from species other than *S. aureus*. One can use a prefiltering step on the reads to make sure this is the case as outlined over at the repository for `Sketchy`.

`SCCion` also uses a simple `MinHash` matching with `MASH` against the small database of whole SCC*mec* cassette types collected by the authors of SCC*mec*Finder. It does not have the rigorous error checking as the original implementation and for detailed typing SCC*mec*Finder should be preferred. 

### Citations
---

We rely on a host of excellent software and all too it can go unnoticed when it is wrapped into a program like `SCCion`. When using `SCCion` please also cite `MASH, SCCmecFinder, Mykrobe, Sketchy, Abricate DBs` and refer to the unpublished programs by URL. For specific assembly and typing pipelines, please refer to the tables below.

You can output all citations in `RIS` format by using:

`sccion cite -o sccion_citations`

---

`sccion type assembly`:

| Program         |Author(s)                |Publication                                                       | Code                                               |
|-----------------|-------------------------|------------------------------------------------------------------|----------------------------------------------------|
| MASH            | Ondov et al.            |![](https://img.shields.io/badge/pub-ncbi-blue.svg)               |![](https://img.shields.io/badge/src-ncbi-green.svg)|
| SCC*mec*Finder  |                         |![](https://img.shields.io/badge/pub-ncbi-blue.svg)               |![](https://img.shields.io/badge/src-ncbi-green.svg)|
| Mykrobe         |                         |![](https://img.shields.io/badge/pub-ncbi-blue.svg)               |![](https://img.shields.io/badge/src-ncbi-green.svg)|
| Ridom Spa       | Ondov et al.            |![](https://img.shields.io/badge/pub-ncbi-blue.svg)               |![](https://img.shields.io/badge/src-ncbi-green.svg)|
| mlst            |                         |![](https://img.shields.io/badge/pub-ncbi-blue.svg)               |![](https://img.shields.io/badge/src-ncbi-green.svg)|
| Abricate        |                         |![](https://img.shields.io/badge/pub-ncbi-blue.svg)               |![](https://img.shields.io/badge/src-ncbi-green.svg)|
| Resfinder       | Ondov et al.            |![](https://img.shields.io/badge/pub-ncbi-blue.svg)               |![](https://img.shields.io/badge/src-ncbi-green.svg)|
| Plasmidfinder   |                         |![](https://img.shields.io/badge/pub-ncbi-blue.svg)               |![](https://img.shields.io/badge/src-ncbi-green.svg)|
| VFDB            |                         |![](https://img.shields.io/badge/pub-ncbi-blue.svg)               |![](https://img.shields.io/badge/src-ncbi-green.svg)|


`sccion type nanopore`:

| Program         |Author(s)                |Publication                                                       | Code                                               |
|-----------------|-------------------------|------------------------------------------------------------------|----------------------------------------------------|
| MASH            | Ondov et al.            |![](https://img.shields.io/badge/pub-ncbi-blue.svg)               |![](https://img.shields.io/badge/src-ncbi-green.svg)|
| Sketchy         | Steinig et al.          |![](https://img.shields.io/badge/pub-ncbi-blue.svg)               |![](https://img.shields.io/badge/src-ncbi-green.svg)|
| Nanopath        | Steinig                 |![](https://img.shields.io/badge/pub-ncbi-blue.svg)               |![](https://img.shields.io/badge/src-ncbi-green.svg)|

`sccion illumina`:

| Program         |Author(s)                |Publication                                                       | Code                                               |
|-----------------|-------------------------|------------------------------------------------------------------|----------------------------------------------------|
| Trimmomatic     |                         |![](https://img.shields.io/badge/pub-ncbi-blue.svg)               |![](https://img.shields.io/badge/src-ncbi-green.svg)|
| Shovill         | Seemann et al.          |![](https://img.shields.io/badge/pub-ncbi-blue.svg)               |![](https://img.shields.io/badge/src-ncbi-green.svg)|
| Prokka          | Seemann                 |![](https://img.shields.io/badge/pub-ncbi-blue.svg)               |![](https://img.shields.io/badge/src-ncbi-green.svg)|
| Snippy          | Seemann et al.          |![](https://img.shields.io/badge/pub-ncbi-blue.svg)               |![](https://img.shields.io/badge/src-ncbi-green.svg)|
| SPANDx          | Sarovich et al.         |![](https://img.shields.io/badge/pub-ncbi-blue.svg)               |![](https://img.shields.io/badge/src-ncbi-green.svg)|


`sccion ont`:

| Program         |Author(s)                |Publication                                                       | Code                                               |
|-----------------|-------------------------|------------------------------------------------------------------|----------------------------------------------------|
| FLYE            |                         |![](https://img.shields.io/badge/pub-ncbi-blue.svg)               |![](https://img.shields.io/badge/src-ncbi-green.svg)|
| wtdbg2          |                         |![](https://img.shields.io/badge/pub-ncbi-blue.svg)               |![](https://img.shields.io/badge/src-ncbi-green.svg)|
| Racon           |                         |![](https://img.shields.io/badge/pub-ncbi-blue.svg)               |![](https://img.shields.io/badge/src-ncbi-green.svg)|
| Medaka          |                         |![](https://img.shields.io/badge/pub-ncbi-blue.svg)               |![](https://img.shields.io/badge/src-ncbi-green.svg)|
| Nanopolish      |                         |![](https://img.shields.io/badge/pub-ncbi-blue.svg)               |![](https://img.shields.io/badge/src-ncbi-green.svg)|

