from sccion.utils import run_assembly_stats
from sccion.type import SpaType, MLST, Species, VirDB, ResDB, MGE, SCCmec
from pathlib import Path

from sccion.type import SpaType
from pathlib import Path


class SCCion:

    """ Base class """

    def __init__(
        self,
        forward: Path = None,
        reverse: Path = None,
        fasta: Path = None,
        outdir=None
    ):

        self.forward = forward
        self.reverse = reverse

        self.fasta = fasta
        self.outdir = outdir

        # Isolate genotype
        self.genotype = {
            'id': 'SRR3647382',
            'species': '',
            'mlst': '',
            'type': '',
            'sccmec': '',
            'pvl': True,
            'spa': '',
            'agr': '',
            'egc': '',
            'scc': '',
        }

        # Assembly statistics
        self.assembly = {
            'contigs': 50,
            'average_contig': 143000,
            'largest_contig': 150000,
            'n50': 50000,
        }

        # Scores

        self.scores = {
            'resistance': 3,
            'virulence': 2
        }

        # Resistance genes and mutations
        self.resistance = {
            'acquired': dict(),
            'mutations': dict(),
            'phenotype': dict(),
        }

        # Virulence genes
        self.virulence = dict(),

        # Mobile Elements
        self.mge = {
            'plasmids': dict(),
            'insertion_sequences': dict(),
            'transposons': dict(),
            'other': dict(),
        }

    def type_assembly(self):

        """ Access method for typing whole genome assemblies """

        # Run and parse assembly statistics module
        # self._get_assembly_statistics()

        self.genotype['spa'] = getattr(
            SpaType(fasta=self.fasta), 'spa_type'
        )

        self.genotype['mlst'] = getattr(
            MLST(fasta=self.fasta), 'mlst'
        )

        self.genotype['species'] = getattr(
            Species(fasta=self.fasta), 'scientific_name'
        )
        resdb = ResDB(fasta=self.fasta)
        self.resistance['acquired'] = getattr(resdb, 'acquired')
        self.genotype['type'] = getattr(resdb, 'type')

        virdb = VirDB(fasta=self.fasta)
        self.resistance['virulence'] = getattr(virdb, 'virulence')
        self.genotype['pvl'] = getattr(virdb, 'pvl')

        mge = MGE(fasta=self.fasta)
        self.mge['plasmids'] = getattr(mge, 'plasmids')

        sccmec = SCCmec(fasta=self.fasta)
        self.genotype['sccmec'] = getattr(sccmec, 'sccmec')

        print(
            f'{self.fasta.name}\t'
            f'{self.genotype["species"]}\t'
            f'ST{self.genotype["mlst"]}\t'
            f'{self.genotype["type"]}\t'
            f'{self.genotype["pvl"]}\t',
            f'{self.genotype["spa"]}\t',
            f'{self.genotype["sccmec"]}\t',
            f'{";".join(self.resistance["acquired"])}\t',
            f'{";".join(self.mge["plasmids"])}'
        )


    # Private methods for assembly genotyping

    def _get_assembly_statistics(self):

        """ Parse assembly metrics from assembly statistics output """

        run_assembly_stats(self.fasta)