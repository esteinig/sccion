import shlex
import subprocess
import sys
import pandas
from pathlib import Path


def run_cmd(cmd, callback=None, watch=False):

    """Runs the given command and gathers the output.

    If a callback is provided, then the output is sent to it, otherwise it
    is just returned.

    Optionally, the output of the command can be "watched" and whenever new
    output is detected, it will be sent to the given `callback`.

    Returns:
        A string containing the output of the command, or None if a `callback`
        was given.
    Raises:
        RuntimeError: When `watch` is True, but no callback is given.

    """
    if watch and not callback:
        raise RuntimeError(
            'You must provide a callback when watching a process.'
        )

    output = None
    try:
        proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)

        if watch:
            while proc.poll() is None:
                line = proc.stdout.readline()
                if line != "":
                    callback(line)

            # Sometimes the process exits before we have all of the output, so
            # we need to gather the remainder of the output.
            remainder = proc.communicate()[0]
            if remainder:
                callback(remainder)
        else:
            output = proc.communicate()[0]
    except:
        err = str(sys.exc_info()[1]) + "\n"
        output = err

    if callback and output is not None:
        return callback(output)

    return output


# Assembly statistics

def run_assembly_stats(fasta):

    """ Run sanger-pathogen/assembly-stats """

    def process(output):

        output = output.decode('utf-8')

        contigs = {
            'number': _get_contig_number(output),
            'longest': _get_longest_contig(output),
            'average': _get_longest_contig(output),
            'n50': _get_contig_n50(output)
        }

        return contigs

    return run_cmd(f'assembly-stats {fasta}', callback=process)


def _get_contig_number(output):
    return output.split('')


def _get_longest_contig(output):
    return output.split('')


def _get_contig_n50(output):
    return output.split('')


def run_mash_dist(
        fasta: Path,
        db: Path = Path(__file__).parent / 'db' / 'staphylococci.msh',
        threads: int = 8
):

    cmd = f"mash dist -p {threads } {db} {fasta}"

    def split_mash_str(output: bytes):

        df = pandas.DataFrame([
            row.split('\t') for row in output.decode(
                'utf-8'
            ).strip().split('\n')
        ], columns=[
            "reference-ID", "query-ID", "distance",
            "p-value", "shared-hashes"
        ]).sort_values(by='distance', ascending=True).reset_index()

        name = Path(
            df.at[0, "reference-ID"].split('-')[-1]
        ).stem

        return name

    return run_cmd(
        cmd, callback=split_mash_str
    )


def run_mlst(fasta):

    """ Run tseemann/mlst """

    cmd = f"mlst {fasta} -q"

    def split_mlst_str(output: bytes):

        out = output.decode('utf-8').strip().split('\t')

        file, species, mlst, alleles = out[0], out[1], out[2], out[3:]

        return file, species, mlst, alleles

    return run_cmd(
        cmd, callback=split_mlst_str
    )


def run_abricate(
    fasta: Path,
    db: str = 'resfinder',
    threads: int = 2,
    min_identity: float = 0.9,
    min_coverage: float = 0.7,
):
    """ Run tseemann/abricate """

    cmd = f"abricate --db {db} --quiet --threads {threads}" \
          f" --minid {min_identity} --mincov {min_coverage} {fasta}"

    def get_abricate_table(output: bytes):

        out = [
            o for o in output.decode('utf-8').split('\n') if o
        ]

        df = pandas.DataFrame(data=[
            row.split('\t') for row in out[1:]
        ], columns=[
            'file',
            'sequence',
            'start',
            'end',
            'strand',
            'gene',
            'coverage',
            'coverage_map',
            'gaps',
            'coverage',
            'identity',
            'database',
            'accession',
            'product',
            'resistance',
        ])

        return df

    return run_cmd(
        cmd, callback=get_abricate_table
    )


