"""Johto_crystal.py: Pokemon Crystal.

Inherits Johto_gs. Structurally identical to Gold/Silver.
"""
from Johto_gs import Johto_gs


class Johto_crystal(Johto_gs):
    """Pokemon Crystal. Inherits Gold/Silver baseline."""

    GAME_CODES = ('PM_', 'PMC')
    TITLES = ('POKÉMON CRYSTAL', 'POKÉMON CRYSTAL')
    YEAR = 2001
    SCRIPT_LOADWILDMON, SCRIPT_STARTBATTLE = 0x5D, 0x5F  # Crystal's command list is shifted +1 here
