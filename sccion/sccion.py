from sccion.utils import run_assembly_stats
from sccion.type import SpaType, MLST, Species, VirDB, ResDB, MGE, SCCmec

from sccion.type import SpaType
from pathlib import Path


class SCCion:

    """ Base class """

    def __init__(
        self,
        fasta: Path = None,
        outdir=None,
        forward: Path = None,
        reverse: Path = None,
    ):

        self.forward = forward
        self.reverse = reverse

        self.fasta = fasta
        self.outdir = outdir

        # Isolate genotype
        self.genotype = {
            'id': str(),
            'species': str(),
            'mlst': str(),
            'type': str(),
            'sccmec': str(),
            'pvl': True,
            'spa': str(),
            'agr': str(),
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

    def type_assembly(
        self,
        min_identity: float = 0.9,
        min_coverage: float = 0.7
    ):

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

        resdb = ResDB(
            fasta=self.fasta,
            min_identity=min_identity,
            min_coverage=min_identity,
        )

        self.resistance['acquired'] = getattr(resdb, 'acquired')
        self.genotype['type'] = getattr(resdb, 'type')

        virdb = VirDB(
            fasta=self.fasta,
            min_identity=min_identity,
            min_coverage=min_identity,
        )

        self.resistance['virulence'] = getattr(virdb, 'virulence')
        self.genotype['pvl'] = getattr(virdb, 'pvl')

        mge = MGE(
            fasta=self.fasta,
            db='plasmidfinder',
            min_identity=min_identity,
            min_coverage=min_identity,
        )

        self.mge['plasmids'] = getattr(mge, 'plasmids')

        sccmec = SCCmec(
            fasta=self.fasta
        )

        if resdb.type == "MRSA":
            # Only if mecA detected get SCCmec - crude filter for now
            self.genotype['sccmec'] = getattr(sccmec, 'sccmec')
        else:
            self.genotype['sccmec'] = '-'

        if self.genotype['species'] != 'Staphylococcus aureus':
            self.genotype['type'] = "-"

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