"""Kalos_sequel.py: Legends: Z-A.

Inherits Paldea_sv. Kalos region revisit, Lumiose City focus.
Second Legends title. Mega Evolution returns.
DLC: Mega Dimension (donuts, hyperspace, pocket dimensions).
"""
import struct
from Paldea_sv import Paldea_sv
from leswitch import fb_field, fb_root, fb_string, fb_table, fb_vector, fb_str, fb_sub, fb_struct, fb_vec, fb_scalars, _vt_off


class Kalos_sequel(Paldea_sv):
    """Legends: Z-A."""

    GAME_CODES = ('LZA', 'LZA', 'LZA')
    TITLE_IDS = (0x0100F43008C44000, 0x0100F43008C44800, 0x0100F43008C45002)
    TITLES = ('Pokémon Legends: Z-A', 'Pokémon Legends: Z-A: Version 2.0.2', 'Pokémon Legends: Z-A: Download Key for Version 2.0.2')
    YEAR = 2025


    SPECIES_COUNT = 1025  # DevID enum max

    EVO_USE_MOVE_BARB_BARRAGE = 62
    PERSONAL_FIELD_SHIFT = -2  # KitakamiDex/BlueberryDex removed from schema

    CONTAINER = 'trinity'
    TRINITY_DATA_PATH = 'arc/data.trpfs'
    TRINITY_DIR_PATH = 'arc/data.trpfd'

    TEXT_PATH = 'arc/ik_messagedatEnglishcommon'
    MEGA_EVO_PATH = 'world/exl/pokemon/megaevo_data/megaevo_data.bin'

    # Z-A: first game with LATAM Spanish (11 languages)
    LANGUAGES = ('ja', 'ja-kanji', 'en', 'fr', 'it', 'de', 'es', 'ko', 'zh-Hans', 'zh-Hant', 'es-419')
    LANG_FOLDERS = {
        **Paldea_sv.LANG_FOLDERS,
        'es-419': 'LATAM',
    }

    # Z-A paths (override SV where they moved)
    PERSONAL_PATH = 'avalon/data/personal_array.bin'
    MOVE_DATA_PATH = 'avalon/data/waza_array.bin'
    ENCOUNTER_PATH = 'world/ik_data/field/pokemon/encount_data/encount_data/encount_data_array.bin'
    TRAINER_PATH = 'world/ik_data/trainer/trdata/trdata_array.bin'
    ITEM_PATH = 'world/exl/item_data/item_data/item_data.bin'
    SHOP_PATH = 'world/exl/shop/shop_item_lineup/shop_item_lineup.bin'
    HOLOGRAM_SHOP_PATH = 'world/exl/hologram/hud_shopping/hud_shopping.bin'

    # Null out inherited paths that don't exist in Z-A
    SHOP_LINEUP_PATH = None
    SHOP_MASTER_PATH = None
    TM_SHOP_PATH = None
    DRESSUP_SHOP_PATH = None
    DRESSUP_CATEGORY_PATH = None
    DRESSUP_ITEM_PATH = None
    RESTAURANT_SHOP_PATH = None
    RESTAURANT_MENU_PATH = None
    RESTAURANT_BUF_PATH = None
    DLC_ITEM_PATH = None
    KITAKAMI_RAID_01 = None
    KITAKAMI_RAID_02 = None
    KITAKAMI_RAID_03 = None
    KITAKAMI_RAID_04 = None
    KITAKAMI_RAID_05 = None
    KITAKAMI_RAID_06 = None
    BLUEBERRY_RAID_01 = None
    BLUEBERRY_RAID_02 = None
    BLUEBERRY_RAID_03 = None
    BLUEBERRY_RAID_04 = None
    BLUEBERRY_RAID_05 = None
    BLUEBERRY_RAID_06 = None
    KITAKAMI_DEST_PATH = None
    BLUEBERRY_DEST_PATH = None
    KITAKAMI_PLACES_PATH = None
    BLUEBERRY_PLACES_PATH = None
    KITAKAMI_DEX_BLACKLIST = None
    BLUEBERRY_DEX_BLACKLIST = None
    KITAKAMI_DEX_DISTRIB = None
    BLUEBERRY_DEX_DISTRIB = None
    KITAKAMI_DEX_MEMO = None
    BLUEBERRY_DEX_MEMO = None
    KITAKAMI_DEX_REWARD = None
    BLUEBERRY_DEX_REWARD = None
    RAID_PATH = None
    FOOD_BUF_PATH = None
    FOOD_RECIPE_PATH = None
    OUTBREAK_PATH = None
    MOVE_SHOP_PATH = None
    GINKGO_ITEM_PATH = None
    GINKGO_TABLE_PATH = None
    MEGA_EVO_PATH = None
    TRADE_PATH = None
    GIFT_PATH = None
    WILD_PATH_E = None
    WILD_PATH_P = None
    TEXT_SCRIPT_PATH = None
    LEARNSET_PATH = None
    EVOLUTION_PATH = None
    BATTLE_DROPS_PATH = None
    FIELD_DROPS_PATH = None
    CRAFT_PATH = None
    DEX_RESEARCH_PATH = None
    NEW_OUTBREAK_GROUP_PATH = None
    NEW_OUTBREAK_LOTTERY_PATH = None
    POKE_MISC_PATH = None
    SHINY_ROLLS_PATH = None
    THROWABLE_PARAM_PATH = None
    THROW_PARAM_PATH = None
    DONUT_PATH = 'world/exl/donut'
    DIM_PATH = 'world/ik_data/field/dimension'
    DONUT_FILES = (
        'world/exl/donut/berry/berry.bin',
        'world/exl/donut/donut/donut.bin',
        'world/exl/donut/donut_recipe/donut_recipe.bin',
        'world/exl/donut/flavor/flavor.bin',
        'world/exl/donut/flavor_lottery/flavor_lottery.bin',
        'world/exl/donut/flavor_parameter/flavor_parameter.bin',
        'world/exl/donut/oneword/oneword.bin',
    )
    DIM_FILES = (
        'world/ik_data/field/dimension/dimension_boss_lottery/dimension_boss_lottery/dimension_boss_lottery_array.bin',
        'world/ik_data/field/dimension/dimension_config/dimension_config/dimension_config.bin',
        'world/ik_data/field/dimension/dimension_gate_object/dimension_gate_object/dimension_gate_object_array.bin',
        'world/ik_data/field/dimension/dimension_gate_spawner/dimension_gate_spawner/dimension_gate_spawner_array.bin',
        'world/ik_data/field/dimension/dimension_gimmick_item/dimension_gimmick_item/dimension_gimmick_item_array.bin',
        'world/ik_data/field/dimension/dimension_map/dimension_map/dimension_map_array.bin',
        'world/ik_data/field/dimension/dimension_progress/dimension_progress/dimension_progress_array.bin',
        'world/ik_data/field/dimension/dimension_rank/dimension_rank/dimension_rank_array.bin',
        'world/ik_data/field/dimension/dimension_special_lottery/dimension_special_lottery/dimension_special_lottery_array.bin',
        'world/ik_data/field/dimension/dimension_unique_lottery/dimension_unique_lottery/dimension_unique_lottery_array.bin',
        'world/ik_data/field/dimension/dimension_wild_pokemon/dimension_wild_pokemon/dimension_wild_pokemon_array.bin',
        'world/ik_data/field/dimension/dimension_zone_lottery/dimension_zone_lottery/dimension_zone_lottery_array.bin',
    )
    ZA_ROYALE_PATH = 'world/ik_data/capture/capture_ball_data/capture_ball_data.bin'

    def iter_learnsets(self):
        """personal_array: field 0 = Info (internal, form, national), field 25 = learnset (u16 move, s8 level, u8 plus)."""
        d = self.read_file(self.PERSONAL_PATH)
        if not d: return None
        vt, to = fb_table(d, fb_root(d))
        n, vo = fb_vector(d, to, _vt_off(vt, 0))
        tag = {-3: 'Evo', -2: 'Relearn'}
        out, seen = [], set()
        for i in range(n):
            p = vo + 4 * i; p += struct.unpack_from('<I', d, p)[0]
            evt, eto = fb_table(d, p)
            o = _vt_off(evt, 0); info = o and struct.unpack_from('<HHH', d, eto + o)
            ls = tuple((tag.get(lv, lv), mv) for mv, lv, _ in fb_vec(d, evt, eto, 25, '<HbB', 4) or [])
            if not info or (info[2], ls) in seen: continue  # megas sharing the base learnset
            seen.add((info[2], ls)); out.append((info[2], list(ls)))
        return out

    def iter_encounters(self):
        """encount_data_array: root vec of 12 groups -> vec of slots. Slot f0 = id (zone code inside), f1 = species, f2/f3 = min/max lv, f5 = form."""
        d = self.read_file(self.ENCOUNTER_PATH)
        if not d: return None
        def vec(vt, to):
            n, vo = fb_vector(d, to, _vt_off(vt, 0))
            return [vo + 4 * i + struct.unpack_from('<I', d, vo + 4 * i)[0] for i in range(n)]
        out = []
        for g in vec(*fb_table(d, fb_root(d))):
            for s in vec(*fb_table(d, g)):
                vt, to = fb_table(d, s)
                eid = fb_str(d, vt, to, 0)
                out.append((eid, fb_field(d, vt, to, 1, '<I'), fb_field(d, vt, to, 5, '<I') or 0,
                            fb_field(d, vt, to, 2, '<I'), fb_field(d, vt, to, 3, '<I'), {'location': eid or 'Wild'}))
        return out

    # ZA-specific: 160 TMs (107 base + 53 DLC), move IDs in bit order
    TM_MOVE_IDS = (
        29, 337, 473, 249, 46, 347, 92, 86, 812, 280,
        339, 157, 58, 424, 423, 113, 182, 612, 408, 583,
        422, 332, 9, 8, 242, 412, 129, 91, 7, 14,
        115, 104, 34, 400, 203, 317, 446, 126, 435, 331,
        352, 202, 19, 63, 282, 341, 97, 120, 196, 315,
        219, 414, 188, 434, 416, 38, 261, 442, 428, 248,
        421, 53, 94, 76, 444, 521, 85, 257, 89, 250,
        304, 83, 57, 247, 406, 710, 398, 523, 542, 334,
        404, 369, 417, 430, 164, 528, 231, 191, 390, 399,
        174, 605, 200, 18, 269, 56, 377, 127, 118, 441,
        527, 411, 526, 394, 59, 87, 370,
        # DLC TMs (Mega Dimension)
        4, 263, 886, 47, 491, 490, 488, 885, 6, 318,
        325, 466, 246, 259, 206, 305, 706, 102, 443, 138,
        402, 509, 451, 409, 458, 299, 814, 530, 815, 480,
        524, 207, 330, 252, 660, 799, 813, 13, 130, 161,
        503, 333, 410, 80, 669, 143, 90, 329, 800, 796,
        307, 308, 338,
    )

    # Evolution method → plib item conversion (evo arg → real item ID)
    PLIB_ITEMS = {
        1: 80, 2: 81, 3: 82, 4: 83, 5: 84, 6: 85, 7: 107, 8: 108,
        9: 110, 10: 1779, 15: 229, 16: 236, 19: 280, 49: 326, 50: 327,
        51: 644, 52: 849, 70: 1103, 71: 1104, 79: 1116, 80: 1117,
        81: 1253, 82: 1254, 83: 1582, 84: 1592, 85: 2344, 86: 1861,
        87: 2345, 88: 1857, 89: 1858, 92: 218, 93: 109, 94: 2403,
        95: 2404, 96: 2402, 102: 765, 111: 537, 112: 325, 113: 252,
        114: 324, 115: 322, 116: 323, 117: 321, 118: 235, 119: 2482,
        121: 847, 1691: 1691,
    }

    # ZARank tiers (Z=weakest, A=strongest, Inf=postgame)
    ZA_RANKS = ('Z','Y','X','W','V','U','T','S','R','Q','P','O','N',
                'M','L','K','J','I','H','G','F','E','D','C','B','A','Inf')

    FLIPNOTE_PAIRS = {
        'Pokemon Legends: Z-A': ['LZA'],
    }

    # ── decode_encounters ───────────────────────────────────────────
    def decode_encounters(self, data, file_idx, text_tables, path='', **kwargs):
        """Decode ZA encounter data (spawner-based).
        Handles both overworld spawners and dimension wild branches."""
        if len(data) < 12:
            return None

        species_list = text_tables.get('species', [])
        root = fb_root(data)
        vt, to = fb_table(data, root)

        # EncountData: Id, DevNo, MinLevel, MaxLevel, Sex, FormNo, Rare,
        #              Tokusei, Seikaku, TalentScale, TalentVNum, OyabunProbability
        enc_id = fb_str(data, vt, to, 0) or "?"
        dev_no = fb_field(data, vt, to, 1, '<H') or 0
        min_lv = fb_field(data, vt, to, 2, '<i') or 0
        max_lv = fb_field(data, vt, to, 3, '<i') or 0
        sex = fb_field(data, vt, to, 4, '<i') or 0
        form = fb_field(data, vt, to, 5, '<i') or 0
        rare = fb_field(data, vt, to, 6, '<i') or 0
        ability = fb_field(data, vt, to, 7, '<i') or 0
        nature = fb_field(data, vt, to, 8, '<i') or 0
        iv_scale = fb_field(data, vt, to, 9, '<i') or 0
        iv_count = fb_field(data, vt, to, 10, '<i') or 0
        oyabun_prob = fb_field(data, vt, to, 11, '<f') or 0.0

        sp_name = species_list[dev_no] if dev_no < len(species_list) else f"#{dev_no}"
        form_str = f"-{form}" if form else ""
        lv_str = f"Lv{min_lv}" if min_lv == max_lv else f"Lv{min_lv}-{max_lv}"
        sex_str = self.SEX_SYMBOLS[sex] if sex < len(self.SEX_SYMBOLS) else ''
        rare_str = ' *Shiny*' if rare == 2 else ''

        out = [f"{sp_name}{form_str}{sex_str} {lv_str}{rare_str}"]
        if oyabun_prob > 0:
            out.append(f"Alpha chance: {oyabun_prob:.1%}")
        if iv_count > 0:
            out.append(f"IVs: {iv_count} perfect (scale {iv_scale})")
        if ability:
            out.append(f"Ability slot: {ability}")
        if nature:
            out.append(f"Nature: fixed #{nature}")
        out[0] = f"[{enc_id}] {out[0]}"

        return "\n".join(out)

    @staticmethod
    def _parse_trid(trid, rank=None):
        """Parse TrID into human-readable card label.
        Two systems: STORY (Ev_) and ROYALE (za_).
        Royale base: Bat # (Rnk X). Rooftop replaces Bat with Rftp."""
        # ── Strip modifiers ──
        variant = ''
        for suf, lbl in (('_hono', ' (Fire)'), ('_kusa', ' (Grass)'), ('_mizu', ' (Water)')):
            if trid.endswith(suf):
                variant = lbl
                trid = trid[:-len(suf)]
                break
        is_multi = '_multi' in trid
        trid = trid.replace('_multi', '')

        # ── SYSTEM 1: STORY ──
        _REST = {'1': 'Le Nah', '2': 'Le Yeah', '3': 'Le Wow'}
        if trid.startswith('Ev_m'):
            parts = trid[4:].split('_')
            mis = str(int(parts[0]))
            if 'boss' in parts:
                if variant:
                    return f"Promo.{variant}"
                if rank and rank not in ('Z', 'rank#0'):
                    return f"Promo. (Rnk {rank})"
                return f"Mis {mis}, Promo."
            nums = [p for p in parts[1:] if p.isdigit()]
            if nums:
                if variant:
                    return f"Mis {mis}{variant}"
                n = int(nums[0])
                ns = f"{n // 1000}k" if n >= 1000 else str(n)
                return f"Mis {mis}, #{ns}"
            return f"Mis {mis}{variant}"
        if trid.startswith('Ev_sub_'):
            parts = trid[7:].split('_')
            mis = str(int(parts[0]))
            multi = '; Multi' if is_multi else ''
            if len(parts) > 1 and parts[1].isdigit():
                return f"Sub-Mis {mis}, #{int(parts[1])}{multi}{variant}"
            return f"Sub-Mis {mis}{multi}{variant}"
        if trid.startswith('Ev_sys_rest'):
            parts = trid[11:].split('_')
            name = _REST.get(parts[0], f'Rest {parts[0]}')
            num = str(int(parts[1])) if len(parts) > 1 and parts[1].isdigit() else '?'
            return f"{name} #{num}{variant}"

        # ── SYSTEM 2: ZA ROYALE ──
        # Base: Bat # (Rnk X)
        # Rooftop: Rftp # (Rnk X) — replaces Bat, not a modifier
        # Inf tiers: Bat # (Rnk ∞; T#)
        is_strong = '_strong' in trid
        trid = trid.replace('_strong', '')

        if trid.startswith('za_rank_inf'):
            rest = trid[11:]
            parts = rest.split('_')
            tier = parts[0]
            num = str(int(parts[1])) if len(parts) > 1 and parts[1].isdigit() else '?'
            return f"Bat {num} (Rnk ∞; T{tier}){variant}"
        if trid.startswith('za_rank_'):
            rest = trid[8:]
            parts = rest.split('_')
            letter = parts[0].upper()
            num = str(int(parts[1])) if len(parts) > 1 and parts[1].isdigit() else '?'
            rnk = f"Rnk {letter}"
            if is_strong:
                if variant:
                    return f"Rftp{variant}"
                return f"Rftp {num} ({rnk}){variant}"
            return f"Bat {num} ({rnk}){variant}"
        if trid.startswith('za_inf_'):
            rest = trid[7:]
            parts = rest.split('_')
            num = str(int(parts[0])) if parts[0].isdigit() else '?'
            rnk = "Rnk ∞"
            if is_strong:
                if variant:
                    return f"Rftp{variant}"
                return f"Rftp {num} ({rnk}){variant}"
            return f"Bat {num} ({rnk}){variant}"

        return trid + variant

    # ── decode_trainer ──────────────────────────────────────────────
    def decode_trainer(self, data, file_idx, text_tables, path='', **kwargs):
        """Decode ZA trainer (TrDataMain FlatBuffer).
        Includes team, mega flags, AI, vision cone, env/dlog."""
        if len(data) < 12:
            return None

        species_list = text_tables.get('species', [])
        moves_list = text_tables.get('moves', [])
        item_list = text_tables.get('items', [])

        root = fb_root(data)
        vt, to = fb_table(data, root)
        # Array wrapper has 1 field (the vector), individual entries have 25+
        if len(vt) <= 8:
            _tf = _vt_off(vt, 0)
            if not _tf:
                return None
            cnt, doff = fb_vector(data, to, _tf)
            if file_idx >= cnt:
                return None
            _eop = doff + file_idx * 4
            _erel = struct.unpack_from('<I', data, _eop)[0]
            vt, to = fb_table(data, _eop + _erel)

        tr_id = fb_str(data, vt, to, 0) or "?"
        tr_type = fb_field(data, vt, to, 1, '<Q') or 0
        tr_type2 = fb_field(data, vt, to, 2, '<Q') or 0
        za_rank = fb_field(data, vt, to, 3, '<B') or 0
        money_rate = fb_field(data, vt, to, 4, '<B') or 0
        mega = fb_field(data, vt, to, 5, '<B') or 0
        last_mega = fb_field(data, vt, to, 6, '<B') or 0

        rank_str = self.ZA_RANKS[za_rank] if za_rank < len(self.ZA_RANKS) else f"rank#{za_rank}"

        # Resolve class + name via AHTB (docs/za_trainer_card_format.md)
        class_name = ''
        trainer_name = tr_id
        fmt_flags = 0
        _text_path = getattr(self, 'TEXT_PATH', '')
        _ahtb_list = getattr(self, '_ahtb_cache', {}).get(_text_path, [])
        _text_narc = self._narc_cache.get(_text_path)

        # trainer_classes file index
        _tc = text_tables.get('trainer_classes')
        _tc_idx = None
        if _tc:
            for k, v in text_tables.items():
                if isinstance(k, int) and v is _tc:
                    _tc_idx = k; break

        # trainer_names file index
        _tn = text_tables.get('trainer_names')
        _tn_idx = None
        if _tn:
            for k, v in text_tables.items():
                if isinstance(k, int) and v is _tn:
                    _tn_idx = k; break

        # Class name via trtype AHTB hash match
        if _tc_idx is not None and _tc_idx < len(_ahtb_list):
            for ci, (h, _) in enumerate(self.parse_ahtb(_ahtb_list[_tc_idx])):
                if h == tr_type:
                    if ci < len(_tc): class_name = _tc[ci]
                    if _text_narc and _tc_idx < len(_text_narc.files):
                        _dat = _text_narc.files[_tc_idx]
                        _foff = 0x14 + ci * 8 + 6
                        if _foff + 2 <= len(_dat):
                            fmt_flags = struct.unpack_from('<H', _dat, _foff)[0]
                    break

        # Display name via trname AHTB: match TrId against AHTB keys
        if _tn_idx is not None and _tn_idx < len(_ahtb_list):
            _ahtb_entries = self.parse_ahtb(_ahtb_list[_tn_idx])
            # Try direct TrID match first
            for ni, (h, key) in enumerate(_ahtb_entries):
                if key == tr_id:
                    if ni < len(_tn): trainer_name = _tn[ni]
                    break
            else:
                # Fallback: reverse lookup index -> trname_keys -> display names
                _i2t = getattr(self, '_idx_to_trname', {})
                _keys = _i2t.get(file_idx, [])
                if _keys:
                    _names = []
                    for _k in _keys:
                        for ni, (h, key) in enumerate(_ahtb_entries):
                            if key == _k:
                                if ni < len(_tn) and _tn[ni] not in _names:
                                    _names.append(_tn[ni])
                                break
                    if _names:
                        _dn = getattr(self, '_dowse_resolved', None)
                        trainer_name = _dn if _dn and _dn in _names else '/'.join(_names)

        # Format template (4 patterns from the game's text flags)
        fmt = (fmt_flags >> 7) & 0b11
        article = ((fmt_flags >> 9) & 1) == 0
        if class_name:
            if fmt == 1 and article: display = f"{trainer_name} of the {class_name}"
            elif fmt == 1:           display = f"{trainer_name} of {class_name}"
            elif fmt == 2:           display = f"{trainer_name} the {class_name}"
            else:                    display = f"{class_name} {trainer_name}"
        else:
            display = trainer_name

        parsed_label = self._parse_trid(tr_id, rank_str)
        out = [f"{display}"]
        if mega:
            out.append(f"Mega Evolution: {'Last Pokemon only' if last_mega else 'Yes'}")

        highest_level = 0
        # Poke1-6 are fields 7-12 (PokeDataBattle sub-tables)
        for slot in range(6):
            pvt, pto = fb_sub(data, vt, to, 7 + slot)
            if not pvt:
                continue
            dev = fb_field(data, pvt, pto, 0, '<H') or 0
            if dev == 0:
                continue
            form = fb_field(data, pvt, pto, 1, '<h') or 0
            sex = fb_field(data, pvt, pto, 2, '<B') or 0
            item = fb_field(data, pvt, pto, 3, '<i') or 0
            level = fb_field(data, pvt, pto, 4, '<i') or 0
            if level > highest_level: highest_level = level

            sp_name = species_list[dev] if dev < len(species_list) else f"#{dev}"
            form_str = f"-{form}" if form else ""
            item_name = item_list[item] if item and item < len(item_list) else ""
            item_str = f" @ {item_name}" if item_name else ""

            # Moves are fields 6-9 (WazaSetBattle sub-tables)
            move_names = []
            for mi in range(4):
                mvt, mto = fb_sub(data, pvt, pto, 6 + mi)
                if mvt:
                    mid = fb_field(data, mvt, mto, 0, '<H') or 0
                    if mid:
                        move_names.append(moves_list[mid] if mid < len(moves_list) else f"move#{mid}")

            moves_str = f" [{' / '.join(move_names)}]" if move_names else ""
            out.append(f"  {slot+1}. {sp_name}{form_str} Lv{level}{item_str}{moves_str}")

        if money_rate and highest_level:
            out.append(f"Prize: \u00a5{money_rate * 4 * highest_level:,}")

        # AI flags (fields 13-20)
        ai_names = ['Basic', 'High', 'Expert', 'Double', 'Raid', 'Weak', 'Item', 'Change']
        ai_flags = [name for i, name in enumerate(ai_names) if fb_field(data, vt, to, 13 + i, '<B')]
        if ai_flags:
            out.append(f"AI: {' / '.join(ai_flags)}")

        _ABBREV = [('Bat', 'Battle'), ('Rftp', 'Rooftop'), ('Rnk', 'Rank'),
                   ('Mis', 'Mission'), ('Promo.', 'Promotion')]
        legend = [f'{a}={full}' for a, full in _ABBREV if a in parsed_label]
        if legend:
            out.append(' | '.join(legend))

        # Rival shared-index note: raw decipher shows both names, dowse disambiguates
        if '/' in trainer_name:
            out.append('')
            out.append("""Ah, seems you stumbled here by accident. In case you didn’t know, the two names up above are those for the rival, who share trainer data in this game. The male’s name is Urbain, the female? Taunie. How is it they share this indice when no other rival (Like Dawn, Lucas, Brendan, or May) in this series has ever shared an indice with their counterpart? Basically, Nintendo managed to make the data in their game irregular (Don’t ask me HOW they did that, as I do not know at all.). But you don’t need to know all of this. All you need to know is they are one character internally, as shown by this data, and that their gender is determined by a byte in a player’s save data. If you come back using the same tool after searching (via dowse), then you may notice a surprise! Bye!""")

        return "\n".join(out), parsed_label

    # ── decode_item ─────────────────────────────────────────────────
    def decode_item(self, data, file_idx, text_tables):
        """Decode ZA item data (FlatBuffer). Includes ball mechanics and shop prices."""
        if len(data) < 12:
            return None

        root = fb_root(data)
        vt, to = fb_table(data, root)

        item_id = fb_field(data, vt, to, 0, '<i') or 0
        # Field 1: ItemType, Field 2: InternalName, Field 3: IconName
        item_type = fb_field(data, vt, to, 1, '<i') or 0
        internal_name = fb_str(data, vt, to, 2) or f"item#{item_id}"
        price = fb_field(data, vt, to, 4, '<i') or 0
        pocket = fb_field(data, vt, to, 5, '<i') or 0
        stack_max = fb_field(data, vt, to, 6, '<i') or 0
        cant_hold = fb_field(data, vt, to, 10, '<B') or 0
        tm_move = fb_field(data, vt, to, 11, '<H') or 0
        tm_index = fb_field(data, vt, to, 12, '<i') or 0

        moves_list = text_tables.get('moves', [])
        out = [f"{internal_name} (#{item_id})"]
        out.append(f"Pocket: {pocket} | Stack: {stack_max}")
        if price: out.append(f"Price: {price}")
        if cant_hold: out.append("Cannot be held")
        if tm_move:
            mname = moves_list[tm_move] if tm_move < len(moves_list) else f"move#{tm_move}"
            out.append(f"TM{tm_index}: {mname}")

        # Healing/stat effects (fields 13-46 cover status healing, stat boosts, etc.)
        heal_pct = fb_field(data, vt, to, 31, '<i') or 0
        revive = fb_field(data, vt, to, 33, '<i') or 0
        exp_gain = fb_field(data, vt, to, 34, '<i') or 0
        if heal_pct: out.append(f"Heals: {heal_pct}% HP")
        if revive: out.append(f"Revive: {revive}% HP")
        if exp_gain: out.append(f"EXP: +{exp_gain}")

        return "\n".join(out)

    # ── decode_donut ────────────────────────────────────────────────
    def decode_donut(self, data, file_idx, text_tables, path='', **kwargs):
        """Decode ZA donut system. Dispatch by path subsection."""
        section = path.split(self.DONUT_PATH + '/')[-1].split('/')[0] if self.DONUT_PATH in path else ''
        method = getattr(self, f'_decode_{section}', None)
        if not method or len(data) < 12: return None
        return method(data, fb_root(data), text_tables)

    def _decode_berry(self, data, root, text_tables):
        vt, to = fb_table(data, root)
        item_id = fb_field(data, vt, to, 0, '<I') or 0
        donut_idx = fb_field(data, vt, to, 1, '<I') or 0
        is_hyper = fb_field(data, vt, to, 2, '<B') or 0
        spicy = fb_field(data, vt, to, 3, '<I') or 0
        fresh = fb_field(data, vt, to, 4, '<I') or 0
        sweet = fb_field(data, vt, to, 5, '<I') or 0
        bitter = fb_field(data, vt, to, 6, '<I') or 0
        sour = fb_field(data, vt, to, 7, '<I') or 0
        lv_boost = fb_field(data, vt, to, 8, '<I') or 0
        calories = fb_field(data, vt, to, 9, '<I') or 0
        items = text_tables.get('items', [])
        iname = items[item_id] if item_id < len(items) else f"item#{item_id}"
        out = [f"{iname} (donut #{donut_idx})"]
        out.append(f"Spicy {spicy} | Fresh {fresh} | Sweet {sweet} | Bitter {bitter} | Sour {sour}")
        out.append(f"Calories: {calories} | Lv Boost: {lv_boost}")
        if is_hyper: out.append("Hyperspace Berry")
        return "\n".join(out)

    def _decode_donut_recipe(self, data, root, text_tables):
        vt, to = fb_table(data, root)
        idx = fb_field(data, vt, to, 0, '<I') or 0
        s_min = fb_field(data, vt, to, 1, '<I') or 0
        s_max = fb_field(data, vt, to, 2, '<I') or 0
        sp_min = fb_field(data, vt, to, 3, '<I') or 0
        sp_max = fb_field(data, vt, to, 4, '<I') or 0
        so_min = fb_field(data, vt, to, 5, '<I') or 0
        so_max = fb_field(data, vt, to, 6, '<I') or 0
        b_min = fb_field(data, vt, to, 7, '<I') or 0
        b_max = fb_field(data, vt, to, 8, '<I') or 0
        f_min = fb_field(data, vt, to, 9, '<I') or 0
        f_max = fb_field(data, vt, to, 10, '<I') or 0
        rname = fb_str(data, vt, to, 12) or f"recipe#{idx}"
        out = [f"Recipe: {rname} (#{idx})"]
        out.append(f"Sweet {s_min}-{s_max} | Spicy {sp_min}-{sp_max} | Sour {so_min}-{so_max} | Bitter {b_min}-{b_max} | Fresh {f_min}-{f_max}")
        return "\n".join(out)

    def _decode_flavor_parameter(self, data, root, text_tables):
        vt, to = fb_table(data, root)
        flavor = fb_str(data, vt, to, 0) or "?"
        boost_arg = fb_field(data, vt, to, 3, '<i') or 0
        is_battle = fb_field(data, vt, to, 6, '<B') or 0
        level = fb_field(data, vt, to, 7, '<i') or 0
        is_special = fb_field(data, vt, to, 9, '<B') or 0
        fname = fb_str(data, vt, to, 10) or flavor
        out = [f"Flavor: {fname} (Lv{level})"]
        out.append(f"Power: {flavor} | Boost: type#{boost_arg}")
        if is_battle: out.append("Battle Stat Boost")
        if is_special: out.append("Special Flavor")
        return "\n".join(out)

    # ── decode_dimension ────────────────────────────────────────────
    def decode_dim(self, data, file_idx, text_tables, path='', **kwargs):
        """Decode ZA dimension system. Dispatch by path subsection."""
        section = path.split(self.DIM_PATH + '/')[-1].split('/')[0] if self.DIM_PATH in path else ''
        if section == 'dimension_wild_pokemon':
            return self.decode_encounters(data, file_idx, text_tables, path=path)
        method = getattr(self, f'_decode_{section}', None)
        if not method or len(data) < 12: return None
        return method(data, fb_root(data), text_tables)

    def _decode_dimension_rank(self, data, root, text_tables):
        vt, to = fb_table(data, root)
        rank = fb_field(data, vt, to, 0, '<i') or 0
        ext_level = fb_field(data, vt, to, 1, '<i') or 0
        est_level = fb_field(data, vt, to, 2, '<i') or 0
        limit_speed = fb_field(data, vt, to, 3, '<f') or 0.0
        rank_str = self.ZA_RANKS[rank] if rank < len(self.ZA_RANKS) else f"#{rank}"
        out = [f"Dimension Rank {rank_str}"]
        out.append(f"Extension Lv: {ext_level} | Estimate Lv: {est_level}")
        out.append(f"Limit Reduction: {limit_speed:.2f}")
        return "\n".join(out)

    def _decode_dimension_boss_lottery(self, data, root, text_tables):
        vt, to = fb_table(data, root)
        species_list = text_tables.get('species', [])
        boss_id = fb_str(data, vt, to, 0) or "?"
        rank = fb_field(data, vt, to, 2, '<i') or 0
        est_lv = fb_field(data, vt, to, 3, '<i') or 0
        ext_lv = fb_field(data, vt, to, 4, '<i') or 0
        rematch = fb_field(data, vt, to, 5, '<B') or 0
        dev_no = fb_field(data, vt, to, 6, '<i') or 0
        form = fb_field(data, vt, to, 7, '<i') or 0
        sp_name = species_list[dev_no] if dev_no < len(species_list) else f"#{dev_no}"
        form_str = f"-{form}" if form else ""
        rank_str = self.ZA_RANKS[rank] if rank < len(self.ZA_RANKS) else f"#{rank}"
        out = [f"Boss: {sp_name}{form_str} [{boss_id}]"]
        out.append(f"Rank {rank_str} | Lv {est_lv}+{ext_lv}")
        if rematch: out.append("Rematch available")
        return "\n".join(out)

    def _decode_dimension_progress(self, data, root, text_tables):
        vt, to = fb_table(data, root)
        prog_id = fb_str(data, vt, to, 0) or "?"
        wild_min = fb_field(data, vt, to, 1, '<i') or 0
        wild_max = fb_field(data, vt, to, 2, '<i') or 0
        battle_min = fb_field(data, vt, to, 3, '<i') or 0
        battle_max = fb_field(data, vt, to, 4, '<i') or 0
        event_min = fb_field(data, vt, to, 5, '<i') or 0
        event_max = fb_field(data, vt, to, 6, '<i') or 0
        out = [f"Dimension Progress: {prog_id}"]
        out.append(f"Wild: {wild_min}-{wild_max} | Battle: {battle_min}-{battle_max} | Event: {event_min}-{event_max}")
        return "\n".join(out)

    # ── decode_za_royale ────────────────────────────────────────────
    def decode_za_royale(self, data, file_idx, text_tables, path='', **kwargs):
        """Decode ZA Royale capture system. Dispatch by path subsection."""
        section = path.split(self.ZA_ROYALE_PATH + '/')[-1].split('/')[0] if self.ZA_ROYALE_PATH in path else ''
        method = getattr(self, f'_decode_{section}', None)
        if not method or len(data) < 12: return None
        return method(data, fb_root(data), text_tables)

    def _decode_capture_ball_data(self, data, root, text_tables):
        vt, to = fb_table(data, root)
        item_list = text_tables.get('items', [])
        out = ['Ball Catch Rate Multipliers']
        # Read all fields as f32 - each is a ball's catch multiplier
        fi = 0
        while True:
            val = fb_field(data, vt, to, fi, '<f')
            if val is None:
                break
            if val != 0.0:
                out.append(f'  field {fi}: {val:.2f}x')
            fi += 1
        return '\n'.join(out)

    def _decode_capture_data(self, data, root, text_tables):
        vt, to = fb_table(data, root)
        out = ['Capture Mechanics']
        svt, sto = fb_sub(data, vt, to, 0)
        if svt:
            status = [('Freeze', 0), ('Sleep', 1), ('Poison', 2), ('Burn', 3), ('Paralysis', 4)]
            bonuses = []
            for name, fi in status:
                v = fb_field(data, svt, sto, fi, '<f')
                if v: bonuses.append(f'{name} {v:.2f}x')
            if bonuses: out.append(f'  Status: {", ".join(bonuses)}')
        rare = fb_field(data, vt, to, 1, '<f')
        if rare: out.append(f'  Shiny bonus: {rare:.2f}x')
        bvt, bto = fb_sub(data, vt, to, 2)
        if bvt:
            cow = fb_field(data, bvt, bto, 0, '<f')
            ncow = fb_field(data, bvt, bto, 1, '<f')
            out.append(f'  Back-strike: coward {cow:.2f}x / brave {ncow:.2f}x')
        oyabun = fb_field(data, vt, to, 6, '<f')
        oyabun_ch = fb_field(data, vt, to, 7, '<f')
        if oyabun: out.append(f'  Alpha penalty: {oyabun:.2f}x (chance {oyabun_ch:.2f})')
        angle = fb_field(data, vt, to, 9, '<i')
        height = fb_field(data, vt, to, 10, '<i')
        if angle: out.append(f'  Back-strike angle: {angle} deg, height: {height}')
        return '\n'.join(out)

    def _decode_capture_zarank_data(self, data, root, text_tables):
        vt, to = fb_table(data, root)
        out = ['ZA Rank Catch Rate Scaling']
        thresh = fb_struct(data, vt, to, 0, '<10i')
        if thresh:
            out.append(f'  Level brackets: {list(thresh)}')
        for ri, rname in enumerate(self.ZA_RANKS):
            ratios = fb_struct(data, vt, to, 1 + ri, '<10f')
            if ratios:
                ratios_str = ' '.join(f'{r:.2f}' for r in ratios)
                out.append(f'  Rank {rname}: [{ratios_str}]')
        return '\n'.join(out)
