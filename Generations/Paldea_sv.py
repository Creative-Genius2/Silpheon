"""Paldea_sv.py: Scarlet / Violet.

Inherits Sinnoh_prequel. Gen IX: Terastallize, open world, Trinity engine.
DLC: The Teal Mask (Kitakami), The Indigo Disk (Blueberry Academy).
"""
from Sinnoh_prequel import Sinnoh_prequel

import struct
from leswitch import fb_field, fb_root, fb_string, fb_table, fb_vector, fb_str, fb_sub, fb_struct, fb_scalars, fb_vec, _vt_off


class Paldea_sv(Sinnoh_prequel):
    """Scarlet / Violet."""

    GAME_CODES = ('SCA', 'SCA', 'SCA', 'VIO', 'VIO', 'VIO')
    TITLE_IDS = (0x0100A3D008C5C000, 0x0100A3D008C5C800, 0x0100A3D008C5D001,
                 0x01008F6008C5E000, 0x01008F6008C5E800, 0x01008F6008C5F001)
    TITLES = ('Pokémon Scarlet', 'Pokémon Scarlet: Version 4.0.0', 'Pokémon Scarlet: Download Key for Version 4.0.0',
              'Pokémon Violet', 'Pokémon Violet: Version 4.0.0', 'Pokémon Violet: Download Key for Version 4.0.0')
    YEAR = 2022

    GEN = 9
    SPECIES_COUNT = 1025

    EVO_WALK_STEPS_WITH = 50
    EVO_UNION_CIRCLE = 51
    EVO_BATTLE_EC25 = 52
    EVO_BATTLE_EC_ELSE = 53
    EVO_COLLECT_999 = 54
    EVO_DEFEAT_EQUALS = 55
    EVO_USE_MOVE_SPECIAL = 56
    EVO_KNOW_MOVE_EC_ELSE = 57
    EVO_KNOW_MOVE_EC25 = 58
    PERSONAL_FIELD_SHIFT = 0  # ZA overrides to -2 (KitakamiDex/BlueberryDex removed)

    # -- Trinity filesystem --
    CONTAINER = 'trinity'
    TRINITY_DATA_PATH = 'arc/data.trpfs'
    TRINITY_DIR_PATH = 'arc/data.trpfd'

    # -- Internal paths (resolved from inside Trinity archive) --
    # Same pml/ pattern as SWSH/PLA once Trinity is unpacked
    PERSONAL_PATH = 'bin/pml/personal'
    LEARNSET_PATH = 'bin/pml/waza_oboe'
    EVOLUTION_PATH = 'bin/pml/evolution'
    MOVE_DATA_PATH = 'bin/pml/waza'
    ITEM_PATH = 'bin/pml/item'
    TEXT_PATH = 'bin/message/English/common'
    TEXT_SCRIPT_PATH = 'bin/message/English/script'
    TRAINER_PATH = 'bin/trainer'
    ENCOUNTER_PATH = 'world/data/encount/pokedata/encount_poke_data'
    RAID_PATH = 'world/data/raid/raid_enemy_table_array'
    FOOD_BUF_PATH = 'world/data/cooking/cooking_buf_data'
    FOOD_RECIPE_PATH = 'world/data/cooking/cooking_recipe_data'
    OUTBREAK_PATH = 'world/data/outbreak/delivery_outbreak_poke_data'
    # ── Shop paths (from pkNX GameDumperSV.cs) ──────────────────────
    SHOP_PATH = 'world/data/ui/shop/friendlyshop/friendlyshop_data/friendlyshop_data_array.bfbs'
    SHOP_LINEUP_PATH = 'world/data/ui/shop/friendlyshop/friendlyshop_lineup_data/friendlyshop_lineup_data_array.bfbs'
    SHOP_MASTER_PATH = 'world/data/ui/shop/shop_data/shop_data_array.bfbs'
    TM_SHOP_PATH = 'world/data/ui/shop/shop_wazamachine/shop_wazamachine_data/shop_wazamachine_data_array.bfbs'
    DRESSUP_SHOP_PATH = 'world/data/ui/shop/dressup_shop/dressup_shop_data/dressup_shop_data_array.bfbs'
    DRESSUP_CATEGORY_PATH = 'world/data/ui/shop/dressup_shop/dressup_category_data/dressup_category_data_array.bfbs'
    DRESSUP_ITEM_PATH = 'world/data/ui/shop/dressup_shop/dressup_item_data/dressup_item_data_array.bfbs'
    RESTAURANT_SHOP_PATH = 'world/data/ui/shop/shop_restaurant/restaurant_shopdata/restaurant_shopdata_array.bfbs'
    RESTAURANT_MENU_PATH = 'world/data/ui/shop/shop_restaurant/restaurant_menudata/restaurant_menudata_array.bfbs'
    RESTAURANT_BUF_PATH = 'world/data/ui/shop/shop_restaurant/restaurant_bufdata/restaurant_bufdata_array.bfbs'

    # ── DLC paths (from pkNX GameDumperSV.cs) ────────────────────────
    # DLC items
    DLC_ITEM_PATH = 'world/data/ui/dlc_item_data/dlc_item_group/dlc_item_group_array.bfbs'
    # Kitakami (Teal Mask) raids
    KITAKAMI_RAID_01 = 'world/data/raid/su1_raid_enemy_01/su1_raid_enemy_01_array.bfbs'
    KITAKAMI_RAID_02 = 'world/data/raid/su1_raid_enemy_02/su1_raid_enemy_02_array.bfbs'
    KITAKAMI_RAID_03 = 'world/data/raid/su1_raid_enemy_03/su1_raid_enemy_03_array.bfbs'
    KITAKAMI_RAID_04 = 'world/data/raid/su1_raid_enemy_04/su1_raid_enemy_04_array.bfbs'
    KITAKAMI_RAID_05 = 'world/data/raid/su1_raid_enemy_05/su1_raid_enemy_05_array.bfbs'
    KITAKAMI_RAID_06 = 'world/data/raid/su1_raid_enemy_06/su1_raid_enemy_06_array.bfbs'
    # Blueberry (Indigo Disk) raids
    BLUEBERRY_RAID_01 = 'world/data/raid/su2_raid_enemy_01/su2_raid_enemy_01_array.bfbs'
    BLUEBERRY_RAID_02 = 'world/data/raid/su2_raid_enemy_02/su2_raid_enemy_02_array.bfbs'
    BLUEBERRY_RAID_03 = 'world/data/raid/su2_raid_enemy_03/su2_raid_enemy_03_array.bfbs'
    BLUEBERRY_RAID_04 = 'world/data/raid/su2_raid_enemy_04/su2_raid_enemy_04_array.bfbs'
    BLUEBERRY_RAID_05 = 'world/data/raid/su2_raid_enemy_05/su2_raid_enemy_05_array.bfbs'
    BLUEBERRY_RAID_06 = 'world/data/raid/su2_raid_enemy_06/su2_raid_enemy_06_array.bfbs'
    # DLC maps
    KITAKAMI_DEST_PATH = 'world/data/ui/ymap/ymap_destination_dlc1_data/ymap_destination_dlc1_data_array.bfbs'
    BLUEBERRY_DEST_PATH = 'world/data/ui/ymap/ymap_destination_dlc2_data/ymap_destination_dlc2_data_array.bfbs'
    KITAKAMI_PLACES_PATH = 'world/data/ui/ymap/ymap_place_name_dlc1_data/ymap_place_name_dlc1_data_array.bfbs'
    BLUEBERRY_PLACES_PATH = 'world/data/ui/ymap/ymap_place_name_dlc2_data/ymap_place_name_dlc2_data_array.bfbs'
    # DLC pokedex
    KITAKAMI_DEX_BLACKLIST = 'world/data/ui/pokedex/blacklist_dlc1/blacklist_dlc1_array.bfbs'
    BLUEBERRY_DEX_BLACKLIST = 'world/data/ui/pokedex/blacklist_dlc2/blacklist_dlc2_array.bfbs'
    KITAKAMI_DEX_DISTRIB = 'world/data/ui/pokedex/distribution_data_dlc1/distribution_data_dlc1_array.bfbs'
    BLUEBERRY_DEX_DISTRIB = 'world/data/ui/pokedex/distribution_data_dlc2/distribution_data_dlc2_array.bfbs'
    KITAKAMI_DEX_MEMO = 'world/data/ui/pokedex/memo_poke_data_dlc1/memo_poke_data_dlc1_array.bfbs'
    BLUEBERRY_DEX_MEMO = 'world/data/ui/pokedex/memo_poke_data_dlc2/memo_poke_data_dlc2_array.bfbs'
    KITAKAMI_DEX_REWARD = 'world/data/ui/pokedex/reward_data_dlc1/reward_data_dlc1_array.bfbs'
    BLUEBERRY_DEX_REWARD = 'world/data/ui/pokedex/reward_data_dlc2/reward_data_dlc2_array.bfbs'

    # -- Removed / restructured from SWSH --
    TRPOKE_PATH = None
    TRAINER_CLASS_PATH = None
    WILD_AREA_PATH = None
    DYNAMAX_PATH = None
    NEST_DATA_PATH = None
    SYMBOL_BEHAVE_PATH = None
    BATTLE_TOWER_POKE_PATH = None
    BATTLE_TOWER_TRAINER_PATH = None
    RENTAL_PATH = None
    GIFT_PATH = 'bin/pokemon/data/poke_add.bin'
    STATIC_ENCOUNTER_PATH = None
    MOVE_SHOP_PATH = None
    GINKGO_ITEM_PATH = None
    GINKGO_TABLE_PATH = None
    MEGA_EVO_PATH = None
    WILD_PATH_E = None
    WILD_PATH_P = None
    TRADE_PATH = None
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
    TRAINER_MAP = None


    FOOD_SKILL = ('None', 'Egg Power', 'Catching Power', 'EXP Power', 'Item Drop',
                  'Raid Power', 'Title Power', 'Sparkling Power', 'Humungo Power',
                  'Teensy Power', 'Encounter Power')

    # Species classification enums (Gen 9+)
    CLASS_MAJOR = {1: 'Legendary', 2: 'Sub-Legendary', 3: 'Mythical'}
    CLASS_MINOR = {1: 'Ultra Beast', 2: 'Paradox (Past)', 4: 'Paradox (Future)', 8: 'Mega Evolution'}

    def get_narc(self, narc_path):
        """Trinity-aware file reader. Reads from trinity_index, unpacks .trpak files."""
        key = narc_path
        if key not in self._narc_cache:
            from leswitch import read_trinity_file
            ti = getattr(self, 'trinity_index', None)
            trpfs = getattr(self, 'TRINITY_DATA_PATH', 'arc/data.trpfs')
            files = []
            ahtb_list = []
            if ti:
                for tpath in sorted(ti.keys()):
                    if not (tpath.startswith(narc_path.rstrip('/')) or tpath == narc_path):
                        continue
                    subfiles = read_trinity_file(self.switch_rom, trpfs, ti, tpath)
                    if subfiles:
                        for f in subfiles:
                            if f[:4] == b'AHTB':
                                ahtb_list.append(f)
                            else:
                                files.append(f)
            if not files:
                # Hash fallback for exact paths not in plaintext index
                from leswitch import _fnv1a_64, _unpack_trpak
                np = narc_path.strip('/')
                h = _fnv1a_64(np)
                # Check TRPFS direct hashes (9.8K .trpak containers)
                h2o = ti.get('__hash_to_offset__') if ti else None
                o2s = ti.get('__offset_to_size__') if ti else None
                if h2o and o2s:
                    off = h2o.get(h)
                    if off is not None:
                        sz = o2s.get(off, 0)
                        trpfs_off = self.switch_rom.files[trpfs][0]
                        raw = self.switch_rom._read(trpfs_off + off, sz)
                        if np.endswith('.trpak'):
                            result = _unpack_trpak(raw)
                            if result:
                                for f in result:
                                    if f[:4] == b'AHTB':
                                        ahtb_list.append(f)
                                    else:
                                        files.append(f)
                        else:
                            files = [raw]
                # Check inner file hashes (178K files inside .trpak containers)
                if not files:
                    ihc = ti.get('__inner_hash_to_container__') if ti else None
                    if ihc:
                        cinfo = ihc.get(h)
                        if cinfo is not None:
                            coff, csz, sub_idx = cinfo
                            trpfs_off = self.switch_rom.files[trpfs][0]
                            raw = self.switch_rom._read(trpfs_off + coff, csz)
                            result = _unpack_trpak(raw)
                            if result:
                                for f in result:
                                    if f[:4] == b'AHTB':
                                        ahtb_list.append(f)
                                data = [f for f in result if f[:4] != b'AHTB']
                                if sub_idx < len(data):
                                    files = [data[sub_idx]]
                                else:
                                    files = data
                if not files:
                    return super().get_narc(narc_path)
            # Enrich __hash_to_path__: scan unpacked files for path strings
            h2p = ti.get('__hash_to_path__') if ti else None
            ihc = ti.get('__inner_hash_to_container__') if ti else None
            if h2p is not None and ihc:
                import re
                _pat = re.compile(rb'[a-z][a-z0-9_]*(?:/[a-z0-9_]+)+\.\w+')
                for f in files + ahtb_list:
                    for m in _pat.finditer(f):
                        ps = m.group().decode('ascii', errors='ignore')
                        h = _fnv1a_64(ps)
                        if h in ihc and h not in h2p:
                            h2p[h] = ps
            class _SwitchNarc:
                pass
            obj = _SwitchNarc()
            obj.files = files
            self._narc_cache[key] = obj
            if ahtb_list:
                self._ahtb_cache[key] = ahtb_list
        return self._narc_cache[key]

    def read_file(self, path):
        """Trinity-aware single file read. Check sketch cache, then trinity_index (plaintext + hash), fall back to RomFS."""
        p = path.strip('/')
        if ':' in p:
            p = p.split(':')[0]
        sc = getattr(self, '_sketch_cache', None)
        if sc and p in sc:
            return sc[p]
        ti = getattr(self, 'trinity_index', None)
        if ti:
            if p in ti:
                from leswitch import read_trinity_file
                trpfs = getattr(self, 'TRINITY_DATA_PATH', 'arc/data.trpfs')
                result = read_trinity_file(self.switch_rom, trpfs, ti, p)
                if result:
                    return result[0]
            else:
                # Hash fallback: 168K inner files only reachable by FNV1a-64
                from leswitch import _fnv1a_64, _unpack_trpak
                h = _fnv1a_64(p)
                # Check TRPFS direct hashes (9.8K .trpak containers)
                h2o = ti.get('__hash_to_offset__')
                o2s = ti.get('__offset_to_size__')
                if h2o and o2s:
                    off = h2o.get(h)
                    if off is not None:
                        sz = o2s.get(off, 0)
                        trpfs = getattr(self, 'TRINITY_DATA_PATH', 'arc/data.trpfs')
                        trpfs_off = self.switch_rom.files[trpfs][0]
                        raw = self.switch_rom._read(trpfs_off + off, sz)
                        if p.endswith('.trpak'):
                            result = _unpack_trpak(raw)
                            if result:
                                return result[0]
                        return raw
                # Check inner file hashes (178K files inside .trpak containers)
                ihc = ti.get('__inner_hash_to_container__')
                if ihc:
                    cinfo = ihc.get(h)
                    if cinfo is not None:
                        coff, csz, sub_idx = cinfo
                        trpfs = getattr(self, 'TRINITY_DATA_PATH', 'arc/data.trpfs')
                        trpfs_off = self.switch_rom.files[trpfs][0]
                        raw = self.switch_rom._read(trpfs_off + coff, csz)
                        result = _unpack_trpak(raw)
                        if result:
                            files = [f for f in result if f[:4] != b'AHTB']
                            if sub_idx < len(files):
                                return files[sub_idx]
        return super().read_file(path)



    def build_trainer_lookup(self):
        """Build 3-hop trainer lookup: trname_key -> NPC_ids -> TrIds -> trdata indices.
        Stores _trid_idx and _trname_to_indices on self."""
        # Map 3: trdata TrId -> array index
        _tdb = self.read_file(getattr(self, 'TRAINER_PATH', ''))
        if not _tdb or len(_tdb) <= 12:
            return
        _trt = fb_root(_tdb)
        _tvt, _tto = fb_table(_tdb, _trt)
        _tvf = _vt_off(_tvt, 0)
        if not _tvf:
            return
        _tcnt, _tdoff = fb_vector(_tdb, _tto, _tvf)
        _idx = {}
        for _i in range(_tcnt):
            _teop = _tdoff + _i * 4
            _terel = struct.unpack_from('<I', _tdb, _teop)[0]
            _tepos = _teop + _terel
            _tevt, _teto = fb_table(_tdb, _tepos)
            _ttrid = fb_str(_tdb, _tevt, _teto, 0) or ''
            if _ttrid:
                _idx[_ttrid] = _i
        self._trid_idx = _idx

        # Map 1: event battle NPC_id -> set(TrIds)
        _evb = self.read_file('ik_event/bin/event_trainer_battle_data/trainer_btl_data_global.bin')
        _npc_trids = {}
        if _evb and len(_evb) > 12:
            _er = fb_root(_evb)
            _evt, _eto = fb_table(_evb, _er)
            _evf = _vt_off(_evt, 0)
            if _evf:
                _ecnt, _edoff = fb_vector(_evb, _eto, _evf)
                for _i in range(_ecnt):
                    _eop = _edoff + _i * 4
                    _erel = struct.unpack_from('<I', _evb, _eop)[0]
                    _epos = _eop + _erel
                    _eevt, _eeto = fb_table(_evb, _epos)
                    _etrid = fb_str(_evb, _eevt, _eeto, 1)
                    _enpc = fb_str(_evb, _eevt, _eeto, 2)
                    if _etrid and _enpc:
                        _npc_trids.setdefault(_enpc, set()).add(_etrid)

        # Map 2: NPC asset trname_key -> set(NPC AssetIds)
        _npcd = self.read_file('world/ik_data/field/npc/npc_asset_data/npc_asset_data/npc_asset_data.bin')
        _trname_npcs = {}
        if _npcd and len(_npcd) > 12:
            _nr = fb_root(_npcd)
            _nvt, _nto = fb_table(_npcd, _nr)
            _nf0 = _vt_off(_nvt, 0)
            if _nf0:
                _ncnt, _ndoff = fb_vector(_npcd, _nto, _nf0)
                for _i in range(_ncnt):
                    _nop = _ndoff + _i * 4
                    _nrel = struct.unpack_from('<I', _npcd, _nop)[0]
                    _npos = _nop + _nrel
                    _naevt, _naeto = fb_table(_npcd, _npos)
                    _aid = fb_str(_npcd, _naevt, _naeto, 0)
                    if not _aid:
                        continue
                    _nif = _vt_off(_naevt, 1)
                    if not _nif:
                        continue
                    _nicnt, _nidoff = fb_vector(_npcd, _naeto, _nif)
                    for _j in range(_nicnt):
                        _niop = _nidoff + _j * 4
                        _nirel = struct.unpack_from('<I', _npcd, _niop)[0]
                        _nipos = _niop + _nirel
                        _nivt, _nito = fb_table(_npcd, _nipos)
                        _nm = fb_str(_npcd, _nivt, _nito, 1)
                        if _nm and len(_nm) < 64 and _nm.isascii():
                            _trname_npcs.setdefault(_nm, set()).add(_aid)

        # Composite: trname_key -> sorted list of trdata indices
        _t2i = {}
        _trid_idx = self._trid_idx
        for _key, _npc_ids in _trname_npcs.items():
            _indices = set()
            if _key in _trid_idx:
                _indices.add(_trid_idx[_key])
            for _nid in _npc_ids:
                for _tid in _npc_trids.get(_nid, set()):
                    if _tid in _trid_idx:
                        _indices.add(_trid_idx[_tid])
            if _indices:
                _t2i[_key] = sorted(_indices)
        self._trname_to_indices = _t2i
        # Reverse: index -> list of trname_keys (for decode_trainer display name)
        _i2t = {}
        for _key, _idxs in _t2i.items():
            for _i in _idxs:
                _i2t.setdefault(_i, []).append(_key)
        self._idx_to_trname = _i2t
        # TrID -> index reverse (for dowse to show TrIDs)
        self._idx_to_trid = {v: k for k, v in _idx.items()}

    def decode_personal(self, data, file_idx, text_tables, tm_table=None):

        """Decode SV personal data (FlatBuffer with sub-tables).
        SV schema has KitakamiDex/BlueberryDex at fields 3-4 (removed in ZA),
        shifting all subsequent fields +2 vs ZA."""
        if len(data) < 12:
            return None

        species_list = text_tables.get('species', [])
        type_list = text_tables.get('type_names', [])
        ability_list = text_tables.get('abilities', [])
        item_list = text_tables.get('items', [])
        moves_list = text_tables.get('moves', [])

        root = fb_root(data)
        vt, to = fb_table(data, root)

        # Field 0: Info (PersonalInfoDetail struct — 16 bytes inline)
        info_off = fb_field(data, vt, to, 0, '<H')
        spec_internal = spec_national = 0
        height = weight = color = debut = 0
        cls_major = cls_minor = form_num = 0
        if info_off:
            base = to + info_off
            spec_internal = struct.unpack_from('<H', data, base)[0]
            form_num = struct.unpack_from('<H', data, base + 2)[0]
            spec_national = struct.unpack_from('<H', data, base + 4)[0]
            color = data[base + 6]
            height = struct.unpack_from('<H', data, base + 8)[0]
            weight = struct.unpack_from('<H', data, base + 10)[0]
            debut = data[base + 12]
            cls_major = data[base + 13]
            cls_minor = struct.unpack_from('<I', data, base + 14)[0]

        # Field 1: IsPresentInGame
        present = fb_field(data, vt, to, 1, '<B')
        present = bool(present) if present is not None else True

        # Field 2: Dex (nullable struct)
        # Fields 3-4: KitakamiDex, BlueberryDex (SV-only, removed in ZA)
        _ps = self.PERSONAL_FIELD_SHIFT
        if _ps == 0:  # SV has DLC dex fields
            kitakami_dex = fb_field(data, vt, to, 3, '<H') or 0
            blueberry_dex = fb_field(data, vt, to, 4, '<H') or 0
        # Types
        type1 = fb_field(data, vt, to, 5 + _ps, '<B') or 0
        type2 = fb_field(data, vt, to, 6 + _ps, '<B') or 0
        # Fields 7-9: Abilities (ZA: 5-7)
        ab1 = fb_field(data, vt, to, 7 + _ps, '<H') or 0
        ab2 = fb_field(data, vt, to, 8 + _ps, '<H') or 0
        abH = fb_field(data, vt, to, 9 + _ps, '<H') or 0
        # Field 10: EXPGrowth, Field 11: CatchRate (ZA: 8-9)
        exp_growth = fb_field(data, vt, to, 10 + _ps, '<B') or 0
        catch_rate = fb_field(data, vt, to, 11 + _ps, '<B') or 0
        # Field 12: Gender struct (ZA: 10)
        gender_off = fb_field(data, vt, to, 12 + _ps, '<H')
        gender_group = gender_ratio = 0
        if gender_off:
            g_base = to + gender_off
            gender_group = data[g_base]
            gender_ratio = data[g_base + 1]
        # Fields 13-14: EggGroups (ZA: 11-12)
        egg1 = fb_field(data, vt, to, 13 + _ps, '<B') or 0
        egg2 = fb_field(data, vt, to, 14 + _ps, '<B') or 0
        # Field 15: Hatch struct (ZA: 13)
        # Field 16: HatchCycles, Field 17: BaseFriendship (ZA: 14-15)
        hatch_cycles = fb_field(data, vt, to, 16 + _ps, '<B') or 0
        friendship = fb_field(data, vt, to, 17 + _ps, '<B') or 0
        # Field 18: BaseEXPAddend (ZA: 16)
        exp_addend = fb_field(data, vt, to, 18 + _ps, '<h') or 0
        # Field 19: EvoStage (ZA: 17)
        evo_stage = fb_field(data, vt, to, 19 + _ps, '<B') or 0
        # Field 20: IsTypeChangeDisallowed (ZA: 18)
        # Field 21: EVYield struct (ZA: 19)
        ev_off = fb_field(data, vt, to, 21 + _ps, '<H')
        evs = []
        if ev_off:
            ev_base = to + ev_off
            for i, stat in enumerate(self.EV_STAT_ORDER):
                val = data[ev_base + i]
                if val: evs.append(f"+{val} {stat}")
        # Field 22: Base stats struct (ZA: 20)
        stat_off = fb_field(data, vt, to, 22 + _ps, '<H')
        hp = atk = dfn = spa = spd = spe = 0
        if stat_off:
            s = to + stat_off
            hp, atk, dfn, spa, spd, spe = data[s], data[s+1], data[s+2], data[s+3], data[s+4], data[s+5]
        bst = hp + atk + dfn + spa + spd + spe

        # Resolve names
        species_name = species_list[spec_national] if spec_national < len(species_list) else f"#{spec_national}"
        t1 = type_list[type1] if type1 < len(type_list) else f"type#{type1}"
        t2 = type_list[type2] if type2 < len(type_list) else f"type#{type2}"
        types_str = t1 if type1 == type2 else f"{t1} / {t2}"

        ability_names = []
        for aid, suffix in ((ab1, ''), (ab2, ''), (abH, ' (Hidden)')):
            if aid > 0:
                name = ability_list[aid] if aid < len(ability_list) else f"ability#{aid}"
                ability_names.append(f"{name}{suffix}")

        gender_str = f"{gender_ratio}% female" if gender_group == 0 else ('Male only', 'Female only', 'Genderless')[gender_group - 1] if 1 <= gender_group <= 3 else f"group#{gender_group}"


        out = [f"{species_name} (#{spec_national})", f"{types_str} | BST {bst}",
               f"HP {hp} | Atk {atk} | Def {dfn} | SpA {spa} | SpD {spd} | Spe {spe}",
               f"Abilities: {' / '.join(ability_names)}" if ability_names else "Abilities: ---"]
        out.append(f"Gender: {gender_str} | Catch Rate: {catch_rate} | Hatch: {hatch_cycles} cycles | Friendship: {friendship}")
        out.append(f"Growth: {self.GROWTH_NAMES[exp_growth]} | Egg Groups: {self.EGG_GROUP_NAMES[egg1]}" +
                   (f" / {self.EGG_GROUP_NAMES[egg2]}" if egg1 != egg2 else ""))
        out.append(f"Height: {height / 100.0}m | Weight: {weight / 10.0}kg")
        out.append(f"Evo Stage: {evo_stage} | EXP Addend: {exp_addend}")
        if evs:
            out.append(f"EVs: {', '.join(evs)}")
        if not present:
            out.append("NOT IN GAME")

        # DLC dex indices (SV-only)
        dex_parts = []
        if kitakami_dex: dex_parts.append(f"Kitakami #{kitakami_dex}")
        if blueberry_dex: dex_parts.append(f"Blueberry #{blueberry_dex}")
        if dex_parts:
            out.append(f"DLC Dex: {' | '.join(dex_parts)}")

        # Classification
        tags = []
        if cls_major in self.CLASS_MAJOR: tags.append(self.CLASS_MAJOR[cls_major])
        if cls_minor in self.CLASS_MINOR: tags.append(self.CLASS_MINOR[cls_minor])
        if tags:
            out.append(f"Classification: {' / '.join(tags)}")

        # Field 23: Evolutions (ZA: 21)
        evo_voff = fb_field(data, vt, to, 23 + _ps, '<H')
        if evo_voff:
            count, doff = fb_vector(data, to, evo_voff)
            for i in range(count):
                e = doff + i * 16
                level = struct.unpack_from('<H', data, e)[0]
                method = struct.unpack_from('<H', data, e + 2)[0]
                arg = struct.unpack_from('<H', data, e + 4)[0]
                target_internal = struct.unpack_from('<H', data, e + 12)[0]
                target_form = struct.unpack_from('<H', data, e + 14)[0]
                tname = species_list[target_internal] if target_internal < len(species_list) else f"#{target_internal}"
                form_str = f"-{target_form}" if target_form else ""
                out.append(f"  Evo: {tname}{form_str} (method {method}, arg {arg}, lv {level})")

        # Field 24: TechnicalMachine (ZA: 22)
        tm_ids = fb_scalars(data, vt, to, 24 + _ps)
        if tm_ids:
            tms = [moves_list[m] if m < len(moves_list) else f"move#{m}" for m in tm_ids]
            out.append(f"TMs ({len(tms)}): {' / '.join(tms)}")

        # Field 25: EggMoves (ZA: 23)
        egg_ids = fb_scalars(data, vt, to, 25 + _ps)
        if egg_ids:
            eggs = [moves_list[m] if m < len(moves_list) else f"move#{m}" for m in egg_ids]
            out.append(f"Egg Moves: {' / '.join(eggs)}")

        # Field 26: ReminderMoves (ZA: 24)
        rem_ids = fb_scalars(data, vt, to, 26)
        if rem_ids:
            rems = [moves_list[m] if m < len(moves_list) else f"move#{m}" for m in rem_ids]
            out.append(f"Reminder: {' / '.join(rems)}")

        # Field 27: Learnset (ZA: 25)
        learn_voff = fb_field(data, vt, to, 27, '<H')
        if learn_voff:
            count, doff = fb_vector(data, to, learn_voff)
            learns = []
            for i in range(count):
                e = doff + i * 4
                mid = struct.unpack_from('<H', data, e)[0]
                level = struct.unpack_from('<b', data, e + 2)[0]
                lplus = data[e + 3]
                mname = moves_list[mid] if mid < len(moves_list) else f"move#{mid}"
                lvl_str = 'EVO' if level == -3 else 'RELEARN' if level == -2 else str(level)
                plus_str = f" {{{lplus}}}" if lplus else ""
                learns.append(f"[{lvl_str}] {mname}{plus_str}")
            if learns:
                out.append(f"Learnset ({len(learns)}):")
                for l in learns:
                    out.append(f"  {l}")

        return "\n".join(out)

    # ── decode_move ─────────────────────────────────────────────────
    def decode_move(self, data, file_idx, text_tables):
        """Decode SV move data (Waza FlatBuffer). Identical schema to ZA."""
        if len(data) < 12:
            return None

        moves_list = text_tables.get('moves', [])
        type_list = text_tables.get('type_names', [])

        root = fb_root(data)
        vt, to = fb_table(data, root)

        move_id = fb_field(data, vt, to, 0, '<H') or 0
        can_use = fb_field(data, vt, to, 1, '<B')
        mtype = fb_field(data, vt, to, 2, '<B') or 0
        quality = fb_field(data, vt, to, 3, '<B') or 0
        category = fb_field(data, vt, to, 4, '<B') or 0
        power = fb_field(data, vt, to, 5, '<B') or 0
        accuracy = fb_field(data, vt, to, 6, '<B') or 0
        pp = fb_field(data, vt, to, 7 + _ps, '<B') or 0
        priority = fb_field(data, vt, to, 8 + _ps, '<b') or 0
        hit_max = fb_field(data, vt, to, 9 + _ps, '<B') or 0
        hit_min = fb_field(data, vt, to, 10 + _ps, '<B') or 0
        inflict_off = fb_field(data, vt, to, 11 + _ps, '<H')
        inflict_val = inflict_chance = 0
        if inflict_off:
            ib = to + inflict_off
            inflict_val = struct.unpack_from('<H', data, ib)[0]
            inflict_chance = data[ib + 2]
        crit = fb_field(data, vt, to, 12 + _ps, '<B') or 0
        flinch = fb_field(data, vt, to, 13 + _ps, '<B') or 0
        effect_seq = fb_field(data, vt, to, 14 + _ps, '<H') or 0
        recoil = fb_field(data, vt, to, 15 + _ps, '<b') or 0
        self_heal = fb_field(data, vt, to, 16 + _ps, '<b') or 0
        dmg_heal = fb_field(data, vt, to, 17 + _ps, '<B') or 0
        target = fb_field(data, vt, to, 18 + _ps, '<B') or 0

        cat_str = self.CATEGORY_NAMES[category]
        move_name = moves_list[move_id] if move_id < len(moves_list) else f"#{move_id}"
        type_name = type_list[mtype] if mtype < len(type_list) else f"type#{mtype}"

        out = [f"{move_name} (#{move_id})", f"{type_name} | {cat_str}"]
        if power: out.append(f"Power: {power}")
        out.append(f"Accuracy: {'--' if accuracy == 101 else accuracy} | PP: {pp}")
        if priority: out.append(f"Priority: {'+' if priority > 0 else ''}{priority}")
        if hit_min and hit_max:
            out.append(f"Hits: {hit_min}-{hit_max}" if hit_min != hit_max else f"Hits: {hit_min}")
        if crit: out.append(f"Crit Stage: +{crit}")
        if flinch: out.append(f"Flinch: {flinch}%")
        if inflict_val and inflict_chance:
            out.append(f"Inflict: status#{inflict_val} ({inflict_chance}%)")
        if recoil: out.append(f"Recoil: {recoil}%")
        if self_heal: out.append(f"Self Heal: {self_heal}%")
        if dmg_heal: out.append(f"Drain: {dmg_heal}%")

        flag_names = [
            (20, 'Contact'), (21, 'Charge'), (22, 'Recharge'), (23, 'Protect'),
            (24, 'Reflectable'), (25, 'Snatch'), (26, 'Mirror'), (27, 'Punch'),
            (28, 'Sound'), (29, 'Dance'), (30, 'Gravity'), (31, 'Defrost'),
            (33, 'Heal'), (34, 'IgnoreSub'), (36, 'AnimateAlly'), (37, 'Metronome'),
            (42, 'Powder'), (43, 'Bite'), (44, 'Bullet'), (47, 'SheerForce'),
            (48, 'Slicing'), (49, 'Wind'),
        ]
        flags = [name for fi, name in flag_names if fb_field(data, vt, to, fi, '<B')]
        if flags:
            out.append(f"Flags: {' / '.join(flags)}")

        return "\n".join(out)

    # ── decode_trainer ─────────────────────────────────────────────
    def decode_trainer(self, data, file_idx, text_tables):
        """Decode SV trainer (TrDataMain FlatBuffer).
        SV schema: TrId/TrNameLabel/TrainerType strings, BattleType, ChangeGem (Tera),
        Poke1-6 at fields 8-13, AI at 14-21.
        Handles both single-entry and array-indexed (trdata_array:N) FlatBuffers."""
        if len(data) < 12:
            return None

        species_list = text_tables.get('species', [])
        moves_list = text_tables.get('moves', [])
        item_list = text_tables.get('items', [])

        root = fb_root(data)
        vt, to = fb_table(data, root)
        # Array-indexed: extract entry N from FlatBuffer vector
        _tf = struct.unpack_from('<H', vt, 4)[0] if len(vt) > 5 else 0
        if _tf and not fb_str(data, vt, to, 0):
            cnt, doff = fb_vector(data, to, _tf)
            if file_idx < cnt:
                _eop = doff + file_idx * 4
                _erel = struct.unpack_from('<I', data, _eop)[0]
                vt, to = fb_table(data, _eop + _erel)

        tr_id = fb_str(data, vt, to, 0) or "?"
        tr_name = fb_str(data, vt, to, 1) or ""
        tr_type = fb_str(data, vt, to, 2) or ""
        is_strong = fb_field(data, vt, to, 3, '<B') or 0
        battle_type = fb_field(data, vt, to, 4, '<B') or 0
        data_type = fb_field(data, vt, to, 5, '<B') or 0
        money_rate = fb_field(data, vt, to, 6, '<B') or 0
        change_gem = fb_field(data, vt, to, 7 + _ps, '<B') or 0

        battle_str = self.BATTLE_TYPES[battle_type] if battle_type < len(self.BATTLE_TYPES) else f'type#{battle_type}'
        out = [f"Trainer: {tr_id} | {tr_type} {tr_name} | {battle_str}"]
        if is_strong:
            out.append("Strong Trainer")
        if change_gem:
            out.append("Terastallizes")

        highest_level = 0
        # Poke1-6 at fields 8-13 (PokeDataBattle sub-tables, same as ZA)
        for slot in range(6):
            pvt, pto = fb_sub(data, vt, to, 8 + slot)
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

        # AI flags (fields 14-21)
        ai_names = ['Basic', 'High', 'Expert', 'Double', 'Raid', 'Weak', 'Item', 'Change']
        ai_flags = [name for i, name in enumerate(ai_names) if fb_field(data, vt, to, 14 + i, '<B')]
        if ai_flags:
            out.append(f"AI: {' / '.join(ai_flags)}")

        return "\n".join(out)


    # ── decode_encounters ─────────────────────────────────────────

    def iter_encounters(self):
        try:
            data = self.read_file(self.ENCOUNTER_PATH)
        except Exception:
            return
        if not data or len(data) < 12: return
        root = fb_root(data)
        vt, to = fb_table(data, root)
        vo = _vt_off(vt, 0)
        if not vo: return
        count, doff = fb_vector(data, to, vo)
        for i in range(count):
            rel = struct.unpack_from('<I', data, doff + i * 4)[0]
            sv, st = fb_table(data, doff + i * 4 + rel)
            species = fb_field(data, sv, st, 0, '<i') or 0
            form = fb_field(data, sv, st, 2, '<b') or 0
            minlv = fb_field(data, sv, st, 3, '<h') or 0
            maxlv = fb_field(data, sv, st, 4, '<h') or 0
            area = fb_str(data, sv, st, 14) or 'Wild'
            if species:
                yield (area, species, form, minlv, maxlv, {'location': area})

    def decode_encounters(self, data, file_idx, text_tables, path='', **kwargs):
        """Decode SV encounter data (EncountPokeData FlatBuffer).
        Biome-based with lot values, area/location strings, band (horde) data."""
        if len(data) < 12:
            return None

        species_list = text_tables.get('species', [])
        root = fb_root(data)
        vt, to = fb_table(data, root)

        dev_id = fb_field(data, vt, to, 0, '<i') or 0
        sex = fb_field(data, vt, to, 1, '<B') or 0
        form = fb_field(data, vt, to, 2, '<b') or 0
        min_lv = fb_field(data, vt, to, 3, '<h') or 0
        max_lv = fb_field(data, vt, to, 4, '<h') or 0
        lot_value = fb_field(data, vt, to, 5, '<h') or 0

        # Biome slots (fields 6-13: 4 pairs of Biome enum + LotValue)
        biomes = []
        for i in range(4):
            biome = fb_field(data, vt, to, 6 + i * 2, '<i') or 0
            blot = fb_field(data, vt, to, 7 + i * 2, '<h') or 0
            if biome and blot:
                biomes.append(f"biome#{biome}:{blot}")

        # Area/Location strings (fields 14-15)
        area = fb_str(data, vt, to, 14 + _ps) or ""
        location = fb_str(data, vt, to, 15 + _ps) or ""

        min_h = fb_field(data, vt, to, 16 + _ps, '<i') or 0
        max_h = fb_field(data, vt, to, 17 + _ps, '<i') or 0

        # Band/horde data (fields 21-25)
        band_rate = fb_field(data, vt, to, 21 + _ps, '<h') or 0
        band_type = fb_field(data, vt, to, 22 + _ps, '<i') or 0
        band_poke = fb_field(data, vt, to, 23 + _ps, '<i') or 0

        outbreak_lot = fb_field(data, vt, to, 26, '<B') or 0

        sp_name = species_list[dev_id] if dev_id < len(species_list) else f"#{dev_id}"
        form_str = f"-{form}" if form else ""
        lv_str = f"Lv{min_lv}" if min_lv == max_lv else f"Lv{min_lv}-{max_lv}"
        sex_str = self.SEX_SYMBOLS[sex] if sex < len(self.SEX_SYMBOLS) else ''

        out = [f"{sp_name}{form_str}{sex_str} {lv_str} (weight {lot_value})"]
        if area or location:
            out.append(f"Area: {area} | Location: {location}")
        if biomes:
            out.append(f"Biomes: {' / '.join(biomes)}")
        if min_h or max_h:
            out.append(f"Height: {min_h}-{max_h}")
        if band_rate:
            bp_name = species_list[band_poke] if band_poke < len(species_list) else f"#{band_poke}"
            out.append(f"Horde: {bp_name} (rate {band_rate}, type {band_type})")
        if outbreak_lot:
            out.append(f"Outbreak weight: {outbreak_lot}")

        return "\n".join(out)

    # ── decode_item ───────────────────────────────────────────────

    def decode_item(self, data, file_idx, text_tables, path='', **kwargs):
        """Decode SV item data (ItemData FlatBuffer).
        Subsets: shop, TM_machine (dispatched by path section)."""
        if len(data) < 12:
            return None

        moves_list = text_tables.get('moves', [])
        root = fb_root(data)
        vt, to = fb_table(data, root)

        item_id = fb_field(data, vt, to, 0, '<i') or 0
        item_type = fb_field(data, vt, to, 1, '<i') or 0
        icon_name = fb_str(data, vt, to, 2) or f"item#{item_id}"
        price = fb_field(data, vt, to, 3, '<i') or 0
        bp = fb_field(data, vt, to, 4, '<i') or 0
        equip_effect = fb_field(data, vt, to, 5, '<i') or 0
        equip_power = fb_field(data, vt, to, 6, '<i') or 0
        machine_waza = fb_field(data, vt, to, 12 + _ps, '<i') or 0
        sort_num = fb_field(data, vt, to, 13 + _ps, '<i') or 0
        item_group = fb_field(data, vt, to, 14 + _ps, '<i') or 0
        group_id = fb_field(data, vt, to, 15 + _ps, '<i') or 0
        pocket = fb_field(data, vt, to, 16 + _ps, '<i') or 0
        field_func = fb_field(data, vt, to, 17 + _ps, '<i') or 0
        battle_func = fb_field(data, vt, to, 18 + _ps, '<i') or 0

        # Healing fields
        heal_hp = fb_field(data, vt, to, 40, '<i') or 0
        revival = fb_field(data, vt, to, 57, '<i') or 0

        out = [f"{icon_name} (#{item_id})"]
        out.append(f"Pocket: {pocket} | Group: {item_group}/{group_id}")
        if price: out.append(f"Price: {price}")
        if bp: out.append(f"BP cost: {bp}")
        if equip_effect: out.append(f"Equip effect: {equip_effect} (power {equip_power})")
        if machine_waza:
            mname = moves_list[machine_waza] if machine_waza < len(moves_list) else f"move#{machine_waza}"
            out.append(f"TM: {mname}")
        if heal_hp: out.append(f"Heals: {heal_hp} HP")
        if revival: out.append(f"Revive: {revival}")

        return "\n".join(out)

    # ── decode_raid ───────────────────────────────────────────────

    def decode_raid(self, data, file_idx, text_tables, path='', **kwargs):
        """Decode SV Tera raid data (RaidEnemyTable → RaidEnemyInfo FlatBuffer).
        Wraps PokeDataBattle for boss pokemon, plus shield/HP/timer mechanics."""
        if len(data) < 12:
            return None

        species_list = text_tables.get('species', [])
        moves_list = text_tables.get('moves', [])
        item_list = text_tables.get('items', [])

        root = fb_root(data)
        vt, to = fb_table(data, root)

        # RaidEnemyTable has one field: Info (RaidEnemyInfo sub-table)
        ivt, ito = fb_sub(data, vt, to, 0)
        if not ivt:
            return None

        rom_ver = fb_field(data, ivt, ito, 0, '<i') or 0
        raid_no = fb_field(data, ivt, ito, 1, '<i') or 0
        group_id = fb_field(data, ivt, ito, 2, '<B') or 0
        difficulty = fb_field(data, ivt, ito, 3, '<i') or 0
        rate = fb_field(data, ivt, ito, 4, '<B') or 0
        capture_rate = fb_field(data, ivt, ito, 7, '<B') or 0
        capture_lv = fb_field(data, ivt, ito, 8, '<B') or 0

        # BossPokePara (field 9) — PokeDataBattle sub-table
        pvt, pto = fb_sub(data, ivt, ito, 9)
        sp_name = "?"
        form_str = ""
        level = 0
        move_names = []
        if pvt:
            dev = fb_field(data, pvt, pto, 0, '<H') or 0
            form = fb_field(data, pvt, pto, 1, '<h') or 0
            level = fb_field(data, pvt, pto, 4, '<i') or 0
            sp_name = species_list[dev] if dev < len(species_list) else f"#{dev}"
            form_str = f"-{form}" if form else ""
            for mi in range(4):
                mvt, mto = fb_sub(data, pvt, pto, 6 + mi)
                if mvt:
                    mid = fb_field(data, mvt, mto, 0, '<H') or 0
                    if mid:
                        move_names.append(moves_list[mid] if mid < len(moves_list) else f"move#{mid}")

        # BossDesc (field 11) — RaidBossData sub-table
        bvt, bto = fb_sub(data, ivt, ito, 11)
        hp_coef = 0
        shield_hp = shield_time = 0
        if bvt:
            hp_coef = fb_field(data, bvt, bto, 0, '<h') or 0
            shield_hp = fb_field(data, bvt, bto, 1, '<B') or 0
            shield_time = fb_field(data, bvt, bto, 2, '<B') or 0

        ver_str = ('', ' [Scarlet]', ' [Violet]')[rom_ver] if rom_ver < 3 else ''
        star_str = f"{'★' * difficulty}" if difficulty else ""

        out = [f"Raid #{raid_no}: {sp_name}{form_str} Lv{level} {star_str}{ver_str}"]
        if move_names:
            out.append(f"Moves: {' / '.join(move_names)}")
        out.append(f"Rate: {rate} | Catch: {capture_rate}% Lv{capture_lv}")
        if hp_coef:
            out.append(f"HP Coef: {hp_coef}x | Shield trigger: {shield_hp}% HP / {shield_time}s")

        return "\n".join(out)

    # ── decode_food ───────────────────────────────────────────────

    def decode_food(self, data, file_idx, text_tables, path='', **kwargs):
        """Decode SV sandwich/cooking data (RecipeData + BufData FlatBuffers).
        Dispatches by path: recipe → ingredients, buf → buff effects."""
        if len(data) < 12:
            return None



        root = fb_root(data)
        vt, to = fb_table(data, root)

        # BufData: sandwich buff effects
        if path == self.FOOD_BUF_PATH:
            bufid = fb_str(data, vt, to, 0) or f"buf#{file_idx}"
            out = [f"Sandwich Buff: {bufid}"]
            for slot in range(3):
                base = 1 + slot * 3
                skill = fb_field(data, vt, to, base, '<i') or 0
                level = fb_field(data, vt, to, base + 1, '<i') or 0
                poke_type = fb_field(data, vt, to, base + 2, '<i') or 0
                if skill:
                    sname = self.FOOD_SKILL[skill] if skill < len(self.FOOD_SKILL) else f'skill#{skill}'
                    out.append(f"  {sname} Lv{level} (type {poke_type})")
            return "\n".join(out)

        # RecipeData: recipe ingredients
        recipe_type = fb_field(data, vt, to, 0, '<i') or 0
        seasonings = []
        for i in range(4):
            s = fb_field(data, vt, to, 1 + i, '<i') or 0
            if s: seasonings.append(f"seasoning#{s}")
        ingredients = []
        for i in range(6):
            ing = fb_field(data, vt, to, 5 + i, '<i') or 0
            if ing: ingredients.append(f"ingredient#{ing}")

        out = [f"Recipe #{file_idx} (type {recipe_type})"]
        if seasonings:
            out.append(f"Seasonings: {' / '.join(seasonings)}")
        if ingredients:
            out.append(f"Ingredients: {' / '.join(ingredients)}")

        return "\n".join(out)

    # ── decode_outbreak ───────────────────────────────────────────

    def decode_outbreak(self, data, file_idx, text_tables, path='', **kwargs):
        """Decode SV mass outbreak data (DeliveryOutbreakPokeData FlatBuffer)."""
        if len(data) < 12:
            return None

        species_list = text_tables.get('species', [])
        root = fb_root(data)
        vt, to = fb_table(data, root)

        ob_id = fb_field(data, vt, to, 0, '<Q') or 0
        dev_id = fb_field(data, vt, to, 1, '<i') or 0
        sex = fb_field(data, vt, to, 2, '<B') or 0
        form = fb_field(data, vt, to, 3, '<b') or 0
        min_lv = fb_field(data, vt, to, 4, '<h') or 0
        max_lv = fb_field(data, vt, to, 5, '<h') or 0

        # Field 11: EnableRarePercentage, Field 12: RarePercentage
        rare_enabled = fb_field(data, vt, to, 11 + _ps, '<B') or 0
        rare_pct = fb_field(data, vt, to, 12 + _ps, '<f') or 0.0

        # Field 15: EnableScaleRange, Fields 16-17: MinScale/MaxScale
        scale_enabled = fb_field(data, vt, to, 15 + _ps, '<B') or 0
        min_scale = fb_field(data, vt, to, 16 + _ps, '<h') or 0
        max_scale = fb_field(data, vt, to, 17 + _ps, '<h') or 0

        sp_name = species_list[dev_id] if dev_id < len(species_list) else f"#{dev_id}"
        form_str = f"-{form}" if form else ""
        sex_str = self.SEX_SYMBOLS[sex] if sex < len(self.SEX_SYMBOLS) else ''
        lv_str = f"Lv{min_lv}" if min_lv == max_lv else f"Lv{min_lv}-{max_lv}"

        out = [f"Outbreak: {sp_name}{form_str}{sex_str} {lv_str} [ID {ob_id:#x}]"]
        if rare_enabled and rare_pct:
            out.append(f"Shiny rate: {rare_pct:.2%}")
        if scale_enabled:
            out.append(f"Scale: {min_scale}-{max_scale}")

        return "\n".join(out)
    FLIPNOTE_PAIRS = {
        'Pokemon Scarlet & Violet': ['SCA', 'VIO'],
    }
