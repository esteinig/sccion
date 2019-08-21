import click
import tqdm
from pathlib import Path
from sccion.sccion import SCCion


@click.command()
@click.option(
    "--assemblies", "-a",
    help="Assembly file (.fasta) or glob to assembly files (*.fasta)"
)
@click.option(
    "--resistance", "-r", is_flag=True,
    help="Enable output of abbreviated resistance genes and mutations",
)
@click.option(
    "--virulence", "-v", is_flag=True,
    help="Enable output of abbreviated virulence factors",
)
@click.option(
    "--mge", "-m", is_flag=True,
    help="Enable advanced detection and typing of mobile elements",
)
@click.option(
    "--min_coverage", "-mc", default=0.7, type=float,
    help="Minimum coverage for hits against databases for assembly typing",
)
@click.option(
    "--min_identity", "-mi", default=0.9, type=float,
    help="Minimum identity for hits against databases for assembly typing"
)
def type(assemblies, min_coverage, min_identity, resistance, virulence, mge):

    if Path(assemblies).is_file():

        sccion = SCCion(
            fasta=Path(assemblies)
        )

        sccion.type_assembly(
            min_coverage=min_coverage,
            min_identity=min_identity
        )

    elif '*' in assemblies:
        fasta = list(
            Path().glob(assemblies)
        )

        for file in tqdm.tqdm(fasta):
            sccion = SCCion(fasta=file)
            sccion.type_assembly(
                min_coverage=min_coverage,
                min_identity=min_identity
            )

