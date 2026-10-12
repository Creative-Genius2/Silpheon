"""Sinnoh_prequel.py: Legends: Arceus.

Inherits Galar_swsh. Ancient Sinnoh (Hisui region). Open-world action RPG.
Agile/Strong style moves, alpha Pokemon, research tasks, crafting.
"""
from Galar_swsh import Galar_swsh

import struct
from leswitch import fb_field, fb_root, fb_str, fb_string, fb_sub, fb_table, fb_vector, _vt_off, unpack_gfpak, _fnv1a_64, unpack_gfpak, _fnv1a_64


class Sinnoh_prequel(Galar_swsh):
    """Legends: Arceus."""

    GAME_CODES = ('PLA',)
    TITLE_IDS = (0x01001F5010DFA000,)
    TITLES = ('Pokémon Legends: Arceus',)
    YEAR = 2022

    SPECIES_COUNT = 242

    EVO_RECOIL_DAMAGE_MALE = 59
    EVO_RECOIL_DAMAGE_FEMALE = 60
    EVO_HISUI = 61
    EVO_USE_ITEM_FULL_MOON = 90
    EVO_USE_MOVE_AGILE = 91
    EVO_USE_MOVE_STRONG = 92

    # -- Paths (from pkNX GameFileMapping.cs) --
    PERSONAL_PATH = 'bin/pml/personal/personal_data_total.perbin'
    LEARNSET_PATH = 'bin/pml/waza_oboe/waza_oboe_total.wazaoboe'
    EVOLUTION_PATH = 'bin/pml/evolution/evolution_data_total.evobin'
    MOVE_DATA_PATH = 'bin/pml/waza'
    ITEM_PATH = 'bin/pml/item/item.dat'
    TEXT_PATH = 'bin/message/English/common'
    TEXT_SCRIPT_PATH = 'bin/message/English/script'
    TRAINER_PATH = 'bin/trainer'

    # -- Encounters --
    STATIC_ENCOUNTER_PATH = 'bin/pokemon/data/poke_event_encount.bin'
    GIFT_PATH = 'bin/pokemon/data/poke_add.bin'
    TRADE_PATH = 'bin/script_event_data/field_trade.bin'
    OUTBREAK_PATH = 'bin/field/encount/huge_outbreak.bin'
    NEW_OUTBREAK_GROUP_PATH = 'bin/field/encount/new_huge_outbreak_group.bin'
    NEW_OUTBREAK_LOTTERY_PATH = 'bin/field/encount/new_huge_outbreak_lottery.bin'

    # -- PLA-specific --
    MOVE_SHOP_PATH = 'bin/appli/wazaremember/bin/wazashop_table.bin'
    POKE_MISC_PATH = 'bin/pokemon/data/poke_misc.bin'
    DEX_RESEARCH_PATH = 'bin/appli/pokedex/res_table/pokedex_research_task_table.bin'
    FIELD_DROPS_PATH = 'bin/pokemon/data/poke_drop_item.bin'
    BATTLE_DROPS_PATH = 'bin/pokemon/data/poke_drop_item_battle.bin'
    SHINY_ROLLS_PATH = 'bin/misc/app_config/pokemon_rare.bin'
    SHOP_PATH = 'bin/appli/shop/bin/ha_shop_data.bin'
    GINKGO_ITEM_PATH = 'bin/event/event_progress/ginkgo/ginkgo_item.bin'
    GINKGO_TABLE_PATH = 'bin/event/event_progress/ginkgo/ginkgo_item_table.bin'
    CRAFT_PATH = 'bin/pokemon/data/poke_make_item.bin'
    THROW_PARAM_PATH = 'bin/pokemon/data/throw_param.bin'
    THROWABLE_PARAM_PATH = 'bin/pokemon/data/throwable_param.bin'

    # -- Container formats --
    PERSONAL_CONTAINER = 'single'
    LEARNSET_CONTAINER = 'single'
    EVOLUTION_CONTAINER = 'single'

    # -- Removed from PLA (not applicable) --
    TRPOKE_PATH = None
    TRAINER_CLASS_PATH = None
    EGG_MOVES_PATH = None
    WILD_AREA_PATH = None
    RESIDENT_GFPAK_PATH = 'bin/archive/field/resident_release.gfpak'
    AREA_SETTINGS_KEY = 'bin/field/resident/AreaSettings.bin'
    PLA_AREA_NAMES = {
        'ha_area00': 'Prelude Beach',
        'ha_area01': 'Obsidian Fieldlands',
        'ha_area02': 'Crimson Mirelands',
        'ha_area03': 'Cobalt Coastlands',
        'ha_area04': 'Coronet Highlands',
        'ha_area05': 'Alabaster Icelands',
        'ha_area06': 'Ancient Retreat',
        'ha_area11': 'Temple of Sinnoh',
    }

    RESIDENT_GFPAK_PATH = 'bin/archive/field/resident_release.gfpak'
    AREA_SETTINGS_KEY = 'bin/field/resident/AreaSettings.bin'
    PLA_AREA_NAMES = {
        'ha_area00': 'Prelude Beach',
        'ha_area01': 'Obsidian Fieldlands',
        'ha_area02': 'Crimson Mirelands',
        'ha_area03': 'Cobalt Coastlands',
        'ha_area04': 'Coronet Highlands',
        'ha_area05': 'Alabaster Icelands',
        'ha_area06': 'Ancient Retreat',
        'ha_area11': 'Temple of Sinnoh',
    }
    BATTLE_TOWER_POKE_PATH = None
    BATTLE_TOWER_TRAINER_PATH = None
    DYNAMAX_PATH = None
    NEST_DATA_PATH = None
    RENTAL_PATH = None
    SYMBOL_BEHAVE_PATH = None
    MEGA_EVO_PATH = None
    WILD_PATH_E = None
    WILD_PATH_P = None


    def decode_personal(self, data, file_idx, text_tables, tm_table=None):
        """Decode PLA personal data (FlatBuffer). Flat schema — no sub-tables.
        Stats at fields 8-13, types 3-4, abilities 5-7, MoveShop bitfields at 56-57."""
        if len(data) < 12:
            return None

        species_list = text_tables.get('species', [])
        type_list = text_tables.get('type_names', [])
        ability_list = text_tables.get('abilities', [])
        item_list = text_tables.get('items', [])

        root = fb_root(data)
        vt, to = fb_table(data, root)

        # Container unwrap: root has 1 field (vector of entries) — extract entry[file_idx]
        vec_foff = _vt_off(vt, 0)
        if vec_foff:
            count, doff = fb_vector(data, to, vec_foff)
            if count > 1:
                if file_idx >= count:
                    return f"Entry {file_idx} out of range ({count} entries)"
                elem_off = doff + file_idx * 4
                ptr = struct.unpack_from('<I', data, elem_off)[0]
                vt, to = fb_table(data, elem_off + ptr)

        dex_national = fb_field(data, vt, to, 0, '<H') or 0
        form = fb_field(data, vt, to, 1, '<H') or 0
        present = fb_field(data, vt, to, 2, '<B')
        present = bool(present) if present is not None else True

        type1 = fb_field(data, vt, to, 3, '<B') or 0
        type2 = fb_field(data, vt, to, 4, '<B') or 0
        ab1 = fb_field(data, vt, to, 5, '<H') or 0
        ab2 = fb_field(data, vt, to, 6, '<H') or 0
        abH = fb_field(data, vt, to, 7, '<H') or 0

        hp = fb_field(data, vt, to, 8, '<B') or 0
        atk = fb_field(data, vt, to, 9, '<B') or 0
        dfn = fb_field(data, vt, to, 10, '<B') or 0
        spa = fb_field(data, vt, to, 11, '<B') or 0
        spd = fb_field(data, vt, to, 12, '<B') or 0
        spe = fb_field(data, vt, to, 13, '<B') or 0
        bst = hp + atk + dfn + spa + spd + spe

        gender = fb_field(data, vt, to, 14, '<B') or 0
        exp_growth = fb_field(data, vt, to, 15, '<B') or 0
        evo_stage = fb_field(data, vt, to, 16, '<B') or 0
        catch_rate = fb_field(data, vt, to, 17, '<B') or 0
        color = fb_field(data, vt, to, 19, '<B') or 0
        height = fb_field(data, vt, to, 20, '<H') or 0
        weight = fb_field(data, vt, to, 21, '<H') or 0
        base_exp = fb_field(data, vt, to, 31, '<H') or 0

        # EVs (fields 32-37)
        evs = []
        ev_names = ('HP', 'Atk', 'Def', 'SpA', 'SpD', 'Spe')
        for i, name in enumerate(ev_names):
            val = fb_field(data, vt, to, 32 + i, '<B') or 0
            if val: evs.append(f"+{val} {name}")

        # Held items (fields 38-40)
        items = []
        for i in range(3):
            iid = fb_field(data, vt, to, 38 + i, '<H') or 0
            if iid:
                iname = item_list[iid] if iid < len(item_list) else f"item#{iid}"
                items.append(iname)

        egg1 = fb_field(data, vt, to, 41, '<B') or 0
        egg2 = fb_field(data, vt, to, 42, '<B') or 0
        hatch_species = fb_field(data, vt, to, 43, '<H') or 0
        hatch_cycles = fb_field(data, vt, to, 47, '<B') or 0
        friendship = fb_field(data, vt, to, 48, '<B') or 0
        dex_hisui = fb_field(data, vt, to, 49, '<H') or 0
        is_regional = fb_field(data, vt, to, 45, '<B') or 0

        # Resolve names
        species_name = species_list[dex_national] if dex_national < len(species_list) else f"#{dex_national}"
        # Apply form name (Hisuian Arcanine, Giratina (Origin Forme), etc.)
        fl = self.FORM_NAMES.get((dex_national, form))
        if fl and fl in self.REGIONAL_PREFIXES:
            species_name = f"{fl} {species_name}"
        elif fl:
            species_name = f"{species_name} ({fl})"
        elif form:
            species_name = f"{species_name} (Form {form})"
        t1 = type_list[type1] if type1 < len(type_list) else f"type#{type1}"
        t2 = type_list[type2] if type2 < len(type_list) else f"type#{type2}"
        types_str = t1 if type1 == type2 else f"{t1} / {t2}"

        ability_names = []
        for aid, suffix in ((ab1, ''), (ab2, ''), (abH, ' (Hidden)')):
            if aid > 0:
                name = ability_list[aid] if aid < len(ability_list) else f"ability#{aid}"
                ability_names.append(f"{name}{suffix}")

        out = [f"{species_name} (#{dex_national})", f"{types_str} | BST {bst}",
               f"HP {hp} | Atk {atk} | Def {dfn} | SpA {spa} | SpD {spd} | Spe {spe}",
               f"Abilities: {' / '.join(ability_names)}" if ability_names else "Abilities: ---"]
        out.append(f"Gender: {gender} | Catch Rate: {catch_rate} | Hatch: {hatch_cycles} cycles | Friendship: {friendship}")
        out.append(f"Growth: {self.GROWTH_NAMES[exp_growth]} | Egg Groups: {self.EGG_GROUP_NAMES[egg1]}" +
                   (f" / {self.EGG_GROUP_NAMES[egg2]}" if egg1 != egg2 else ""))
        out.append(f"Height: {height / 100.0}m | Weight: {weight / 10.0}kg")
        out.append(f"Evo Stage: {evo_stage} | Base EXP: {base_exp}")
        if evs:
            out.append(f"EVs: {', '.join(evs)}")
        if items:
            out.append(f"Held items: {' / '.join(items)}")
        if dex_hisui:
            out.append(f"Hisui Dex: #{dex_hisui}")
        if not present:
            out.append("NOT IN GAME")

        return "\n".join(out)

    # ── decode_move ───────────────────────────────────────────────

    def decode_move(self, data, file_idx, text_tables):
        """Decode PLA move data (Waza FlatBuffer). Includes Agile/Strong style modifiers."""
        if len(data) < 12:
            return None

        moves_list = text_tables.get('moves', [])
        type_list = text_tables.get('type_names', [])

        root = fb_root(data)
        vt, to = fb_table(data, root)

        move_id = fb_field(data, vt, to, 0, '<i') or 0
        mtype = fb_field(data, vt, to, 2, '<B') or 0
        category = fb_field(data, vt, to, 4, '<B') or 0
        power = fb_field(data, vt, to, 5, '<B') or 0
        accuracy = fb_field(data, vt, to, 6, '<B') or 0
        pp = fb_field(data, vt, to, 7, '<B') or 0
        priority = fb_field(data, vt, to, 8, '<b') or 0
        hit_max = fb_field(data, vt, to, 9, '<B') or 0
        hit_min = fb_field(data, vt, to, 10, '<B') or 0
        inflict = fb_field(data, vt, to, 11, '<h') or 0
        inflict_pct = fb_field(data, vt, to, 12, '<B') or 0
        crit = fb_field(data, vt, to, 16, '<B') or 0
        flinch = fb_field(data, vt, to, 17, '<B') or 0
        recoil = fb_field(data, vt, to, 19, '<B') or 0
        healing = fb_field(data, vt, to, 20, '<B') or 0

        # Agile/Strong style (field 68+)
        can_style = fb_field(data, vt, to, 68, '<B') or 0
        agile_power = fb_field(data, vt, to, 74, '<B') or 0
        strong_power = fb_field(data, vt, to, 79, '<B') or 0
        strong_acc = fb_field(data, vt, to, 80, '<B') or 0
        strong_crit = fb_field(data, vt, to, 81, '<B') or 0

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
        if inflict and inflict_pct:
            out.append(f"Inflict: status#{inflict} ({inflict_pct}%)")
        if recoil: out.append(f"Recoil: {recoil}%")
        if healing: out.append(f"Healing: {healing}%")

        # Style info
        if can_style:
            style_parts = []
            if agile_power: style_parts.append(f"Agile Power: {agile_power}")
            if strong_power: style_parts.append(f"Strong Power: {strong_power}")
            if strong_acc: style_parts.append(f"Strong Acc: {strong_acc}")
            if strong_crit: style_parts.append(f"Strong Crit: +{strong_crit}")
            out.append(f"Styles: {' | '.join(style_parts)}" if style_parts else "Styles: Yes")

        # Flags
        flag_names = [
            (35, 'Contact'), (36, 'Charge'), (37, 'Recharge'), (38, 'Protect'),
            (39, 'Reflectable'), (40, 'Snatch'), (41, 'Mirror'), (42, 'Punch'),
            (43, 'Sound'), (44, 'Gravity'), (45, 'Defrost'), (47, 'Heal'),
            (48, 'IgnoreSub'), (50, 'AnimateAlly'), (51, 'Dance'), (52, 'Metronome'),
        ]
        flags = [name for fi, name in flag_names if fb_field(data, vt, to, fi, '<B')]
        if flags:
            out.append(f"Flags: {' / '.join(flags)}")

        return "\n".join(out)

    # ── iter_encounters ───

    def iter_encounters(self):
        raw = self.switch_rom.read_file(self.RESIDENT_GFPAK_PATH)
        pack = unpack_gfpak(raw)
        settings = pack.get(_fnv1a_64(self.AREA_SETTINGS_KEY))
        if not settings: return
        root = fb_root(settings)
        vt, to = fb_table(settings, root)
        vo = _vt_off(vt, 0)
        if not vo: return
        count, doff = fb_vector(settings, to, vo)
        seen = set()
        for i in range(count):
            rel = struct.unpack_from('<I', settings, doff + i * 4)[0]
            sv, st = fb_table(settings, doff + i * 4 + rel)
            name = fb_str(settings, sv, st, 0) or ''
            enc_path = fb_str(settings, sv, st, 18) or ''
            if not enc_path or enc_path in seen: continue
            seen.add(enc_path)
            base = name.split('_s')[0] if '_s' in name else name
            if base not in self.PLA_AREA_NAMES: continue
            label = self.PLA_AREA_NAMES[base]
            enc_data = pack.get(_fnv1a_64(enc_path))
            if not enc_data: continue
            eroot = fb_root(enc_data)
            evt, eto = fb_table(enc_data, eroot)
            evo = _vt_off(evt, 0)
            if not evo: continue
            tc, td = fb_vector(enc_data, eto, evo)
            for t in range(tc):
                trel = struct.unpack_from('<I', enc_data, td + t * 4)[0]
                tv, tt = fb_table(enc_data, td + t * 4 + trel)
                minlv = fb_field(enc_data, tv, tt, 1, '<i') or 0
                maxlv = fb_field(enc_data, tv, tt, 2, '<i') or 0
                svo = _vt_off(tv, 3)
                if not svo: continue
                sc, sd = fb_vector(enc_data, tt, svo)
                for s in range(sc):
                    srel = struct.unpack_from('<I', enc_data, sd + s * 4)[0]
                    ssv, sst = fb_table(enc_data, sd + s * 4 + srel)
                    species = fb_field(enc_data, ssv, sst, 0, '<i') or 0
                    form = fb_field(enc_data, ssv, sst, 3, '<i') or 0
                    if species:
                        yield (label, species, form, minlv, maxlv)

    # ── decode_encounters ─────────────────────────────────────────

    def decode_encounters(self, data, file_idx, text_tables, path='', **kwargs):
        """Decode PLA encounter slot (EncounterSlot FlatBuffer).
        Includes alpha traits, IVs/GVs, movesets, time/weather multipliers."""
        if len(data) < 12:
            return None

        species_list = text_tables.get('species', [])
        moves_list = text_tables.get('moves', [])
        root = fb_root(data)
        vt, to = fb_table(data, root)

        species = fb_field(data, vt, to, 0, '<i') or 0
        gender = fb_field(data, vt, to, 2, '<i') or 0
        form = fb_field(data, vt, to, 3, '<i') or 0
        shiny_lock = fb_field(data, vt, to, 4, '<i') or 0
        nature = fb_field(data, vt, to, 6, '<i') or 0
        num_perfect_ivs = fb_field(data, vt, to, 24, '<i') or 0
        base_prob = fb_field(data, vt, to, 28, '<i') or 0
        min_lv = fb_field(data, vt, to, 29, '<i') or 0
        max_lv = fb_field(data, vt, to, 30, '<i') or 0

        # Moveset (fields 33-36, with mastered flags 37-40)
        has_moveset = fb_field(data, vt, to, 32, '<B') or 0
        move_names = []
        if has_moveset:
            for mi in range(4):
                mid = fb_field(data, vt, to, 33 + mi, '<i') or 0
                mastered = fb_field(data, vt, to, 37 + mi, '<B') or 0
                if mid:
                    mname = moves_list[mid] if mid < len(moves_list) else f"move#{mid}"
                    move_names.append(f"{mname}{'*' if mastered else ''}")

        # Oyabun/Alpha traits (field 46)
        oybn_off = fb_field(data, vt, to, 46, '<H')
        is_alpha = False
        if oybn_off:
            o_abs = to + oybn_off
            o_sub = o_abs + struct.unpack_from('<I', data, o_abs)[0]
            ovt, oto = fb_table(data, o_sub)
            is_alpha = bool(fb_field(data, ovt, oto, 0, '<B') or 0)

        sp_name = species_list[species] if species < len(species_list) else f"#{species}"
        fl = self.FORM_NAMES.get((species, form))
        if fl and fl in self.REGIONAL_PREFIXES:
            sp_name = f"{fl} {sp_name}"
        elif fl:
            sp_name += f" ({fl})"
        elif form:
            sp_name += f" (Form {form})"
        lv_str = f"Lv{min_lv}" if min_lv == max_lv else f"Lv{min_lv}-{max_lv}"
        sex_str = self.SEX_SYMBOLS[gender] if gender < len(self.SEX_SYMBOLS) else ''
        shiny_str = '' if shiny_lock == 0 else ' *ShinyLocked*' if shiny_lock == 1 else ' *AlwaysShiny*'

        out = [f"{sp_name}{sex_str} {lv_str}{shiny_str} (weight {base_prob})"]
        if is_alpha:
            out.append("α")
        if num_perfect_ivs:
            out.append(f"IVs: {num_perfect_ivs} perfect")
        if nature:
            out.append(f"Nature: fixed #{nature}")
        if move_names:
            out.append(f"Moves: {' / '.join(move_names)}")

        return "\n".join(out)

    # ── decode_trainer ────────────────────────────────────────────

    def decode_trainer(self, data, file_idx, text_tables, path='', **kwargs):
        """Decode PLA trainer (TrainerData FlatBuffer).
        Matches Gen 4-7 formatting: class+name header, Team: block, footer."""
        if len(data) < 12:
            return None

        species_list = text_tables.get('species', [])
        moves_list = text_tables.get('moves', [])
        natures_list = text_tables.get('natures', [])

        GENDER_SYM = {0: ' ♂', 1: ' ♀'}

        root = fb_root(data)
        vt, to = fb_table(data, root)

        # Music (field 3)
        music_tag = fb_str(data, vt, to, 3) or ''
        music_name = self.BATTLE_MUSIC.get(music_tag, music_tag)

        # Trainer identity from filename prefix → TRAINER_MAP
        trainer_id = ''
        trainer_name = f'Trainer #{file_idx}'
        class_name = ''
        if path:
            fname = path.rsplit('/', 1)[-1]
            bare = fname.replace('trdata_', '').replace('.bin', '')
            trainer_id = bare
            for prefix, name, cls in self.TRAINER_MAP:
                if bare.startswith(prefix):
                    trainer_name = name
                    class_name = cls
                    break

        # Header
        if class_name:
            lines = [f"{class_name} {trainer_name} (#{trainer_id})"]
        else:
            lines = [f"{trainer_name} (#{trainer_id})"]
        lines.append('')

        # Team (field 22)
        has_alpha = False
        has_mastered = False

        team_voff = _vt_off(vt, 22)
        if team_voff:
            count, doff = fb_vector(data, to, team_voff)
            lines.append('Team:')
            for i in range(count):
                elem_off = doff + i * 4
                ptr = struct.unpack_from('<I', data, elem_off)[0]
                p_abs = elem_off + ptr
                pvt, pto = fb_table(data, p_abs)

                species = fb_field(data, pvt, pto, 0, '<i') or 0
                form = fb_field(data, pvt, pto, 1, '<i') or 0
                level = fb_field(data, pvt, pto, 6, '<i') or 0
                nature = fb_field(data, pvt, pto, 7, '<i') or 0
                gender = fb_field(data, pvt, pto, 8, '<i') or 0
                shiny = fb_field(data, pvt, pto, 15, '<B') or 0
                is_alpha = fb_field(data, pvt, pto, 16, '<B') or 0

                sp_name = species_list[species] if species < len(species_list) else f'#{species}'
                fl = self.FORM_NAMES.get((species, form))
                if fl and fl in self.REGIONAL_PREFIXES:
                    sp_name = f"{fl} {sp_name}"
                elif fl:
                    sp_name += f" ({fl})"
                elif form:
                    sp_name += f" (Form {form})"
                gender_str = GENDER_SYM.get(gender, '')

                tags = ''
                if is_alpha:
                    tags += '  α'
                    has_alpha = True
                if shiny:
                    tags += '  ✨'

                lines.append(f"{sp_name}{gender_str} (Lv. {level}){tags}")

                # Nature
                if natures_list and 0 <= nature < len(natures_list):
                    lines.append(f"{natures_list[nature]} Nature")

                # Moves (fields 2-5, WazaSet sub-tables)
                move_names = []
                for mi in range(4):
                    mvt, mto = fb_sub(data, pvt, pto, 2 + mi)
                    if mvt is not None:
                        mid = fb_field(data, mvt, mto, 0, '<i') or 0
                        mastered = fb_field(data, mvt, mto, 1, '<B') or 0
                        if mid:
                            mname = moves_list[mid] if mid < len(moves_list) else f'move#{mid}'
                            if mastered:
                                mname += '*'
                                has_mastered = True
                            move_names.append(mname)
                if move_names:
                    lines.append(' / '.join(move_names))

                lines.append('')

        # Footer
        if music_name:
            lines.append(f'Battle Theme: {music_name}')
        legend = []
        if has_alpha:
            legend.append('α = This Pokémon is an Alpha Pokémon')
        if has_mastered:
            legend.append('* next to a move = This move has been mastered')
        if legend:
            lines.append(' | '.join(legend))

        return '\n'.join(lines)

    # ── decode_item ───────────────────────────────────────────────

    def decode_item(self, data, file_idx, text_tables, path='', **kwargs):
        """Decode PLA item-related data. Subsets: drops, craftworks.
        Dispatches by path: drop_item → field/battle drops, craft → MakeList recipes."""
        if len(data) < 12:
            return None

        item_list = text_tables.get('items', [])
        root = fb_root(data)
        vt, to = fb_table(data, root)

        # Craftworks (MakeList): RecipeID, RecipeItemID, ResultItemID, materials
        if path == self.CRAFT_PATH:
            recipe_id = fb_field(data, vt, to, 0, '<B') or 0
            recipe_item = fb_field(data, vt, to, 1, '<I') or 0
            result_item = fb_field(data, vt, to, 2, '<I') or 0
            result_qty = fb_field(data, vt, to, 3, '<I') or 0

            rname = item_list[result_item] if result_item < len(item_list) else f"item#{result_item}"
            out = [f"Recipe #{recipe_id}: {rname} x{result_qty}"]
            for i in range(4):
                mat_id = fb_field(data, vt, to, 4 + i * 2, '<I') or 0
                mat_qty = fb_field(data, vt, to, 5 + i * 2, '<I') or 0
                if mat_id:
                    mname = item_list[mat_id] if mat_id < len(item_list) else f"item#{mat_id}"
                    out.append(f"  {mname} x{mat_qty}")
            return "\n".join(out)

        # Battle drops: 5 pairs of (rate, item_index)
        if path == self.BATTLE_DROPS_PATH:
            out = [f"Battle Drops #{file_idx}"]
            for i in range(5):
                rate = fb_field(data, vt, to, i * 2, '<i') or 0
                item_id = fb_field(data, vt, to, i * 2 + 1, '<i') or 0
                if rate and item_id:
                    iname = item_list[item_id] if item_id < len(item_list) else f"item#{item_id}"
                    out.append(f"  {iname} ({rate}%)")
            return "\n".join(out)

        # Field drops: hash, regular item+prob, rare item+prob
        drop_hash = fb_field(data, vt, to, 0, '<Q') or 0
        reg_item = fb_field(data, vt, to, 1, '<i') or 0
        reg_prob = fb_field(data, vt, to, 2, '<i') or 0
        rare_item = fb_field(data, vt, to, 3, '<i') or 0
        rare_prob = fb_field(data, vt, to, 4, '<i') or 0

        out = [f"Drops [{drop_hash:#x}]"]
        if reg_item:
            rname = item_list[reg_item] if reg_item < len(item_list) else f"item#{reg_item}"
            out.append(f"  Regular: {rname} ({reg_prob}%)")
        if rare_item:
            rname = item_list[rare_item] if rare_item < len(item_list) else f"item#{rare_item}"
            out.append(f"  Rare: {rname} ({rare_prob}%)")
        return "\n".join(out)

    # ── decode_outbreak ───────────────────────────────────────────

    def decode_outbreak(self, data, file_idx, text_tables, path='', **kwargs):
        """Decode PLA mass outbreak data (NewHugeOutbreakLottery FlatBuffer).
        Lottery-based spawning with outbreak chances and thresholds."""
        if len(data) < 12:
            return None

        root = fb_root(data)
        vt, to = fb_table(data, root)

        ob_hash = fb_field(data, vt, to, 0, '<Q') or 0
        group_off = fb_field(data, vt, to, 1, '<H')
        group_str = fb_string(data, to, group_off) if group_off else "?"
        chance = fb_field(data, vt, to, 2, '<i') or 0
        total_min = fb_field(data, vt, to, 3, '<i') or 0
        total_max = fb_field(data, vt, to, 4, '<i') or 0
        rare2 = fb_field(data, vt, to, 5, '<i') or 0
        rare1 = fb_field(data, vt, to, 6, '<i') or 0
        first_min = fb_field(data, vt, to, 7, '<i') or 0
        first_max = fb_field(data, vt, to, 8, '<i') or 0
        second_min = fb_field(data, vt, to, 9, '<i') or 0
        second_max = fb_field(data, vt, to, 10, '<i') or 0

        out = [f"Outbreak: {group_str} [{ob_hash:#x}]"]
        out.append(f"Chance: {chance}% | Total: {total_min}-{total_max}")
        out.append(f"Wave 1: {first_min}-{first_max} | Wave 2: {second_min}-{second_max}")
        if rare1 or rare2:
            out.append(f"Rare rates: tier1={rare1}% tier2={rare2}%")

        return "\n".join(out)

    # ── decode_research ───────────────────────────────────────────

    def decode_research(self, data, file_idx, text_tables, path='', **kwargs):
        """Decode PLA Pokedex research tasks (PokedexResearchTask FlatBuffer).
        Subset: wld (throw/catch mechanics) dispatched by path."""
        if len(data) < 12:
            return None

        # Throw/catch subset (decode_wld)
        if path == self.THROW_PARAM_PATH or path == self.THROWABLE_PARAM_PATH:
            return self._decode_wld(data, file_idx, text_tables)

        species_list = text_tables.get('species', [])
        moves_list = text_tables.get('moves', [])
        root = fb_root(data)
        vt, to = fb_table(data, root)

        TASK_TYPES = ('Unknown', 'Use Move', 'Defeat')

        species = fb_field(data, vt, to, 0, '<i') or 0
        task_type = fb_field(data, vt, to, 1, '<i') or 0
        threshold = fb_field(data, vt, to, 2, '<i') or 0
        move = fb_field(data, vt, to, 3, '<i') or 0
        move_type = fb_field(data, vt, to, 4, '<i') or 0
        time_of_day = fb_field(data, vt, to, 5, '<i') or 0
        points_single = fb_field(data, vt, to, 13, '<i') or 0
        points_bonus = fb_field(data, vt, to, 14, '<i') or 0
        required = fb_field(data, vt, to, 15, '<B') or 0

        sp_name = species_list[species] if species < len(species_list) else f"#{species}"
        type_str = TASK_TYPES[task_type] if task_type < len(TASK_TYPES) else f'type#{task_type}'

        out = [f"Research: {sp_name} — {type_str}"]
        if move:
            mname = moves_list[move] if move < len(moves_list) else f"move#{move}"
            out.append(f"Move: {mname}")
        if threshold:
            out.append(f"Threshold: {threshold}")

        # Progressive thresholds (fields 9-13)
        thresholds = []
        for i in range(5):
            t = fb_field(data, vt, to, 9 + i, '<i') or 0
            if t: thresholds.append(str(t))
        if thresholds:
            out.append(f"Milestones: {'/'.join(thresholds)}")

        out.append(f"Points: {points_single}" + (f" (bonus: {points_bonus})" if points_bonus else ""))
        if required:
            out.append("Required for completion")

        return "\n".join(out)

    def _decode_wld(self, data, file_idx, text_tables):
        """Decode PLA throw/catch parameters (ThrowParam / ThrowableParam)."""
        root = fb_root(data)
        vt, to = fb_table(data, root)

        # Try ThrowableParam first (has ItemID at field 0 as int)
        item_id = fb_field(data, vt, to, 0, '<i') or 0
        field_05 = fb_field(data, vt, to, 5, '<i')

        if field_05 is not None:
            # ThrowableParam format
            item_list = text_tables.get('items', [])
            iname = item_list[item_id] if item_id < len(item_list) else f"item#{item_id}"
            return f"Throwable: {iname} (#{item_id})"

        # ThrowParam format (velocity, arc, gravity, angle)
        velocity = fb_field(data, vt, to, 1, '<f') or 0.0
        arc = fb_field(data, vt, to, 2, '<f') or 0.0
        gravity = fb_field(data, vt, to, 3, '<f') or 0.0
        angle = fb_field(data, vt, to, 4, '<f') or 0.0

        return f"Throw params | Velocity: {velocity:.1f} | Arc: {arc:.1f} | Gravity: {gravity:.1f} | Angle: {angle:.1f}"

    # ── decode_moveshop ───────────────────────────────────────────

    def decode_moveshop(self, data, file_idx, text_tables):
        """Decode PLA move tutor shop (MoveShopIndex FlatBuffer)."""
        if len(data) < 12:
            return None

        moves_list = text_tables.get('moves', [])
        root = fb_root(data)
        vt, to = fb_table(data, root)

        index = fb_field(data, vt, to, 0, '<i') or 0
        move_id = fb_field(data, vt, to, 1, '<i') or 0
        price = fb_field(data, vt, to, 2, '<i') or 0

        move_name = moves_list[move_id] if move_id < len(moves_list) else f"move#{move_id}"
        return f"Shop #{index}: {move_name} (#{move_id}) — {price} pts"


    def build_personal_index(self, data):
        """Scan FlatBuffer personal container, build species_id -> container_index map.
        Forms are interleaved, so container index != national dex number.
        Only maps base forms (form 0) — form variants get index+N."""
        root = fb_root(data)
        vt, to = fb_table(data, root)
        vec_foff = _vt_off(vt, 0)
        if not vec_foff:
            return {}
        count, doff = fb_vector(data, to, vec_foff)
        sp_map = {}  # species_id -> container_index (base form only)
        form_map = {}  # container_index -> (species_id, form)
        for i in range(count):
            elem_off = doff + i * 4
            ptr = struct.unpack_from('<I', data, elem_off)[0]
            evT, eTO = fb_table(data, elem_off + ptr)
            dex = fb_field(data, evT, eTO, 0, '<H') or 0
            form = fb_field(data, evT, eTO, 1, '<H') or 0
            # Check base stats - all zeros = placeholder, not a real entry
            hp = fb_field(data, evT, eTO, 8, '<B') or 0
            atk = fb_field(data, evT, eTO, 9, '<B') or 0
            real = (hp + atk) > 0
            form_map[i] = (dex, form)
            if real and dex not in sp_map:
                sp_map[dex] = i
        self.personal_species_map = sp_map
        self.personal_form_map = form_map
        return sp_map


    # Regional prefixes get prepended ("Hisuian Arcanine")
    # Everything else goes in parens ("Giratina (Origin Forme)")
    REGIONAL_PREFIXES = {'Hisuian', 'Alolan', 'Galarian'}

    FORM_NAMES = {
        # Hisuian forms (form 1 = Hisuian for all)
        (58, 1): "Hisuian", (59, 1): "Hisuian",       # Growlithe, Arcanine
        (100, 1): "Hisuian", (101, 1): "Hisuian",     # Voltorb, Electrode
        (157, 1): "Hisuian",                           # Typhlosion
        (211, 1): "Hisuian",                           # Qwilfish
        (215, 1): "Hisuian",                           # Sneasel
        (503, 1): "Hisuian",                           # Samurott
        (549, 1): "Hisuian",                           # Lilligant
        (570, 1): "Hisuian", (571, 1): "Hisuian",     # Zorua, Zoroark
        (628, 1): "Hisuian",                           # Braviary
        (705, 1): "Hisuian", (706, 1): "Hisuian",     # Sliggoo, Goodra
        (713, 1): "Hisuian",                           # Avalugg
        (724, 1): "Hisuian",                           # Decidueye
        # Legendary formes
        (483, 0): "Altered Forme", (483, 1): "Origin Forme",   # Dialga
        (484, 0): "Altered Forme", (484, 1): "Origin Forme",   # Palkia
        (487, 0): "Altered Forme", (487, 1): "Origin Forme",   # Giratina
        (492, 0): "Land Forme", (492, 1): "Sky Forme", # Shaymin
        # Forces of Nature
        (641, 0): "Incarnate Forme", (641, 1): "Therian Forme",   # Tornadus
        (642, 0): "Incarnate Forme", (642, 1): "Therian Forme",   # Thundurus
        (645, 0): "Incarnate Forme", (645, 1): "Therian Forme",   # Landorus
        (905, 0): "Incarnate Forme", (905, 1): "Therian Forme",   # Enamorus
        # Basculin
        (550, 0): "Red-Striped", (550, 1): "Blue-Striped", (550, 2): "White-Striped",
        # Rotom
        (479, 1): "Heat", (479, 2): "Wash", (479, 3): "Frost", (479, 4): "Fan", (479, 5): "Mow",
        # Misc
        (421, 1): "Sunshine",                          # Cherrim
        # Shellos / Gastrodon
        (422, 0): "West Sea", (422, 1): "East Sea",    # Shellos
        (423, 0): "West Sea", (423, 1): "East Sea",    # Gastrodon
        # Basculegion
        (902, 0): "Male", (902, 1): "Female",          # Basculegion
        # Unown (A-Z, !, ?)
        (201, 0): "A", (201, 1): "B", (201, 2): "C", (201, 3): "D",
        (201, 4): "E", (201, 5): "F", (201, 6): "G", (201, 7): "H",
        (201, 8): "I", (201, 9): "J", (201, 10): "K", (201, 11): "L",
        (201, 12): "M", (201, 13): "N", (201, 14): "O", (201, 15): "P",
        (201, 16): "Q", (201, 17): "R", (201, 18): "S", (201, 19): "T",
        (201, 20): "U", (201, 21): "V", (201, 22): "W", (201, 23): "X",
        (201, 24): "Y", (201, 25): "Z", (201, 26): "!", (201, 27): "?",
        # Arceus type formes
        (493, 1): "Fighting", (493, 2): "Flying", (493, 3): "Poison",
        (493, 4): "Ground", (493, 5): "Rock", (493, 6): "Bug",
        (493, 7): "Ghost", (493, 8): "Steel", (493, 9): "Fire",
        (493, 10): "Water", (493, 11): "Grass", (493, 12): "Electric",
        (493, 13): "Psychic", (493, 14): "Ice", (493, 15): "Dragon",
        (493, 16): "Dark", (493, 17): "Fairy",
        # Misc
        (412, 0): "Plant", (412, 1): "Sandy", (412, 2): "Trash",  # Burmy
        (413, 0): "Plant", (413, 1): "Sandy", (413, 2): "Trash",  # Wormadam
    }

    # Trainer filename prefix -> (name, class)
    # Confirmed by cross-referencing team data with game sources
    TRAINER_MAP = (
        # (prefix,      name,       class)
        ('giratina',    'Volo',     'Pokemon Wielder'),
        ('trainer01',   'Charm',    'The Bandit'),
        ('trainer02',   'Clover',   'The Bandit'),
        ('trainer03',   'Coin',     'The Bandit'),
        ('trainer04',   'Ingo',     'Warden'),
        ('trainer05',   'Melli',    'Warden'),
        ('trainer06',   'Sabi',     'Warden'),
        ('trainer07',   'Gaeric',   'Warden'),
        ('trainer08',   'Beni',     "The Galaxy Team's"),
        ('trainer09',   'Kamado',   "The Galaxy Team's"),
        ('trainer10',   'Volo',     'Pokemon Wielder'),
        ('trainer11',   'Adaman',   'Clan Leader'),
        ('trainer12',   'Irida',    'Clan Leader'),
        ('trainer13',   'Rei',      "The Survey Corps'"),
        ('trainer14',   'Akari',    "The Survey Corps'"),
        ('trainer15',   'Zisu',     'The Security Corps'),
        ('trainer16',   'Wenton',   'The Security Corps'),
        ('trainer17',   'Bren',     'The Security Corps'),
        ('trainer18',   'Mai',      'Warden'),
        ('trainer19',   'Lian',     'Warden'),
    )

    # Music tag -> official soundtrack name
    BATTLE_MUSIC = {
        'PLAY_BGM_VS_TRAINER_01':   'Battle! (Pokemon Wielder)',
        'PLAY_BGM_VS_TRAINER_02':   'Battle! (Clan Warden)',
        'PLAY_BGM_VS_TRAINER10_01': 'Battle! (Pokemon Wielder Volo)',
        'PLAY_BGM_VS_BOSS_03':      'Battle! (Volo & Giratina)',
    }

    FLIPNOTE_PAIRS = {
        'Pokemon Legends Arceus': ['PLA'],
    }
