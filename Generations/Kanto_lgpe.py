"""Kanto_lgpe.py: Let’s Go, Pikachu! / Let’s Go, Eevee!

Inherits Alola_usum. First Switch mainline title. Simplified mechanics,
no wild battles (Go-style catching), no held items, no abilities in battle.
Kanto region revisit with Mega Evolution carried forward from Gen VI.
"""
from Alola_usum import Alola_usum

import struct
from leswitch import fb_field, fb_root, fb_table, fb_vector


class Kanto_lgpe(Alola_usum):
    """Let’s Go, Pikachu! / Let’s Go, Eevee!"""

    GAME_CODES = ('GP1', 'GE1')
    TITLE_IDS = (0x010003F003A34000, 0x0100187003A36000)
    TITLES = ("Pokémon: Let’s Go, Pikachu!", "Pokémon: Let’s Go, Eevee!")
    YEAR = 2018

    PLATFORM = 'Nintendo Switch'

    CONTAINER = 'switch'

    SPECIES_COUNT = 809

    # -- Paths (from pkNX GameFileMapping.cs) --
    PERSONAL_PATH = 'bin/pokelib/personal'
    LEARNSET_PATH = 'bin/archive/waza_oboe.gfpak'
    # learnset_moves inherited: gfpak entries are the Gen V u16 move + u16 level pairs

    def iter_learnsets(self):
        """One gfpak entry per personal slot (980), LZ4-packed; leswitch unpacks."""
        if self.learnset_moves is None: return None
        from leswitch import unpack_gfpak
        pak = unpack_gfpak(self.switch_rom.read_file(self.LEARNSET_PATH)) or {}
        return ((i, self.learnset_moves(d)) for i, d in enumerate(pak.values()))
    EVOLUTION_PATH = 'bin/pokelib/evolution'
    MEGA_EVO_PATH = 'bin/pokelib/mega_evolution'
    MOVE_DATA_PATH = 'bin/pokelib/waza/waza_data.bin'
    ITEM_PATH = 'bin/pokelib/item'
    TEXT_PATH = 'bin/message/English/common'
    TEXT_SCRIPT_PATH = 'bin/message/English/script'

    # Switch text: .dat files map to roles by filename (from pkNX TextMapping.cs)
    # Same filenames across all Switch titles (LGPE/SWSH/PLA/SV/ZA)
    TEXT_FILE_MAP = {
        'monsname.dat': 'species',
        'wazaname.dat': 'moves',
        'itemname.dat': 'items',
        'tokusei.dat': 'abilities',
        'seikaku.dat': 'natures',
        'typename.dat': 'type_names',
        'trname.dat': 'trainer_names',
        'trtype.dat': 'trainer_classes',
        'wazainfo.dat': 'move_descriptions',
        'tokuseiinfo.dat': 'ability_descriptions',
        'iteminfo.dat': 'item_descriptions',
        'zkn_form.dat': 'forms',
        'zkn_type.dat': 'species_classifications',
    }

    TRAINER_PATH = 'bin/trainer/trainer_data'
    TRPOKE_PATH = 'bin/trainer/trainer_poke'
    TRAINER_CLASS_PATH = 'bin/trainer/trainer_type'

    # -- Encounters --
    WILD_PATH_P = 'bin/field/param/encount/encount_data_p.bin'
    WILD_PATH_E = 'bin/field/param/encount/encount_data_e.bin'
    STATIC_ENCOUNTER_PATH = 'bin/script_event_data/event_encount.bin'
    GIFT_PATH = 'bin/script_event_data/add_poke.bin'
    TRADE_PATH = 'bin/script_event_data/field_trade_data.bin'
    ZONE_AHTB_PATH = 'bin/field/param/placement/table/ZoneNameHashTable.tbl'
    PLACE_NAME_PATH = 'bin/message/English/common/place_name.dat'
    _DUNGEON_IDX = {
        'r004d': 40, 'r010d': 41, 'r010r': 42, 'r011d': 43,
        'r020d': 44, 'r023d': 45, 't004d': 46, 't005r03': 47, 't009r02': 51,
    }

    # -- Misc --
    SHOP_PATH = 'bin/app/shop/shop_data.bin'

    # Null out inherited DS/3DS paths that don't exist in LGPE
    BABY_SPECIES_PATH = None
    CONTEST_PATH = None
    EGG_MOVES_PATH = None
    ENCOUNTER_PATH = None
    ENCOUNTER_PATH_D = None
    ENCOUNTER_PATH_P = None
    MAISON_POKEMON_NORMAL_PATH = None
    MAISON_POKEMON_SUPER_PATH = None
    MAISON_TRAINERS_NORMAL_PATH = None
    MAISON_TRAINERS_SUPER_PATH = None
    MEGA_EVOS_PATH = None
    POKEATHLON_PATH = None
    PWT_CHAMPIONS_B_PATH = None
    PWT_CHAMPIONS_PATH = None
    PWT_DEFS_PATH = None
    PWT_DOWNLOAD_PATH = None
    PWT_MIX_PATH = None
    PWT_POKEMON_B_PATH = None
    PWT_POKEMON_PATH = None
    PWT_ROSTERS_2_PATH = None
    PWT_ROSTERS_B_PATH = None
    PWT_ROSTERS_PATH = None
    PWT_TRAINERS_2_PATH = None
    PWT_TRAINERS_B_PATH = None
    PWT_TRAINERS_PATH = None
    SUBWAY_POKEMON_PATH = None
    SUBWAY_TRAINERS_PATH = None
    TRCLASS_PATH = None

    # -- Container format --
    LEARNSET_CONTAINER = 'gfpak'
    MOVE_DATA_CONTAINER = 'binlinker'


    def get_narc(self, narc_path):
        key = narc_path
        if key not in self._narc_cache:
            # Switch: list files under path, wrap as narc-like object
            matches = sorted(f for f in self.switch_rom.files if f.startswith(narc_path.rstrip('/') + '/') or f == narc_path)
            class _SwitchNarc:
                pass
            obj = _SwitchNarc()
            obj.files = [self.switch_rom.read_file(m) for m in matches]
            self._narc_cache[key] = obj
        return self._narc_cache[key]

    def read_file(self, path):
        p = path.strip('/')
        if ':' in p:
            folder, fi = p.rsplit(':', 1)
            fi = int(fi)
            narc = self.get_narc(folder.lstrip('/'))
            if len(narc.files) == 1:
                return narc.files[0]  # single container — decoder handles entry index
            if fi >= len(narc.files):
                raise ValueError(f"Index {fi} out of range ({len(narc.files)} files)")
            return narc.files[fi]
        return self.switch_rom.read_file(p)

    # Language code -> folder name (same across all Switch titles)
    LANG_FOLDERS = {
        'ja': 'JPN', 'ja-kanji': 'JPN_KANJI',
        'en': 'English', 'fr': 'French', 'it': 'Italian',
        'de': 'German', 'es': 'Spanish', 'ko': 'Korean',
        'zh-Hans': 'Simp_Chinese', 'zh-Hant': 'Trad_Chinese',
    }

    def text_path_for(self, lang='en'):
        """Swap the language folder name in TEXT_PATH."""
        cur = self.LANG_FOLDERS.get(self._lang or 'en', 'English')
        tgt = self.LANG_FOLDERS.get(lang)
        if not tgt:
            raise ValueError(f"Unknown language '{lang}'. Options: {', '.join(self.LANGUAGES)}")
        return self.TEXT_PATH.replace(cur, tgt)

    def decode_personal(self, data, file_idx, text_tables, tm_table=None):
        """Decode LGPE personal data (0x54 bytes). Same as SM with GoSpecies, reduced TMs."""
        if len(data) < 0x54 or data == b'\x00' * len(data):
            return None
        # Base fields identical to SM — call parent
        result = super().decode_personal(data, file_idx, text_tables, tm_table)
        if result is None:
            return None

        # LGPE-specific: GO species mapping at 0x48
        go_species = struct.unpack_from('<H', data, 0x48)[0]
        if go_species > 0:
            species_list = text_tables.get('species', [])
            go_name = species_list[go_species] if go_species < len(species_list) else f"#{go_species}"
            result += f"\nGO Species: {go_name} (#{go_species})"

        return result

    # ── decode_trainer ──────────────────────────────────────────────
    def decode_trainer(self, data, file_idx, text_tables):
        """Decode LGPE trainer (TrainerData7b 0x17 bytes + fetches TrainerPoke7b).
        Layout from pkNX TrainerData7b.cs: Class(u16 0x00), Mode(0x02),
        NumPoke(0x03), Items(4xu16 0x04), AI(u32 0x0C), Heal(0x10),
        Money(0x11), Gift(u16 0x14), GiftQty(0x16)."""
        if len(data) < 0x17:
            return None

        tr_class = struct.unpack_from('<H', data, 0x00)[0]
        battle_mode = data[0x02]
        num_pokemon = data[0x03]
        items = [struct.unpack_from('<H', data, 0x04 + i*2)[0] for i in range(4)]
        ai = struct.unpack_from('<I', data, 0x0C)[0]
        heal = bool(data[0x10])
        money = data[0x11]
        gift = struct.unpack_from('<H', data, 0x14)[0]
        gift_qty = data[0x16]

        class_list = text_tables.get('trainer_classes', [])
        name_list = text_tables.get('trainer_names', [])
        item_list = text_tables.get('items', [])

        class_name = class_list[tr_class] if tr_class < len(class_list) else f'class#{tr_class}'
        tr_name = name_list[file_idx] if file_idx < len(name_list) else f'#{file_idx}'

        out = [f'{class_name} {tr_name} (#{file_idx})']
        out.append('')

        # Fetch trpoke
        highest_level = 0
        trpoke_path = getattr(self, 'TRPOKE_PATH', None)
        if trpoke_path:
            trpoke_data = self.read_file(f"{trpoke_path}:{file_idx}")
            if trpoke_data:
                team = self.decode_trpoke(trpoke_data, file_idx, text_tables)
                if team and team.get('pokemon'):
                    out.append('Team:')
                    for pk in team['pokemon']:
                        lv = pk['level']
                        if lv > highest_level:
                            highest_level = lv
                        gender = f" {pk['gender']}" if pk.get('gender') else ''
                        held_str = f"  [{pk['held_item']}]" if pk.get('held_item') else ''
                        out.append(f"{pk['species']}{gender} (Lv. {lv}){held_str}")
                        if pk.get('nature'):
                            out.append(f"  {pk['nature']} Nature | Ability: slot {pk['ability_slot']}")
                        if pk.get('moves'):
                            out.append(f"  {' / '.join(pk['moves'])}")
                        out.append(f"  IVs: {pk['ivs']}")
                        if pk.get('evs'):
                            out.append(f"  EVs: {' / '.join(pk['evs'])}")
                        if pk.get('avs'):
                            out.append(f"  AVs: {' / '.join(pk['avs'])}")
                        if pk.get('friendship'):
                            bonus = int(((pk['friendship'] / 255.0 / 10.0) + 1.0) * 100)
                            out.append(f"  Friendship: {pk['friendship']} (stat scale: {bonus}%)")
                        extras = []
                        if pk.get('shiny'): extras.append('Shiny')
                        if pk.get('can_mega'): extras.append(f"Mega (form {pk['mega_form']})")
                        if pk.get('rank'): extras.append(f"Rank {pk['rank']}")
                        if extras:
                            out.append(f"  {' / '.join(extras)}")
                        out.append('')

        # Footer
        mode_str = {0: 'Single', 1: 'Double', 2: 'Triple', 3: 'Rotation'}.get(battle_mode, f'mode#{battle_mode}')
        footer = [f'{mode_str} Battle']
        if money and highest_level: footer.append(f'Prize: \u00a5{money * 4 * highest_level:,}')
        held = [item_list[i] if i and i < len(item_list) else None for i in items]
        held = [h for h in held if h]
        if held: footer.append(f'Items: {", ".join(held)}')
        ai_flags = self.decode_ai_flags(ai)
        if ai_flags: footer.append(f'AI: {ai_flags}')
        if heal: footer.append('Heals')
        if gift:
            gname = item_list[gift] if gift < len(item_list) else f'item#{gift}'
            footer.append(f'Gift: {gname} x{gift_qty}')
        out.append(' | '.join(footer))

        return '\n'.join(out)

    # ── decode_trpoke ──────────────────────────────────────────────
    def decode_trpoke(self, data, file_idx, text_tables):
        """Decode LGPE trainer pokemon (0x28 bytes per entry).
        LGPE-unique: Awakening Values, friendship stat scaling, mega choice."""
        if len(data) < 0x28:
            return {"pokemon": []}

        species_list = text_tables.get('species', [])
        moves_list = text_tables.get('moves', [])
        item_list = text_tables.get('items', [])
        nature_list = text_tables.get('natures', [])

        entry_size = 0x28
        count = len(data) // entry_size
        pokemon = []

        STAT_NAMES = ['HP', 'Atk', 'Def', 'Spe', 'SpA', 'SpD']
        EV_NAMES = ['HP', 'Atk', 'Def', 'SpA', 'SpD', 'Spe']

        for i in range(count):
            e = i * entry_size
            gender = data[e] & 0x3
            ability_slot = (data[e] >> 4) & 0x3
            nature = data[e + 1]
            evs = [data[e + 2 + j] for j in range(6)]
            avs = [data[e + 8 + j] for j in range(6)]
            friendship = data[e + 0x0E]
            rank = data[e + 0x0F]

            iv32 = struct.unpack_from('<I', data, e + 0x10)[0]
            ivs = [(iv32 >> (j*5)) & 0x1F for j in range(6)]
            shiny = bool((iv32 >> 30) & 1)
            can_mega = bool((iv32 >> 31) & 1)

            mega_form = struct.unpack_from('<H', data, e + 0x14)[0]
            level = struct.unpack_from('<H', data, e + 0x16)[0]
            species = struct.unpack_from('<H', data, e + 0x18)[0]
            form = struct.unpack_from('<H', data, e + 0x1A)[0]
            held_item = struct.unpack_from('<H', data, e + 0x1C)[0]
            moves = [struct.unpack_from('<H', data, e + 0x20 + j*2)[0] for j in range(4)]

            sp_name = species_list[species] if species < len(species_list) else f'#{species}'
            if form: sp_name += f'-{form}'
            gender_str = {0: '', 1: '\u2642', 2: '\u2640'}.get(gender, '')
            item_name = item_list[held_item] if held_item and held_item < len(item_list) else ''
            nat_name = nature_list[nature] if nature < len(nature_list) else f'nature#{nature}'
            move_names = [moves_list[m] if m < len(moves_list) else f'move#{m}' for m in moves if m]

            pokemon.append({
                "species": sp_name, "level": level, "gender": gender_str,
                "held_item": item_name, "nature": nat_name, "ability_slot": ability_slot,
                "moves": move_names, "shiny": shiny,
                "ivs": ' / '.join(f'{STAT_NAMES[j]}:{ivs[j]}' for j in range(6)),
                "evs": [f'{EV_NAMES[j]}:{evs[j]}' for j in range(6) if evs[j]],
                "avs": [f'{EV_NAMES[j]}:{avs[j]}' for j in range(6) if avs[j]],
                "friendship": friendship, "rank": rank,
                "can_mega": can_mega, "mega_form": mega_form,
            })

        return {"pokemon": pokemon}


    # ── decode_encounters ──────────────────────────────────────────
    def decode_encounters(self, data, file_idx, text_tables, path='', **kwargs):
        """Decode LGPE encounters. Path routes to sub-type:
        encount_data → wild (FlatBuffer), event_encount → static (0x40),
        add_poke → gift (0x20), field_trade → trade (0x58)."""
        if not data or len(data) < 4:
            return None

        species_list = text_tables.get('species', [])
        moves_list = text_tables.get('moves', [])
        nature_list = text_tables.get('natures', [])
        item_list = text_tables.get('items', [])

        def sp(idx):
            return species_list[idx] if idx < len(species_list) else f'#{idx}'
        def mv(idx):
            return moves_list[idx] if idx and idx < len(moves_list) else None
        def nat(idx):
            return nature_list[idx] if idx < 25 and idx < len(nature_list) else 'Random'

        if 'encount_data' in path:
            return self._decode_wild_lgpe(data, species_list)
        elif 'event_encount' in path:
            return self._decode_static_lgpe(data, sp, mv, nat)
        elif 'add_poke' in path:
            return self._decode_gift_lgpe(data, sp, mv, nat)
        elif 'field_trade' in path:
            return self._decode_trade_lgpe(data, sp, nat, item_list)
        return None

    def _zone_names(self):
        if hasattr(self, '_zone_map'): return self._zone_map
        import struct as st, re as _re
        import xoleon
        ahtb = self.switch_rom.read_file(self.ZONE_AHTB_PATH) or b''
        zh, off = {}, 8
        while off < len(ahtb):
            h = st.unpack_from('<Q', ahtb, off)[0]
            slen = st.unpack_from('<H', ahtb, off + 8)[0]
            zh[h] = ahtb[off + 10:off + 10 + slen].rstrip(b'\x00').decode('utf-8')
            off += 10 + slen
        pn = xoleon.decode_gen5_text(self.switch_rom.read_file(self.PLACE_NAME_PATH) or b'')
        def _idx(z):
            z0 = _re.sub(r'_\d+$', '', z)
            if z0.startswith('road'): return int(z0[4:]) + 2
            if z0.startswith('town'): return int(z0[4:]) + 27
            if z0 == 'forest001': return 39
            for pfx, idx in self._DUNGEON_IDX.items():
                if z.startswith(pfx): return idx
            return 0
        self._zone_map = {}
        for h, s in zh.items():
            i = _idx(s)
            if 0 < i < len(pn): self._zone_map[h] = pn[i]
        return self._zone_map

    WILD_PATHS = {'Eevee': 'bin/field/param/encount/encount_data_e.bin', 'Pikachu': 'bin/field/param/encount/encount_data_p.bin'}

    def iter_encounters(self):
        """(id, species, form, lo, hi). Both version files ship in each ROM. Zone vec (f0) -> per-area rate/lv/slot-vec fields."""
        import struct as st
        from leswitch import _vt_off
        areas = [('Ground', 6, 7, 8, 10), ('Water', 14, 15, 16, 18), ('Old Rod', 19, 20, 21, 23),
                 ('Good Rod', 24, 25, 26, 28), ('Super Rod', 29, 30, 31, 33), ('Sky', 37, 38, 39, 41)]
        def vec(d, vt, to, k):
            if not _vt_off(vt, k): return []
            n, vo = fb_vector(d, to, _vt_off(vt, k))
            return [vo + 4 * i + st.unpack_from('<I', d, vo + 4 * i)[0] for i in range(n)]
        out = []
        zm = self._zone_names()
        for ver, path in self.WILD_PATHS.items():
            if ver not in self.header['game_title']: continue  # only this cartridge's version file
            d = self.switch_rom.read_file(path)
            for zi, z in enumerate(vec(d, *fb_table(d, fb_root(d)), 0)):
                zvt, zto = fb_table(d, z)
                zid = fb_field(d, zvt, zto, 0, '<Q') or 0
                zn = zm.get(zid, f'zone {zi}')
                for name, rate_f, lo_f, hi_f, sl_f in areas:
                    if not fb_field(d, zvt, zto, rate_f, '<i'): continue
                    lo, hi = fb_field(d, zvt, zto, lo_f, '<i') or 0, fb_field(d, zvt, zto, hi_f, '<i') or 0
                    for s in vec(d, zvt, zto, sl_f):
                        svt, sto = fb_table(d, s); sp = fb_field(d, svt, sto, 1, '<i') or 0
                        if sp: out.append((f"{zn} {name}", sp, fb_field(d, svt, sto, 2, '<h') or 0, lo, hi, {'location': zn, 'method': name}))
        # event_encount.bin: 64B records, shared by both versions. u64 id hash, u16 species, u8 form, u8 level
        d = self.switch_rom.read_file(self.STATIC_ENCOUNTER_PATH) or b''
        for i in range(len(d) // 64):
            sp, fm, lv = st.unpack_from('<HBB', d, i * 64 + 8)
            if sp: out.append((f"Static #{i} ({d[i * 64:i * 64 + 8][::-1].hex()})", sp, fm, lv, lv))
        return out

    def _decode_wild_lgpe(self, data, species_list):
        """Wild encounters — FlatBuffer EncounterArchive."""
        import struct as st

        root = fb_root(data)
        vt, to = fb_table(data, root)
        zones_off = fb_field(data, vt, to, 0, '<i')
        if not zones_off:
            return 'No encounter zones'

        vec_off = to + zones_off
        count = st.unpack_from('<i', data, vec_off)[0]
        out = [f'LGPE Wild Encounters ({count} zones)']

        TABLES = [
            ('Ground', 6, 7, 8, 10),
            ('Water', 14, 15, 16, 18),
            ('Old Rod', 19, 20, 21, 23),
            ('Good Rod', 24, 25, 26, 28),
            ('Super Rod', 29, 30, 31, 33),
            ('Sky', 37, 38, 39, 41),
        ]

        for i in range(count):
            zone_ref = st.unpack_from('<i', data, vec_off + 4 + i*4)[0]
            zone_abs = vec_off + 4 + i*4 + zone_ref
            zvt, zto = fb_table(data, zone_abs)

            zone_id = fb_field(data, zvt, zto, 0, '<Q') or 0
            out.append(f'\n--- Zone {i} (ID: {zone_id:#x}) ---')

            for name, rate_f, lmin_f, lmax_f, slots_f in TABLES:
                rate = fb_field(data, zvt, zto, rate_f, '<i')
                if not rate:
                    continue
                lmin = fb_field(data, zvt, zto, lmin_f, '<i') or 0
                lmax = fb_field(data, zvt, zto, lmax_f, '<i') or 0
                out.append(f'  {name} (rate {rate}, Lv{lmin}-{lmax}):')

                slots_off = fb_field(data, zvt, zto, slots_f, '<i')
                if not slots_off:
                    continue
                svec = zto + slots_off
                scount = st.unpack_from('<i', data, svec)[0]
                for s in range(scount):
                    sref = st.unpack_from('<i', data, svec + 4 + s*4)[0]
                    sabs = svec + 4 + s*4 + sref
                    svt2, sto2 = fb_table(data, sabs)
                    prob = fb_field(data, svt2, sto2, 0, '<i') or 0
                    sp_id = fb_field(data, svt2, sto2, 1, '<i') or 0
                    form = fb_field(data, svt2, sto2, 2, '<h') or 0
                    if sp_id == 0:
                        continue
                    sp_name = species_list[sp_id] if sp_id < len(species_list) else f'#{sp_id}'
                    form_str = f'-{form}' if form else ''
                    out.append(f'    {sp_name}{form_str} ({prob}%)')

        return '\n'.join(out)

    def _decode_static_lgpe(self, data, sp, mv, nat):
        """Static encounters — 0x40 bytes each."""
        import struct as st
        SIZE = 0x40
        count = len(data) // SIZE
        out = [f'LGPE Static Encounters ({count})']
        GENDER = {0: '', 1: ' (M)', 2: ' (F)', 3: ''}
        SHINY = {0: '', 1: ' [Shiny]', 2: ' [Never Shiny]'}

        for i in range(count):
            e = i * SIZE
            species = st.unpack_from('<H', data, e + 0x08)[0]
            form = data[e + 0x0A]
            level = data[e + 0x0B]
            shiny = data[e + 0x0C] & 3
            gender = data[e + 0x0D] & 3
            nature = data[e + 0x0E]
            ability = data[e + 0x0F]
            moves = [st.unpack_from('<H', data, e + 0x20 + j*2)[0] for j in range(4)]
            ivs = [data[e + 0x2C + j] for j in range(6)]

            form_str = f'-{form}' if form else ''
            line = f'{i}: {sp(species)}{form_str} Lv{level}{GENDER.get(gender,"")}{SHINY.get(shiny,"")}'
            out.append(line)

            move_names = [mv(m) for m in moves if mv(m)]
            if move_names:
                out.append(f'   Moves: {" / ".join(move_names)}')
            out.append(f'   Nature: {nat(nature)} | Ability: slot {ability}')

            stat_names = ['HP','Atk','Def','SpA','SpD','Spe']
            fixed = [(stat_names[j], ivs[j]) for j in range(6) if ivs[j] != 0xFF]
            if fixed:
                out.append(f'   IVs: {", ".join(f"{n}:{v}" for n, v in fixed)}')

        return '\n'.join(out)

    def _decode_gift_lgpe(self, data, sp, mv, nat):
        """Gift pokemon — 0x20 bytes each."""
        import struct as st
        SIZE = 0x20
        count = len(data) // SIZE
        out = [f'LGPE Gift Pokemon ({count})']
        GENDER = {0: '', 1: ' (M)', 2: ' (F)', 3: ''}

        for i in range(count):
            e = i * SIZE
            species = st.unpack_from('<H', data, e + 0x08)[0]
            form = data[e + 0x0A]
            level = data[e + 0x0B]
            shiny = data[e + 0x0C] & 3
            gender = data[e + 0x0D] & 3
            nature = data[e + 0x0E]
            ability = data[e + 0x0F]
            special_move = st.unpack_from('<H', data, e + 0x10)[0]
            ivs = [data[e + 0x12 + j] for j in range(6)]
            avs = [data[e + 0x18 + j] for j in range(6)]

            form_str = f'-{form}' if form else ''
            out.append(f'{i}: {sp(species)}{form_str} Lv{level}{GENDER.get(gender,"")}')
            out.append(f'   Nature: {nat(nature)} | Ability: slot {ability}')

            if special_move:
                mname = mv(special_move) or f'move#{special_move}'
                out.append(f'   Special Move: {mname}')

            stat_names = ['HP','Atk','Def','SpA','SpD','Spe']
            fixed = [(stat_names[j], ivs[j]) for j in range(6) if ivs[j] != 0xFF]
            if fixed:
                out.append(f'   IVs: {", ".join(f"{n}:{v}" for n, v in fixed)}')
            av_parts = [(stat_names[j], avs[j]) for j in range(6) if avs[j]]
            if av_parts:
                out.append(f'   AVs: {", ".join(f"{n}:{v}" for n, v in av_parts)}')

        return '\n'.join(out)

    def _decode_trade_lgpe(self, data, sp, nat, item_list):
        """In-game trades — 0x58 bytes each."""
        import struct as st
        SIZE = 0x58
        count = len(data) // SIZE
        out = [f'LGPE In-Game Trades ({count})']

        for i in range(count):
            e = i * SIZE
            species = st.unpack_from('<H', data, e + 0x08)[0]
            form = data[e + 0x0A]
            level = data[e + 0x0C]

            ivs = []
            for j in range(6):
                v = st.unpack_from('<h', data, e + 0x0E + j*2)[0]
                ivs.append(v if v >= 0 else -1)

            avs = []
            for j in range(6):
                v = st.unpack_from('<h', data, e + 0x1A + j*2)[0]
                avs.append(v & 0xFF if v >= 0 else -1)

            gender_raw = st.unpack_from('<h', data, e + 0x26)[0]
            gender = {-1: '', 0: ' (M)', 1: ' (F)'}.get(gender_raw, '')
            nature_raw = st.unpack_from('<h', data, e + 0x28)[0]
            nature_str = nat(nature_raw) if nature_raw >= 0 else 'Random'

            req_species = st.unpack_from('<H', data, e + 0x42)[0]
            req_form = st.unpack_from('<H', data, e + 0x44)[0]

            form_str = f'-{form}' if form else ''
            out.append(f'{i}: {sp(species)}{form_str} Lv{level}{gender}')
            out.append(f'   Nature: {nature_str}')

            req_form_str = f'-{req_form}' if req_form else ''
            out.append(f'   Wants: {sp(req_species)}{req_form_str}')

            stat_names = ['HP','Atk','Def','SpA','SpD','Spe']
            fixed = [(stat_names[j], ivs[j]) for j in range(6) if ivs[j] >= 0]
            if fixed:
                out.append(f'   IVs: {", ".join(f"{n}:{v}" for n, v in fixed)}')

        return '\n'.join(out)



    # ── decode_shop ────────────────────────────────────────────────
    def decode_shop(self, data, file_idx, text_tables, path='', **kwargs):
        """Decode LGPE shop inventory (FlatBuffer). Single + Multi shops."""
        import struct as st

        if len(data) < 8:
            return None

        item_list = text_tables.get('items', [])
        def iname(idx):
            return item_list[idx] if idx < len(item_list) else f'item#{idx}'

        root = fb_root(data)
        vt, to = fb_table(data, root)
        out = ['LGPE Shop Inventory']

        # Field 0: Single shops vector
        single_off = fb_field(data, vt, to, 0, '<i')
        if single_off:
            svec = to + single_off
            scount = st.unpack_from('<i', data, svec)[0]
            out.append(f'\nSingle Shops ({scount}):')
            for i in range(scount):
                ref = st.unpack_from('<i', data, svec + 4 + i*4)[0]
                sabs = svec + 4 + i*4 + ref
                svt2, sto2 = fb_table(data, sabs)
                shop_hash = fb_field(data, svt2, sto2, 0, '<Q') or 0
                # Field 1: Inventory table
                inv_off = fb_field(data, svt2, sto2, 1, '<i')
                items = []
                if inv_off:
                    iabs = sto2 + inv_off
                    ivt, ito = fb_table(data, iabs)
                    items_off = fb_field(data, ivt, ito, 0, '<i')
                    if items_off:
                        ivec = ito + items_off
                        ic = st.unpack_from('<i', data, ivec)[0]
                        items = [st.unpack_from('<i', data, ivec + 4 + j*4)[0] for j in range(ic)]
                out.append(f'  Shop {shop_hash:#x}: {", ".join(iname(x) for x in items)}')

        # Field 1: Multi shops vector
        multi_off = fb_field(data, vt, to, 1, '<i')
        if multi_off:
            mvec = to + multi_off
            mcount = st.unpack_from('<i', data, mvec)[0]
            out.append(f'\nMulti Shops ({mcount}):')
            for i in range(mcount):
                ref = st.unpack_from('<i', data, mvec + 4 + i*4)[0]
                mabs = mvec + 4 + i*4 + ref
                mvt2, mto2 = fb_table(data, mabs)
                shop_hash = fb_field(data, mvt2, mto2, 0, '<Q') or 0
                out.append(f'  Shop {shop_hash:#x}:')
                # Field 1: vector of Inventory tables
                invs_off = fb_field(data, mvt2, mto2, 1, '<i')
                if invs_off:
                    invvec = mto2 + invs_off
                    inv_count = st.unpack_from('<i', data, invvec)[0]
                    for k in range(inv_count):
                        iref = st.unpack_from('<i', data, invvec + 4 + k*4)[0]
                        iabs = invvec + 4 + k*4 + iref
                        ivt, ito = fb_table(data, iabs)
                        items_off = fb_field(data, ivt, ito, 0, '<i')
                        items = []
                        if items_off:
                            itemvec = ito + items_off
                            ic = st.unpack_from('<i', data, itemvec)[0]
                            items = [st.unpack_from('<i', data, itemvec + 4 + j*4)[0] for j in range(ic)]
                        out.append(f'    Inv {k}: {", ".join(iname(x) for x in items)}')

        return '\n'.join(out)


    FLIPNOTE_PAIRS = {
        "Pokemon Let’s Go": ['GP1', 'GE1'],
    }
