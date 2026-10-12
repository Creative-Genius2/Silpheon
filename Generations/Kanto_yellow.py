"""Kanto_yellow.py: Pokemon Yellow (EN + JP).

Inherits Kanto_rbg. Structurally identical to Red/Blue/Green.
Separate file because game codes differ.
"""
from Kanto_rbg import Kanto_rbg


class Kanto_yellow(Kanto_rbg):
    """Pokemon Yellow (EN + JP). Inherits Red/Blue/Green baseline."""

    GAME_CODES = ('PMY', 'PMYJ')
    TITLES = ('POKÉMON YELLOW', 'POCKET MONSTERS YELLOW')
    YEAR = 1999
    ENC_ANCHOR_LEVELS = (2, 7)  # Yellow's Route 1 runs Lv 2-7 (Red/Blue: 2-5)
