"""sdk.py: Defines the constants that the Pokemon engine uses, divided by generation.

Game Freak's SDK vocabulary — evolution methods, gender values, growth curves,
egg groups, move categories. This class knows no specific game exists.
Every game class inherits from SDK. The class tree IS the registry.

Import chain: SDK class -> game classes -> server.py
This file has zero imports. It is a leaf dependency.
"""


class SDK:
    """Engine vocabulary. Knows no specific game."""

    # ── Evolution method IDs ──
    # Gen 1-5 base. Gen 6+ games add new ones in their own files.
    EVO_NONE = 0
    EVO_HAPPINESS = 1
    EVO_HAPPINESS_DAY = 2
    EVO_HAPPINESS_NIGHT = 3
    EVO_LEVEL_UP = 4
    EVO_TRADE = 5
    EVO_TRADE_WITH_ITEM = 6
    EVO_STONE = 7
    EVO_ATK_GT_DEF = 8
    EVO_ATK_EQ_DEF = 9
    EVO_ATK_LT_DEF = 10
    EVO_PERSONALITY_LO = 11
    EVO_PERSONALITY_HI = 12
    EVO_NINJASK = 13
    EVO_SHEDINJA = 14
    EVO_BEAUTY = 15
    EVO_STONE_MALE = 16
    EVO_STONE_FEMALE = 17
    EVO_HOLD_ITEM_DAY = 18
    EVO_HOLD_ITEM_NIGHT = 19
    EVO_MOVE = 20
    EVO_PARTY_SPECIES = 21
    EVO_LEVEL_MALE = 22
    EVO_LEVEL_FEMALE = 23
    EVO_LEVEL_ELECTRIC = 24
    EVO_LEVEL_MOSSY = 25
    EVO_LEVEL_ICY = 26

    # ── Gender byte values ──
    GENDER_ALL_MALE = 0
    GENDER_7M_1F = 31
    GENDER_3M_1F = 63
    GENDER_HALF = 127
    GENDER_1M_3F = 191
    GENDER_1M_7F = 223
    GENDER_ALL_FEMALE = 254
    GENDER_GENDERLESS = 255

    learnset_moves = None  # reverse lookup off until a class defines its learnset format

    def _iter_narc_learnsets(self):
        """(species_idx, [(level, move_id)]) per learnset file. None if format unknown."""
        if not self.learnset_moves or not getattr(self, 'LEARNSET_PATH', None): return None
        return ((i, self.learnset_moves(d)) for i, d in enumerate(self.get_narc(self.LEARNSET_PATH).files))

    def iter_learnsets(self):
        return self._iter_narc_learnsets()

    # ── Growth curves ──
    GROWTH_MEDIUM_FAST = 0
    GROWTH_ERRATIC = 1
    GROWTH_FLUCTUATING = 2
    GROWTH_MEDIUM_SLOW = 3
    GROWTH_FAST = 4
    GROWTH_SLOW = 5

    # ── Egg groups ──
    EGG_NONE = 0
    EGG_MONSTER = 1
    EGG_WATER1 = 2
    EGG_BUG = 3
    EGG_FLYING = 4
    EGG_FIELD = 5
    EGG_FAIRY = 6
    EGG_GRASS = 7
    EGG_HUMAN_LIKE = 8
    EGG_WATER3 = 9
    EGG_MINERAL = 10
    EGG_AMORPHOUS = 11
    EGG_WATER2 = 12
    EGG_DITTO = 13
    EGG_DRAGON = 14
    EGG_UNDISCOVERED = 15

    # ── Move categories (Gen 5+ order) ──
    CAT_STATUS = 0
    CAT_PHYSICAL = 1
    CAT_SPECIAL = 2

    # ── Display-name lookups ──
    GROWTH_NAMES = ('Medium Fast', 'Erratic', 'Fluctuating', 'Medium Slow', 'Fast', 'Slow')
    EGG_GROUP_NAMES = ('---', 'Monster', 'Water 1', 'Bug', 'Flying', 'Field', 'Fairy', 'Grass',
                       'Human-Like', 'Water 3', 'Mineral', 'Amorphous', 'Water 2', 'Ditto',
                       'Dragon', 'Undiscovered')
    CATEGORY_NAMES = ('Status', 'Physical', 'Special')
    SEX_SYMBOLS = ('', ' M', ' F')
    BATTLE_TYPES = ('Single',)

    # ── EV yield stat order (bitfield) ──
    EV_STAT_ORDER = ('HP', 'Atk', 'Def', 'Spe', 'SpA', 'SpD')

    # ── Language system ──
    # Game Freak's filesystem order — each language is a consecutive GARC.
    # The GARC number IS the language. No dict needed.
    LANGUAGES_8 = ('ja', 'ja-kanji', 'en', 'fr', 'it', 'de', 'es', 'ko')
    LANGUAGES_10 = ('ja', 'ja-kanji', 'en', 'fr', 'it', 'de', 'es', 'ko', 'zh-Hans', 'zh-Hant')

    # Specs override these to enable multilingual text
    TEXT_LANG_BASE = None    # GARC path prefix, e.g. 'a/0/7/'
    TEXT_LANG_FIRST = 0      # GARC index where JPN starts
    LANGUAGES = ()           # which tuple — LANGUAGES_8 or LANGUAGES_10

    # ── Game identity defaults ──
    JP = False
    YEAR = None
    TITLES = ()
    GAME_CODES = ()

    # ── Region codes (Nintendo's single-char region in ROM headers) ──
    REGION_MAP = {
        'J': 'JP', 'E': 'US', 'P': 'EU', 'D': 'DE', 'F': 'FR',
        'S': 'ES', 'I': 'IT', 'K': 'KR', 'C': 'CN', 'W': 'World',
    }

    # ── GB game code lookup (GB ROMs have titles, not 4-char codes) ──
    _GB_GAME_CODES = {
        'POKEMON RED': 'PMR', 'POKEMON BLUE': 'PMB', 'POKEMON BLU': 'PMB',
        'POKEMON YELLOW': 'PMY', 'POKEMON GREEN': 'PMG', 'POKEMON YEL': 'PMY', 'POKEMON GRE': 'PMG',
        'POKEMON_GLDAAUE': 'PMG2', 'POKEMON_GLD': 'PMG2', 'POKEMON GOLD': 'PMG2',
        'PM_CRYSTAL': 'PMC', 'POKEMON CRYSTAL': 'PMC',
        'POKEMON SILVER': 'PMS',
    }

    # ── Instance state (populated by spotlight) ──

    # Content fingerprints — universal across all Pokemon games
    TABLE_FINGERPRINTS = (
        ('species',        ((1, "Bulbasaur"), (4, "Charmander"))),
        ('moves',          ((1, "Pound"), (5, "Mega Punch"))),
        ('items',          ((1, "Master Ball"), (17, "Potion"))),
        ('abilities',      ((1, "Stench"), (22, "Intimidate"))),
        ('natures',        ((0, "Hardy"), (1, "Lonely"), (3, "Adamant"))),
        ('type_names',     ((0, "Normal"), (1, "Fighting"), (2, "Flying"))),
        ('tournament_names', ((4, "Champions Tournament"), (13, "Rental Tournament"))),
    )

    HEURISTIC_MARKERS = (
        ('trainer_classes', ("Youngster", "Hiker", "Ace Trainer")),
        ('location_names',  ("Mystery Zone",)),
        ('trainer_names',   ("Palmer", "Cynthia")),
        ('trainer_names_gen5', ("Bianca", "Shauntal", "Grimsley")),
        ('trainer_names_gen7', ("Lana", "Acerola", "Gladion")),
        ('trainer_names_gen9a', ("Taunie", "Urbain", "Jacinthe")),
    )

    HEURISTIC_SUBSTR = (
        ('item_descriptions',  ("best Ball with the ultimate",)),
        ('move_descriptions',  ("pounded with a long tail",)),
        ('ability_descriptions', ("repel wild",)),
        ('pokedex_flavor',     ("seed on its back",)),
        ('pokedex_category',   ("Seed Pok", "Lizard Pok")),
    )

    def __init__(self):
        self._lang = 'en'
        self._text_indices = {}  # {name: file_idx} — survives language switches
        self.text_tables = {}
        self.tm_table = []
        self.enc_loc = {}
        self.narc_roles = {}
        self.text_narc = None
        self.text_mult = None
        self.text_narc_path = None
        self._text_modified = set()
        self.pwt_name_to_entries = {}
        self.pwt_entry_tournaments = {}
        self.rom = None           # ndspy ROM object (NDS) or raw bytes (GBA/GB)
        self.rom_type = None      # 'nds', '3ds', 'gba', 'gbc', 'gb'
        self.rom_path = None
        self.header = {}
        self.arm9_data = None
        self.arm7_data = None
        self.overlays = {}
        self.romfs_fh = None      # 3DS file handle
        self.romfs_files = {}     # 3DS romfs dict
        self.code_data = None     # 3DS ExeFS .code
        self.compression_state = {}
        self._narc_cache = {}
        self._ahtb_cache = {}   # {narc_path: [ahtb_bytes, ...]} — parallel with _narc_cache .files
        self.switch_rom = None
        self.flipnote = None      # {path, data}
        self.eonet_labels = {}
        self.eonet_index = []

    def get_narc(self, narc_path):
        """Get parsed NARC/GARC, cached. Platform specs override."""
        raise ValueError(f"get_narc not implemented for {self.__class__.__name__}")

    def read_file(self, path):
        """Read a file from the ROM. Platform specs override this."""
        raise ValueError(f"read_file not implemented for {self.__class__.__name__}")

    @classmethod
    def get_spec(cls, code):
        """Walk subclass tree to find the spec for a game code or title ID."""
        if code in cls.__dict__.get('GAME_CODES', ()):
            return cls
        if code in cls.__dict__.get('TITLE_IDS', ()):
            return cls
        for sub in cls.__subclasses__():
            result = sub.get_spec(code)
            if result:
                return result

    @classmethod
    def spec_narcs(cls, spec):
        """Build role->path dict from a spec class's _PATH attributes."""
        narcs = {}
        for attr in dir(spec):
            if attr.endswith('_PATH') and attr != 'PLATFORM':
                role = attr[:-5].lower()
                narcs[role] = getattr(spec, attr)
        return narcs

    # ── Header readers (ROM identification) ──

    @staticmethod
    def _read_nds_banner_title(path, banner_offset):
        """Read English title from NDS banner (UTF-16LE at banner+0x340)."""
        try:
            with open(path, 'rb') as f:
                f.seek(banner_offset + 0x340)
                raw = f.read(256).decode('utf-16-le', errors='ignore').split('\x00')[0]
                lines = raw.split('\n')
                return f"{lines[0]} {lines[1]}".strip() if len(lines) >= 2 else lines[0].strip()
        except:
            return ""

    @classmethod
    def read_header(cls, path, update_path=None):
        """Read ROM header. Returns dict with game_code, region, etc."""
        import struct as _st
        ext = path.rsplit('.', 1)[-1].lower()

        if ext == 'nds':
            with open(path, 'rb') as f:
                short_title = f.read(12).decode('ascii', errors='ignore').strip('\x00')
                full_code = f.read(4).decode('ascii', errors='ignore')
                f.seek(0x68)
                banner_offset = _st.unpack('<I', f.read(4))[0]
            game_code = full_code[:3] if len(full_code) >= 3 else full_code
            region_char = full_code[3] if len(full_code) >= 4 else 'E'
            english_title = cls._read_nds_banner_title(path, banner_offset) if banner_offset else ""
            is_english = bool(english_title and any(c.isalpha() for c in english_title))
            return {'game_code': game_code, 'full_code': full_code,
                    'region_char': region_char, 'short_title': short_title,
                    'game_title': english_title if is_english else short_title,
                    'is_english': is_english,
                    'region': cls.REGION_MAP.get(region_char, 'INT')}

        if ext == 'gba':
            with open(path, 'rb') as f:
                f.seek(0xA0)
                title = f.read(12).decode('ascii', errors='ignore').strip('\x00')
                full_code = f.read(4).decode('ascii', errors='ignore')
            game_code = full_code.strip() if full_code.strip() else full_code[:3]
            region_char = full_code[3] if len(full_code) >= 4 else 'E'
            return {'game_code': game_code, 'full_code': full_code,
                    'region_char': region_char, 'game_title': title,
                    'region': cls.REGION_MAP.get(region_char, 'US'),
                    'is_english': region_char in ('E', 'P', 'D', 'F', 'S', 'I')}

        if ext in ('gb', 'gbc'):
            with open(path, 'rb') as f:
                data = f.read(0x150)
            title = data[0x134:0x13F].decode('ascii', errors='ignore').strip('\x00').strip()
            region_byte = data[0x14A] if len(data) > 0x14A else 0x01
            region = 'JP' if region_byte == 0x00 else 'US'
            region_char = 'J' if region == 'JP' else 'E'
            game_code = cls._GB_GAME_CODES.get(title.upper(), title[:3].upper())
            return {'game_code': game_code, 'full_code': title[:4],
                    'region_char': region_char, 'game_title': title,
                    'region': region, 'is_english': region != 'JP'}

        if ext in ('xci', 'nsp'):
            return cls._read_switch_header(path, update_path)

        raise ValueError(f"Unknown ROM extension: .{ext}")

    @classmethod
    def _read_switch_header(cls, path, update_path=None):
        """Read Switch ROM header. Extracts title ID, finds spec via get_spec."""
        from leswitch import open_rom
        sw = open_rom(path, update_path=update_path)
        title_id = sw.title_id
        spec = cls.get_spec(title_id)
        if not spec:
            raise ValueError(f'Unknown Switch title ID: 0x{title_id:016X}')
        idx = spec.TITLE_IDS.index(title_id) if title_id in spec.TITLE_IDS else 0
        return {'game_code': spec.GAME_CODES[idx], 'game_title': spec.TITLES[idx],
                'region': 'World', 'region_char': 'W', 'is_english': True,
                'title_id': title_id, '_switch_rom': sw}

    # ── Role dispatch ──

    def decode(self, role, data, file_idx=0, path='', **kwargs):
        """Route role to decode method via getattr. No dict needed."""
        method = getattr(self, f'decode_{role}', None)
        if not method:  # try plural/singular and _data suffix
            method = getattr(self, f'decode_{role}s', None) or getattr(self, f'decode_{role.rstrip("s")}', None)
        if not method and role.endswith('_data'):
            method = getattr(self, f'decode_{role[:-5]}', None)
        if not method:
            return None
        try:
            try:
                r = method(data, file_idx, self.text_tables, path=path, **kwargs)
            except TypeError:
                r = method(data, file_idx, self.text_tables)
        except Exception:
            return None
        if isinstance(r, list) and r and isinstance(r[0], tuple) and len(r[0]) == 5:
            sp = self.text_tables.get('species', [])
            return '\n'.join(f"{lb}: {sp[s] if s < len(sp) else s}" + (f" form{fm}" if fm else '') + f" Lv{lo}" + (f"-{hi}" if hi != lo else '') for lb, s, fm, lo, hi in r)
        return r

    def _map_text_tables(self):
        """Map indices to named keys. Saved indices (from fingerprinting) take priority."""
        # Saved indices from a previous fingerprint pass — same file positions, any language
        if self._text_indices:
            for name, idx in self._text_indices.items():
                if idx in self.text_tables:
                    self.text_tables[name] = self.text_tables[idx]
            return
        tmap = getattr(self, 'TEXT_TABLE_MAP', None)
        if tmap:
            for name, idx in tmap.items():
                if idx in self.text_tables:
                    self.text_tables[name] = self.text_tables[idx]

    def bootstrap_text(self, narc_files):
        """Decrypt text files and map named tables. Override per gen for decrypt method."""
        pass

    def text_path_for(self, lang='en'):
        """Compute text path for any language. Switch: folder-name swap. 3DS: index math."""
        folders = getattr(self, 'LANG_FOLDERS', None)
        if folders:
            cur = folders.get(self._lang or 'en', 'English')
            tgt = folders.get(lang)
            if not tgt:
                raise ValueError(f"Unknown language '{lang}'. Options: {', '.join(self.LANGUAGES)}")
            return self.TEXT_PATH.replace(cur, tgt)
        if not self.TEXT_LANG_BASE or not self.LANGUAGES:
            return getattr(self, 'TEXT_PATH', None)
        return f'{self.TEXT_LANG_BASE}{self.TEXT_LANG_FIRST + self.LANGUAGES.index(lang)}'

    def set_language(self, lang):
        """Switch language and clear text tables for re-bootstrap."""
        if not self.LANGUAGES:
            raise ValueError(f"{self.__class__.__name__} has no language support")
        if lang not in self.LANGUAGES:
            raise ValueError(f"'{lang}' not available. Options: {', '.join(self.LANGUAGES)}")
        self._lang = lang
        self.TEXT_PATH = self.text_path_for(lang)
        self.text_tables.clear()


    @staticmethod
    def parse_ahtb(data):
        """Parse AHTB sidecar: returns list of (hash_u64, name_str) parallel with .tbl entries."""
        if not data or data[:4] != b'AHTB':
            return []
        import struct
        count = struct.unpack_from('<I', data, 4)[0]
        entries = []
        off = 8
        for _ in range(count):
            h = struct.unpack_from('<Q', data, off)[0]; off += 8
            slen = struct.unpack_from('<H', data, off)[0]; off += 2
            name = data[off:off+slen].decode('utf-8', errors='replace').rstrip('\x00')
            off += slen  # slen includes null terminator
            entries.append((h, name))
        return entries

    # ── Shared decoders ──

    def decode_ev_spread(self, byte_val):
        """Decode EV bitmask: each set bit = 252 EVs in that stat."""
        stats = [self.EV_STAT_ORDER[i] for i in range(6) if byte_val & (1 << i)]
        return stats if stats else ["None"]

    def decode_trainer_iv(self, byte_val):
        """TRPoke difficulty byte -> IV for all stats. 255 -> 31, 0 -> 0."""
        return byte_val * 31 // 255

    def decode_gender(self, gender_byte, species_id=0):
        """Decode trainer-pokemon gender byte. 0=default, 1=male, 2=female, 3=genderless."""
        if gender_byte == 1:
            return "Male"
        elif gender_byte == 2:
            return "Female"
        elif gender_byte == 3:
            return "Genderless"
        else:
            return "Random"

    def get_challenge_delta(self, file_idx):
        """Challenge mode level delta. Only BW2 overrides this."""
        return 0

    def decode_ai_flags(self, flags):
        """Decode AI flags into comma-separated string."""
        flag_map = getattr(self, 'AI_FLAGS', {})
        active_flags = []
        for bit, name in sorted(flag_map.items()):
            if flags & bit:
                active_flags.append(name)
        return ', '.join(active_flags) if active_flags else 'None'

    def _format_section(self, entries, rates, header):
        """Format a consolidated encounter section."""
        consolidated = self._consolidate_slots(entries, rates)
        if not consolidated:
            return ""
        lines = [f"\n{header}:"]
        for e in consolidated:
            lv = e['level'].replace('Lv', 'Lv. ')
            lines.append(f"  {e['species']:<20}{lv:<12}{e['rate']:>3}%")
        return "\n".join(lines)



    def _format_trainer_card(self, trdata: dict, pokemon: list, file_idx: int, prize: int = 0) -> str:
        """Format a trainer as positional text. Works for all gens — no gen check needed.
        trdata: dict with 'class', 'name', 'battle_type', 'ai_flags', 'battle_items'
        pokemon: list of dicts with 'species', 'species_id', 'level', 'ivs', 'held_item', 'moves', etc.
        """
        class_name = trdata.get('class', '???')
        trainer_name = trdata.get('name', f'Trainer #{file_idx}')
        battle_type = trdata.get('battle_type', 'Single')

        # Location from bootstrap (gym leaders, league, etc.)
        location = None
        for indices, loc in getattr(self, '_gym_locations', ()):
            if file_idx in indices:
                location = loc
                break
        if location is None and file_idx in getattr(self, '_league_indices', set()):
            location = "Pokémon League"

        if location:
            lines = [f"{class_name} {trainer_name} - {location}"]
        else:
            lines = [f"{class_name} {trainer_name}"]

        if battle_type != 'Single':
            lines[0] += f"  [{battle_type} Battle]"

        _chal_delta = self.get_challenge_delta(file_idx)

        if pokemon:
            lines.append("")
            lines.append("Team:")

        for poke in pokemon:
            species = poke.get('species', '???')
            species_id = poke.get('species_id', 0)
            level = poke.get('level', '?')
            held = poke.get('held_item', None)

            # Form resolution
            form_idx = poke.get('form', 0)
            if form_idx:
                form_label = getattr(self, 'FORM_NAMES', {}).get((species_id, form_idx), '')
                if form_label:
                    species = f"{species}-{form_label}"

            # Gender symbol for header line
            gender = poke.get('gender')
            gender_sym = {'Male': '♂', 'Female': '♀', 'Genderless': '☲'}.get(gender, '')
            g = f" {gender_sym}" if gender_sym else ""

            if _chal_delta:
                header = f"{species}{g} (Lv. {level + _chal_delta})"
            else:
                header = f"{species}{g} (Lv. {level})"
            if held and held != 'None':
                header += f"  [{held}]"
            lines.append(header)

            # Ability / Nature / EVs / IVs
            ability = poke.get('ability')
            nature = poke.get('nature')
            evs = poke.get('evs')
            iv_val = poke.get('ivs')
            if ability:
                lines.append(f"Ability: {ability}")
            if nature:
                lines.append(f"{nature} Nature")
            if evs:
                lines.append(f"EVs: {evs}")
            if iv_val is not None:
                if isinstance(iv_val, str):
                    lines.append(f"IVs: {iv_val}")
                else:
                    lines.append(f"IVs: {iv_val} HP / {iv_val} Atk / {iv_val} Def / {iv_val} SpA / {iv_val} SpD / {iv_val} Spe")
            moves = poke.get('moves', [])
            if moves:
                move_str = " / ".join(m for m in moves if m != '---')
                if move_str:
                    lines.append(move_str)

        # Footer metadata
        footer = []
        if prize > 0:
            footer.append(f"Prize: ¥{prize:,}")

        items = trdata.get('battle_items', 'None')
        if isinstance(items, list) and items:
            footer.append(f"Items Used in Battle: {', '.join(items)}")
        else:
            footer.append("No Items Used")

        ai = trdata.get('ai_flags', [])
        if ai and ai != ['None']:
            footer.append(f"AI: {', '.join(ai)}")

        if footer:
            lines.append("")
            lines.append(" | ".join(footer))

        return "\n".join(lines)



    def scan_rom_text(self, rom_data: bytes, charmap: dict, eos: int,
                      min_strlen: int = 3, min_table: int = 8,
                      max_strlen: int = 20) -> list:
        """Scan a raw ROM binary for text tables.

        Looks for runs of back-to-back valid strings (terminated by eos byte).
        Returns list of lists — each inner list is a candidate text table (list of strings).

        Strategy: slide over the ROM at every offset. If we hit a valid string
        followed by EOS, keep going. When the run breaks, if we collected enough
        strings, save it as a candidate table.
        """
        tables = []
        current_table = []
        i = 0
        data_len = min(len(rom_data), 8 * 1024 * 1024)  # text lives in first 8MB

        while i < data_len:
            # Skip leading 0x00 bytes — these are null padding between fixed-width
            # table entries, not spaces at the start of a string.
            while i < data_len and rom_data[i] == 0x00:
                i += 1

            # Try to decode a string starting at i
            j = i
            chars = []
            while j < data_len and j < i + max_strlen:
                b = rom_data[j]
                if b == eos:
                    break
                ch = charmap.get(b)
                if ch is None:
                    break
                chars.append(ch)
                j += 1

            # Strip trailing spaces (from in-string 0x00s near end of entry)
            name = ''.join(chars).rstrip()

            if j < data_len and rom_data[j] == eos and len(name) >= min_strlen:
                # Valid string found
                current_table.append(name)
                i = j + 1  # advance past EOS
            else:
                # Not a valid string here
                if len(current_table) >= min_table:
                    tables.append(current_table)
                current_table = []
                i += 1

        if len(current_table) >= min_table:
            tables.append(current_table)

        return tables



    def _auto_detect_tables(self) -> dict:
        """Scan decoded text_tables to identify named tables by content fingerprinting."""
        # Seed with tables already set by dedicated scanners so they aren't overwritten.
        # Use -1 as sentinel (no valid integer key is negative).
        found = {k: -1 for k in self.text_tables if isinstance(k, str)}

        # Pass 1: exact fingerprints (entry at specific index must match)
        # Try English first, then Japanese — same indices, different strings.
        # Gather fingerprint sets: main + any from spec chain (Gen 3, JP, etc.)
        _fp_sets = [self.TABLE_FINGERPRINTS]
        if self.TABLE_FINGERPRINTS is not SDK.TABLE_FINGERPRINTS:
            _fp_sets.append(SDK.TABLE_FINGERPRINTS)
        fp_jp = getattr(self, 'TABLE_FINGERPRINTS_JP', None)
        if fp_jp:
            _fp_sets.append(fp_jp)
        for fingerprint_set in _fp_sets:
            for file_idx in sorted(k for k in self.text_tables if isinstance(k, int)):
                strings = self.text_tables[file_idx]
                if not isinstance(strings, list) or len(strings) < 2:
                    continue
                for table_name, markers in fingerprint_set:
                    if table_name in found:
                        continue
                    if all(idx < len(strings) and strings[idx].strip().upper() == expected.upper() for idx, expected in markers):
                        self.text_tables[table_name] = strings
                        found[table_name] = file_idx

        # Pass 2: heuristic markers (all listed strings must exist in file)
        # For trainer_names variants, multiple files can match — keep the largest.
        _heuristic_sizes = {}  # table_name -> entry count of current match
        for file_idx in sorted(k for k in self.text_tables if isinstance(k, int)):
            strings = self.text_tables[file_idx]
            if not isinstance(strings, list):
                continue
            string_set_upper = set(s.strip().upper() for s in strings if isinstance(s, str))
            for table_name, markers in self.HEURISTIC_MARKERS:
                if table_name in found and 'trainer_names' not in table_name:
                    continue
                if all(m.upper() in string_set_upper for m in markers):
                    if table_name in found and len(strings) <= _heuristic_sizes.get(table_name, 0):
                        continue  # keep larger match
                    self.text_tables[table_name] = strings
                    found[table_name] = file_idx
                    _heuristic_sizes[table_name] = len(strings)

        # Pass 2b: substring markers
        for file_idx in sorted(k for k in self.text_tables if isinstance(k, int)):
            strings = self.text_tables[file_idx]
            if not isinstance(strings, list):
                continue
            for table_name, markers in self.HEURISTIC_SUBSTR:
                if table_name in found:
                    continue
                joined = ' '.join(s for s in strings if isinstance(s, str)).lower()
                if all(m.lower() in joined for m in markers):
                    self.text_tables[table_name] = strings
                    found[table_name] = file_idx

        # Promote gen-specific trainer_names variants -> trainer_names
        # Use gen moniker to pick the right variant — no blind priority
        _gen_variant = {9: 'trainer_names_gen9a', 7: 'trainer_names_gen7', 6: 'trainer_names_gen7',
                        5: 'trainer_names_gen5'}
        preferred = _gen_variant.get(self.GEN)
        if preferred and preferred in found and 'trainer_names' not in found:
            found['trainer_names'] = found.pop(preferred)
            self.text_tables['trainer_names'] = self.text_tables.pop(preferred)
        # Clean up any unmatched variants
        for variant in ('trainer_names_gen9a', 'trainer_names_gen7', 'trainer_names_gen5'):
            if variant in found:
                found.pop(variant)
                self.text_tables.pop(variant, None)

        # Pass 3b: Gen IV has TWO trainer name files — generic NPC names and battle
        # trainer names. Heuristic markers match both. Use PPRE-verified indices.
        VERIFIED_TRAINER_NAMES = {
            'ADA': 559, 'APA': 559,   # Diamond / Pearl
            'CPU': 618,                # Platinum
            'IPK': 729, 'IPG': 729,   # HeartGold / SoulSilver
        }
        gc = self.header.get('game_code') if self.header else None
        if gc in VERIFIED_TRAINER_NAMES:
            correct_idx = VERIFIED_TRAINER_NAMES[gc]
            if correct_idx in self.text_tables and isinstance(self.text_tables[correct_idx], list):
                old_idx = found.get('trainer_names')
                if old_idx is not None and old_idx != correct_idx:
                    self.text_tables['npc_names'] = self.text_tables[old_idx]
                    found['npc_names'] = old_idx
                self.text_tables['trainer_names'] = self.text_tables[correct_idx]
                found['trainer_names'] = correct_idx

        # Pass 4: description tables — usually near their name tables.
        # Gen V: typically ±1. Gen IV: can be ±1 to ±3.
        # Descriptions have similar entry count but longer average string length.
        for name_tbl, desc_tbl in [('items', 'item_descriptions'), ('moves', 'move_descriptions'), ('abilities', 'ability_descriptions')]:
            if found.get(name_tbl, -1) >= 0 and desc_tbl not in found:
                name_idx = found[name_tbl]
                name_count = len(self.text_tables[name_tbl])
                for offset in [-1, 1, -2, 2, -3, 3]:
                    candidate = name_idx + offset
                    if candidate in self.text_tables and isinstance(self.text_tables[candidate], list) and candidate not in found.values():
                        entries = self.text_tables[candidate]
                        if abs(len(entries) - name_count) < 10:
                            avg_len = sum(len(s) for s in entries[:20]) / max(1, min(20, len(entries)))
                            if avg_len > 10:  # descriptions longer than names (Gen IV can be short)
                                self.text_tables[desc_tbl] = entries
                                found[desc_tbl] = candidate
                                break

        # Pass 5: verified description indices (BW2 confirmed from PPRE)
        VERIFIED_DESCS = {
            'IRE': {'item_descriptions': 63, 'ability_descriptions': 375, 'move_descriptions': 402},
            'IRD': {'item_descriptions': 63, 'ability_descriptions': 375, 'move_descriptions': 402},
        }
        if gc in VERIFIED_DESCS:
            for desc_tbl, idx in VERIFIED_DESCS[gc].items():
                if desc_tbl not in found and idx in self.text_tables and isinstance(self.text_tables[idx], list):
                    self.text_tables[desc_tbl] = self.text_tables[idx]
                    found[desc_tbl] = idx

        # Pass 6: pokedex flavor — near species table, much longer entries (full dex descriptions)
        if 'species' in found and 'pokedex_flavor' not in found:
            sp_idx = found['species']
            sp_count = len(self.text_tables['species'])
            for offset in range(-5, 6):
                if offset == 0:
                    continue
                candidate = sp_idx + offset
                if candidate in self.text_tables and isinstance(self.text_tables[candidate], list) and candidate not in found.values():
                    entries = self.text_tables[candidate]
                    if abs(len(entries) - sp_count) < 10:
                        avg_len = sum(len(s) for s in entries[:20]) / max(1, min(20, len(entries)))
                        if avg_len > 30:  # dex entries are much longer than species names
                            self.text_tables['pokedex_flavor'] = entries
                            found['pokedex_flavor'] = candidate
                            break

        # Save indices so language switches skip fingerprinting
        for name, idx in found.items():
            if idx >= 0:
                self._text_indices[name] = idx
        return found

    def discover_tm_table(self, binary_data):
        """Search ARM9/ExeFS .code for TM->move table, return bit-ordered list of (label, move_id)."""
        import struct
        tm_table = []
        gen = self.GEN

        if gen >= 6:
            # Gen 6/7: TM02-04 identical across gens, back up 2 bytes for TM01
            pattern = struct.pack('<3H', 337, 473, 347)
            offset = binary_data.find(pattern)
            if offset < 2: return tm_table
            offset -= 2
            entry_count = 100
        else:
            search = getattr(self, 'TM_SEARCH', {}).get(gen)
            if not search: return tm_table
            pattern, entry_count = search
            offset = binary_data.find(pattern)
            if offset < 0: return tm_table

        raw = []
        for i in range(entry_count):
            pos = offset + i * 2
            if pos + 2 > len(binary_data): return tm_table
            raw.append(struct.unpack_from('<H', binary_data, pos)[0])

        if gen == 5:
            for bit in range(101):
                if bit < 92:
                    tm_table.append((f"TM{bit+1:02d}", raw[bit]))
                elif bit < 95:
                    tm_table.append((f"TM{bit+1:02d}", raw[98 + (bit-92)]))
                else:
                    tm_table.append((f"HM{bit-94:02d}", raw[92 + (bit-95)]))
        elif gen >= 6:
            for i in range(100):
                tm_table.append((f"TM{i+1:02d}", raw[i]))
        else:
            for bit in range(100):
                if bit < 92: tm_table.append((f"TM{bit+1:02d}", raw[bit]))
                else: tm_table.append((f"HM{bit-91:02d}", raw[bit]))

        return tm_table

