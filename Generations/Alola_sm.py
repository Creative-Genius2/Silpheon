"""Alola_sm.py: Sun/Moon — Gen VII structural baseline.

Inherits Hoenn_remake.
Gen VII: Z-Moves, Alolan forms, 802 species, Mini/BinLinkerAccessor containers.
"""
from Hoenn_remake import Hoenn_remake

import struct


class Alola_sm(Hoenn_remake):
    """Sun/Moon. Gen VII baseline."""

    GAME_CODES = ('1Q1', '1Q2')
    TITLES = ('Pokémon Sun', 'Pokémon Moon')
    YEAR = 2016

    GEN = 7
    EVO_SLOT_SIZE = 8
    VERSION_PARAMS = (30, 31)  # SN, MN
    EVO_LEVEL_VERSION = 36
    EVO_LEVEL_DAY_VERSION = 37
    EVO_LEVEL_NIGHT_VERSION = 38
    EVO_LEVEL_SUMMIT = 39
    EVO_LEVEL_DUSK = 40
    EVO_LEVEL_WORMHOLE = 41
    EVO_USE_ITEM_WORMHOLE = 42

    SPECIES_COUNT = 802

    # Text: 9 languages (10 GARCs — ja has kana + kanji) at a/0/3/0 through a/0/3/9
    TEXT_LANG_BASE = 'a/0/3/'
    TEXT_LANG_FIRST = 0
    LANGUAGES = ('ja', 'ja-kanji', 'en', 'fr', 'it', 'de', 'es', 'ko', 'zh-Hans', 'zh-Hant')
    TEXT_PATH = 'a/0/3/2'
    PERSONAL_PATH = 'a/0/1/7'
    LEARNSET_PATH = 'a/0/1/3'
    EVOLUTION_PATH = 'a/0/1/4'
    EGG_MOVES_PATH = 'a/0/1/2'
    BABY_SPECIES_PATH = 'a/0/1/8'
    ITEM_PATH = 'a/0/1/9'
    TRAINER_PATH = 'a/1/0/2'
    TRPOKE_PATH = 'a/1/0/3'
    MOVE_DATA_PATH = 'a/0/1/1'

    # ── Text table indices (shared SM/USUM) ──


    FLIPNOTE_PAIRS = {
        'Pokémon Sun & Moon': ['1Q1', '1Q2'],
    }

    def bootstrap_text(self, narc_files):
        """Gen VII: same cipher as Gen V, with PUA→CJK fix for Chinese."""
        super().bootstrap_text(narc_files)
        lang = getattr(self, '_lang', 'en')
        if lang in ('zh-Hans', 'zh-Hant'):
            table = PUA_HANS_TABLE if lang == 'zh-Hans' else PUA_HANT_TABLE
            for idx in self.text_tables:
                self.text_tables[idx] = [s.translate(table) for s in self.text_tables[idx]]

    @staticmethod
    def _unpack_mini(data, ident="EA"):
        """Unpack a Mini/BinLinkerAccessor container. Returns list of byte arrays."""
        if not data or len(data) < 4:
            return None
        if chr(data[0]) != ident[0] or chr(data[1]) != ident[1]:
            return None
        count = struct.unpack_from('<H', data, 2)[0]
        if len(data) < 4 + (count + 1) * 4:
            return None
        ctr = 4
        start = struct.unpack_from('<I', data, ctr)[0]; ctr += 4
        entries = []
        for i in range(count):
            end = struct.unpack_from('<I', data, ctr)[0]; ctr += 4
            length = end - start
            entries.append(data[start:start + length])
            start = end
        return entries

    def _parse_encounter_table(self, t):
        """Parse a single 0x164-byte Gen VII encounter table."""
        if not t or len(t) < 0x164:
            return None
        min_level = t[0]
        max_level = t[1]
        if min_level == 0 and max_level == 0:
            return None
        rates = list(t[2:12])
        slot_sets = []
        for i in range(8):
            slots = []
            ofs = 0x0C + (i * 40)
            for j in range(10):
                val = struct.unpack_from('<I', t, ofs + j * 4)[0]
                species = val & 0x7FF
                form = (val >> 11) & 0x1F
                slots.append((species, form))
            slot_sets.append(slots)
        sos_weather = []
        for i in range(6):
            val = struct.unpack_from('<I', t, 0x14C + i * 4)[0]
            species = val & 0x7FF
            form = (val >> 11) & 0x1F
            sos_weather.append((species, form))
        return {
            'min_level': min_level, 'max_level': max_level,
            'rates': rates, 'slot_sets': slot_sets, 'sos_weather': sos_weather,
        }


    def decode_personal(self, data, file_idx, text_tables, tm_table=None):
        """Decode Gen VII personal data (0x54 bytes). SM/USUM."""
        if len(data) < 0x54 or data == b'\x00' * len(data):
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

        items = [struct.unpack_from('<h', data, 0x0C + i * 2)[0] for i in range(3)]
        gender = data[0x12]
        hatch_cycles = data[0x13]
        base_happiness = data[0x14]
        exp_growth = data[0x15]
        egg1, egg2 = data[0x16], data[0x17]

        # Gen VII: abilities are u8 (same as Gen VI)
        ability_names = []
        for i in range(3):
            aid = data[0x18 + i]
            if aid > 0:
                name = ability_list[aid] if aid < len(ability_list) else f"ability#{aid}"
                ability_names.append(f"{name} (Hidden)" if i == 2 else name)

        forme_count = data[0x20]
        form_stats_idx = struct.unpack_from('<H', data, 0x1C)[0]
        base_exp = struct.unpack_from('<H', data, 0x22)[0]
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
        out.append(f"Height: {height_dm / 10.0}m | Weight: {weight_hg / 10.0}kg | Base EXP: {base_exp}")
        if forme_count > 1:
            out.append(f"Forms: {forme_count} (base index {form_stats_idx})")

        # TM/HM compatibility (128 bits at 0x28)
        if tm_table and len(data) >= 0x38:
            tm_flags = data[0x28:0x38]
            tms, hms = [], []
            for bit_idx, (label, move_id) in enumerate(tm_table):
                if tm_flags[bit_idx // 8] & (1 << (bit_idx % 8)):
                    move_name = moves_list[move_id] if move_id < len(moves_list) else f"move#{move_id}"
                    (hms if label.startswith('HM') else tms).append(f"{label[2:]} {move_name}")
            if tms: out.append(f"TM: {' / '.join(tms)}")
            if hms: out.append(f"HM: {' / '.join(hms)}")

        # Z-Move signature (SM/USUM specific)
        z_item = struct.unpack_from('<H', data, 0x4C)[0]
        z_base = struct.unpack_from('<H', data, 0x4E)[0]
        z_move = struct.unpack_from('<H', data, 0x50)[0]
        if z_item > 0:
            z_item_name = item_list[z_item] if z_item < len(item_list) else f"item#{z_item}"
            z_base_name = moves_list[z_base] if z_base < len(moves_list) else f"move#{z_base}"
            z_move_name = moves_list[z_move] if z_move < len(moves_list) else f"move#{z_move}"
            out.append(f"Z-Move: {z_item_name} + {z_base_name} -> {z_move_name}")

        # Regional form flag
        if data[0x52]:
            out.append("Regional Form: Yes (Alolan)")

        return "\n".join(out)


    def decode_trainer(self, data, file_idx, text_tables):
        """Decode Gen VII trainer. trdata=0x14 bytes, trpoke=0x20 per pokemon."""
        if len(data) < 0x14:
            return None

        trainer_names = text_tables.get('trainer_names', [])
        trainer_classes = text_tables.get('trainer_classes', [])
        items_list = text_tables.get('items', [])
        species_list = text_tables.get('species', [])
        moves_list = text_tables.get('moves', [])
        natures_list = text_tables.get('natures', [])

        BATTLE_MODES = {0: "Single", 1: "Double", 2: "Multi"}
        GENDER_SYM = {1: ' \u2642', 2: ' \u2640'}

        tr_class = struct.unpack_from('<H', data, 0x00)[0]
        battle_mode = data[0x02]
        num_pokemon = data[0x03]
        battle_items = []
        for i in range(4):
            item_id = struct.unpack_from('<H', data, 0x04 + i * 2)[0]
            if item_id > 0:
                name = items_list[item_id] if item_id < len(items_list) else f"item#{item_id}"
                battle_items.append(name)
        ai_raw = data[0x0C]
        AI_FLAGS_7 = {0: 'Basic', 1: 'Strong', 2: 'Expert', 3: 'Doubles',
                      4: 'No Whiteout', 5: 'Battle Royal', 6: 'Switches Pok\u00e9mon'}
        ai_names = [v for b, v in AI_FLAGS_7.items() if ai_raw & (1 << b)]
        ai_str = ', '.join(ai_names) if ai_names else 'None'
        uses_items = bool(ai_raw & (1 << 7))
        money = data[0x11]

        class_name = trainer_classes[tr_class] if tr_class < len(trainer_classes) else f"class#{tr_class}"
        if file_idx is not None and file_idx < len(trainer_names):
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

        # Mode + battle type from bootstrap
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
                if trpoke_data and len(trpoke_data) >= num_pokemon * 0x20:
                    lines.append('Team:')
                    for p in range(num_pokemon):
                        pk = trpoke_data[p * 0x20:(p + 1) * 0x20]
                        gender_val = pk[0] & 0x3
                        ability_slot = (pk[0] >> 4) & 3
                        nature_id = pk[1]
                        evs = list(pk[2:8])
                        iv32 = struct.unpack_from('<I', pk, 0x08)[0]
                        ivs = [(iv32 >> (s * 5)) & 0x1F for s in range(6)]
                        shiny = bool((iv32 >> 30) & 1)
                        level = pk[0x0E]
                        if level > highest_level:
                            highest_level = level
                        species_id = struct.unpack_from('<H', pk, 0x10)[0]
                        form = pk[0x12]
                        held_item = struct.unpack_from('<H', pk, 0x14)[0]
                        move_ids = [struct.unpack_from('<H', pk, 0x18 + m * 2)[0] for m in range(4)]

                        sp_name = species_list[species_id] if species_id < len(species_list) else f"#{species_id}"
                        if form: sp_name += f" (Form {form})"
                        gender = GENDER_SYM.get(gender_val, '')
                        held_str = ''
                        if held_item:
                            hi_name = items_list[held_item] if held_item < len(items_list) else f"item#{held_item}"
                            held_str = f"  [{hi_name}]"
                        shiny_str = '  \u2728' if shiny else ''
                        lines.append(f"{sp_name}{gender} (Lv. {level}){held_str}{shiny_str}")

                        nat_name = natures_list[nature_id] if nature_id < len(natures_list) else f"nature#{nature_id}"
                        lines.append(f"{nat_name} Nature")

                        stat_names = ['HP', 'Atk', 'Def', 'SpA', 'SpD', 'Spe']
                        ev_parts = [f"{evs[i]} {stat_names[i]}" for i in range(6) if evs[i] > 0]
                        if ev_parts:
                            lines.append(f"EVs: {' / '.join(ev_parts)}")
                        iv_parts = [f"{ivs[i]} {stat_names[i]}" for i in range(6)]
                        lines.append(f"IVs: {' / '.join(iv_parts)}")

                        move_names = []
                        for mid in move_ids:
                            if mid == 0: continue
                            move_names.append(moves_list[mid] if mid < len(moves_list) else f"move#{mid}")
                        if move_names:
                            lines.append(' / '.join(move_names))

                        lines.append('')
        except Exception:
            pass

        # Footer — prize + items + AI
        footer = []
        if money and highest_level:
            prize = money * 4 * highest_level
            footer.append(f"Prize: \u00a5{prize:,}")
        if battle_items and uses_items:
            footer.append(f"Items Used in Battle: {', '.join(battle_items)}")
        if footer:
            lines.append(' | '.join(footer))
        lines.append(f"AI: {ai_str}")

        return '\n'.join(lines)

    ZONE_DATA_PATH = 'a/0/7/7'
    WORLD_DATA_PATH = 'a/0/8/9'

    def _enc_locations(self):
        m = getattr(self, '_enc_loc_map', None)
        if m is not None: return m
        from xoleon import decompress_lz11
        zf = self.get_narc(self.ZONE_DATA_PATH).files
        zd = zf[0]
        if zd[:1] == b'\x11': zd = decompress_lz11(zd)
        wd_raw = zf[1]  # u16 per zone -> world index
        nz = len(zd) // 0x54
        worlds_garc = self.get_narc(self.WORLD_DATA_PATH).files
        m = {}
        for i in range(nz):
            loc = struct.unpack_from('<I', zd, i * 0x54 + 0x1C)[0]
            wi = struct.unpack_from('<H', wd_raw, i * 2)[0]
            if wi >= len(worlds_garc): continue
            w = worlds_garc[wi]
            if w[:1] == b'\x11': w = decompress_lz11(w)
            entries = self._unpack_mini(w, 'WD')
            if not entries: continue
            w0 = entries[0]
            mofs = struct.unpack_from('<I', w0, 0x08)[0]
            for o in range(mofs, len(w0) - 3, 4):
                if struct.unpack_from('<H', w0, o)[0] == i:
                    area = struct.unpack_from('<H', w0, o + 2)[0]
                    if area not in m: m[area] = loc
                    break
        self._enc_loc_map = m
        return m

    def decode_encounters(self, data, file_idx=0, text_tables=None, **kwargs):
        if file_idx % 11 != 9 or not data: return []
        if data[0] == 0x11:
            from xoleon import decompress_lz11
            data = decompress_lz11(data)
        locs = (text_tables or self.text_tables).get('location_names', [])
        loc_idx = self._enc_locations().get(file_idx // 11)
        loc = locs[loc_idx] if loc_idx is not None and loc_idx < len(locs) and locs[loc_idx] and locs[loc_idx] != 'Mystery Zone' else f'Area {file_idx // 11}'
        out = []
        for j, e in enumerate(Alola_sm._unpack_mini(data, 'EA') or []):
            for tod, s in (('Day', 4), ('Night', 4 + 0x164)):
                t = self._parse_encounter_table(e[s:s + 0x164])
                if not t: continue
                for area, slots in (('', t['slot_sets'][0]), (' SOS', [x for ss in t['slot_sets'][1:] for x in ss] + t['sos_weather'])):
                    for sp, fm in dict.fromkeys(slots):
                        if sp: out.append((f'{loc} Table {j + 1} ({tod}){area}', sp, fm, t['min_level'], t['max_level'], {'location': loc, 'method': 'SOS' if area else 'Wild', 'period': tod}))
        return out

    @staticmethod
    def format_encounter_gen7(decoded, file_idx, name_resolver=None):
        """Format Gen VII encounter data as readable text."""
        if not decoded or 'tables' not in decoded:
            return None

        def resolve(species_id, form):
            if species_id == 0: return None
            if name_resolver: return name_resolver(species_id, form)
            suffix = f" (Form {form})" if form else ""
            return f"#{species_id}{suffix}"

        lines = []
        tables = decoded['tables']
        for t_idx, tbl in enumerate(tables):
            if len(tables) > 1:
                lines.append(f"\nTable {t_idx + 1}:")
            for time_key, label in [('day', 'Day'), ('night', 'Night')]:
                table = tbl.get(time_key)
                if not table: continue
                rates = table['rates']
                slots = table['slot_sets'][0]
                min_lv = table['min_level']
                max_lv = table['max_level']
                lv_str = f"Lv. {min_lv}-{max_lv}" if min_lv != max_lv else f"Lv. {min_lv}"
                combined = {}
                for i, (sp, fm) in enumerate(slots):
                    if sp == 0: continue
                    name = resolve(sp, fm)
                    if not name: continue
                    rate = rates[i] if i < len(rates) else 0
                    if name in combined: combined[name] += rate
                    else: combined[name] = rate
                if not combined: continue
                lines.append(f"\n{label} ({lv_str}):")
                for name, rate in sorted(combined.items(), key=lambda x: -x[1]):
                    lines.append(f"  {name:<22}{rate:>3}%")
                sos_names = []
                for sos_set in table['slot_sets'][1:]:
                    for sp, fm in sos_set:
                        if sp == 0: continue
                        n = resolve(sp, fm)
                        if n and n not in sos_names: sos_names.append(n)
                if sos_names:
                    lines.append(f"  SOS Allies: {', '.join(sos_names)}")
                weather_names = []
                for sp, fm in table['sos_weather']:
                    if sp == 0: continue
                    n = resolve(sp, fm)
                    if n and n not in weather_names: weather_names.append(n)
                if weather_names:
                    lines.append(f"  Weather SOS: {', '.join(weather_names)}")

        return "\n".join(lines).strip() if lines else None

    # ── Clean-name aliases ──
    FORMAT_ENCOUNTER = staticmethod(format_encounter_gen7.__func__)

    MAISON_POKEMON_NORMAL_PATH = None
    MAISON_POKEMON_SUPER_PATH = None
    MAISON_TRAINERS_NORMAL_PATH = None
    MAISON_TRAINERS_SUPER_PATH = None
    MEGA_EVOS_PATH = None
    TRCLASS_PATH = None
    @property
    def ENCOUNTER_PATH(self):
        return 'a/0/8/2' if self.header.get('game_code', '')[-1:] in ('1', 'A') else 'a/0/8/3'


# PUA → CJK translation tables (Gen 7 Chinese text uses Private Use Area codepoints)
# Derived from USUM species text cross-referenced with PLA national dex
_PUA_HANS = '\ue800\ue801\ue802\ue803\ue804\ue805\ue806\ue807\ue808\ue809\ue80a\ue80b\ue80c\ue80d\ue80e\ue80f\ue810\ue811\ue812\ue813\ue814\ue815\ue816\ue817\ue818\ue819\ue81a\ue81b\ue81c\ue81d\ue81e\ue81f\ue820\ue821\ue822\ue823\ue824\ue825\ue826\ue827\ue828\ue829\ue82a\ue82b\ue82c\ue82d\ue82e\ue82f\ue830\ue831\ue832\ue833\ue834\ue835\ue836\ue837\ue838\ue839\ue83a\ue83b\ue83c\ue83d\ue83e\ue83f\ue840\ue841\ue842\ue843\ue844\ue845\ue846\ue847\ue848\ue849\ue84a\ue84b\ue84c\ue84d\ue84e\ue84f\ue850\ue851\ue852\ue853\ue854\ue855\ue856\ue857\ue858\ue859\ue85a\ue85b\ue85c\ue85d\ue85e\ue85f\ue860\ue861\ue862\ue863\ue864\ue865\ue866\ue867\ue868\ue869\ue86a\ue86b\ue86c\ue86d\ue86e\ue86f\ue870\ue871\ue872\ue873\ue874\ue875\ue876\ue877\ue878\ue879\ue87a\ue87b\ue87c\ue87d\ue87e\ue87f\ue880\ue881\ue882\ue883\ue884\ue885\ue886\ue887\ue888\ue889\ue88a\ue88b\ue88c\ue88d\ue88e\ue88f\ue890\ue891\ue892\ue893\ue894\ue895\ue896\ue897\ue898\ue899\ue89a\ue89b\ue89c\ue89d\ue89e\ue89f\ue8a0\ue8a1\ue8a2\ue8a3\ue8a4\ue8a5\ue8a6\ue8a7\ue8a8\ue8a9\ue8aa\ue8ab\ue8ac\ue8ad\ue8ae\ue8af\ue8b0\ue8b1\ue8b2\ue8b3\ue8b4\ue8b5\ue8b6\ue8b7\ue8b8\ue8b9\ue8ba\ue8bb\ue8bc\ue8bd\ue8be\ue8bf\ue8c0\ue8c1\ue8c2\ue8c3\ue8c4\ue8c5\ue8c6\ue8c7\ue8c8\ue8c9\ue8ca\ue8cb\ue8cc\ue8cd\ue8ce\ue8cf\ue8d0\ue8d1\ue8d2\ue8d3\ue8d4\ue8d5\ue8d6\ue8d7\ue8d8\ue8d9\ue8da\ue8db\ue8dc\ue8dd\ue8de\ue8df\ue8e0\ue8e1\ue8e2\ue8e3\ue8e4\ue8e5\ue8e6\ue8e7\ue8e8\ue8e9\ue8ea\ue8eb\ue8ec\ue8ed\ue8ee\ue8ef\ue8f0\ue8f1\ue8f2\ue8f3\ue8f4\ue8f5\ue8f6\ue8f7\ue8f8\ue8f9\ue8fa\ue8fb\ue8fc\ue8fd\ue8fe\ue8ff\ue900\ue901\ue902\ue903\ue904\ue905\ue906\ue907\ue908\ue909\ue90a\ue90b\ue90c\ue90d\ue90e\ue90f\ue910\ue911\ue912\ue913\ue914\ue915\ue916\ue917\ue918\ue919\ue91a\ue91b\ue91c\ue91d\ue91e\ue91f\ue920\ue921\ue922\ue923\ue924\ue925\ue926\ue927\ue928\ue929\ue92a\ue92b\ue92c\ue92d\ue92e\ue92f\ue930\ue931\ue932\ue933\ue934\ue935\ue936\ue937\ue938\ue939\ue93a\ue93b\ue93c\ue93d\ue93e\ue93f\ue940\ue941\ue942\ue943\ue944\ue945\ue946\ue947\ue948\ue949\ue94a\ue94b\ue94c\ue94d\ue94e\ue94f\ue950\ue951\ue952\ue953\ue954\ue955\ue956\ue957\ue958\ue959\ue95a\ue95b\ue95c\ue95d\ue95e\ue95f\ue960\ue961\ue962\ue963\ue964\ue965\ue966\ue967\ue968\ue969\ue96a\ue96b\ue96c\ue96d\ue96e\ue96f\ue970\ue971\ue972\ue973\ue974\ue975\ue976\ue977\ue978\ue979\ue97a\ue97b\ue97c\ue97d\ue97e\ue97f\ue980\ue981\ue982\ue983\ue984\ue985\ue986\ue987\ue988\ue989\ue98a\ue98b\ue98c\ue98d\ue98e\ue98f\ue990\ue991\ue992\ue993\ue994\ue995\ue996\ue997\ue998\ue999\ue99a\ue99b\ue99c\ue99d\ue99e\ue99f\ue9a0\ue9a1\ue9a2\ue9a3\ue9a4\ue9a5\ue9a6\ue9a7\ue9a8\ue9a9\ue9aa\ue9ab\ue9ac\ue9ad\ue9ae\ue9af\ue9b0\ue9b1\ue9b2\ue9b3\ue9b4\ue9b5\ue9b6\ue9b7\ue9b8\ue9b9\ue9ba\ue9bb\ue9bc\ue9bd\ue9be\ue9bf\ue9c0\ue9c1\ue9c2\ue9c3\ue9c4\ue9c5\ue9c6\ue9c7\ue9c8\ue9c9\ue9ca\ue9cb\ue9cc\ue9cd\ue9ce\ue9cf\ue9d0\ue9d1\ue9d2\ue9d3\ue9d4\ue9d5\ue9d6\ue9d7\ue9d8\ue9d9\ue9da\ue9db\ue9dc\ue9dd\ue9de\ue9df\ue9e0\ue9e1\ue9e2\ue9e3\ue9e4\ue9e5\ue9e6\ue9e7\ue9e8\ue9e9\ue9ea\ue9eb\ue9ec\ue9ed\ue9ee\ue9ef\ue9f0\ue9f1\ue9f2\ue9f3\ue9f4\ue9f5\ue9f6\ue9f7\ue9f8\ue9f9\ue9fa\ue9fb\ue9fc\ue9fd\ue9fe\ue9ff\uea00\uea01\uea02\uea03\uea04\uea05\uea06\uea07\uea08\uea09\uea0a\uea0b\uea0c\uea0d\uea0e\uea0f\uea10\uea11\uea12\uea13\uea14\uea15\uea16\uea17\uea18\uea19\uea1a\uea1b\uea1c\uea1d\uea1e\uea1f\uea20\uea21\uea22\uea23\uea24\uea25\uea26\uea27\uea28\uea29\uea2a\uea2b\uea2c\uea2d\uea2e\uea2f\uea30\uea31\uea32\uea33\uea34\uea35\uea36\uea37\uea38\uea39\uea3a\uea3b\uea3c\uea3d\uea3e\uea3f\uea40\uea41\uea42\uea43\uea44\uea45\uea46\uea47\uea48\uea49\uea4a\uea4b\uea4c\uea4d\uea4e\uea4f\uea50\uea51\uea52\uea53\uea54\uea55\uea56\uea57\uea58\uea59\uea5a\uea5b\uea5c\uea5d\uea5e\uea5f\uea60\uea61\uea62\uea63\uea64\uea65\uea66\uea67\uea68\uea69\uea6a\uea6b\uea6c\uea6d\uea6e\uea6f\uea70\uea71\uea72\uea73\uea74\uea75\uea76\uea77\uea78\uea79\uea7a\uea7b\uea7c\uea7d\uea7e\uea7f\uea80\uea81\uea82\uea83\uea84\uea85\uea86\uea87\uea88\uea89\uea8a\uea8b\uea8c\uea8d\uea8e\uea8f\uea90\uea91\uea92\uea93\uea94\uea95\uea96\uea97\uea98\uea99\uea9a\uea9b\uea9c\uea9d\uea9e\uea9f\ueaa0\ueaa1\ueaa2\ueaa3\ueaa4\ueaa5\ueaa6\ueaa7\ueaa8\ueaa9\ueaaa\ueaab\ueaac\ueaad\ueaae\ueaaf\ueab0\ueab1\ueab2\ueab3\ueab4\ueab5\ueab6\ueab7\ueab8\ueab9\ueaba\ueabb\ueabc\ueabd\ueabe\ueabf\ueac0\ueac1\ueac2\ueac3\ueac4\ueac5\ueac6\ueac7\ueac8\ueac9\ueaca\ueacb\ueacc\ueacd\ueace\ueacf\uead0\uead1\uead2\uead3\uead4\uead5\uead6\uead7\uead8\uead9\ueada\ueadb\ueadc\ueadd\ueade\ueadf\ueae0\ueae1\ueae2\ueae3\ueae4\ueae5\ueae6\ueae7\ueae8\ueae9\ueaea\ueaeb\ueaec\ueaed\ueaee\ueaef\ueaf0\ueaf1\ueaf2\ueaf3\ueaf4\ueaf5\ueaf6\ueaf7\ueaf8\ueaf9\ueafa\ueafb\ueafc\ueafd\ueafe\ueaff\ueb00\ueb01\ueb02\ueb03\ueb04\ueb05\ueb06\ueb07\ueb08\ueb09\ueb0a\ueb0b\ueb0c\ueb0d\ueb0e\uee1e\uee1f\uee20\uee21'
_CJK_HANS = '蛋妙蛙种子草花小火龙恐喷杰尼龟卡咪水箭绿毛虫铁甲蛹巴大蝶独角壳针蜂波比鸟拉达烈雀嘴阿柏蛇怪皮丘雷穿山鼠王多兰娜后朗力诺可西六尾九胖丁超音蝠走路臭霸派斯特球摩鲁蛾地三喵猫老鸭哥猴暴蒂狗风速蚊香蝌蚪君泳士凯勇基胡腕豪喇叭芽口呆食玛瑙母毒刺拳石隆岩马焰兽磁合一葱嘟利海狮白泥舌贝鬼通耿催眠貘引梦人钳蟹巨霹雳电顽弹椰树嘎啦飞腿郎快头瓦双犀牛钻吉蔓藤袋墨金鱼星宝魔墙偶天螳螂迷唇姐击罗肯泰鲤普百变伊布边菊化盔镰刀翼急冻闪你哈克幻叶月桂竺葵锯鳄蓝立咕夜鹰芭瓢安圆丝蛛叉字灯笼古然咩羊茸美丽露才皇毽棉长手向日蜻蜓乌沼太阳亮黑暗鸦妖未知图腾果翁麒麟奇榛佛托土弟蝎钢千壶赫狃熊圈熔蜗猪珊瑚炮章桶信使翅戴加象顿Ⅱ惊鹿犬无畏战舞娃奶罐幸福公炎帝幼沙班洛亚凤时木守宫森林蜥蜴稚鸡壮跃狼纹直冲茧狩猎盾粉莲童帽乐河橡实鼻狡猾傲骨燕鸥莉奈朵溜糖雨蘑菇斗笠懒獭过动猿请假居忍面者脱妞吼爆幕下掌朝北优雅勾魂眼那恰姆落正拍负萤甜蔷薇溶吞牙鲨鲸驼煤炭跳噗晃斑颚蚁漠仙歌青绵七夕鼬斩饭匙鳅鲶虾兵螯秤念触摇篮羽丑纳飘浮泡隐怨影诅咒巡灵彷徨热带铃勃梭雪冰护豹珍珠樱空棘爱心哑属艾欧盖固坐祈代希苗台猛曼拿儿狸法师箱蟀勒伦琴含羞苞槌城结贵妇绅蜜女帕兹潜兔随卷耳魅东施铛响坦铜镜钟盆聒噪陆尖咬不良骷荧光霓虹自舔狂远Ｚ由卢席恩骑色霏莱谢米尔宙提主暖炒武刃丸剑探步哨约扒酷冷蚀豆鸽高雉幔庞滚蝙螺钉差搬运匠修建蟾蜍投摔打包保足蜈蚣车轮精根裙野蛮鲈混流氓红倒狒殿滑巾征哭具迭神棺原肋始祖破灰尘索沫栗德单卵细胞造鹅倍四季萌哎呀败轻蜘坚齿组麻鳗宇烛幽晶斧嚏几何敏捷功夫父赤驹劈司令炸雄秃丫首恶燃烧毕云酋迪耶塔赛里狐呱贺掘彩蓓洁能鞘芳芙妮好鱿贼脚铠垃藻臂枪伞咚碎黏钥朽南瓜嗡哲裴格枭狙射炽咆哮虎漾壬笃啄铳少强锹农胜虻鬃弱坏驴仔重挽滴伪睡罩盗着竹疗环智挥猩掷胆噬堡爷参性：银伴陨枕戈谜拟丘磨舵鳞杖璞・鸣哞鳍科莫迦虚吾肌费束辉纸御机夏垒磊砰奥'
_PUA_HANT = '\ueb0f\ueb10\ueb11\ueb12\ueb13\ueb14\ueb15\ueb16\ueb17\ueb18\ueb19\ueb1a\ueb1b\ueb1c\ueb1d\ueb1e\ueb1f\ueb20\ueb21\ueb22\ueb23\ueb24\ueb25\ueb26\ueb27\ueb28\ueb29\ueb2a\ueb2b\ueb2c\ueb2d\ueb2e\ueb2f\ueb30\ueb31\ueb32\ueb33\ueb34\ueb35\ueb36\ueb37\ueb38\ueb39\ueb3a\ueb3b\ueb3c\ueb3d\ueb3e\ueb3f\ueb40\ueb41\ueb42\ueb43\ueb44\ueb45\ueb46\ueb47\ueb48\ueb49\ueb4a\ueb4b\ueb4c\ueb4d\ueb4e\ueb4f\ueb50\ueb51\ueb52\ueb53\ueb54\ueb55\ueb56\ueb57\ueb58\ueb59\ueb5a\ueb5b\ueb5c\ueb5d\ueb5e\ueb5f\ueb60\ueb61\ueb62\ueb63\ueb64\ueb65\ueb66\ueb67\ueb68\ueb69\ueb6a\ueb6b\ueb6c\ueb6d\ueb6e\ueb6f\ueb70\ueb71\ueb72\ueb73\ueb74\ueb75\ueb76\ueb77\ueb78\ueb79\ueb7a\ueb7b\ueb7c\ueb7d\ueb7e\ueb7f\ueb80\ueb81\ueb82\ueb83\ueb84\ueb85\ueb86\ueb87\ueb88\ueb89\ueb8a\ueb8b\ueb8c\ueb8d\ueb8e\ueb8f\ueb90\ueb91\ueb92\ueb93\ueb94\ueb95\ueb96\ueb97\ueb98\ueb99\ueb9a\ueb9b\ueb9c\ueb9d\ueb9e\ueb9f\ueba0\ueba1\ueba2\ueba3\ueba4\ueba5\ueba6\ueba7\ueba8\ueba9\uebaa\uebab\uebac\uebad\uebae\uebaf\uebb0\uebb1\uebb2\uebb3\uebb4\uebb5\uebb6\uebb7\uebb8\uebb9\uebba\uebbb\uebbc\uebbd\uebbe\uebbf\uebc0\uebc1\uebc2\uebc3\uebc4\uebc5\uebc6\uebc7\uebc8\uebc9\uebca\uebcb\uebcc\uebcd\uebce\uebcf\uebd0\uebd1\uebd2\uebd3\uebd4\uebd5\uebd6\uebd7\uebd8\uebd9\uebda\uebdb\uebdc\uebdd\uebde\uebdf\uebe0\uebe1\uebe2\uebe3\uebe4\uebe5\uebe6\uebe7\uebe8\uebe9\uebea\uebeb\uebec\uebed\uebee\uebef\uebf0\uebf1\uebf2\uebf3\uebf4\uebf5\uebf6\uebf7\uebf8\uebf9\uebfa\uebfb\uebfc\uebfd\uebfe\uebff\uec00\uec01\uec02\uec03\uec04\uec05\uec06\uec07\uec08\uec09\uec0a\uec0b\uec0c\uec0d\uec0e\uec0f\uec10\uec11\uec12\uec13\uec14\uec15\uec16\uec17\uec18\uec19\uec1a\uec1b\uec1c\uec1d\uec1e\uec1f\uec20\uec21\uec22\uec23\uec24\uec25\uec26\uec27\uec28\uec29\uec2a\uec2b\uec2c\uec2d\uec2e\uec2f\uec30\uec31\uec32\uec33\uec34\uec35\uec36\uec37\uec38\uec39\uec3a\uec3b\uec3c\uec3d\uec3e\uec3f\uec40\uec41\uec42\uec43\uec44\uec45\uec46\uec47\uec48\uec49\uec4a\uec4b\uec4c\uec4d\uec4e\uec4f\uec50\uec51\uec52\uec53\uec54\uec55\uec56\uec57\uec58\uec59\uec5a\uec5b\uec5c\uec5d\uec5e\uec5f\uec60\uec61\uec62\uec63\uec64\uec65\uec66\uec67\uec68\uec69\uec6a\uec6b\uec6c\uec6d\uec6e\uec6f\uec70\uec71\uec72\uec73\uec74\uec75\uec76\uec77\uec78\uec79\uec7a\uec7b\uec7c\uec7d\uec7e\uec7f\uec80\uec81\uec82\uec83\uec84\uec85\uec86\uec87\uec88\uec89\uec8a\uec8b\uec8c\uec8d\uec8e\uec8f\uec90\uec91\uec92\uec93\uec94\uec95\uec96\uec97\uec98\uec99\uec9a\uec9b\uec9c\uec9d\uec9e\uec9f\ueca0\ueca1\ueca2\ueca3\ueca4\ueca5\ueca6\ueca7\ueca8\ueca9\uecaa\uecab\uecac\uecad\uecae\uecaf\uecb0\uecb1\uecb2\uecb3\uecb4\uecb5\uecb6\uecb7\uecb8\uecb9\uecba\uecbb\uecbc\uecbd\uecbe\uecbf\uecc0\uecc1\uecc2\uecc3\uecc4\uecc5\uecc6\uecc7\uecc8\uecc9\uecca\ueccb\ueccc\ueccd\uecce\ueccf\uecd0\uecd1\uecd2\uecd3\uecd4\uecd5\uecd6\uecd7\uecd8\uecd9\uecda\uecdb\uecdc\uecdd\uecde\uecdf\uece0\uece1\uece2\uece3\uece4\uece5\uece6\uece7\uece8\uece9\uecea\ueceb\uecec\ueced\uecee\uecef\uecf0\uecf1\uecf2\uecf3\uecf4\uecf5\uecf6\uecf7\uecf8\uecf9\uecfa\uecfb\uecfc\uecfd\uecfe\uecff\ued00\ued01\ued02\ued03\ued04\ued05\ued06\ued07\ued08\ued09\ued0a\ued0b\ued0c\ued0d\ued0e\ued0f\ued10\ued11\ued12\ued13\ued14\ued15\ued16\ued17\ued18\ued19\ued1a\ued1b\ued1c\ued1d\ued1e\ued1f\ued20\ued21\ued22\ued23\ued24\ued25\ued26\ued27\ued28\ued29\ued2a\ued2b\ued2c\ued2d\ued2e\ued2f\ued30\ued31\ued32\ued33\ued34\ued35\ued36\ued37\ued38\ued39\ued3a\ued3b\ued3c\ued3d\ued3e\ued3f\ued40\ued41\ued42\ued43\ued44\ued45\ued46\ued47\ued48\ued49\ued4a\ued4b\ued4c\ued4d\ued4e\ued4f\ued50\ued51\ued52\ued53\ued54\ued55\ued56\ued57\ued58\ued59\ued5a\ued5b\ued5c\ued5d\ued5e\ued5f\ued60\ued61\ued62\ued63\ued64\ued65\ued66\ued67\ued68\ued69\ued6a\ued6b\ued6c\ued6d\ued6e\ued6f\ued70\ued71\ued72\ued73\ued74\ued75\ued76\ued77\ued78\ued79\ued7a\ued7b\ued7c\ued7d\ued7e\ued7f\ued80\ued81\ued82\ued83\ued84\ued85\ued86\ued87\ued88\ued89\ued8a\ued8b\ued8c\ued8d\ued8e\ued8f\ued90\ued91\ued92\ued93\ued94\ued95\ued96\ued97\ued98\ued99\ued9a\ued9b\ued9c\ued9d\ued9e\ued9f\ueda0\ueda1\ueda2\ueda3\ueda4\ueda5\ueda6\ueda7\ueda8\ueda9\uedaa\uedab\uedac\uedad\uedae\uedaf\uedb0\uedb1\uedb2\uedb3\uedb4\uedb5\uedb6\uedb7\uedb8\uedb9\uedba\uedbb\uedbc\uedbd\uedbe\uedbf\uedc0\uedc1\uedc2\uedc3\uedc4\uedc5\uedc6\uedc7\uedc8\uedc9\uedca\uedcb\uedcc\uedcd\uedce\uedcf\uedd0\uedd1\uedd2\uedd3\uedd4\uedd5\uedd6\uedd7\uedd8\uedd9\uedda\ueddb\ueddc\ueddd\uedde\ueddf\uede0\uede1\uede2\uede3\uede4\uede5\uede6\uede7\uede8\uede9\uedea\uedeb\uedec\ueded\uedee\uedef\uedf0\uedf1\uedf2\uedf3\uedf4\uedf5\uedf6\uedf7\uedf8\uedf9\uedfa\uedfb\uedfc\uedfd\uedfe\uedff\uee00\uee01\uee02\uee03\uee04\uee05\uee06\uee08\uee09\uee0a\uee0b\uee0c\uee0d\uee0e\uee0f\uee10\uee11\uee12\uee13\uee14\uee15\uee16\uee17\uee18\uee19\uee1a\uee1b\uee1c\uee1d\uee22\uee23\uee24\uee25\uee26Ｑ'
_CJK_HANT = '蛋妙蛙種子草花小火龍恐噴傑尼龜卡咪水箭綠毛蟲鐵甲蛹巴大蝶獨角殼針蜂波比鳥拉達烈雀嘴阿柏蛇怪皮丘雷穿山鼠王多蘭娜后朗力諾可西六尾九胖丁超音蝠走路臭霸派斯特球摩魯蛾地三喵貓老鴨哥猴爆蒂狗風速蚊香蝌蚪君泳士凱勇基胡腕豪喇叭芽口呆食瑪瑙母毒刺拳石隆岩馬焰獸磁合一蔥嘟利海獅白泥舌貝鬼通耿催眠貘引夢人鉗蟹巨霹靂電頑彈椰樹嘎啦飛腿郎快頭瓦雙犀牛鑽吉蔓藤袋墨金魚星寶魔牆偶天螳螂迷唇姐擊羅肯泰鯉暴普百變伊布邊菊化盔鐮刀翼急凍閃你哈克幻葉月桂竺葵鋸鱷藍立咕夜鷹芭瓢安圓絲蛛叉字燈籠古然咩羊茸美麗露才皇毽棉長手向日蜻蜓烏沼太陽亮黑暗鴉妖未知圖騰果翁麒麟奇榛佛托土弟蠍鋼千壺赫狃熊圈熔蝸豬珊瑚炮章桶信使翅戴加象頓Ⅱ驚鹿犬無畏戰舞娃奶罐幸福公炎帝幼沙班洛亞鳳時木守宮森林蜥蜴稚雞壯躍狼紋直衝繭狩獵盾粉蓮童帽樂河橡實鼻狡猾傲骨燕鷗莉奈朵溜糖雨蘑菇斗笠懶獺過動猿請假居忍面者脫妞吼幕下掌朝北優雅勾魂眼那恰姆落正拍負螢甜薔薇溶吞牙鯊鯨駝煤炭跳噗晃斑顎蟻漠仙歌青綿七夕鼬斬飯匙鰍鯰蝦兵螯秤念觸搖籃羽醜納飄浮泡隱怨影詛咒巡靈彷徨熱帶鈴勃梭雪冰護豹珍珠櫻空棘愛心啞屬艾歐蓋固坐祈代希苗台猛曼拿兒狸法師箱蟀勒倫琴含羞苞槌城結貴婦紳蜜女帕茲潛兔隨捲耳魅東施鐺響坦銅鏡鐘盆聒噪陸尖咬不良骷光霓虹自舔狂遠Ｚ由盧席恩騎色霏萊謝米爾宙提主暖炒武刃丸劍探步哨約扒酷冷蝕豆鴿高雉幔龐滾蝙螺釘差搬運匠修建蟾蜍投摔打包保足蜈蚣車輪毬精根裙野蠻鱸混流氓紅倒狒殿滑巾徵哭具死神棺原肋始祖破灰塵索沫栗德單卵細胞造鵝倍四季萌哎呀敗輕蜘堅齒組麻鰻宇燭幽晶斧嚏幾何敏捷功夫父赤駒劈司令炸雄禿丫首惡燃燒畢雲酋迪耶塔賽里狐呱賀掘彩蓓潔能鞘芳芙妮好魷賊腳鎧垃藻臂槍傘咚碎黏鑰朽南瓜嗡哲裴格梟狙射熾咆哮虎漾壬篤啄銃少強鍬農勝虻鬃弱壞驢仔重挽滴偽睡罩盜著竹療環智揮猩擲膽噬堡爺參性：銀伴隕枕戈謎擬磨舵鱗杖璞・鳴哞鰭科莫迦虛吾肌費束輝紙御機夏壘磊砰丑奧Ｑ'
PUA_HANS_TABLE = str.maketrans(_PUA_HANS, _CJK_HANS)
PUA_HANT_TABLE = str.maketrans(_PUA_HANT, _CJK_HANT)
