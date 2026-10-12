"""Unova_prequel.py: Black/White — Gen V structural baseline.

Inherits Johto_remake. Gen V: fully 3D, reboot dex, seasons, triple/rotation battles.
"""
from Johto_remake import Johto_remake
import struct


class Unova_prequel(Johto_remake):
    """Black/White. Gen V baseline."""

    GAME_CODES = ('IRB', 'IRA')
    TITLES = ('Pokémon Black', 'Pokémon White')
    YEAR = 2011

    PLATFORM = 'Nintendo DS'
    GEN = 5
    CONTAINER = 'nds'

    EVO_TRADE_FOR_SPECIES = 7
    EVO_STONE = 8
    EVO_ATK_GT_DEF = 9
    EVO_ATK_EQ_DEF = 10
    EVO_ATK_LT_DEF = 11
    EVO_PERSONALITY_LO = 12
    EVO_PERSONALITY_HI = 13
    EVO_NINJASK = 14
    EVO_SHEDINJA = 15
    EVO_BEAUTY = 16
    EVO_STONE_MALE = 17
    EVO_STONE_FEMALE = 18
    EVO_HOLD_ITEM_DAY = 19
    EVO_HOLD_ITEM_NIGHT = 20
    EVO_MOVE = 21
    EVO_PARTY_SPECIES = 22
    EVO_LEVEL_MALE = 23
    EVO_LEVEL_FEMALE = 24
    EVO_LEVEL_ELECTRIC = 25
    EVO_LEVEL_MOSSY = 26
    EVO_LEVEL_ICY = 27

    SPECIES_COUNT = 649

    BATTLE_TYPES = ('Single', 'Double', 'Triple', 'Rotation', '', 'Multi')

    TEXT_PATH = 'a/0/0/2'
    PERSONAL_PATH = 'a/0/1/6'
    LEARNSET_PATH = 'a/0/1/8'
    EVOLUTION_PATH = 'a/0/1/9'
    EGG_MOVES_PATH = 'a/0/2/0'
    MOVE_DATA_PATH = 'a/0/2/1'
    TRAINER_PATH = 'a/0/9/2'
    TRPOKE_PATH = 'a/0/9/3'
    ITEM_PATH = 'a/0/2/4'
    ENCOUNTER_PATH = 'a/1/2/6'
    BATTLE_TOWER_POKEMON_PATH = None
    BATTLE_TOWER_TRAINERS_PATH = None
    SUBWAY_POKEMON_PATH = 'a/2/1/4'
    SUBWAY_TRAINERS_PATH = 'a/2/1/5'

    PERSONAL_SIZE = 76
    MOVE_DATA_SIZE = 36
    EVOLUTION_SIZE = 42




    AI_FLAGS = {
        0x001: "Basic AI",
        0x002: "Check bad moves",
        0x004: "Try to faint",
        0x008: "Check viability",
        0x010: "Setup first turn",
        0x020: "Risky",
        0x040: "Prefer strongest",
        0x080: "Prefer status",
        0x100: "Risky (advanced)",
        0x200: "Weather",
        0x400: "Trapping",
        0x800: "Expert",
        0x1000: "Double battle",
        0x2000: "HP aware",
        0x4000: "Unknown (0x4000)",
        0x8000: "Roaming",
    }

    TRPOKE_FORMATS = {
        0: 8,   # base
        1: 16,  # + moves(8)
        2: 10,  # + item(2)
        3: 18,  # + item(2) + moves(8)
    }

    # # decode_encounters


    def bootstrap_text(self, narc_files):
        """Gen V: decrypt all text files, fingerprint to identify tables."""
        from xoleon import decode_gen5_text
        for i, f in enumerate(narc_files):
            self.text_tables[i] = decode_gen5_text(f)
        self._auto_detect_tables()

    def decode_personal(self, data, file_idx, text_tables, tm_table=None):
        """Decode Gen V personal data (76 bytes). BW/B2W2."""
        if len(data) < 76 or data == b'\x00' * len(data):
            return None
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

        # Gen V: 3 items, gender at 0x12, abilities 3x u8 at 0x18-0x1A
        items = [struct.unpack_from('<h', data, 0x0C + i * 2)[0] for i in range(3)]
        gender = data[0x12]
        hatch_cycles = data[0x13]
        base_happiness = data[0x14]
        exp_growth = data[0x15]
        egg1, egg2 = data[0x16], data[0x17]

        ability_names = []
        for i in range(3):
            aid = data[0x18 + i]
            if aid > 0:
                name = ability_list[aid] if aid < len(ability_list) else f"ability#{aid}"
                ability_names.append(f"{name} (Hidden)" if i == 2 else name)

        forme_count = data[0x20] if len(data) > 0x20 else 1
        height_dm = struct.unpack_from('<H', data, 0x24)[0]
        weight_hg = struct.unpack_from('<H', data, 0x26)[0]

        species_name = species_list[file_idx] if file_idx < len(species_list) else f"#{file_idx}"
        t1 = type_list[type1] if type1 < len(type_list) else f"type#{type1}"
        t2 = type_list[type2] if type2 < len(type_list) else f"type#{type2}"
        types_str = t1 if type1 == type2 else f"{t1} / {t2}"

        def _lbl(prefix, val):
            for k in dir(self):
                if k.startswith(prefix) and getattr(_SDK, k) == val:
                    return k[len(prefix):].replace('_', ' ').title()
            return f"#{val}"

        held_parts = []
        for label, item_id in zip(['common', 'rare', 'hidden'], items):
            if item_id > 0:
                iname = item_list[item_id] if item_id < len(item_list) else f"item#{item_id}"
                held_parts.append(f"{iname} ({label})")

        out = [f"{species_name} (#{file_idx})", f"{types_str} | BST {bst}",
               f"HP {hp} | Atk {atk} | Def {dfn} | SpA {spa} | SpD {spd} | Spe {spe}",
               f"Abilities: {' / '.join(ability_names)}" if ability_names else "Abilities: ---"]
        out.append(f"Gender: {_lbl('GENDER_', gender)} | Catch Rate: {catch_rate} | Hatch: {hatch_cycles} cycles | Happiness: {base_happiness}")
        out.append(f"Growth: {_lbl('GROWTH_', exp_growth)} | Egg Groups: {_lbl('EGG_', egg1)}" +
                   (f" / {_lbl('EGG_', egg2)}" if egg1 != egg2 else ""))
        if held_parts:
            out.append(f"Held Items: {' / '.join(held_parts)}")
        if evs:
            out.append(f"EVs: {', '.join(evs)}")
        out.append(f"Height: {height_dm / 10.0}m | Weight: {weight_hg / 10.0}kg")
        if forme_count > 1:
            out.append(f"Forms: {forme_count}")

        # TM flags at 0x28 (16 bytes = 128 bits)
        if tm_table and len(data) >= 0x38:
            tm_flags = data[0x28:0x38]
            tms, hms = [], []
            for bit_idx, (label, move_id) in enumerate(tm_table):
                if tm_flags[bit_idx // 8] & (1 << (bit_idx % 8)):
                    move_name = moves_list[move_id] if move_id < len(moves_list) else f"move#{move_id}"
                    (hms if label.startswith('HM') else tms).append(f"{label[2:]} {move_name}")
            if tms: out.append(f"TM: {' / '.join(tms)}")
            if hms: out.append(f"HM: {' / '.join(hms)}")

        return "\n".join(out)

    def learnset_moves(self, data):
        """Raw learnset for reverse lookup: [(level, move_id)]. u16 move + u16 level, ends FFFFFFFF."""
        out = []
        for i in range(0, len(data) - 3, 4):
            m, lv = struct.unpack_from('<HH', data, i)
            if m == 0xFFFF and lv == 0xFFFF: break
            out.append((lv, m))
        return out

    def decode_learnset(self, data, file_idx, text_tables, **kwargs):
        """Decode Gen V+ learnset: (move_id u16, level u16) pairs, terminated by FFFFFFFF."""
        if len(data) < 4:
            return None
        species_list = text_tables.get('species', [])
        moves_list = text_tables.get('moves', [])
        species_name = species_list[file_idx] if file_idx < len(species_list) else f"#{file_idx}"

        moves = []
        for i in range(0, len(data) - 3, 4):
            move_id = struct.unpack_from('<H', data, i)[0]
            level = struct.unpack_from('<H', data, i + 2)[0]
            if move_id == 0xFFFF and level == 0xFFFF:
                break
            move_name = moves_list[move_id] if move_id < len(moves_list) else f"move#{move_id}"
            moves.append((level, move_name))

        lines = [f"{species_name} (#{file_idx}) — Learnset"]
        for level, move_name in moves:
            lines.append(f"  Lv{level:<4}{move_name}")
        if not moves:
            lines.append("  (none)")
        return "\n".join(lines)

    ZONE_HEADER_PATH = 'a/0/1/2'

    def _enc_locations(self):
        m = getattr(self, '_enc_loc_map', None)
        if m is not None: return m
        z = self.get_narc(self.ZONE_HEADER_PATH).files[0]
        m = {}
        for i in range(len(z) // 48):
            if z[i * 48 + 0x14] != 0xFF: m.setdefault(z[i * 48 + 0x14], struct.unpack_from('<H', z, i * 48 + 0x1A)[0] & 0x3FF)
        self._enc_loc_map = m
        return m

    def decode_encounters(self, data, file_idx=0, text_tables=None, **kwargs):
        if len(data) < 232 or len(data) % 232: return []
        locs = (text_tables or self.text_tables).get('location_names', [])
        li = self._enc_locations().get(file_idx)
        loc = locs[li] if li is not None and li < len(locs) else f'Zone {file_idx}'
        seasons = len(data) // 232
        if all(data[s * 232:(s + 1) * 232] == data[:232] for s in range(seasons)): seasons = 1
        out = []
        for s in range(seasons):
            b = s * 232
            tag = f" ({('Spring', 'Summer', 'Autumn', 'Winter')[s]})" if seasons > 1 else ''
            for area, off, n, ri in (('Grass', 8, 12, 0), ('Dark Grass', 56, 12, 1), ('Shaking Grass', 104, 12, 2), ('Surf', 152, 5, 3),
                                     ('Rippling Surf', 172, 5, 4), ('Fishing', 192, 5, 5), ('Rippling Fishing', 212, 5, 6)):
                if data[b + ri]:
                    for i in range(n):
                        raw, mn, mx = struct.unpack_from('<HBB', data, b + off + i * 4)
                        if raw & 0x7FF: out.append((f'{loc} {area}{tag}', raw & 0x7FF, raw >> 11, mn, mx, {'location': loc, 'method': area, 'period': ('Spring', 'Summer', 'Autumn', 'Winter')[s] if seasons > 1 else ''}))
        return out
    FLIPNOTE_PAIRS = {
        # Gen V
        'Pokémon Black & White': ['IRB', 'IRA'],
        'Pokémon Black & White 2': ['IRE', 'IRD'],
    }


    TM_SEARCH = {
        5: (bytes([0xD4, 0x01, 0x51, 0x01, 0xD9, 0x01, 0x5B, 0x01]), 101),  # 95 TMs + 6 HMs
    }


    FORM_NAMES = {
        (351, 1): "Sunny", (351, 2): "Rainy", (351, 3): "Snowy",
        (386, 1): "Attack", (386, 2): "Defense", (386, 3): "Speed",
        (412, 0): "Plant", (412, 1): "Sandy", (412, 2): "Trash",
        (413, 0): "Plant", (413, 1): "Sandy", (413, 2): "Trash",
        (421, 1): "Sunshine",
        (422, 0): "West", (422, 1): "East",
        (423, 0): "West", (423, 1): "East",
        (479, 1): "Heat", (479, 2): "Wash", (479, 3): "Frost", (479, 4): "Fan", (479, 5): "Mow",
        (487, 1): "Origin",
        (492, 1): "Sky",
        (550, 0): "Red-Striped", (550, 1): "Blue-Striped",
        (555, 0): "Standard", (555, 1): "Zen Mode",
        (585, 0): "Spring", (585, 1): "Summer", (585, 2): "Autumn", (585, 3): "Winter",
        (586, 0): "Spring", (586, 1): "Summer", (586, 2): "Autumn", (586, 3): "Winter",
        (641, 1): "Therian", (642, 1): "Therian", (645, 1): "Therian",
        (646, 1): "White", (646, 2): "Black",
        (647, 1): "Resolute",
        (648, 1): "Pirouette",
    }

    def get_ability_from_personal(self, species_id, ability_slot, text_tables):
        """Resolve ability slot to ability name via personal data."""
        ability_list = text_tables.get('abilities', [])
        try:
            personal_path = getattr(self, 'PERSONAL_PATH', '')
            if not personal_path:
                return f"ability_slot_{ability_slot}"
            personal_narc = self.get_narc(personal_path)
            if species_id >= len(personal_narc.files):
                return f"ability_slot_{ability_slot}"
            pd = personal_narc.files[species_id]
            # Gen V: abilities at 0x18, 0x19, 0x1A (3 slots)
            if len(pd) < 0x1B:
                return f"ability_slot_{ability_slot}"
            aid = pd[0x18 + min(ability_slot, 2)]
            return ability_list[aid] if aid < len(ability_list) else f"ability#{aid}"
        except Exception:
            return f"ability_slot_{ability_slot}"

    def decode_trpoke(self, data, file_idx=0, text_tables=None, trainer_data=None, **kwargs) -> dict:
        """Decode Gen V TRPoke. 8B base: iv(u8) ability_gender(u8) level(u8) pad(u8) species(u16) form(u16)."""
        if len(data) == 0:
            return {"pokemon": []}

        species_list = text_tables.get('species', [])
        moves_list = text_tables.get('moves', [])
        items_list = text_tables.get('items', [])

        formats = getattr(self, 'TRPOKE_FORMATS', {})
        template = 0
        if trainer_data and len(trainer_data) >= 1:
            template = trainer_data[0] & 0x03

        pokemon_size = formats.get(template, formats[0])
        num_pokemon = len(data) // pokemon_size
        GENDER_SYM = {1: '\u2642', 2: '\u2640'}

        pokemon = []
        for i in range(num_pokemon):
            off = i * pokemon_size
            if off + pokemon_size > len(data):
                break

            difficulty = data[off]
            ability_gender = data[off + 1]
            level = data[off + 2]
            species_id = struct.unpack_from('<H', data, off + 4)[0]
            form = struct.unpack_from('<H', data, off + 6)[0]

            ability_slot = (ability_gender >> 4) & 0xF
            gender_val = ability_gender & 0xF
            species_name = species_list[species_id] if species_id < len(species_list) else f"#{species_id}"
            if form: species_name += f" (Form {form})"
            ability_name = self.get_ability_from_personal(species_id, ability_slot, text_tables)
            gender = GENDER_SYM.get(gender_val, '')
            ivs = difficulty * 31 // 255 if difficulty <= 255 else 31
            base_size = 8

            entry = {
                "species": species_name,
                "species_id": species_id,
                "level": level,
                "ability": ability_name,
                "gender": gender,
                "ivs": ivs,
                "form": form,
            }

            if template & 2:
                item_id = struct.unpack_from('<H', data, off + base_size)[0]
                item_name = items_list[item_id] if item_id < len(items_list) else f"item#{item_id}"
                entry["held_item"] = item_name if item_id > 0 else "None"

            if template & 1:
                move_off = off + base_size + (2 if template & 2 else 0)
                moves = []
                for m in range(4):
                    mid = struct.unpack_from('<H', data, move_off + m * 2)[0]
                    if mid > 0:
                        moves.append(moves_list[mid] if mid < len(moves_list) else f"move#{mid}")
                entry["moves"] = moves

            pokemon.append(entry)

        return {"template": template, "count": num_pokemon, "pokemon": pokemon}

    def decode_trainer(self, data, file_idx, text_tables):
        """Decode Gen V trainer. trdata=20B, trpoke=8B base per pokemon."""
        if len(data) < 16:
            return None

        trainer_names = text_tables.get('trainer_names', [])
        trainer_classes = text_tables.get('trainer_classes', [])
        items_list = text_tables.get('items', [])

        flags = data[0]
        trainer_class = data[1]
        battle_type = data[2]
        num_pokemon = data[3]

        battle_items = []
        for i in range(4):
            item_id = struct.unpack_from('<H', data, 4 + i * 2)[0]
            if item_id > 0:
                name = items_list[item_id] if item_id < len(items_list) else f"item#{item_id}"
                battle_items.append(name)

        ai_flags_raw = struct.unpack_from('<I', data, 12)[0]
        ai_flags = self.decode_ai_flags(ai_flags_raw)
        class_name = trainer_classes[trainer_class] if trainer_class < len(trainer_classes) else f"class#{trainer_class}"
        prize_money_base = data[17] if len(data) > 17 else 0

        # Resolve trainer name (with rival injection)
        _RIVAL_NAMES = {145: "Hugh"}
        if trainer_class in _RIVAL_NAMES:
            name = _RIVAL_NAMES[trainer_class]
        elif file_idx is not None and file_idx < len(trainer_names):
            name = trainer_names[file_idx].strip() or f"Trainer #{file_idx}"
        else:
            name = f"Trainer #{file_idx}"

        # Location from bootstrap (gym leaders, league)
        location = None
        for indices, loc in getattr(self, '_gym_locations', ()):
            if file_idx in indices:
                location = loc
                break
        if location is None and file_idx in getattr(self, '_league_indices', set()):
            location = "Pokémon League"

        # Mode + battle type from bootstrap (B2W2 challenge mode, first/rematch)
        paren_parts = []
        challenge_start = getattr(self, '_challenge_start', None)
        if challenge_start is not None:
            paren_parts.append('Challenge Mode' if file_idx >= challenge_start else 'Normal Mode')
        if file_idx in getattr(self, '_rematch_indices', set()):
            paren_parts.append('Rematch')
        elif file_idx in getattr(self, '_initial_indices', set()):
            paren_parts.append('First Battle')
        paren = f" ({', '.join(paren_parts)})" if paren_parts else ""

        if location:
            lines = [f"{class_name} {name}{paren} | {location}"]
        else:
            lines = [f"{class_name} {name}{paren}"]
        lines.append('')

        # Fetch trpoke — team block
        highest_level = 0
        try:
            trpoke_path = getattr(self, 'TRPOKE_PATH', '')
            if trpoke_path:
                trpoke_data = self.read_file(f"{trpoke_path}:{file_idx}")
                team = self.decode_trpoke(trpoke_data, text_tables, data)
                if team and team.get('pokemon'):
                    lines.append('Team:')
                    for pk in team['pokemon']:
                        lv = pk['level']
                        if lv > highest_level:
                            highest_level = lv
                        gender = f" {pk['gender']}" if pk.get('gender') else ''
                        held = pk.get('held_item', 'None')
                        held_str = f"  [{held}]" if held and held != 'None' else ''
                        lines.append(f"{pk['species']}{gender} (Lv. {lv}){held_str}")

                        if pk.get('ability'):
                            lines.append(f"Ability: {pk['ability']}")

                        iv = pk.get('ivs', '?')
                        lines.append(f"IVs: {iv} HP / {iv} Atk / {iv} Def / {iv} SpA / {iv} SpD / {iv} Spe")

                        if pk.get('moves'):
                            lines.append(' / '.join(pk['moves']))

                        lines.append('')
        except Exception:
            pass

        # Footer
        footer = []
        if prize_money_base and highest_level:
            prize = prize_money_base * 4 * highest_level
            footer.append(f"Prize: \u00a5{prize:,}")
        if battle_items:
            footer.append(f"Items Used in Battle: {', '.join(battle_items)}")
        if footer:
            lines.append(' | '.join(footer))
        lines.append(f"AI: {ai_flags}")

        return '\n'.join(lines)

    def _format_encounter_gen5(self, decoded, file_idx):
        """Format Gen V encounter data as template text."""
        seasons_data = decoded.get('seasons', None)
        if seasons_data:
            return self._format_encounter_gen5_seasonal(seasons_data, file_idx)

        lines = []
        location = decoded.get('location', '')
        if location:
            lines.append(f"Location: {location}\n")

        sections = [
            ('grass', 'Grass (Default)', self.GRASS_SLOT_RATES),
            ('double_grass', 'Dark Grass', self.GRASS_SLOT_RATES),
            ('special_grass', 'Shaking Grass', self.GRASS_SLOT_RATES),
            ('surf', 'Surf (Default)', self.WATER_SLOT_RATES),
            ('special_surf', 'Rippling Water', self.WATER_SLOT_RATES),
            ('fishing', 'Fishing (Default)', self.WATER_SLOT_RATES),
            ('special_fishing', 'Fishing (Rippling)', self.WATER_SLOT_RATES),
        ]
        for key, header, rates in sections:
            entries = decoded.get(key, [])
            if entries:
                section = self._format_section(entries, rates, header)
                if section:
                    lines.append(section)

        return "\n".join(lines).strip() if lines else None



    def _format_encounter_gen5_seasonal(self, seasons, file_idx):
        """Format Gen V seasonal encounters with inline season notes."""
        section_types = [
            ('grass', 'Grass (Default)', self.GRASS_SLOT_RATES),
            ('double_grass', 'Dark Grass', self.GRASS_SLOT_RATES),
            ('special_grass', 'Shaking Grass', self.GRASS_SLOT_RATES),
            ('surf', 'Surf (Default)', self.WATER_SLOT_RATES),
            ('special_surf', 'Rippling Water', self.WATER_SLOT_RATES),
            ('fishing', 'Fishing (Default)', self.WATER_SLOT_RATES),
            ('special_fishing', 'Fishing (Rippling)', self.WATER_SLOT_RATES),
        ]
        season_names = ['Spring', 'Summer', 'Fall', 'Winter']
        lines = []
        location = seasons[0].get('location', '') if seasons else ''
        if location:
            lines.append(f"Location: {location}\n")

        for key, header, rates in section_types:
            season_consolidated = []
            has_data = False
            for s in seasons:
                entries = s.get(key, [])
                if entries:
                    has_data = True
                    season_consolidated.append(_consolidate_slots(entries, rates))
                else:
                    season_consolidated.append([])
            if not has_data:
                continue
            all_species = set()
            for sc in season_consolidated:
                for e in sc:
                    all_species.add(e['species'])
            species_info = []
            for sp in all_species:
                season_rates = []
                all_levels = set()
                for si, sc in enumerate(season_consolidated):
                    rate = 0
                    for e in sc:
                        if e['species'] == sp:
                            rate = e['rate']
                            lv = e['level'].replace('Lv', '')
                            if '-' in lv:
                                lo, hi = lv.split('-')
                                all_levels.update(range(int(lo), int(hi) + 1))
                            else:
                                all_levels.add(int(lv))
                            break
                    season_rates.append(rate)
                levels = sorted(all_levels)
                lv = f"Lv{levels[0]}" if len(levels) <= 1 else f"Lv{levels[0]}-{levels[-1]}"
                if all(r == season_rates[0] for r in season_rates):
                    rate_str = f"{season_rates[0]}%"
                else:
                    rate_groups = {}
                    for i, rate in enumerate(season_rates):
                        if rate > 0 and i < len(season_names):
                            rate_groups.setdefault(rate, []).append(season_names[i])
                    parts = []
                    for rate, snames in sorted(rate_groups.items(), reverse=True):
                        parts.append(f"{rate}% ({', '.join(snames)})")
                    rate_str = " / ".join(parts)
                species_info.append({'species': sp, 'rate_str': rate_str, 'level': lv, 'sort_key': max(season_rates)})
            species_info.sort(key=lambda x: -x['sort_key'])
            lines.append(f"\n{header}:")
            for si in species_info:
                lv = si['level'].replace('Lv', 'Lv. ')
                lines.append(f"  {si['species']:<20}{lv:<12}{si['rate_str']}")

        return "\n".join(lines).strip() if lines else None

    def discover_enc_loc(self, rom, enc_path):
        """Gen 5: enc->loc via species fingerprinting + story-progression formula.
        loc = enc + C0 - N where C0 = loc_anchor - enc_anchor."""
        import ndspy.narc as _n
        try:
            enc_narc = _n.NARC(rom.getFileByName(enc_path))
        except Exception:
            return {}

        def gsp(f):
            sp, lv = set(), 99
            for j in range(12):
                p = 8 + j * 4
                if p + 4 <= len(f):
                    s = struct.unpack_from('<H', f, p)[0] & 0x7FF
                    if s: sp.add(s); lv = min(lv, f[p + 2])
            return sp, lv

        A = [(frozenset([504, 509]),  15,  4,  7),
             (frozenset([504, 506]), 14,  0,  5),
             (frozenset([39, 505, 507]), 14, 50, 99),
             (frozenset([193,505,507,509,520,523]),16,10,99),
             (frozenset([504, 509]), 124, 0,  4),
             (frozenset([55,183,337,338,591]),127,35,55),
             (frozenset([592, 458, 223]), 126, 0, 99)]

        C = {frozenset([524,527]):53, frozenset([525,527,610]):37, frozenset([524,527,447]):54,
             frozenset([605,607]):56, frozenset([536,616,618]):57, frozenset([536,618]):57,
             frozenset([532,546]):33, frozenset([551,557]):34, frozenset([551,562]):35,
             frozenset([532,533]):38, frozenset([619,622]):39,     frozenset([42,354]):133,
             frozenset([325,326,451]):132, frozenset([525,632]):137, frozenset([19,41,88]):129}

        enc_map, fsp = {}, {}
        anchors = []
        for i, f in enumerate(enc_narc.files):
            if len(f) < 232: continue
            sp, lv = gsp(f)
            if not sp: continue
            fsp[i] = (sp, lv)
            for fp, loc, lo, hi in A:
                if fp.issubset(sp) and lo <= lv <= hi:
                    anchors.append((i, loc)); break
            else:
                for csp, cloc in C.items():
                    if csp.issubset(sp): enc_map[i] = cloc; break

        anchors.sort()
        for ai, aloc in anchors:
            enc_map[ai] = aloc

        for idx, (enc_a, loc_a) in enumerate(anchors):
            enc_b = anchors[idx + 1][0] if idx + 1 < len(anchors) else len(enc_narc.files)
            C0, N = loc_a - enc_a, 0
            for e in range(enc_a, enc_b):
                if e in enc_map and e != enc_a: N += 1; continue
                pl = e + C0 - N
                if (14 <= pl <= 31) or (93 <= pl <= 128): enc_map[e] = pl
                elif e not in fsp: N += 1
                else: N += 1

        return enc_map

    def decode_item(self, data, file_idx, text_tables):
        """Decode item data (0x24 / 36 bytes). Gen V through LGPE share this layout."""
        if len(data) < 0x24:
            return None

        items_list = text_tables.get('items', [])
        desc_list = text_tables.get('item_descriptions', [])

        name = items_list[file_idx] if file_idx < len(items_list) else f'Item #{file_idx}'
        description = desc_list[file_idx] if file_idx < len(desc_list) else ''

        raw_price = struct.unpack_from('<H', data, 0x00)[0]
        buy = raw_price * 10
        sell = raw_price * 5

        held_effect = data[0x02]
        held_arg = data[0x03]
        fling_effect = data[0x05]
        fling_power = data[0x06]
        natural_gift_power = data[0x07]

        packed = struct.unpack_from('<H', data, 0x08)[0]
        pocket = (packed >> 7) & 0xF

        field_effect = data[0x0A]
        battle_effect = data[0x0B]
        consumable = data[0x0E]
        sort_index = data[0x0F]

        cure_inflict = data[0x10]

        # Stat boosts packed in nibbles (0x11-0x14)
        boost0, boost1, boost2, boost3 = data[0x11], data[0x12], data[0x13], data[0x14]
        boosts = {
            'Atk': boost0 >> 4, 'Def': boost1 & 0xF,
            'SpA': boost1 >> 4, 'SpD': boost2 & 0xF,
            'Spe': boost2 >> 4, 'Acc': boost3 & 0xF,
            'Crit': (boost3 >> 4) & 3,
        }

        # EV yields (signed bytes, 0x17-0x1C)
        ev_names = ['HP', 'Atk', 'Def', 'Spe', 'SpA', 'SpD']
        evs = [struct.unpack_from('<b', data, 0x17 + i)[0] for i in range(6)]

        heal_amount = data[0x1D]
        pp_gain = data[0x1E]
        friendship = [struct.unpack_from('<b', data, 0x1F + i)[0] for i in range(3)]

        POCKET_NAMES = {1: 'Items', 2: 'Medicine', 3: 'TMs', 4: 'Berries', 5: 'Key Items', 6: 'Battle Items', 7: 'Poké Balls'}
        pocket_name = POCKET_NAMES.get(pocket, f'pocket#{pocket}')

        out = [name]
        out.append(f'Pocket: {pocket_name}')
        if buy > 0:
            out.append(f'Buy: ${buy:,} | Sell: ${sell:,}')
        else:
            out.append('Cannot be bought')

        if fling_power:
            out.append(f'Fling: {fling_power} power (effect {fling_effect})')
        if natural_gift_power:
            ng_type = packed & 0x1F
            out.append(f'Natural Gift: {natural_gift_power} power, type {ng_type}')

        if held_effect:
            out.append(f'Held effect: {held_effect} (arg {held_arg})')

        active_boosts = {k: v for k, v in boosts.items() if v}
        if active_boosts:
            parts = [f'{k}+{v}' for k, v in active_boosts.items()]
            out.append(f'Boosts: {", ".join(parts)}')

        active_evs = [(ev_names[i], evs[i]) for i in range(6) if evs[i]]
        if active_evs:
            parts = [f'{n}{v:+d}' for n, v in active_evs]
            out.append(f'EVs: {", ".join(parts)}')

        if heal_amount:
            out.append(f'Heal: {heal_amount}')
        if pp_gain:
            out.append(f'PP restore: {pp_gain}')

        active_friend = [f for f in friendship if f]

        if active_friend:
            out.append(f'Friendship: {"/".join(str(f) for f in friendship)}')

        if description:
            out.append('')
            out.append(description)

        return "\n".join(out)

    POKEATHLON_PATH = None
    BABY_SPECIES_PATH = None

 