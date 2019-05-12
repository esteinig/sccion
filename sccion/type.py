import sys
from itertools import groupby
from pathlib import Path
from sccion.utils import run_mlst, run_mash_dist, run_abricate


class MGE:

    def __init__(
        self,
        fasta: Path,
        db: str = 'plasmidfinder',
        min_identity: float = 0.9,
        min_coverage: float = 0.7
    ):

        self.fasta = fasta

        # Abricate

        self.db = db
        self.min_identity = min_identity
        self.min_coverage = min_coverage

        self.plasmids = self._get_plasmidfinder()

    def _get_plasmidfinder(self):

        self.plasmid_table = run_abricate(
            fasta=self.fasta,
            db=self.db,
            min_identity=self.min_identity,
            min_coverage=self.min_coverage,
        )

        self.plasmid_table['gene'] = [
            gene.split('_')[0] for gene in self.plasmid_table['gene']
        ]

        return list(
            set(self.plasmid_table['gene'])
        )


class SCCmec:

    def __init__(
        self,
        fasta: Path,
        db: Path = Path(__file__).parent / 'db' / 'sccmec.msh'
    ):

        self.sccmec = "; subtype: ".join(
            run_mash_dist(fasta=fasta, db=db).split('|')[:2]
        )


class VirDB:

    def __init__(
        self,
        fasta: Path,
        db: str = 'vfdb',
        min_identity: float = 0.9,
        min_coverage: float = 0.7
    ):

        self.fasta = fasta

        # Abricate

        self.db = db
        self.min_identity = min_identity
        self.min_coverage = min_coverage

        self.virulence, self.pvl = self._get_abricate_vir()

    def _get_abricate_vir(self):

        self.virulence_table = run_abricate(
            fasta=self.fasta,
            db=self.db,
            min_identity=self.min_identity,
            min_coverage=self.min_coverage,
        )

        self.virulence_table['gene'] = [
            gene.split('_')[0] for gene in self.virulence_table['gene']
        ]

        return list(
            set(self.virulence_table['gene'])
        ), self._get_pvl_status()

    def _get_pvl_status(self):

        lukf = 'lukF-PV' in self.virulence_table['gene'].to_list()
        luks = 'lukS-PV' in self.virulence_table['gene'].to_list()

        if lukf and luks:
            return 'PVL+'
        if not lukf and not luks:
            return 'PVL-'
        else:
            return 'PVL*'


class ResDB:

    def __init__(
        self,
        fasta: Path,
        db: str = 'resfinder',
        min_identity: float = 0.9,
        min_coverage: float = 0.7
    ):

        self.fasta = fasta

        # Abricate

        self.db = db
        self.min_identity = min_identity
        self.min_coverage = min_coverage

        self.acquired, self.type = self._get_acquired_resistance()

    def _get_acquired_resistance(self):

        self.acquired_table = run_abricate(
            fasta=self.fasta,
            db=self.db,
            min_identity=self.min_identity,
            min_coverage=self.min_coverage,
        )

        self.acquired_table['gene'] = [
            gene.split('_')[0] for gene in self.acquired_table['gene']
        ]

        return self.acquired_table['gene'].to_list(), self._get_type_status()

    def _get_type_status(self):

        return 'MRSA' \
            if 'mecA' in \
               self.acquired_table['gene'].to_list() \
            else 'MSSA'


    def _get_mutations(self):
        pass


class Species:
    """ Wrapper for mash/screen """

    def __init__(
        self,
        fasta: Path,
    ):

        self.scientific_name = run_mash_dist(
            fasta
        )


class MLST:
    """ Wrapper for tseemann/mlst """

    def __init__(
        self,
        fasta: Path,
    ):

        _, self.species, self.mlst, self.alleles = run_mlst(fasta)



class SpaType:
    """ Based on """
    def __init__(
        self,
        fasta: Path,
        spa_repeat_file: Path = Path(__file__).parent / 'db' / 'spa.repeats.fasta',
        spa_type_file: Path = Path(__file__).parent / 'db' / 'spa.types.csv'
    ):

        self.fasta = fasta
        self.spa_repeat_file = spa_repeat_file
        self.spa_type_file = spa_type_file

        self.spa_repeat, self.spa_type = self._get_spa_type()

    def _get_spa_type(self):

        seq_dict, let_dict, type_dict, seq_lengths = self.get_spa_types(
            self.spa_repeat_file,
            self.spa_type_file
        )

        return self.find_spa_type(
            infile=self.fasta,
            seq_dict=seq_dict,
            let_dict=let_dict,
            type_dict=type_dict,
            seq_lengths=seq_lengths
        )

    # reverse translate a DNA sequence
    @staticmethod
    def revseq(seq):
        transtab = str.maketrans('atcgATCG', 'tagcTAGC')
        seq = seq[::-1]
        seq = seq.translate(transtab)
        return seq

    @staticmethod
    def fasta_dict(fasta_name):
        """
        given a fasta file. yield dict of header, sequence
        """
        seq_dict = {}
        with open(fasta_name) as fh:
            faiter = (x[1] for x in groupby(fh, lambda line: line[0] == ">"))
            for header in faiter:
                header = next(header)[1:].strip()
                seq = "".join(s.strip() for s in next(faiter))
                if header in seq_dict:
                    sys.exit('FASTA contains multiple entries with the same name')
                else:
                    seq_dict[header] = seq
        return seq_dict

    def enrich_seq(self, seq, fortemp, revtemp):
        index = 0
        found = None
        out1 = []
        out_list = []
        while found != -1:
            found = seq.find(fortemp, index)
            index = found + 1
            if found != -1:
                out1.append(found)
        index = 0
        found = None
        out2 = []
        revtempr = self.revseq(revtemp)
        while found != -1:
            found = seq.find(revtempr, index)
            index = found + 1
            if found != -1:
                out2.append(found)
        for j in out1:
            for k in out2:
                if k - j > 50 and k - j < 5000:
                    enriched_seq = seq[j:k+len(revtemp)]
                    out_list.append(enriched_seq)
        index = 0
        found = None
        out1 = []
        fortempr = self.revseq(fortemp)
        while found != -1:
            found = seq.find(fortempr, index)
            index = found + 1
            if found != -1:
                out1.append(found)
        index = 0
        found = None
        out2 = []
        while found != -1:
            found = seq.find(revtemp, index)
            index = found + 1
            if found != -1:
                out2.append(found)
        for j in out2:
            for k in out1:
                if k - j > 50 and k - j < 5000:
                    enriched_seq = seq[j:k+len(fortemp)]
                    out_list.append(
                        self.revseq(enriched_seq)
                    )
        return out_list

    def get_spa_types(self, spa_repeats, spa_types):

        seq_dict = {}
        let_dict = {
            '58': 'B4', '30': 'O2', '54': 'H3',
            '42': 'M2', '48': 'V2', '45': 'A3',
            '43': 'X2', '60': 'S2', '61': 'W3',
            '62': 'U3', '57': 'S', '64': 'X3',
            '49': 'Y2', '66': 'F4', '90': 'I',
            '68': 'E4', '69': 'C4', '80': 'K4',
            '52': 'R3', '53': 'G3', '02': 'A',
            '03': 'D2', '26': 'T', '01': 'XX',
            '06': 'G2', '07': 'U', '04': 'Z', '05': 'C',
            '46': 'Y3', '47': 'Z3', '08': 'X',
            '09': 'A2', '28': 'R', '29': 'F2', '41': 'U2',
            '14': 'I2', '59': 'T3', '78': 'J4',
            '51': 'P2', '24': 'Q', '56': 'J2', '25': 'O',
            '39': 'E3', '65': 'S3', '76': 'K3',
            '75': 'I4', '38': 'F3', '73': 'G4', '72': 'P3',
            '71': 'Q3', '70': 'D4', '20': 'D',
            '74': 'H4', '21': 'F', '11': 'Y', '10': 'C2',
            '13': 'E', '12': 'G', '15': 'W',
            '22': 'L', '17': 'M', '16': 'K',
            '19': 'H', '18': 'H2',
            '31': 'N', '23': 'J', '37': 'D3',
            '36': 'W2', '35': 'C3', '34': 'B',
            '33': 'P', '55': 'A4',
            '63': 'V3', '32': 'E2', '44': 'Z2',
            '50': 'T2'
        }
        type_dict = {}
        seq_lengths = set()

        reps_dict = self.fasta_dict(spa_repeats)
        for i in reps_dict:
            seq = reps_dict[i]
            num = i[1:]
            seq_dict[seq.upper()] = num
            seq_lengths.add(len(seq))
        with open(spa_types) as f:
            for line in f:
                st, pattern = line.rstrip().split(',')
                type_dict[pattern] = st
        return seq_dict, let_dict, type_dict, seq_lengths

    def find_spa_type(
        self,
        infile,
        seq_dict,
        let_dict,
        type_dict,
        seq_lengths
    ):
        q_dict = self.fasta_dict(infile)
        seq_list = []

        # progress through a set of primes looking for an enriched sequence
        for i in q_dict:
            enriched_seqs = self.enrich_seq(
                q_dict[i].upper(),
                'TAAAGACGATCCTTCGGTGAG',
                'CAGCAGTAGTGCCGTTTGCTT'
            )
            seq_list += enriched_seqs

        if len(seq_list) == 0:
            for i in q_dict:
                enriched_seqs = self.enrich_seq(
                    q_dict[i].upper(),
                    'AGACGATCCTTCGGTGAGC',
                    'GCTTTTGCAATGTCATTTACTG'
                )
                seq_list += enriched_seqs
        if len(seq_list) == 0:
            for i in q_dict:
                enriched_seqs = self.enrich_seq(
                    q_dict[i].upper(),
                    'ATAGCGTGATTTTGCGGTT',
                    'CTAAATATAAATAATGTTGTCACTTGGA'
                )
                seq_list += enriched_seqs
        if len(seq_list) == 0:
            for i in q_dict:
                enriched_seqs = self.enrich_seq(
                    q_dict[i].upper(),
                    'CAACGCAATGGTTTCATCCA',
                    'GCTTTTGCAATGTCATTTACTG'
                )
                seq_list += enriched_seqs
        if len(seq_list) == 0:
            return ['no enriched sequence.']
        if len(seq_list) > 1:
            sys.stderr.write(
                'More than one enriched sequence in ' + infile + '\n'
            )
        rep_list = []
        for i in seq_list:
            index = 0
            adjacent = False
            rep_order = []
            while index <= len(i):
                gotit = False
                for j in seq_lengths:
                    if i[index:index+j] in seq_dict:
                        if adjacent or rep_order == []:
                            rep_order.append(seq_dict[i[index:index + j]])
                        else:
                            rep_order.append('xx')
                            rep_order.append(seq_dict[i[index:index + j]])
                        index += j
                        gotit = True
                        adjacent = True
                        break
                if not gotit:
                    index += 1
                    adjacent = False
            rep_list.append(rep_order)
        out_list = []
        for i in rep_list:
            let_out = ''
            for j in i:
                if j in let_dict:
                    let_out += let_dict[j] + '-'
                else:
                    let_out += 'xx-'
            let_out = let_out[:-1]
            if '-'.join(i) in type_dict:
                type_out = type_dict['-'.join(i)]
            else:
                type_out = '-'.join(i)
            out_list.append(let_out)
            out_list.append(type_out)

        return out_list