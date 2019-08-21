#!/usr/bin/env nextflow

/*
 *
 *  Pipeline            SCCion parallel
 *  Version             0.1
 *  Description         Parallel exeution of sccion type -a
 *  Authors             Eike Steinig
 *
 */


log.info """

|===================================================|
|                     PF-SCCION                     |
|                        v0.1                       |
|===================================================|

fasta           = $params.fasta
outdir          = $params.outdir

|===================================================|
|===================================================|

"""




fasta = Channel.fromPath(params.fasta).map { file -> tuple(file.baseName, file) }



process SCCionAssembly {

  label "sccion"
  tag { "$id" }

  publishDir "${params.outdir}"


  input:
  set id, file(fasta) from fasta

  output:
  file("${id}.txt")


  script:
  """
  sccion type -a $fasta > ${id}.txt
  """

}
