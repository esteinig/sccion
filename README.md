# SCCion <a href='https://github.com/esteinig'><img src='docs/img/sccion.png' align="right" height="210" /></a>

![](https://img.shields.io/badge/version-0.1-blue.svg)
![](https://img.shields.io/badge/docs-none-green.svg)
![](https://img.shields.io/badge/lifecycle-experimental-orange.svg)

## Overview

`SCCion` is a bioinformatics toolkit for genotyping of *Staphylococcus aureus* sequence data. It provides three analysis streams:

1. fast whole genome typing from assemblies similar to `Kleborate`
2. parallelized read-to-assembly and read-genotyping pipeline in `Nextflow` 
3. real-time `MinHash` typing of uncorrected nanopore reads with `Sketchy`

`SCCion` combines a variety of databases sourced from many different open-source projects. Please make sure to have a look at the `Citations` section to see who to pay respect to for their valiant efforts in creating the databases used by `SCCion`.

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

`sccion type assembly`:

* Mash: https://github.com/marbl/Mash
* SCC*mec*-Finder: https://bitbucket.org/genomicepidemiology/
* Mykrobe: https://github.com/iqbal-lab/Mykrobe-predictor
* Ridom spa typing scheme: https://www.spaserver.ridom.de/
* mlst: https://github.com/tseemann/mlst
* Abricate: https://github.com/tseemann/abricate
* Resfinder: https://bitbucket.org/genomicepidemiology/
* VFDB: https://10.1093/nar/gki008
* Plasmidfinder: https://bitbucket.org/genomicepidemiology/

`sccion type nanopore`:

* Mash: https://github.com/marbl/Mash
* Nanopath @np-core: https://github.com/np-core/nanopath
* Sketchy: https://github.com/esteinig/sketchy

`sccion type nextflow illumina`:

* Trimmomatic: https://10.1093/bioinformatics/btu170
* Shovill: https://github.com/tseemann/shovill
* Prokka: https://github.com/tseemann/prokka
* Snippy: https://github.com/tseemann/snippy
* Spandx: https://github.com/dsarovich/spandx
* `sccion type assembly`

`sccion type nextflow ont`:

* wtdbg2: https://github.com/ruanjue/wtdbg2
* Nanopolish: https://github.com/jts/nanopolish
* `sccion type assembly`
