"""Johto_gs.py: Gold/Silver — Gen II structural baseline.

Inherits Kanto_yellow. Gen II added: Special split (5->6 stats),
Dark/Steel types, breeding, held items, time-of-day, 251 species.
Same charmap as Gen I (EN), same EOS.
"""
from Kanto_yellow import Kanto_yellow
import struct


class Johto_gs(Kanto_yellow):
    """Gold/Silver. Gen II baseline."""

    GAME_CODES = ('PMG2', 'PMS')
    TITLES = ('POKÉMON GOLD', 'POKÉMON SILVER')
    YEAR = 2000

    PLATFORM = 'Game Boy Color'
    GEN = 2
    CONTAINER = 'gbc'

    STAT_COUNT = 6
    LEARNSET_COUNT = 251

    def _discover_gen2_tables(self):
        """Gen I finder + the evo/learnset pointer table (Gen I's locator doesn't match Gen II)."""
        off = super()._discover_gen1_tables() or {}
        d = bytes(self.rom or b'')
        P = d.find(bytes([1, 16, 2, 0, 1, 0x21, 4, 0x2D, 7, 0x49]))  # Bulbasaur: Lv16->Ivysaur, then Tackle/Growl/Leech Seed
        if P > 0:
            b = P // 0x4000
            ptr = (P % 0x4000 + 0x4000).to_bytes(2, 'little')
            t = d.find(ptr, b * 0x4000, (b + 1) * 0x4000)
            if t >= 0:
                off['evo_learnset_table'] = t
                off['evo_learnset_data_base'] = b * 0x4000 - 0x4000  # banked ptr -> file offset
        self._gen1_offsets = off
        return off

    DISCOVER_TABLES = _discover_gen2_tables
    STAT_ORDER = ('HP', 'Atk', 'Def', 'Spe', 'SpA', 'SpD')

    CHARMAP_EN = dict(Kanto_yellow.CHARMAP_EN)

    SPECIES_COUNT = 251

    FLIPNOTE_PAIRS = {
        'Pokémon Gold & Silver': ['PMG2', 'PMS'],
        'Pokémon Crystal': ['PM_'],
    }

    @staticmethod
    def _scan_gen2_trainer_classes_en(rom_data: bytes, charmap: dict, eos: int, text_tables: dict):
        """Scan Gen II EN trainer class names. Anchors at LEADER (class 0 = first gym leader class).
        Class ordering matches group pointer table (pret/pokegold): LEADER×8, RIVAL, PROF, ELITE FOUR×4,
        CHAMPION, LEADER×3(Kanto), then random trainers.
        Populates text_tables['trainer_classes'].
        """
        if 'trainer_classes' in text_tables:
            return

        reverse = {v: k for k, v in charmap.items() if isinstance(v, str) and len(v) == 1}
        # Anchor: "LEADER" appears first in both the text table and the group pointer table
        # Find the occurrence of LEADER followed 8 entries later by RIVAL
        try:
            leader_enc = bytes([reverse[c] for c in 'LEADER']) + bytes([eos])
            rival_enc  = bytes([reverse[c] for c in 'RIVAL'])  + bytes([eos])
        except KeyError:
            return

        # Find LEADER occurrence that has RIVAL exactly 8 names later
        table_start = -1
        search_off = 0
        while True:
            pos = rom_data.find(leader_enc, search_off)
            if pos < 0:
                break
            # Scan forward 8 names from here to see if the 9th is RIVAL
            j = pos + len(leader_enc)
            for _ in range(7):   # skip 7 more names (total 8 LEADER entries)
                while j < len(rom_data) and rom_data[j] != eos:
                    j += 1
                j += 1  # skip eos
            if rom_data[j: j + len(rival_enc)] == rival_enc:
                table_start = pos
                break
            search_off = pos + 1

        if table_start < 0:
            # Fallback: anchor at RIVAL like before
            table_start = rom_data.find(rival_enc)
        if table_start < 0:
            return

        names = []
        i = table_start
        while i < len(rom_data) and len(names) < 80:
            chars = []
            while i < len(rom_data) and rom_data[i] != eos:
                b = rom_data[i]
                ch = charmap.get(b)
                if ch is not None:
                    chars.append(ch)
                elif b >= 0x80:
                    break
                i += 1
            name = ''.join(chars).strip()
            if i < len(rom_data) and rom_data[i] == eos:
                names.append(name)
                i += 1
            else:
                break

        if len(names) > 4:
            text_tables['trainer_classes'] = names

    def decode_encounters(self, map_group: int, map_number: int, current_rom: dict, text_tables: dict) -> str:
        """Decode Gen II wild encounters for a map identified by (group, map_number).
        Format: [group][map][morn_rate][day_rate][nite_rate][7×lv,sp morning][day][night] = 47B
        Species = Pokédex numbers (same as Gen 2 trainer data)."""
        if not current_rom:
            return ''
        g1off    = current_rom.get('gen1_offsets', {})
        table        = g1off.get('enc2_table_base', 0)
        kanto_table  = g1off.get('enc2_kanto_table_base', 0)
        if not table:
            return ''
        rom_data = bytes(current_rom.get('data') or b'')
        sp_list  = text_tables.get('species', [])

        def sp_name(dex):
            if 0 < dex < len(sp_list) and sp_list[dex]:
                return sp_list[dex]
            return f'sp#{dex}'

        # Scan both tables for matching entry (Johto table + Kanto table)
        for table_start in [t for t in [table, kanto_table] if t]:
            off = table_start
            while off + 47 <= len(rom_data):
                mg = rom_data[off]
                mn = rom_data[off + 1]
                if mg == 0xFF:
                    break
                if mg == map_group and mn == map_number:
                    morn_rate = rom_data[off + 2]
                    day_rate  = rom_data[off + 3]
                    nite_rate = rom_data[off + 4]
                    lines = [f'Map {map_group}/{map_number}']
                    for period_idx, (label, rate) in enumerate(
                            [('Morning', morn_rate), ('Day', day_rate), ('Night', nite_rate)]):
                        if rate == 0:
                            continue
                        lines.append(f'Grass ({label}):')
                        seen = {}
                        for slot in range(7):
                            base = off + 5 + period_idx * 14 + slot * 2
                            lv = rom_data[base]
                            sp = rom_data[base + 1]
                            name = sp_name(sp)
                            seen.setdefault(name, []).append(lv)
                        for name, lvs in seen.items():
                            lv_str = f'Lv. {min(lvs)}-{max(lvs)}' if min(lvs) != max(lvs) else f'Lv. {min(lvs)}'
                            lines.append(f'  {name:<20}{lv_str}')
                    return '\n'.join(lines)
                off += 47
        return ''

    SCRIPT_LOADWILDMON, SCRIPT_STARTBATTLE, SCRIPT_GIVEPOKE = 0x5C, 0x5E, 0x2D

    def map_name(self, group, num):
        """Landmark name for map (group, num), 1-based like the wild tables. Map groups found by shape: a u16 pointer list
        into runs of 9B headers (bank, tileset, env 1-7, attr ptr, landmark, ...); attrs -> height/width, script bank+ptr, events ptr.
        Landmark list = run of (x, y, name ptr) entries whose length == max landmark + 1. Also caches each map's script region."""
        import struct
        if getattr(self, '_map_names', None) is None:
            self._map_names, self._map_regions = {}, {}
            r = bytes(self._current_rom_ref().get('data') or b''); L = len(r); NB = L // 0x4000
            A = lambda b, p: b * 0x4000 + p - 0x4000 if 0x4000 <= p < 0x8000 and 0 < b < NB else None
            def head(o):
                if o is None or o + 9 > L or not 1 <= r[o + 2] <= 7: return None
                a = A(r[o], struct.unpack_from('<H', r, o + 3)[0])
                if a is None or a + 12 > L or not (0 < r[a + 1] <= 64 and 0 < r[a + 2] <= 64): return None
                s, e = A(r[a + 6], struct.unpack_from('<H', r, a + 7)[0]), A(r[a + 6], struct.unpack_from('<H', r, a + 9)[0])
                return (s, e) if s is not None and e is not None and s <= e else None
            T = None
            for o in range(0x4000, L - 40):
                ps = struct.unpack_from('<20H', r, o)
                if all(0x4000 <= p < 0x8000 for p in ps) and all(ps[i + 1] > ps[i] and (ps[i + 1] - ps[i]) % 9 == 0 for i in range(19)) and all(head(A(o // 0x4000, p)) for p in ps):
                    T = o; break
            if T is None: return None
            B = T // 0x4000; gs = []
            while head(A(B, (p := struct.unpack_from('<H', r, T + 2 * len(gs))[0]))) and (not gs or p > gs[-1]): gs.append(p)
            lm = {}
            for i, p in enumerate(gs):
                o = A(B, p); n = (gs[i + 1] - p) // 9 if i + 1 < len(gs) else None; j = 0
                while (n is None or j < n) and (reg := head(o + 9 * j)):
                    lm[(i + 1, j + 1)] = r[o + 9 * j + 5]; self._map_regions[(i + 1, j + 1)] = reg; j += 1
            span = max(lm.values()) + 1
            def ok(o):
                a = A(o // 0x4000, struct.unpack_from('<H', r, o + 2)[0]); e = r.find(bytes([self.EOS]), a, a + 20) if a is not None else -1
                return a is not None and e > a and 0 not in r[a:e]
            o = next((o for o in range(4, L - 4 * span) if not ok(o - 4) and all(ok(o + 4 * i) for i in range(span))), None)
            if o is None: return None
            def nm(i):
                a = A(o // 0x4000, struct.unpack_from('<H', r, o + 4 * i + 2)[0])
                return ''.join(' ' if c == 0x1F else self.CHARMAP_EN.get(c, '') for c in r[a:r.find(bytes([self.EOS]), a)])
            self._map_names = {k: nm(v) for k, v in lm.items()}
        return self._map_names.get((group, num))

    def iter_encounters(self):
        """(id, dex, form, lo, hi) per map/time/species. Johto + Kanto grass tables, 47B rows, FF-terminated."""
        ref = self._current_rom_ref(); g, rom = ref.get('gen1_offsets', {}), bytes(ref.get('data') or b'')
        out = []
        tables = [x for x in (g.get('enc2_table_base', 0), g.get('enc2_kanto_table_base', 0)) if x]  # swarm table appended below
        for t in tables:
            off = t
            tag = '' if t in (g.get('enc2_table_base', 0), g.get('enc2_kanto_table_base', 0)) else ' (swarm)'
            while off + 47 <= len(rom) and rom[off] != 0xFF:
                for pi, tod in enumerate(('morning', 'day', 'night')):
                    if not rom[off + 2 + pi]: continue
                    seen = {}
                    for s in range(7):
                        b = off + 5 + pi * 14 + s * 2; seen.setdefault(rom[b + 1], []).append(rom[b])
                    out += [(f"{self.map_name(rom[off], rom[off + 1]) or 'Map'} [{rom[off]}/{rom[off + 1]}] {tod}", sp, 0, min(l), max(l), {'location': self.map_name(rom[off], rom[off + 1]) or f'Map [{rom[off]}/{rom[off + 1]}]', 'method': 'grass', 'period': tod, 'variant': 'swarm' if tag else ''}) for sp, l in seen.items()]
                off += 47
            # Each grass table's FF is followed by its water table: 9B rows (group, map, rate, 3 x lv/sp)
            off += 1
            while off + 9 <= len(rom) and rom[off] != 0xFF and self.map_name(rom[off], rom[off + 1]):
                if rom[off + 2]:
                    seen = {}
                    for s in range(3): seen.setdefault(rom[off + 4 + s * 2], []).append(rom[off + 3 + s * 2])
                    out += [(f"{self.map_name(rom[off], rom[off + 1])} [{rom[off]}/{rom[off + 1]}] surf{tag}", sp, 0, min(l), max(l), {'location': self.map_name(rom[off], rom[off + 1]), 'method': 'surf', 'variant': 'swarm' if tag else ''}) for sp, l in seen.items()]
                off += 9
            # Kanto water is followed by the swarm grass + water tables
            if t == g.get('enc2_kanto_table_base', 0) and len(tables) == 2 and rom[off:off + 1] == b'\xff': tables.append(off + 1)
        # Statics/gifts: each map's scripts sit between its script header and its events (same bank).
        # loadwildmon (sp, lv) with startbattle a few bytes on; givepoke (sp, lv, item, trainer flag 0/1).
        self.map_name(1, 1)
        for (g, n), (s, e) in sorted((getattr(self, '_map_regions', None) or {}).items()):
            b = s - s % 0x4000 - 0x4000
            jmp = lambda o: rom[o] in (0x00, 0x02, 0x03, 0x05, 0x08, 0x09) and s <= b + (rom[o + 1] | rom[o + 2] << 8) < e  # byte is the pointer operand of a call/jump into this same script
            LW, SB = self.SCRIPT_LOADWILDMON, self.SCRIPT_STARTBATTLE
            for x in range(s, e - 5):
                if jmp(x - 1) or jmp(x - 2): continue
                # startbattle right after, or after one 3-byte command that isn't loadtrainer (LW+1), e.g. writecode BATTLETYPE for the red Gyarados
                if rom[x] == LW and 0 < rom[x + 1] < 252 and 0 < rom[x + 2] <= 100 and (rom[x + 3] == SB or rom[x + 6] == SB and rom[x + 3] != LW + 1): kind = 'static'
                elif rom[x] == self.SCRIPT_GIVEPOKE and 0 < rom[x + 1] < 252 and 0 < rom[x + 2] <= 100 and rom[x + 4] in (0, 1): kind = 'gift'
                else: continue
                out.append((f"{self.map_name(g, n) or 'Map'} [{g}/{n}] {kind}", rom[x + 1], 0, rom[x + 2], rom[x + 2], {'location': self.map_name(g, n) or f'Map [{g}/{n}]', 'method': kind}))
        return out

    def bootstrap_text(self, rom_data, region='US'):
        """Gen II text bootstrap — dex-order species, Gen II trainer classes."""
        charmap = self.CHARMAP_JP if region == 'JP' else self.CHARMAP_EN
        eos = self.EOS
        self.text_tables = {}

        candidates = self.scan_rom_text(rom_data, charmap, eos)
        for idx, table in enumerate(candidates):
            self.text_tables[idx] = table

        self._scan_gen1_species(rom_data, charmap, eos, self.text_tables,
                                anchor_pair=('BULBASAUR', 'IVYSAUR'),
                                max_entries=252, skip_reorder=True)
        self._scan_gen2_trainer_classes_en(rom_data, charmap, eos, self.text_tables)
        self._scan_gen1_items(rom_data, charmap, eos, self.text_tables)
        self._scan_gen12_moves_en(rom_data, charmap, eos, self.text_tables, 251)

        self._auto_detect_tables()
        self._map_text_tables()

    SCAN_TRAINER_CLASSES_EN = _scan_gen2_trainer_classes_en

