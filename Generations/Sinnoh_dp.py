"""Sinnoh_dp.py: Diamond/Pearl — Gen IV structural baseline.

Inherits Hoenn_rse. Gen IV jump: NDS platform, NARC filesystem,
text encryption (XOR cipher + 9-bit packing), 493 species,
physical/special split per move, online play.
"""
from Hoenn_rse import Hoenn_rse
import struct
from xoleon import decode_gen4_text


class Sinnoh_dp(Hoenn_rse):
    """Diamond/Pearl. Gen IV baseline."""

    GAME_CODES = ('ADA', 'APA')
    TITLES = ('Pokémon Diamond', 'Pokémon Pearl')
    YEAR = 2007

    PLATFORM = 'Nintendo DS'
    GEN = 4
    CONTAINER = 'nds'

    SPECIES_COUNT = 493

    TEXT_PATH = 'msgdata/msg.narc'
    PERSONAL_PATH = 'poketool/personal/personal.narc'
    LEARNSET_PATH = 'poketool/personal/wotbl.narc'
    EVOLUTION_PATH = 'poketool/personal/evo.narc'
    BABY_SPECIES_PATH = 'poketool/personal/pms.narc'
    MOVE_DATA_PATH = 'poketool/waza/waza_tbl.narc'
    TRAINER_PATH = 'poketool/trainer/trdata.narc'
    TRPOKE_PATH = 'poketool/trainer/trpoke.narc'
    ITEM_PATH = 'itemtool/itemdata/item_data.narc'
    CONTEST_PATH = 'contest/data/contest_data.narc'
    BATTLE_TOWER_POKEMON_PATH = 'battle/b_tower/btdpm.narc'
    BATTLE_TOWER_TRAINERS_PATH = 'battle/b_tower/btdtr.narc'
    ENCOUNTER_PATH_D = 'fielddata/encountdata/d_enc_data.narc'
    ENCOUNTER_PATH_P = 'fielddata/encountdata/p_enc_data.narc'

    PERSONAL_SIZE = 44
    MOVE_DATA_SIZE = 16
    EVOLUTION_SIZE = 44

    def iter_encounters(self):
        enc = getattr(self, 'ENCOUNTER_PATH', None)
        if not enc:
            gc = self.header.get('game_code', '')
            enc = self.ENCOUNTER_PATH_D if gc.startswith('AD') else getattr(self, 'ENCOUNTER_PATH_P', self.ENCOUNTER_PATH_D)
        if not enc: return []
        out = []
        for fi, f in enumerate(self.get_narc(enc).files):
            r = self.decode_encounters(f, fi, self.text_tables)
            if isinstance(r, list): out.extend(t[:5] + ({**t[5], 'path': f'{enc}:{fi}'},) for t in r)
        return out
    GRASS_SLOT_RATES = (20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1)
    WATER_SLOT_RATES = (60, 30, 5, 4, 1)



    AI_FLAGS = {
        0x001: "Basic AI",
        0x002: "Check bad moves",
        0x004: "Try to faint",
        0x008: "Check viability",
        0x010: "Setup first turn",
        0x020: "Risky",
        0x040: "Prefer strongest",
        0x080: "Prefer status",
        0x100: "Weather",
        0x200: "Trapping",
        0x400: "Unknown (0x400)",
        0x800: "Unknown (0x800)",
        0x1000: "Unknown (0x1000)",
        0x2000: "Unknown (0x2000)",
        0x4000: "Unknown (0x4000)",
        0x8000: "Unknown (0x8000)",
    }

    TRPOKE_FORMATS = {
        0: 6,   # base
        1: 14,  # + moves(8)
        2: 8,   # + item(2)
        3: 18,  # + item(2) + moves(8) + pad(2)
    }
    def get_narc(self, narc_path):
        import ndspy.narc
        key = narc_path
        if key not in self._narc_cache:
            data = self.rom.getFileByName(narc_path)
            self._narc_cache[key] = ndspy.narc.NARC(data)
        return self._narc_cache[key]

    def read_file(self, path):
        p = path.strip('/')
        if p.lower() == 'arm9.bin':
            return bytes(self.arm9_data)
        if p.lower() == 'arm7.bin':
            return bytes(self.arm7_data)
        # Overlay: overlay/overlay_XXXX.bin or ovN
        if 'overlay' in p.lower() or p.startswith('ov'):
            import re
            m = re.search(r'(\d+)', p)
            if m:
                ov_id = int(m.group(1))
                if ov_id in self.overlays:
                    return bytes(self.overlays[ov_id])
                raise ValueError(f"Overlay {ov_id} not found")
        if ':' in p:
            narc_path, file_idx = p.rsplit(':', 1)
            file_idx = int(file_idx)
            narc = self.get_narc(narc_path.lstrip('/'))
            if file_idx >= len(narc.files):
                raise ValueError(f"Index {file_idx} out of range (NARC has {len(narc.files)} files)")
            return bytes(narc.files[file_idx])
        return bytes(self.rom.getFileByName(p))

    def bootstrap_text(self, narc_files):
        """Gen IV: each file has its own seed. decode_gen4_text handles it."""
        from xoleon import decode_gen4_text
        for i, f in enumerate(narc_files):
            self.text_tables[i] = decode_gen4_text(f)
        self._auto_detect_tables()

    def decode_personal(self, data, file_idx, text_tables, tm_table=None):
        """Decode Gen IV personal data (44 bytes). DP/Pt/HGSS."""
        if len(data) < 44 or data == b'\x00' * len(data):
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

        # Gen IV: 2 items, gender at 0x10, abilities 2x u8 at 0x16-0x17
        items = [struct.unpack_from('<H', data, 0x0C + i * 2)[0] for i in range(2)]
        gender = data[0x10]
        hatch_cycles = data[0x11]
        base_happiness = data[0x12]
        exp_growth = data[0x13]
        egg1, egg2 = data[0x14], data[0x15]
        ability_names = [ability_list[a] if a < len(ability_list) else f"ability#{a}" for a in [data[0x16], data[0x17]] if a > 0]

        species_name = species_list[file_idx] if file_idx < len(species_list) else f"#{file_idx}"
        t1 = type_list[type1] if type1 < len(type_list) else f"type#{type1}"
        t2 = type_list[type2] if type2 < len(type_list) else f"type#{type2}"
        types_str = t1 if type1 == type2 else f"{t1} / {t2}"

        held_parts = []
        for label, item_id in zip(['common', 'rare'], items):
            if item_id > 0:
                iname = item_list[item_id] if item_id < len(item_list) else f"item#{item_id}"
                held_parts.append(f"{iname} ({label})")

        def _lbl(prefix, val):
            for k in dir(self):
                if k.startswith(prefix) and getattr(self, k) == val:
                    return k[len(prefix):].replace('_', ' ').title()
            return f"#{val}"

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

        # TM flags at 0x1C (16 bytes = 128 bits)
        if tm_table and len(data) >= 0x2C:
            tm_flags = data[0x1C:0x2C]
            tms, hms = [], []
            for bit_idx, (label, move_id) in enumerate(tm_table):
                if tm_flags[bit_idx // 8] & (1 << (bit_idx % 8)):
                    move_name = moves_list[move_id] if move_id < len(moves_list) else f"move#{move_id}"
                    (hms if label.startswith('HM') else tms).append(f"{label[2:]} {move_name}")
            if tms: out.append(f"TM: {' / '.join(tms)}")
            if hms: out.append(f"HM: {' / '.join(hms)}")

        return "\n".join(out)

    MAP_HEADER_WILD = (0x0E, '<H', 0xFFFF)
    MAP_HEADER_MUSIC = 10

    def _enc_locations(self):
        m = getattr(self, '_enc_loc_map', None)
        if m is not None: return m
        import struct as st
        a, (wo, wf, none), mo = self.arm9_data, self.MAP_HEADER_WILD, self.MAP_HEADER_MUSIC
        mus = lambda p: 1000 <= st.unpack_from('<H', a, p)[0] <= 1300 and 1000 <= st.unpack_from('<H', a, p + 2)[0] <= 1300
        s = next((s for s in range(0, len(a) - 24 * 30, 4) if all(mus(s + i * 24 + mo) for i in range(30))), None)
        m = {}
        while s is not None and s + 24 <= len(a) and mus(s + mo):
            w = st.unpack_from(wf, a, s + wo)[0]
            if w != none: m.setdefault(w, a[s + 0x12])
            s += 24
        self._enc_loc_map = m
        return m

    def decode_encounters(self, data, file_idx=0, text_tables=None, **kwargs):
        import struct as st
        if len(data) != 424: return []
        locs = (text_tables or self.text_tables).get('location_names', [])
        li = self._enc_locations().get(file_idx)
        loc = locs[li] if li is not None and li < len(locs) else f'Zone {file_idx}'
        out = []
        if st.unpack_from('<I', data, 0)[0]:
            lv = [st.unpack_from('<I', data, 4 + i * 8)[0] for i in range(12)]
            for i in range(12):
                sp = st.unpack_from('<I', data, 8 + i * 8)[0]
                if sp: out.append((f'{loc} Grass', sp, 0, lv[i], lv[i], {'location': loc, 'method': 'Grass'}))
            for area, off, slots in (('Swarm', 100, (0, 1)), ('Day', 108, (2, 3)), ('Night', 116, (2, 3)), ('Radar', 124, (4, 5, 10, 11)),
                                     ('Ruby', 164, (8, 9)), ('Sapphire', 172, (8, 9)), ('Emerald', 180, (8, 9)), ('FireRed', 188, (8, 9)), ('LeafGreen', 196, (8, 9))):
                for k, s in enumerate(slots):
                    sp = st.unpack_from('<I', data, off + k * 4)[0]
                    if sp: out.append((f'{loc} Grass ({area})', sp, 0, lv[s], lv[s], {'location': loc, 'method': 'Grass', ('period' if area in ('Day', 'Night') else 'variant'): area}))
        wo = 204
        for area in ('Surf', 'Surf Special', 'Old Rod', 'Good Rod', 'Super Rod'):
            rate = st.unpack_from('<I', data, wo)[0]; wo += 4
            if rate:
                for i in range(5):
                    mx, mn = data[wo + i*8], data[wo + i*8 + 1]
                    sp = st.unpack_from('<H', data, wo + i*8 + 4)[0]
                    if sp: out.append((f'{loc} {area}', sp, 0, mn, mx, {'location': loc, 'method': area}))
            wo += 40
        return out
    FLIPNOTE_PAIRS = {
        # Gen IV
        'Pokémon Diamond & Pearl': ['ADA', 'APA'],
        'Pokémon Platinum': ['CPU'],
        'Pokémon HeartGold & SoulSilver': ['IPK', 'IPG'],
    }


    TRAINER_LOCATIONS = {
        # Gen IV - Diamond/Pearl
        "ADA": {
            ("Leader", "Roark"): "Oreburgh Gym",
            ("Leader", "Gardenia"): "Eterna Gym",
            ("Leader", "Maylene"): "Veilstone Gym",
            ("Leader", "Crasher Wake"): "Pastoria Gym",
            ("Leader", "Wake"): "Pastoria Gym",
            ("Leader", "Fantina"): "Hearthome Gym",
            ("Leader", "Byron"): "Canalave Gym",
            ("Leader", "Candice"): "Snowpoint Gym",
            ("Leader", "Volkner"): "Sunyshore Gym",
            ("Elite Four", "Aaron"): "Pokémon League",
            ("Elite Four", "Bertha"): "Pokémon League",
            ("Elite Four", "Flint"): "Pokémon League",
            ("Elite Four", "Lucian"): "Pokémon League",
            ("Champion", "Cynthia"): "Pokémon League",
        },
        "APA": "ADA",  # Pearl alias

        # Gen IV - Platinum
        "CPU": {
            ("Leader", "Roark"): "Oreburgh Gym",
            ("Leader", "Gardenia"): "Eterna Gym",
            ("Leader", "Fantina"): "Hearthome Gym",
            ("Leader", "Maylene"): "Veilstone Gym",
            ("Leader", "Crasher Wake"): "Pastoria Gym",
            ("Leader", "Wake"): "Pastoria Gym",
            ("Leader", "Byron"): "Canalave Gym",
            ("Leader", "Candice"): "Snowpoint Gym",
            ("Leader", "Volkner"): "Sunyshore Gym",
            ("Elite Four", "Aaron"): "Pokémon League",
            ("Elite Four", "Bertha"): "Pokémon League",
            ("Elite Four", "Flint"): "Pokémon League",
            ("Elite Four", "Lucian"): "Pokémon League",
            ("Champion", "Cynthia"): "Pokémon League",
            ("Tower Tycoon", "Palmer"): "Battle Tower",
        },

        # Gen IV - HeartGold/SoulSilver
        "IPK": {
            # Johto Gym Leaders
            ("Leader", "Falkner"): "Violet Gym",
            ("Leader", "Bugsy"): "Azalea Gym",
            ("Leader", "Whitney"): "Goldenrod Gym",
            ("Leader", "Morty"): "Ecruteak Gym",
            ("Leader", "Chuck"): "Cianwood Gym",
            ("Leader", "Jasmine"): "Olivine Gym",
            ("Leader", "Pryce"): "Mahogany Gym",
            ("Leader", "Clair"): "Blackthorn Gym",
            # Kanto Gym Leaders (class = name in HGSS)
            ("Leader", "Brock"): "Pewter Gym",
            ("Leader", "Misty"): "Cerulean Gym",
            ("Leader", "Lt. Surge"): "Vermilion Gym",
            ("Leader", "Erika"): "Celadon Gym",
            ("Leader", "Janine"): "Fuchsia Gym",
            ("Leader", "Sabrina"): "Saffron Gym",
            ("Leader", "Blaine"): "Seafoam Gym",
            ("Leader", "Blue"): "Viridian Gym",
            # Elite Four & Champion
            ("Elite Four", "Will"): "Indigo Plateau",
            ("Elite Four", "Koga"): "Indigo Plateau",
            ("Elite Four", "Bruno"): "Indigo Plateau",
            ("Elite Four", "Karen"): "Indigo Plateau",
            ("Champion", "Lance"): "Indigo Plateau",
            # Special
            ("PKMN Trainer", "Red"): "Mt. Silver (Summit)",
        },
        "IPG": "IPK",  # SoulSilver alias
    }


    CLASS_LOCATIONS = {
        "ADA": {"Elite Four": "Pokémon League", "Champion": "Pokémon League"},
        "APA": "ADA",
        "CPU": {"Elite Four": "Pokémon League", "Champion": "Pokémon League", "Tower Tycoon": "Battle Tower"},
        "IPK": {"Elite Four": "Indigo Plateau", "Champion": "Indigo Plateau",
                "Brock": "Pewter Gym", "Misty": "Cerulean Gym", "Lt. Surge": "Vermilion Gym",
                "Erika": "Celadon Gym", "Janine": "Fuchsia Gym", "Sabrina": "Saffron Gym",
                "Blaine": "Seafoam Gym", "Blue": "Viridian Gym"},
        "IPG": "IPK",
    }


    TM_SEARCH = {
        4: (bytes([0x08, 0x01, 0x51, 0x01, 0x60, 0x01, 0x5B, 0x01]), 100),  # 92 TMs + 8 HMs
    }

    def decode_trpoke(self, data, file_idx=0, text_tables=None, trainer_data=None, **kwargs) -> dict:
        """Decode a TRPoke file into human-readable format using text_tables.
        Gen IV: iv(u16) level(u16) species(u16) = 6B base."""
        if len(data) == 0:
            return {"pokemon": []}

        species_list = text_tables.get('species', [])
        moves_list = text_tables.get('moves', [])
        items_list = text_tables.get('items', [])
        natures_list = text_tables.get('natures', [])

        formats = getattr(self, 'TRPOKE_FORMATS', {})

        # Determine template from TRData byte 0 if available
        template = 0
        if trainer_data and len(trainer_data) >= 1:
            template = trainer_data[0] & 0x03
        else:
            # Guess from file size
            for t in [3, 2, 1, 0]:
                if len(data) % formats[t] == 0 and len(data) // formats[t] > 0:
                    template = t
                    break

        pokemon_size = formats.get(template, formats[0])
        num_pokemon = len(data) // pokemon_size

        pokemon = []
        for i in range(num_pokemon):
            off = i * pokemon_size
            if off + pokemon_size > len(data):
                break

            # Gen IV layout: iv(u16) level(u16) species(u16)
            iv_raw = struct.unpack_from('<H', data, off)[0]
            level = struct.unpack_from('<H', data, off + 2)[0]
            species_id = struct.unpack_from('<H', data, off + 4)[0]
            species_name = species_list[species_id] if species_id < len(species_list) else f"#{species_id}"
            ivs = iv_raw * 31 // 255 if iv_raw <= 255 else 31
            base_size = 6

            entry = {
                "species": species_name,
                "species_id": species_id,
                "level": level,
                "ivs": ivs,
            }

            if template & 2:  # Has held item
                item_id = struct.unpack_from('<H', data, off + base_size)[0]
                item_name = items_list[item_id] if item_id < len(items_list) else f"item#{item_id}"
                entry["held_item"] = item_name if item_id > 0 else "None"

            if template & 1:  # Has moves
                move_off = off + base_size + (2 if template & 2 else 0)
                moves = []
                for m in range(4):
                    mid = struct.unpack_from('<H', data, move_off + m * 2)[0]
                    mname = moves_list[mid] if mid < len(moves_list) else f"move#{mid}"
                    moves.append(mname if mid > 0 else "---")
                entry["moves"] = moves

            pokemon.append(entry)

        return {"template": template, "count": num_pokemon, "pokemon": pokemon, "raw": data.hex()}



    def decode_trainer(self, data, file_idx, text_tables):
        """Decode trainer: reads trdata, fetches matching trpoke, returns formatted string.
        16B = Gen IV (flags, class, battle_type, npoke, items×4, ai_flags)
        20B = Gen V  (+ pad, prize_base, area_id, pad)"""
        if len(data) < 16:
            return None

        trainer_names = text_tables.get('trainer_names', [])
        trainer_classes = text_tables.get('trainer_classes', [])
        items_list = text_tables.get('items', [])

        BATTLE_TYPES = {0: "Single", 1: "Double", 2: "Triple", 3: "Rotation"}

        flags = data[0]
        trainer_class = data[1]
        battle_type = data[2]
        num_pokemon = data[3]
        has_moves = bool(flags & 1)
        has_items = bool(flags & 2)

        battle_items = []
        for i in range(4):
            item_id = struct.unpack_from('<H', data, 4 + i * 2)[0]
            if item_id > 0:
                item_name = items_list[item_id] if item_id < len(items_list) else f"item#{item_id}"
                battle_items.append(item_name)

        ai_flags_raw = struct.unpack_from('<I', data, 12)[0]
        ai_flags = self.decode_ai_flags(ai_flags_raw)
        class_name = trainer_classes[trainer_class] if trainer_class < len(trainer_classes) else f"class#{trainer_class}"

        prize_money_base = data[17] if len(data) > 17 else 0

        # Resolve trainer name
        _RIVAL_NAMES_16B = {
            23: "Silver", 95: "Barry", 96: "Barry",
        }
        if len(data) < 20 and trainer_class in _RIVAL_NAMES_16B:
            name = _RIVAL_NAMES_16B[trainer_class]
        elif file_idx is not None and file_idx < len(trainer_names):
            name = trainer_names[file_idx].strip() or f"Trainer #{file_idx}"
        else:
            name = f"Trainer #{file_idx}"

        lines = [f"{class_name} {name} (#{file_idx})"]
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
                        held = pk.get('held_item', 'None')
                        held_str = f"  [{held}]" if held and held != 'None' else ''
                        lines.append(f"{pk['species']} (Lv. {lv}){held_str}")
                        iv = pk.get('ivs', '?')
                        lines.append(f"IVs: {iv} HP / {iv} Atk / {iv} Def / {iv} SpA / {iv} SpD / {iv} Spe")
                        if pk.get('moves'):
                            real_moves = [m for m in pk['moves'] if m != '---']
                            if real_moves:
                                lines.append(' / '.join(real_moves))
                        lines.append('')
        except Exception:
            pass

        # Footer — prize + items + AI
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








    def iter_learnsets(self):
        """Back to one NARC file per species (Gen III's pointer table ends here)."""
        return self._iter_narc_learnsets()

    def decode_learnset(self, data, file_idx, text_tables):
        """Decode learnset. All gens: u8 pairs (Gen 1/2), packed u16 (Gen 3/4), paired u16×2 (Gen 5)."""
        if len(data) < 2:
            return None
        species_list = text_tables.get('species', [])
        moves_list = text_tables.get('moves', [])
        species_name = species_list[file_idx] if file_idx < len(species_list) else f"#{file_idx}"

        moves = []
        for i in range(0, len(data) - 1, 2):
            raw = struct.unpack_from('<H', data, i)[0]
            if raw == 0xFFFF or raw == 0: break
            move_id = raw & 0x1FF
            level = (raw >> 9) & 0x7F
            move_name = moves_list[move_id] if move_id < len(moves_list) else f"move#{move_id}"
            moves.append((level, move_name))


        lines = [f"{species_name} (#{file_idx}) — Learnset"]
        for level, move_name in moves:
            lines.append(f"  Lv{level:<4}{move_name}")
        if not moves:
            lines.append("  (none)")
        return "\n".join(lines)




    def decode_evolution(self, data, file_idx, text_tables):
        """Decode evolution data. Uses self.EVO_* constants for gen-correct method IDs."""
        slot_size = getattr(self, 'EVO_SLOT_SIZE', 6)
        slots = 8 if self.GEN >= 6 else 7
        min_size = slot_size * slots
        if len(data) < min_size or data[:min_size] == b'\x00' * min_size:
            return None
        species = text_tables.get('species', [])
        items = text_tables.get('items', [])
        moves = text_tables.get('moves', [])
        types = text_tables.get('type_names', [])
        name = species[file_idx] if file_idx < len(species) else f"#{file_idx}"

        def _lk(table, idx, fb):
            return table[idx] if idx < len(table) else f"{fb}#{idx}"

        def _a(word):
            return f"an {word}" if word[:1].lower() in 'aeiou' else f"a {word}"

        def _evo_name(mid):
            for k in dir(self):
                if k.startswith('EVO_') and getattr(self, k) == mid:
                    return k
            return None

        evo_lines = []
        for i in range(slots):
            off = i * slot_size
            method = struct.unpack_from('<H', data, off)[0]
            param = struct.unpack_from('<H', data, off + 2)[0]
            target = struct.unpack_from('<H', data, off + 4)[0]
            if method == 0 and target == 0:
                continue
            lvl = data[off + 7] if slot_size == 8 else param
            tgt = _lk(species, target, 'species')
            ename = _evo_name(method)
            S = self

            if method == S.EVO_LEVEL_UP:
                line = f"{tgt} at level {lvl}"
            elif method == S.EVO_HAPPINESS:
                line = f"{tgt} when leveled up with high friendship"
            elif method == S.EVO_HAPPINESS_DAY:
                line = f"{tgt} during the day if leveled up with high friendship"
            elif method == S.EVO_HAPPINESS_NIGHT:
                line = f"{tgt} during the night if leveled up with high friendship"
            elif method == S.EVO_TRADE:
                line = f"{tgt} when traded"
            elif method == S.EVO_TRADE_WITH_ITEM:
                line = f"{tgt} when traded while holding {_a(_lk(items, param, 'item'))}"
            elif method == S.EVO_STONE:
                line = f"{tgt} when exposed to {_a(_lk(items, param, 'item'))}"
            elif method == getattr(S, 'EVO_TRADE_FOR_SPECIES', -1):
                line = f"{tgt} when traded for {_lk(species, param, 'species')}"
            elif method == getattr(S, 'EVO_STONE_MALE', -1):
                line = f"{tgt} when exposed to {_a(_lk(items, param, 'item'))} if male"
            elif method == getattr(S, 'EVO_STONE_FEMALE', -1):
                line = f"{tgt} when exposed to {_a(_lk(items, param, 'item'))} if female"
            elif method == getattr(S, 'EVO_HOLD_ITEM_DAY', -1):
                line = f"{tgt} when leveled up while holding {_a(_lk(items, param, 'item'))} during the day"
            elif method == getattr(S, 'EVO_HOLD_ITEM_NIGHT', -1):
                line = f"{tgt} when leveled up while holding {_a(_lk(items, param, 'item'))} during the night"
            elif method == S.EVO_ATK_GT_DEF:
                line = f"{tgt} at level {lvl} if its Attack is higher than its Defense" if lvl else f"{tgt} when its Attack is higher than its Defense"
            elif method == S.EVO_ATK_EQ_DEF:
                line = f"{tgt} at level {lvl} if its Attack and Defense are equal" if lvl else f"{tgt} when its Attack and Defense are equal"
            elif method == S.EVO_ATK_LT_DEF:
                line = f"{tgt} at level {lvl} if its Attack is lower than its Defense" if lvl else f"{tgt} when its Attack is lower than its Defense"
            elif method == S.EVO_PERSONALITY_LO:
                line = f"{tgt} at level {lvl}, at random" if lvl else f"{tgt}, at random"
            elif method == S.EVO_PERSONALITY_HI:
                line = f"{tgt} at level {lvl}, at random" if lvl else f"{tgt}, at random"
            elif method == S.EVO_NINJASK:
                line = f"{tgt} at level {lvl}" if lvl else f"{tgt}"
            elif method == S.EVO_SHEDINJA:
                line = f"{tgt} when Nincada evolves, if there's an empty party slot and a spare Poké Ball"
            elif method == S.EVO_BEAUTY:
                line = f"{tgt} when leveled up with high Beauty"
            elif method == S.EVO_MOVE:
                line = f"{tgt} when leveled up while knowing {_lk(moves, param, 'move')}"
            elif method == S.EVO_PARTY_SPECIES:
                line = f"{tgt} when leveled up with {_lk(species, param, 'species')} in the party"
            elif method == S.EVO_LEVEL_MALE:
                line = f"{tgt} at level {lvl} if male" if lvl else f"{tgt} if male"
            elif method == S.EVO_LEVEL_FEMALE:
                line = f"{tgt} at level {lvl} if female" if lvl else f"{tgt} if female"
            elif method == S.EVO_LEVEL_ELECTRIC:
                line = f"{tgt} when leveled up in a special magnetic field"
            elif method == S.EVO_LEVEL_MOSSY:
                line = f"{tgt} when leveled up near a Moss Rock"
            elif method == S.EVO_LEVEL_ICY:
                line = f"{tgt} when leveled up near an Ice Rock"
            elif method == getattr(S, 'EVO_LEVEL_UPSIDE_DOWN', -1):
                line = f"{tgt} at level {lvl} while holding the console upside-down" if lvl else f"{tgt} while holding the console upside-down"
            elif method == getattr(S, 'EVO_AFFECTION_TYPE', -1):
                tn = _lk(types, param, 'type')
                line = f"{tgt} with high Affection and also knowing {_a(tn)} type move"
            elif method == getattr(S, 'EVO_LEVEL_DARK_PARTY', -1):
                line = f"{tgt} at level {lvl} with a Dark type in the party" if lvl else f"{tgt} when leveled up with a Dark type in the party"
            elif method == getattr(S, 'EVO_LEVEL_RAIN', -1):
                line = f"{tgt} at level {lvl} during rain" if lvl else f"{tgt} during rain"
            elif method == getattr(S, 'EVO_LEVEL_DAY', -1):
                line = f"{tgt} at level {lvl} during the day" if lvl else f"{tgt} during the day"
            elif method == getattr(S, 'EVO_LEVEL_NIGHT', -1):
                line = f"{tgt} at level {lvl} during the night" if lvl else f"{tgt} during the night"
            elif method == getattr(S, 'EVO_LEVEL_FEMALE_SPECIAL', -1):
                line = f"{tgt} at level {lvl} if female" if lvl else f"{tgt} if female"
            elif method == getattr(S, 'EVO_LEVEL_VERSION', -1):
                vp = getattr(S, 'VERSION_PARAMS', ())
                vname = S.TITLES[vp.index(param)] if param in vp else f'version {param}'
                line = f"{tgt} at level {lvl} in {vname}"
            elif method == getattr(S, 'EVO_LEVEL_DAY_VERSION', -1):
                vp = getattr(S, 'VERSION_PARAMS', ())
                vname = S.TITLES[vp.index(param)] if param in vp else f'version {param}'
                line = f"{tgt} at level {lvl} during the day in {vname}"
            elif method == getattr(S, 'EVO_LEVEL_NIGHT_VERSION', -1):
                vp = getattr(S, 'VERSION_PARAMS', ())
                vname = S.TITLES[vp.index(param)] if param in vp else f'version {param}'
                line = f"{tgt} at level {lvl} during the night in {vname}"
            elif method == getattr(S, 'EVO_LEVEL_SUMMIT', -1):
                line = f"{tgt} at the Altar of the Sunne/Moone"
            elif method == getattr(S, 'EVO_LEVEL_DUSK', -1):
                line = f"{tgt} at dusk (Own Tempo)"
            elif method == getattr(S, 'EVO_LEVEL_WORMHOLE', -1):
                line = f"{tgt} in the Ultra Wormhole"
            elif method == getattr(S, 'EVO_USE_ITEM_WORMHOLE', -1):
                line = f"{tgt} using {_lk(items, param, 'item')} in the Ultra Wormhole"
            elif method == getattr(S, 'EVO_CRITICAL_HITS', -1):
                line = f"{tgt} after landing 3 critical hits in one battle"
            elif method == getattr(S, 'EVO_HP_LOST', -1):
                line = f"{tgt} after taking {param}+ damage without fainting"
            elif method == getattr(S, 'EVO_SPIN', -1):
                line = f"{tgt} when spinning while holding a sweet"
            elif method == getattr(S, 'EVO_NATURE_AMPED', -1):
                line = f"{tgt}'s either Amped Forme, or its Low-Key Forme, at level {lvl}, based on the Pokémon's Nature" if lvl else f"{tgt}'s either Amped Forme, or its Low-Key Forme, based on the Pokémon's Nature"
            elif method == getattr(S, 'EVO_NATURE_LOW_KEY', -1):
                continue  # merged into Amped line
            elif method == getattr(S, 'EVO_TOWER_DARKNESS', -1):
                line = f"{tgt} at the Tower of Darkness"
            elif method == getattr(S, 'EVO_TOWER_WATERS', -1):
                line = f"{tgt} at the Tower of Waters"
            elif method == getattr(S, 'EVO_WALK_STEPS_WITH', -1):
                line = f"{tgt} after walking 1000 steps using Let's Go"
            elif method == getattr(S, 'EVO_UNION_CIRCLE', -1):
                line = f"{tgt} while in a Union Circle"
            elif method == getattr(S, 'EVO_BATTLE_EC25', -1):
                line = f"Either into a family of three or four at level {lvl}, at random" if lvl else f"Either into a family of three or four, at random"
            elif method == getattr(S, 'EVO_BATTLE_EC_ELSE', -1):
                continue  # merged into EC25 line
            elif method == getattr(S, 'EVO_COLLECT_999', -1):
                line = f"{tgt} after collecting 999 Gimmighoul Coins"
            elif method == getattr(S, 'EVO_DEFEAT_EQUALS', -1):
                line = f"{tgt} after defeating 3 of the same species holding Leader's Crest"
            elif method == getattr(S, 'EVO_USE_MOVE_SPECIAL', -1):
                line = f"{tgt} after using a specific move 20 times"
            elif method == getattr(S, 'EVO_KNOW_MOVE_EC_ELSE', -1):
                line = f"Either into a two-segment or three-segment form when leveled up while knowing {_lk(moves, param, 'move')}, at random"
            elif method == getattr(S, 'EVO_KNOW_MOVE_EC25', -1):
                continue  # merged into EC_ELSE line
            elif method == getattr(S, 'EVO_RECOIL_DAMAGE_MALE', -1):
                line = f"{tgt} after taking recoil damage (male)"
            elif method == getattr(S, 'EVO_RECOIL_DAMAGE_FEMALE', -1):
                line = f"{tgt} after taking recoil damage if female"
            elif method == getattr(S, 'EVO_HISUI', -1):
                line = f"{tgt} in Pokémon Legends: Arceus"
            elif method == getattr(S, 'EVO_USE_ITEM_FULL_MOON', -1):
                line = f"{tgt} using {_lk(items, param, 'item')} during a full moon"
            elif method == getattr(S, 'EVO_USE_MOVE_AGILE', -1):
                line = f"{tgt} after using a move in Agile Style"
            elif method == getattr(S, 'EVO_USE_MOVE_STRONG', -1):
                line = f"{tgt} after using a move in Strong Style"
            elif method == getattr(S, 'EVO_USE_MOVE_BARB_BARRAGE', -1):
                line = f"{tgt} after using Barb Barrage"
            else:
                label = ename[4:].replace('_', ' ').lower() if ename else f"method {method}"
                line = f"{tgt} via {label}" + (f" (param {param})" if param else "")
            evo_lines.append(f"  {line}")

        if not evo_lines:
            return None
        return f"{name} Evolution Methods\nEvolves into:\n" + "\n".join(evo_lines)

    def decode_move(self, data, file_idx, text_tables):
        """Decode move data. Format detected by size — no gen check needed.
        12B = Gen III, 16B = Gen IV, 36B = Gen V."""
        if data == b'\x00' * len(data):
            return None
        type_list = text_tables.get('type_names', [])
        moves_list = text_tables.get('moves', [])
        move_name = moves_list[file_idx] if file_idx < len(moves_list) else f"move#{file_idx}"

        if len(data) < 16:
            # 12-byte entries: effect(1), power(1), type(1), accuracy(1), pp(1), ...
            move_type = data[2]
            power = data[1]
            accuracy = data[3]
            pp = data[4]
            type_name = type_list[move_type] if move_type < len(type_list) else f"type#{move_type}"
            category = '—'
            extras = []
        elif len(data) < 36:
            # 16-byte entries: category at byte 2 uses Gen IV mapping
            category = {0: 'Status', 1: 'Physical', 2: 'Special'}.get(data[2], f"cat#{data[2]}")
            power = data[3]
            move_type = data[4]
            accuracy = data[5]
            pp = data[6]
            type_name = type_list[move_type] if move_type < len(type_list) else f"type#{move_type}"
            extras = []
        elif len(data) >= 36:
            move_type = data[0]
            category = {0: 'Status', 1: 'Physical', 2: 'Special'}.get(data[2], f"cat#{data[2]}")
            power = data[3]
            accuracy = data[4]
            pp = data[5]
            priority = struct.unpack_from('b', data, 6)[0]
            multi_hit = data[7]
            effect_chance = data[10]
            type_name = type_list[move_type] if move_type < len(type_list) else f"type#{move_type}"
            extras = []
            if priority != 0:
                extras.append(f"{'+' if priority > 0 else ''}{priority} priority")
            if multi_hit > 0:
                lo, hi = multi_hit & 0xF, (multi_hit >> 4) & 0xF
                extras.append(f"{lo}-{hi} hits" if lo != hi else f"{lo} hits")
            if effect_chance > 0:
                extras.append(f"{effect_chance}% effect")
        else:
            return None

        pow_str = f"{power} pow" if power > 0 else "—"
        acc_str = f"{accuracy}%" if accuracy <= 100 else "—"
        line = f"{move_name} (#{file_idx})\n{type_name} | {category} | {pow_str} | {acc_str} | {pp} PP"
        if extras:
            line += f" | {' | '.join(extras)}"
        desc_list = text_tables.get('move_descriptions', [])
        if file_idx < len(desc_list) and desc_list[file_idx]:
            line += f"\n{desc_list[file_idx]}"
        return line



    def decode_item(self, data, file_idx, text_tables):
        """Decode item data. Gen IV: 34 bytes, price direct. Gen V: 36 bytes, price * 10."""
        items_list = text_tables.get('items', [])
        desc_list = text_tables.get('item_descriptions', [])

        name = items_list[file_idx] if file_idx < len(items_list) else f'Item #{file_idx}'
        description = desc_list[file_idx] if file_idx < len(desc_list) else ''

        if len(data) < 10:
            return None

        raw_price = struct.unpack_from('<H', data, 0)[0]
        price = raw_price  # Gen IV: price is direct

        fling_power = data[6] if len(data) > 6 else 0

        lines = [name]
        lines.append("")
        if price > 0:
            lines.append(f"Buy: ${price:,}")
            lines.append(f"Sell: ${price // 2:,}")
        else:
            lines.append("Buy: Not sold in shops")
        if fling_power > 0:
            lines.append(f"Fling Power: {fling_power}")
        if description:
            lines.append("")
            lines.append(description)

        return "\n".join(lines)



    def decode_contest(self, data, file_idx, text_tables):
        """Decode Gen IV Contest data (Diamond/Pearl/Platinum).
        File 0: Contest pokemon data (96 bytes per entry, 80 entries).
        """
        if file_idx != 0 or len(data) < 96:
            return None

        species_list = text_tables.get('species', [])
        moves_list = text_tables.get('moves', [])

        num_entries = len(data) // 96
        lines = ["Contest Hall", "", f"Pokemon: {num_entries}"]

        for i in range(num_entries):
            offset = i * 96
            entry_data = data[offset:offset + 96]

            species_id = struct.unpack_from('<H', entry_data, 8)[0]
            if species_id == 0 or species_id >= len(species_list):
                continue

            species_name = species_list[species_id]
            moves = []
            for m in range(4):
                move_id = struct.unpack_from('<H', entry_data, 12 + m * 2)[0]
                if move_id > 0 and move_id < len(moves_list):
                    moves.append(moves_list[move_id])

            lines.append("")
            lines.append(f"  #{i+1:<4}{species_name}")
            if moves:
                lines.append(f"       {' / '.join(moves)}")

        return "\n".join(lines)


    # ============ Template Formatters ============

    GRASS_SLOT_RATES = [20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1]
    WATER_SLOT_RATES = [60, 30, 5, 4, 1]


    def _consolidate_slots(self, entries, rates):
        """Consolidate species across encounter slots, summing rates."""
        combined = {}
        for i, entry in enumerate(entries):
            name = entry['species']
            rate = rates[i] if i < len(rates) else 0
            if name not in combined:
                combined[name] = {'rate': 0, 'levels': set()}
            combined[name]['rate'] += rate
            lvl_str = str(entry.get('level', 0))
            if '-' in lvl_str:
                lo, hi = lvl_str.split('-')
                combined[name]['levels'].update(range(int(lo), int(hi) + 1))
            else:
                combined[name]['levels'].add(int(lvl_str))
        result = []
        for name, d in sorted(combined.items(), key=lambda x: -x[1]['rate']):
            levels = sorted(d['levels'])
            lv = f"Lv{levels[0]}" if len(levels) <= 1 else f"Lv{levels[0]}-{levels[-1]}"
            result.append({'species': name, 'rate': d['rate'], 'level': lv})
        return result



    def _format_encounter_dpp(self, decoded, file_idx):
        """Format DPPt encounter data as template text."""
        lines = []
        grass = decoded.get('grass', [])
        if grass:
            section = self._format_section(grass, self.GRASS_SLOT_RATES, "Grass (Default)")
            if section:
                lines.append(section)
        for key, label in [('swarm', 'Swarm'), ('day_replacements', 'Day'), ('night_replacements', 'Night'), ('radar', 'Radar')]:
            species = decoded.get(key, [])
            if species:
                names = species if isinstance(species[0], str) else [e['species'] for e in species]
                lines.append(f"\nGrass ({label}):\n  {', '.join(names)}")
        water_sections = [
            ('surf', 'Surf (Default)'), ('surf_special', 'Surf (Special)'),
            ('old_rod', 'Fishing (Old Rod)'), ('good_rod', 'Fishing (Good Rod)'),
            ('super_rod', 'Fishing (Super Rod)'),
        ]
        for key, header in water_sections:
            entries = decoded.get(key, [])
            if entries:
                section = self._format_section(entries, self.WATER_SLOT_RATES, header)
                if section:
                    lines.append(section)
        return "\n".join(lines).strip() if lines else None


