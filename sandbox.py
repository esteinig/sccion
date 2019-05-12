from pathlib import Path
from sccion.sccion import SCCion

sccion1 = SCCion(
    fasta=Path() / 'tests' / 'data' / 'm03.fasta'
)

sccion1.type_assembly()

sccion2 = SCCion(
    fasta=Path() / 'tests' / 'data' / 'dar4145.fasta'
)

sccion2.type_assembly()


