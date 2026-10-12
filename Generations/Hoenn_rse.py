"""Hoenn_rse.py: Ruby/Sapphire/Emerald/FireRed/LeafGreen — Gen III baseline.

Inherits Johto_crystal. Gen III added: abilities, natures, GBA platform.
"""
from Johto_crystal import Johto_crystal
import struct


class Hoenn_rse(Johto_crystal):
    """Ruby/Sapphire/Emerald/FireRed/LeafGreen. Gen III baseline."""

    GAME_CODES = ('AXVE', 'AXPE', 'BPEE', 'BPRE', 'BPGE')
    TITLES = ('POKÉMON RUBY', 'POKÉMON SAPPHIRE', 'POKÉMON EMERALD', 'POKÉMON FIRERED', 'POKÉMON LEAFGREEN')
    YEAR = 2003

    PLATFORM = 'Game Boy Advance'
    GEN = 3
    CONTAINER = 'gba'

    EOS = 0xFF
    CHARMAP_JP = None
    SPECIES_COUNT = 386

    BATTLE_TYPES = ('Single', 'Double')


    # Gen III (GBA) character map — English FireRed/Ruby/Emerald
    # Empirically verified from FireRed (USA): A=0xBB, confirmed via BULBASAUR at 0x245EEB.
    # Bulbapedia listed A=0xC1 but that was wrong for this ROM version.
    # EOS=0xFF. 0x00 is null padding between fixed-width entries (NOT space).
    # Space within strings (e.g. "MASTER BALL") is 0x00 contextually — we skip leading 0x00s.
    CHARMAP_EN: dict = {}
    for _i, _c in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        CHARMAP_EN[0xBB + _i] = _c
    for _i, _c in enumerate('abcdefghijklmnopqrstuvwxyz'):
        CHARMAP_EN[0xD5 + _i] = _c
    for _i, _c in enumerate('0123456789'):
        CHARMAP_EN[0xA1 + _i] = _c
    CHARMAP_EN.update({
        0x00: ' ',   # space within strings; skip leading 0x00 (entry padding) in scanner
        0x1B: 'é',   # POKé BALL etc.
        0xAB: '!', 0xAC: '?', 0xAD: '.', 0xAE: '-', 0xB8: ',',
        0xB2: "'", 0xB5: '♀', 0xB6: '♂',
        0x53: '', 0x54: '',  # control-code prefixes in some class names (silently skipped)
    })


    @staticmethod
    def _scan_gen3_abilities(rom_data: bytes, charmap: dict, eos: int, text_tables: dict):
        """Scan Gen III ability names starting from STENCH.

        Ability names are all-uppercase and short (≤12 chars).
        Descriptions are mixed-case and longer — we stop when we hit those.
        Prepends a blank entry at index 0 (ability 0 = no ability).
        Populates an integer-keyed entry in text_tables.
        """
        if 'abilities' in text_tables:
            return  # already found by fingerprinting

        reverse = {v: k for k, v in charmap.items() if isinstance(v, str) and len(v) == 1}
        try:
            stench_bytes = bytes([reverse[c] for c in 'STENCH']) + bytes([eos])
        except KeyError:
            return

        idx = rom_data.find(stench_bytes)
        if idx < 0:
            return

        abilities = ['']  # index 0 = no ability (blank)
        i = idx
        while i < len(rom_data):
            while i < len(rom_data) and rom_data[i] == 0x00:
                i += 1
            j = i
            chars = []
            while j < len(rom_data) and rom_data[j] != eos and j < i + 15:
                ch = charmap.get(rom_data[j])
                if ch is None:
                    break
                chars.append(ch)
                j += 1
            name = ''.join(chars).rstrip()
            if rom_data[j] == eos and 2 <= len(name) <= 13:
                # Accept only if looks like an ability name (no lowercase, not a sentence)
                if name == name.upper():
                    abilities.append(name)
                    i = j + 1
                    continue
            break  # hit descriptions or end

        if len(abilities) > 5:
            next_key = max((k for k in text_tables if isinstance(k, int)), default=-1) + 1
            text_tables[next_key] = abilities

    @staticmethod
    def _scan_gen3_species(rom_data: bytes, charmap: dict, eos: int, text_tables: dict):
        """Scan Gen III species names starting from BULBASAUR.

        Species are fixed-width name slots. Find BULBASAUR, verify IVYSAUR follows
        at the right distance (to get slot size), then read forward.
        Prepends a dummy at index 0. Sets text_tables['species'] directly.
        """
        if 'species' in text_tables:
            return

        reverse = {v: k for k, v in charmap.items() if isinstance(v, str) and len(v) == 1}
        try:
            bulb = bytes([reverse[c] for c in 'BULBASAUR']) + bytes([eos])
            ivy  = bytes([reverse[c] for c in 'IVYSAUR'])
        except KeyError:
            return

        # Find BULBASAUR followed by IVYSAUR at the right slot distance
        search = 0
        while True:
            pos = rom_data.find(bulb, search)
            if pos < 0:
                return
            # Slot size = distance from BULBASAUR start to next non-padding byte
            nxt = pos + len(bulb)
            while nxt < len(rom_data) and rom_data[nxt] in (0x00, eos):
                nxt += 1
            slot = nxt - pos
            if 2 <= slot <= 20 and rom_data[nxt: nxt + len(ivy)] == ivy:
                break
            search = pos + 1

        # Read backwards one slot for dummy (index 0 = Missingno)
        start = max(0, pos - slot)
        names = []
        i = start
        while i < len(rom_data) and len(names) < 500:
            j, chars = i, []
            while j < i + slot and j < len(rom_data) and rom_data[j] != eos:
                ch = charmap.get(rom_data[j])
                if ch is None:
                    break
                chars.append(ch)
                j += 1
            name = ''.join(chars).rstrip()
            if len(names) > 10 and not name:
                break
            names.append(name)
            i += slot

        if len(names) > 10:
            text_tables['species'] = names

    @staticmethod
    def _scan_gen3_trainer_names(rom_data: bytes, charmap: dict, eos: int, text_tables: dict):
        """Scan Gen III ROM for trainer structs and extract names into text_tables['trainer_names'].

        Trainer struct (40 bytes): flags(1), class(1), music(1), sprite(1), name(12), ...
        party_count(u32 at +32), party_ptr(u32 at +36).
        Validates each candidate by checking flags 0-3, class 1-199, count 1-6, valid GBA ptr.
        """
        if 'trainer_names' in text_tables:
            return

        import struct as _struct
        names_by_offset = {}
        for i in range(0, len(rom_data) - 40, 4):
            if rom_data[i] > 3 or rom_data[i + 1] == 0 or rom_data[i + 1] >= 200:
                continue
            count = _struct.unpack_from('<I', rom_data, i + 32)[0]
            if not (1 <= count <= 6):
                continue
            ptr = _struct.unpack_from('<I', rom_data, i + 36)[0]
            if not (0x08000000 <= ptr <= 0x0AFFFFFF):
                continue
            j, chars = i + 4, []
            while j < i + 16 and rom_data[j] != eos:
                ch = charmap.get(rom_data[j])
                if ch is None:
                    break
                chars.append(ch)
                j += 1
            name = ''.join(chars).strip()
            if len(name) >= 2 and name == name.upper():
                names_by_offset[i] = name

        if len(names_by_offset) > 10:
            sorted_entries = sorted(names_by_offset.items())
            text_tables['trainer_names']   = [n for _, n in sorted_entries]
            text_tables['trainer_offsets'] = [off for off, _ in sorted_entries]

    @staticmethod
    def _scan_gen3_items(rom_data: bytes, charmap: dict, eos: int, text_tables: dict):
        """Scan Gen III item table (44-byte structs, name in first 14 bytes).

        Finds MASTER BALL to anchor the table, then reads fixed-stride entries.
        Populates text_tables['items'] directly.
        """
        reverse = {v: k for k, v in charmap.items() if isinstance(v, str) and len(v) == 1}
        try:
            mb_bytes = bytes([reverse[c] for c in 'MASTER BALL']) + bytes([eos])
        except KeyError:
            return

        idx = rom_data.find(mb_bytes)
        if idx < 0:
            return

        ITEM_STRUCT = 44
        NAME_LEN = 14
        items = []
        offset = idx
        while offset + ITEM_STRUCT <= len(rom_data):
            name_bytes = rom_data[offset:offset + NAME_LEN]
            name = ''
            for b in name_bytes:
                if b == eos:
                    break
                ch = charmap.get(b)
                if ch is None:
                    break
                name += ch
            name = name.strip()
            if not name:
                break
            items.append(name)
            offset += ITEM_STRUCT

        if items:
            # Add as integer key so auto_detect_tables can fingerprint it
            next_key = max((k for k in text_tables if isinstance(k, int)), default=-1) + 1
            text_tables[next_key] = items

    def decode_trainer(self, header: bytes, party_data: bytes, party_flags: int) -> dict:
        """Decode Gen III trainer header (40 bytes) and party data.

        party_flags: bit 0 = has custom moves, bit 1 = has held item
        """
        import struct
        if len(header) < 40:
            return {}

        flags = header[0]
        trainer_class = header[1]
        name_bytes = header[4:16]
        items = [struct.unpack_from('<H', header, 16 + i*2)[0] for i in range(4)]
        is_double = struct.unpack_from('<I', header, 24)[0]
        ai_flags = struct.unpack_from('<I', header, 28)[0]
        party_count = struct.unpack_from('<I', header, 32)[0]

        # Decode name using Gen III charmap
        name = ''.join(Hoenn_rse.CHARMAP_EN.get(b, '') for b in name_bytes).strip()

        # Party member size depends on flags
        has_moves = bool(flags & 1)
        has_item = bool(flags & 2)
        if has_moves and has_item:
            member_size = 18  # iv(2)+level(2)+species(2)+item(2)+moves(8)+pad(2)
        elif has_moves:
            member_size = 16  # iv(2)+level(2)+species(2)+moves(8)+pad(2)
        elif has_item:
            member_size = 8   # iv(2)+level(2)+species(2)+item(2)
        else:
            member_size = 8   # iv(2)+level(2)+species(2)+pad(2)

        party = []
        for i in range(min(party_count, 6)):
            off = i * member_size
            if off + member_size > len(party_data):
                break
            m = party_data[off:off+member_size]
            iv = struct.unpack_from('<H', m, 0)[0]
            level = struct.unpack_from('<H', m, 2)[0]
            species = struct.unpack_from('<H', m, 4)[0]
            member = {'species': species, 'level': level, 'iv': iv}
            pos = 6
            if has_item:
                member['item'] = struct.unpack_from('<H', m, pos)[0]
                pos += 2
            if has_moves:
                moves = [struct.unpack_from('<H', m, pos + j*2)[0] for j in range(4)]
                member['moves'] = [mv for mv in moves if mv > 0]
            party.append(member)

        return {
            'trainer_class': trainer_class,
            'name': name,
            'ai_flags': ai_flags,
            'is_double': bool(is_double),
            'battle_items': [it for it in items if it > 0],
            'party': party,
        }

    @staticmethod
    def _discover_gen3_tables(current_rom: dict):
        """Find personal/move/trainer table offsets in a GBA ROM by searching for known anchors.

        Same philosophy as _discover_tm_table() — the data finds itself.
        Results stored in current_rom['gen3_offsets'].
        """
        if not current_rom or current_rom['type'] != 'gba':
            return None
        rom_data = bytes(current_rom.get('data') or b'')
        if not rom_data:
            return None

        offsets = {}

        # ── Personal data: find via Bulbasaur's unique stat+type+catch signature ──
        # HP=45, Atk=49, Def=49, Spe=45, SpA=65, SpD=65, Type1=12(Grass), Type2=3(Poison), Catch=45
        bulb_sig = bytes([45, 49, 49, 45, 65, 65, 12, 3, 45])
        idx = rom_data.find(bulb_sig)
        if idx >= 0:
            # Bulbasaur is species index 1 → base = found - 1 * 28
            offsets['personal_base'] = idx - 28
            offsets['personal_size'] = 28

        # ── Move data: find via Pound's signature with blank entry before it ──
        # effect=0, power=40, type=0(Normal), acc=100, pp=35
        pound_sig = bytes([0, 40, 0, 100, 35])
        idx = rom_data.find(pound_sig)
        while idx >= 0:
            if all(b == 0 for b in rom_data[idx - 12: idx]):
                offsets['move_base'] = idx - 12  # entry 0 = blank, entry 1 = Pound
                offsets['move_size'] = 12
                break
            idx = rom_data.find(pound_sig, idx + 1)

        # ── Learnset pointer table: find via species 1 (Bulbasaur) lv1 Tackle ──
        # Table is an array of GBA pointers, one per species. Each points to u16 pairs
        # (level << 9) | move_id, terminated by 0x0000.
        tackle_lv1 = struct.pack('<H', (1 << 9) | 33)  # 0x0221
        for i in range(0, min(len(rom_data) - 8, 0x800000), 4):
            ptr = struct.unpack_from('<I', rom_data, i)[0]
            if not (0x08000000 <= ptr <= 0x0A000000):
                continue
            off = ptr - 0x08000000
            if off + 2 <= len(rom_data) and rom_data[off:off+2] == tackle_lv1:
                ptr2 = struct.unpack_from('<I', rom_data, i + 4)[0]
                if 0x08000000 <= ptr2 <= 0x0A000000:
                    off2 = ptr2 - 0x08000000
                    if off2 + 2 <= len(rom_data) and rom_data[off2:off2+2] == tackle_lv1:
                        offsets['learnset_ptr_table'] = i  # i = entry 0 (NONE shares Bulbasaur's list), i+4 = Bulbasaur
                        break

        # ── Evolution table: find via Bulbasaur (sp1) level 16 → Ivysaur (sp2) ──
        # Struct: 5 slots × {u16 method, u16 param, u16 target, u16 pad} = 40B per species
        # Method 4 = EVO_LEVEL. Verify Ivysaur at +40 also has its evo (level 32 → Venusaur).
        bulb_evo = struct.pack('<HHHH', 4, 16, 2, 0)
        idx = rom_data.find(bulb_evo)
        while idx >= 0:
            if (all(b == 0 for b in rom_data[idx+8:idx+40]) and
                    rom_data[idx+40:idx+48] == struct.pack('<HHHH', 4, 32, 3, 0)):
                offsets['evo_base'] = idx - 40  # species 0 (dummy) precedes Bulbasaur
                break
            idx = rom_data.find(bulb_evo, idx + 1)

        # ── Wild encounter table: WildPokemonHeader[] terminated by {0xFF, 0xFF, 0, 0, NULL×4}
        # Each entry: mapGroup(u8) mapNum(u8) pad(2) landPtr(u32) waterPtr(u32) rockPtr(u32) fishPtr(u32)
        # Sentinel has 0xFF at bytes 0-1 and all remaining bytes 0.
        sentinel_20 = bytes([0xFF, 0xFF, 0x00, 0x00]) + bytes(16)
        si = 0
        while si < len(rom_data) - 20:
            si = rom_data.find(sentinel_20, si)
            if si < 0: break
            if si >= 20:
                prev = rom_data[si-20:si]
                mg, mn = prev[0], prev[1]
                if mg < 50 and mn < 200:
                    for poff in (4, 8, 12, 16):
                        ptr = struct.unpack_from('<I', prev, poff)[0]
                        if 0x08000000 <= ptr <= 0x0AFFFFFF:
                            # Walk backward to find table start
                            tbl_start = si
                            while tbl_start >= 20:
                                e = rom_data[tbl_start-20:tbl_start]
                                emg, emn = e[0], e[1]
                                if emg > 50 or emn > 200: break
                                if not any(0x08000000 <= struct.unpack_from('<I',e,o)[0] <= 0x0AFFFFFF
                                           for o in (4,8,12,16)): break
                                tbl_start -= 20
                            offsets['enc_table_offset'] = tbl_start
                            break
            if 'enc_table_offset' in offsets: break
            si += 1

        # ── Item table: find via MASTER BALL name (same anchor as _scan_gen3_items) ──
        # Struct: 44B. name(14B) | index(u16) | price(u16) | holdEffect(u8) | holdParam(u8)
        # | descPtr(u32) | importance(u8) | pad | pocket(u8) | type(u8) | ...
        # MASTER BALL = item 1, so table_base = anchor - 44 (item 0 is blank entry).
        reverse = {v: k for k, v in Hoenn_rse.CHARMAP_EN.items() if isinstance(v, str) and len(v) == 1}
        try:
            mb_bytes = bytes([reverse[c] for c in 'MASTER BALL']) + bytes([Hoenn_rse.EOS])
            mb_idx = rom_data.find(mb_bytes)
            if mb_idx >= 44:
                offsets['item_base'] = mb_idx - 44  # item 0 = blank entry before Master Ball
        except (KeyError, TypeError):
            pass

        # ── Trainer data: no global base needed — search by name at query time ──
        offsets['trainer_size'] = 40

        if offsets:
            current_rom['gen3_offsets'] = offsets

        return offsets if offsets else None

    FLIPNOTE_PAIRS = {
        # Gen III (GBA)
        'Pokémon FireRed & LeafGreen': ['BPRE', 'BPGE'],
        'Pokémon Ruby & Sapphire': ['AXVE', 'AXPE'],
        'Pokémon Emerald': ['BPEE'],
    }

    TABLE_FINGERPRINTS = (
        ('moves',      ((0, "Pound"), (4, "Mega Punch"))),
        ('items',      ((0, "Master Ball"), (3, "Poké Ball"), (12, "Potion"))),
        ('type_names', ((0, "NORMAL"), (1, "FIGHT"), (2, "FLYING"))),  # Gen III abbreviated
    )


    LEARNSET_COUNT = 411  # internal species slots (Treecko=277), not dex order

    def learnset_moves(self, data):
        """Raw learnset for reverse lookup: [(level, move_id)]. Packed u16 (level<<9)|move."""
        out = []
        for i in range(0, len(data) - 1, 2):
            raw = struct.unpack_from('<H', data, i)[0]
            if raw == 0xFFFF or raw == 0: break
            out.append(((raw >> 9) & 0x7F, raw & 0x1FF))
        return out

    def map_name(self, group, num):
        """Same chain the game walks for the location popup: map-groups ptr list -> group's header ptr list -> header byte 0x14
        (region-map section) -> name ptr list. Both lists found by shape; the name list's length must equal the section range
        the headers use. Emerald/Ruby: 8B entries (x, y, w, h, name ptr), FRLG: bare ptrs. Cached."""
        import struct
        rom = bytes(self.rom or b''); L = len(rom); B = 0x08000000
        u = lambda a: struct.unpack_from('<I', rom, a)[0]
        V = lambda q: B <= q < B + L - 32
        def head(q):
            if not V(q): return None
            a = q - B; lay, ev, sc, cn = struct.unpack_from('<4I', rom, a)
            if not (V(lay) and V(ev) and V(sc) and (cn == 0 or V(cn))): return None
            w, h = struct.unpack_from('<II', rom, lay - B); return a if 0 < w <= 0x200 and 0 < h <= 0x200 else None
        if getattr(self, '_map_names', None) is None:
            self._map_names = {}
            self._map_headers = {}
            grp = lambda q: V(q) and head(u(q - B)) is not None and head(u(q - B + 4)) is not None
            g = next((o for o in range(0, L - 12, 4) if grp(u(o)) and grp(u(o + 4)) and grp(u(o + 8))), None)
            if g is None: return None
            hdrs = {}; i = 0
            while V(u(g + 4 * i)) and head(u(u(g + 4 * i) - B)) is not None:
                A = u(g + 4 * i) - B; j = 0
                while (h := head(u(A + 4 * j))) is not None: hdrs[(i, j)] = rom[h + 0x14]; self._map_headers[(i, j)] = h; j += 1
                i += 1
            lo, span = min(hdrs.values()), max(hdrs.values()) - min(hdrs.values()) + 1
            def s_ok(q):
                if not V(q): return False
                a = q - B; k = 0
                while rom[a + k] != self.EOS:
                    if k > 30: return False
                    k += 1
                return True
            names = None
            for st, po in ((8, 4), (4, 0)):
                o = 0
                while names is None and o < L - st * span:
                    if not V(u(o + po)): o += 4; continue
                    n = 0
                    while n <= span and s_ok(u(o + po + st * n)): n += 1
                    if n == span: names = [u(o + po + st * k) - B for k in range(span)]
                    o += st * n if n else 4
                if names: break
            if not names: return None
            def dec(a):
                s = ''
                while rom[a] != self.EOS: s += '' if rom[a] == 0xFC else ' ' if rom[a] in (0x00, 0xFE) else self.CHARMAP_EN.get(rom[a], '?'); a += 2 if rom[a] == 0xFC else 1
                return ' '.join(s.split())
            self._map_names = {k: dec(names[v - lo]) for k, v in hdrs.items() if 0 <= v - lo < span}
        return self._map_names.get((group, num))

    def iter_encounters(self):
        """(id, species, form, lo, hi). Wild header list found by shape: 20B rows (group, map, pad, 4 ptrs: land/water/rock/fish),
        each ptr -> (rate u8, pad, mons ptr) -> n x (min, max, species u16). FF FF terminates. Located once, cached."""
        import struct
        rom = bytes(self.rom or b''); L = len(rom)
        def info(p, n):
            if not p: return True
            a = p - 0x08000000
            if not (0 <= a and a + 8 <= L and 0 < rom[a] <= 100): return False
            m = struct.unpack_from('<I', rom, a + 4)[0] - 0x08000000
            return 0 <= m <= L - 4 * n and all(rom[m + 4 * i] <= rom[m + 4 * i + 1] <= 100 and 0 < struct.unpack_from('<H', rom, m + 4 * i + 2)[0] < 440 for i in range(n))
        def hdr(o):
            ps = struct.unpack_from('<4I', rom, o + 4)
            return any(ps) and all(p == 0 or 0x08000000 <= p < 0x08000000 + L for p in ps) and all(info(p, n) for p, n in zip(ps, (12, 5, 5, 10)))
        if getattr(self, '_wild_table', None) is None:
            self._wild_table = 0
            for o in range(0, L - 60, 4):
                if hdr(o) and hdr(o + 20) and hdr(o + 40):
                    while o >= 20 and hdr(o - 20): o -= 20
                    self._wild_table = o; break
        o, out = self._wild_table, []
        if not o: return None
        while o + 20 <= L and not (rom[o] == 0xFF and rom[o + 1] == 0xFF):
            for p, n, area in zip(struct.unpack_from('<4I', rom, o + 4), (12, 5, 5, 10), ('grass', 'water', 'rock smash', 'fishing')):
                if not p: continue
                m = struct.unpack_from('<I', rom, p - 0x08000000 + 4)[0] - 0x08000000
                seen = {}
                for i in range(n):
                    lo, hi, sp = struct.unpack_from('<BBH', rom, m + 4 * i); seen.setdefault(sp, []).extend((lo, hi))
                out += [(f"{self.map_name(rom[o], rom[o + 1]) or 'Map'} [{rom[o]}/{rom[o + 1]}] {area}", sp, 0, min(l), max(l), {'location': self.map_name(rom[o], rom[o + 1]) or f'Map [{rom[o]}/{rom[o + 1]}]', 'method': area}) for sp, l in seen.items()]
            o += 20
        # Statics: scan the script region (all map script starts, found via map headers) for
        # setwildbattle B6 (sp u16, lv, item u16), givemon 79 (sp u16, lv, item u16), and event mons
        # (setvar 8004 sp / 8005 lv / 8006 item, then a "create" special). An event special counts if a
        # special that follows a setwildbattle also follows it, or it shares its create special with one that does.
        import re, bisect
        self.map_name(0, 0); P = lambda a: (lambda q: q - 0x08000000 if 0x08000000 <= q < 0x08000000 + L else None)(struct.unpack_from('<I', rom, a)[0])
        st = []
        for k, h in self._map_headers.items():
            e = P(h + 4)
            for n, t, sz, so in ((rom[e], P(e + 4), 24, 16), (rom[e + 2], P(e + 12), 16, 12), (rom[e + 3], P(e + 16), 12, 8)) if e is not None else ():
                st += [(q, k) for i in range(n if t is not None else 0) if (q := P(t + i * sz + so)) is not None]
            m = P(h + 8)
            while m is not None and rom[m]:
                if (q := P(m + 1)) is not None: st.append((q, k))
                m += 5
        if not st: return out
        st.sort(); ks = [a for a, _ in st]; base = ks[0]; reg = rom[base:ks[-1] + 0x800]
        def where(x):
            i = bisect.bisect_right(ks, x + base) - 1
            return st[i][1] if i >= 0 and x + base - ks[i] < 0x800 else None
        after = lambda x: {reg[x + j + 1:x + j + 3] for j in range(32) if x + j < len(reg) and reg[x + j] == 0x25}
        hits = [(mm.start(), 'static' if reg[mm.start()] == 0xB6 else 'gift', *struct.unpack_from('<HB', reg, mm.start() + 1)) for mm in re.finditer(rb'[\xb6\x79]....[\x00\x01]', reg, re.S)]
        hits = [x for x in hits if 0 < x[2] < 440 and 0 < x[3] <= 100 and where(x[0])]
        S = set().union(*(after(x[0]) for x in hits if x[1] == 'static'))
        ev = [(mm.start() + 15, 'event', struct.unpack_from('<H', reg, mm.start() + 3)[0], reg[mm.start() + 8]) for mm in re.finditer(rb'\x16\x04\x80..\x16\x05\x80..\x16\x06\x80..\x25', reg, re.S)]
        ev = [x for x in ev if 0 < x[2] < 440 and 0 < x[3] <= 100 and where(x[0])]
        C = {reg[x[0] + 1:x[0] + 3] for x in ev if after(x[0] + 3) & S}
        for x, kind, sp, lv in hits + [x for x in ev if reg[x[0] + 1:x[0] + 3] in C]:
            g, n = where(x); out.append((f"{self.map_name(g, n) or 'Map'} [{g}/{n}] {kind}", sp, 0, lv, lv, {'location': self.map_name(g, n) or f'Map [{g}/{n}]', 'method': kind}))
        return out

    def iter_learnsets(self):
        """GBA: one pointer per species slot. Table located once by the Gen III finder, cached."""
        rom = bytes(self.rom or b'')
        if getattr(self, '_learnset_table', None) is None:
            self._learnset_table = (self._discover_gen3_tables(self._current_rom_ref()) or {}).get('learnset_ptr_table', 0)
        t = self._learnset_table
        if not t: return
        for s in range(1, self.LEARNSET_COUNT + 1):
            p = struct.unpack_from('<I', rom, t + 4 * s)[0] - 0x08000000
            if 0 <= p < len(rom): yield s, self.learnset_moves(rom[p:p + 256])

    # Clean attribute names
    DISCOVER_TABLES = _discover_gen3_tables
    def bootstrap_text(self, rom_data, region='US'):
        """Gen III text bootstrap — struct-based items, ability scanner."""
        charmap = self.CHARMAP_JP if region == 'JP' else self.CHARMAP_EN
        eos = self.EOS
        self.text_tables = {}

        candidates = self.scan_rom_text(rom_data, charmap, eos)
        for idx, table in enumerate(candidates):
            self.text_tables[idx] = table

        self._scan_gen3_abilities(rom_data, charmap, eos, self.text_tables)
        self._scan_gen3_items(rom_data, charmap, eos, self.text_tables)
        self._scan_gen3_species(rom_data, charmap, eos, self.text_tables)
        self._scan_gen3_trainer_names(rom_data, charmap, eos, self.text_tables)

        self._auto_detect_tables()
        self._map_text_tables()

    SCAN_ABILITIES = _scan_gen3_abilities
    SCAN_ITEMS = _scan_gen3_items
    SCAN_SPECIES = _scan_gen3_species
    SCAN_TRAINER_NAMES = _scan_gen3_trainer_names

    def decode_personal(self, data, file_idx, text_tables, tm_table=None):
        """Decode Gen III/IV personal data (28B or 44B). Returns formatted string."""
        if len(data) < 28 or data == b'\x00' * len(data):
            return None
        import struct
        species_list = text_tables.get('species', [])
        type_list = text_tables.get('type_names', [])
        ability_list = text_tables.get('abilities', [])
        item_list = text_tables.get('items', [])
        moves_list = text_tables.get('moves', [])

        hp, atk, dfn, spe, spa, spd = data[0], data[1], data[2], data[3], data[4], data[5]
        bst = hp + atk + dfn + spe + spa + spd
        type1, type2 = data[6], data[7]
        catch_rate = data[8]

        ev_raw = struct.unpack_from('<H', data, 0x0A)[0]
        evs = []
        for i, stat in enumerate(self.EV_STAT_ORDER):
            val = (ev_raw >> (i * 2)) & 3
            if val: evs.append(f"+{val} {stat}")

        items = [struct.unpack_from('<H', data, 0x0C + i * 2)[0] for i in range(2)]
        held_labels = ['common', 'rare']
        gender = data[0x10]
        hatch_cycles = data[0x11]
        base_happiness = data[0x12]
        exp_growth = data[0x13]
        egg1, egg2 = data[0x14], data[0x15]
        abilities = [data[0x16], data[0x17]]
        ability_names = [ability_list[a] if a < len(ability_list) else f"ability#{a}" for a in abilities if a > 0]

        species_name = species_list[file_idx] if file_idx < len(species_list) else f"#{file_idx}"
        t1 = type_list[type1] if type1 < len(type_list) else f"type#{type1}"
        t2 = type_list[type2] if type2 < len(type_list) else f"type#{type2}"
        types_str = t1 if type1 == type2 else f"{t1} / {t2}"

        held_parts = []
        for label, item_id in zip(held_labels, items):
            if item_id > 0:
                iname = item_list[item_id] if item_id < len(item_list) else f"item#{item_id}"
                held_parts.append(f"{iname} ({label})")

        gender_str = {0:"100% \u2642", 31:"87.5% \u2642 / 12.5% \u2640", 63:"75% \u2642 / 25% \u2640",
                      127:"50% \u2642 / 50% \u2640", 191:"25% \u2642 / 75% \u2640",
                      223:"12.5% \u2642 / 87.5% \u2640", 254:"100% \u2640", 255:"Genderless"}.get(gender, f"ratio {gender}")
        _egg = {v: n[4:].replace('_',' ').title() for n in dir(self) if n.startswith('EGG_') for v in [getattr(_SDK,n)]}
        _egg[0] = '\u2014'
        _growth = {v: n[7:].replace('_',' ').title() for n in dir(self) if n.startswith('GROWTH_') for v in [getattr(_SDK,n)]}

        lines = [f"{species_name} (#{file_idx})", f"{types_str} | BST {bst}",
                 f"HP {hp} | Atk {atk} | Def {dfn} | SpA {spa} | SpD {spd} | Spe {spe}",
                 f"Abilities: {' / '.join(ability_names)}" if ability_names else "Abilities: ---",
                 f"Gender: {gender_str} | Catch Rate: {catch_rate} | Hatch: {hatch_cycles} cycles | Happiness: {base_happiness}",
                 f"Growth: {_growth.get(exp_growth, f'#{exp_growth}')} | Egg Groups: {_egg.get(egg1,'?')} / {_egg.get(egg2,'?')}"]
        if held_parts:
            lines.append(f"Held Items: {' / '.join(held_parts)}")
        if evs:
            lines.append(f"EVs: {', '.join(evs)}")

        if tm_table and len(data) >= 0x2C:
            tm_flags = data[0x1C:0x2C]
            tms, hms = [], []
            for bit_idx, (label, move_id) in enumerate(tm_table):
                if tm_flags[bit_idx // 8] & (1 << (bit_idx % 8)):
                    move_name = moves_list[move_id] if move_id < len(moves_list) else f"move#{move_id}"
                    (hms if label.startswith('HM') else tms).append(f"{label[2:]} {move_name}")
            if tms: lines.append(f"TM: {' / '.join(tms)}")
            if hms: lines.append(f"HM: {' / '.join(hms)}")

        ab_desc = text_tables.get('ability_descriptions', [])
        if ab_desc:
            for ab in abilities:
                if ab and ab < len(ab_desc) and ab_desc[ab]:
                    ab_name = ability_list[ab] if ab < len(ability_list) else f'ability#{ab}'
                    lines.append(f'{ab_name}: {ab_desc[ab]}')

        return "\n".join(lines)

