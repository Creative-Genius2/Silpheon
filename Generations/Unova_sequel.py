"""Unova_sequel.py: Black 2/White 2.

Inherits Unova_prequel. Different trdata/trpoke/encounter paths,
adds PWT (Pokemon World Tournament), Challenge Mode trainer delta.
"""
from Unova_prequel import Unova_prequel


class Unova_sequel(Unova_prequel):
    """Black 2/White 2. Inherits Black/White, adds PWT."""

    GAME_CODES = ('IRE', 'IRD')
    TITLES = ('Pokémon Black 2', 'Pokémon White 2')
    YEAR = 2012

    TRDATA_PATH = 'a/0/9/1'
    TRPOKE_PATH = 'a/0/9/2'
    ENCOUNTER_PATH = 'a/1/2/7'

    PWT_POKEMON_PATH = 'a/2/5/0'
    PWT_TRAINERS_PATH = 'a/2/5/1'
    PWT_ROSTERS_PATH = 'a/2/5/2'
    PWT_POKEMON_B_PATH = 'a/2/5/3'
    PWT_TRAINERS_B_PATH = 'a/2/5/4'
    PWT_ROSTERS_B_PATH = 'a/2/5/5'
    PWT_CHAMPIONS_PATH = 'a/2/5/6'
    PWT_CHAMPIONS_B_PATH = 'a/2/5/7'
    PWT_DOWNLOAD_PATH = 'a/2/5/8'
    PWT_TRAINERS_2_PATH = 'a/2/4/8'
    PWT_ROSTERS_2_PATH = 'a/2/4/9'
    PWT_MIX_PATH = 'a/2/6/1'
    PWT_DEFS_PATH = 'a/2/6/9'

    SUBWAY_POKEMON_PATH = 'a/2/4/0'
    SUBWAY_TRAINERS_PATH = 'a/2/4/1'

    TEXT_SPECIES = 90
    TEXT_MOVES = 403
    TEXT_ITEMS = 64
    TEXT_ABILITIES = 374
    TEXT_NATURES = 380
    TEXT_TRAINER_NAMES = 382
    TEXT_TRAINER_CLASSES = 383
    TEXT_TYPE_NAMES = 398
    TEXT_LOCATIONS = 109

    # BW2 Challenge Mode runtime level delta table.
    # Verified by measuring stored trpoke levels vs actual in-game levels.
    # The game applies a flat per-trainer-file delta at runtime on top of stored levels.
    # Pattern: +1 per pair of gyms, capped at +4 from gym 7 onward (E4, Champion included).
    # Keyed by trdata/trpoke file index -> challenge delta.
    # Normal mode files and unkeyed files get delta 0.
    CHALLENGE_FILE_DELTA = {
        # Gym 1 - Cheren (Aspertia)
        764: 1,
        # Gym 2 - Roxie (Virbank)
        765: 1,
        # Gym 3 - Burgh (Castelia)
        766: 2,
        # Gym 4 - Elesa (Nimbasa)
        767: 2,
        # Gym 5 - Clay (Driftveil)
        768: 3,
        # Gym 6 - Skyla (Mistralton)
        769: 3,
        # Gym 7 - Drayden (Opelucid)
        770: 4,
        # Gym 8 - Marlon (Humilau)
        771: 4,
        # Elite Four - Shauntal, Caitlin, Grimsley, Marshal (pre-champion)
        772: 4, 773: 4, 774: 4, 775: 4,
        # Champion Iris (pre-champion)
        776: 4,
        # Elite Four rematches (post-game)
        777: 4, 778: 4, 779: 4, 780: 4,
        # Champion Iris rematch
        781: 4,
    }

    def get_challenge_delta(self, file_idx):
        """BW2 Challenge Mode level delta. Overrides SDK default (0)."""
        return self.CHALLENGE_FILE_DELTA.get(file_idx, 0)

    def _role_path(self, role_name):
        """Look up a NARC path by its role name, using self.narc_roles."""
        for path, role in self.narc_roles.items():
            if role == role_name:
                return path
        return None


    def bootstrap_pwt(self):
        """Build PWT lookup maps from ROM data. Called once at spotlight for B2W2."""
        self.pwt_name_to_entries = {}
        self.pwt_entry_tournaments = {}
        tt = self.text_tables
        classes = tt.get('trainer_classes', [])
        _JUNK = {'Pokmon Trainer', 'Boss Trainer', 'no data', 'Team Plasma',
                 'GAME FREAK', 'Leader', ''}
        try:
            # 1) Tournament defs → which trainers_b indices appear in which tournament
            defs = self.get_narc(self.PWT_DOWNLOAD_PATH)
            tourn_names = tt.get('tournament_names', [])
            for fi, raw in enumerate(defs.files):
                data = bytes(raw)
                if len(data) < 0x1A8: continue
                tid = struct.unpack_from('<H', data, 0)[0]
                tname = ''
                if tid < len(tourn_names):
                    r = tourn_names[tid]
                    if isinstance(r, str):
                        tname = re.sub(r'[^\x20-\x7E]', '', r).strip()
                if not tname or tname == '???': tname = f"Tournament #{tid}"
                indices = set()
                for rs, re_ in [(0xA0, 0x130), (0x160, 0x1A8)]:
                    for off in range(rs, re_, 2):
                        val = struct.unpack_from('<H', data, off)[0]
                        if 1 <= val <= 68: indices.add(val)
                for idx in indices:
                    self.pwt_entry_tournaments.setdefault(idx, []).append(tname)

            # 2) Trainer map → resolve names by class ID at u16[8]
            try:
                map_data = bytes(self.get_narc(self._role_path('pwt_trainer_map')).files[0])
            except Exception:
                map_data = b''
            tb = self.get_narc(self.PWT_TRAINERS_B_PATH)
            unresolved = []
            for idx in range(1, len(tb.files)):
                name = None
                off = idx * 20
                if off + 20 <= len(map_data):
                    cid = struct.unpack_from('<H', map_data, off + 16)[0]  # u16[8]
                    if 0 < cid < len(classes):
                        raw = classes[cid]
                        if isinstance(raw, str):
                            clean = re.sub(r'[^\x20-\x7E]', '', raw).strip()
                            if clean and clean not in _JUNK: name = clean
                if name:
                    self.pwt_name_to_entries.setdefault(name.lower(), []).append(idx)
                else:
                    unresolved.append(idx)

            # 3) Resolve remaining by type cross-reference against gym leaders
            if not unresolved: return
            leader_cids = {ci for ci, cn in enumerate(classes)
                           if isinstance(cn, str) and cn.strip() == 'Leader'}
            if not leader_cids: return
            td_narc = self.get_narc(self.TRAINER_PATH)
            tp_narc = self.get_narc(self.TRPOKE_PATH)
            ps_narc = self.get_narc(self.PERSONAL_PATH)
            tnames = tt.get('trainer_names', [])
            PSIZES = {0: 8, 1: 16, 2: 10, 3: 18}

            def _dom_type(sids):
                counts = {}
                for sid in sids:
                    if sid >= len(ps_narc.files): continue
                    pers = bytes(ps_narc.files[sid])
                    if len(pers) < 8: continue
                    t1, t2 = pers[6], pers[7]
                    counts[t1] = counts.get(t1, 0) + 1
                    if t2 != t1: counts[t2] = counts.get(t2, 0) + 1
                return max(counts, key=counts.get) if counts else None

            leaders = []
            seen = set()
            for ti in range(min(764, len(td_narc.files))):
                td = bytes(td_narc.files[ti])
                if len(td) < 16 or td[1] not in leader_cids: continue
                nm = tnames[ti] if ti < len(tnames) else None
                if not isinstance(nm, str): continue
                nm = re.sub(r'[^\x20-\x7E]', '', nm).strip()
                if not nm or nm in seen: continue
                seen.add(nm)
                psize = PSIZES.get(td[0] & 3, 8)
                tp = bytes(tp_narc.files[ti]) if ti < len(tp_narc.files) else b''
                sids = []
                for pi in range(td[3]):
                    o = pi * psize
                    if o + 6 > len(tp): break
                    sids.append(struct.unpack_from('<H', tp, o + 4)[0])
                t = _dom_type(sids)
                if t is not None: leaders.append((nm, t))

            if not leaders: return
            ro_narc = self.get_narc(self.PWT_ROSTERS_B_PATH)
            po_narc = self.get_narc(self.PWT_CHAMPIONS_PATH)
            matched = set()
            for idx in unresolved:
                if idx >= len(ro_narc.files): continue
                rd = bytes(ro_narc.files[idx])
                if len(rd) < 6: continue
                r_count = struct.unpack_from('<H', rd, 2)[0]
                sids = []
                for ri in range(r_count):
                    po = 4 + ri * 2
                    if po + 2 > len(rd): break
                    pidx = struct.unpack_from('<H', rd, po)[0]
                    if pidx < len(po_narc.files):
                        pd = bytes(po_narc.files[pidx])
                        if len(pd) >= 2: sids.append(struct.unpack_from('<H', pd, 0)[0])
                t = _dom_type(sids)
                if t is None: continue
                for lname, ltype in leaders:
                    if lname not in matched and ltype == t:
                        self.pwt_name_to_entries.setdefault(lname.lower(), []).append(idx)
                        matched.add(lname)
                        break
        except Exception:
            pass

    def _decode_pwt_pool_entry(self, data):
        """Decode one 16B PWT pool entry → one-line string."""
        if len(data) < 16 or data == b'\x00' * 16: return None
        tt = self.text_tables
        sp = tt.get('species', []); mv = tt.get('moves', [])
        nat = tt.get('natures', []); it = tt.get('items', [])
        sid = struct.unpack_from('<H', data, 0)[0]
        moves = [struct.unpack_from('<H', data, 2+i*2)[0] for i in range(4)]
        ev, nature, item = data[10], data[11], struct.unpack_from('<H', data, 12)[0]
        sname = sp[sid] if sid < len(sp) else f"#{sid}"
        nraw = nat[nature] if nature < len(nat) else ""
        nname = re.sub(r'[^\x20-\x7E]', '', nraw).replace(' nature.', '').strip() if nraw else f"nature#{nature}"
        mnames = [mv[m] if m < len(mv) else f"move#{m}" for m in moves if m]
        evs = self.decode_ev_spread(ev)
        itag = f" @ {it[item]}" if item and item < len(it) else ""
        parts = [f"{sname} ({nname}){itag}"]
        if mnames: parts.append(" / ".join(mnames))
        if evs and evs != ['None']: parts.append(f"EVs: {', '.join(evs)}")
        return "\n".join(parts)

    def decode_pwt(self, data, file_idx, text_tables, path='', **kw):
        """Decode any PWT file. Path tells us the format."""
        # Which PWT NARC are we in?
        pool_paths = {self.PWT_POKEMON_PATH, self.PWT_POKEMON_B_PATH,
                      self.PWT_CHAMPIONS_PATH, self.PWT_CHAMPIONS_B_PATH}
        roster_paths = {self.PWT_ROSTERS_PATH, self.PWT_ROSTERS_B_PATH}
        trainer_paths = {self.PWT_TRAINERS_PATH, self.PWT_TRAINERS_B_PATH}
        narc = path.rsplit(':', 1)[0] if ':' in path else path

        # Pool entry (16B)
        if narc in pool_paths:
            return self._decode_pwt_pool_entry(data)

        # Roster: format(u16) + count(u16) + pool_indices
        if narc in roster_paths:
            if len(data) < 4: return None
            count = struct.unpack_from('<H', data, 2)[0]
            if count == 0 and struct.unpack_from('<H', data, 0)[0] == 0: return None
            indices = [struct.unpack_from('<H', data, 4+i*2)[0]
                       for i in range(count) if 4+i*2+2 <= len(data)]
            out = [f"Roster #{file_idx} | {count} Pokémon"]
            try:
                pool = self.get_narc(self.PWT_CHAMPIONS_PATH)
                for pi in indices:
                    line = self._decode_pwt_pool_entry(bytes(pool.files[pi])) if pi < len(pool.files) else None
                    out.append(f"  [{pi}] {line.replace(chr(10), '  |  ')}" if line else f"  [{pi}] (empty)")
            except: pass
            return "\n".join(out)

        # Trainer config (6B): format + count + start
        if narc in trainer_paths:
            if len(data) < 6: return None
            fmt, count, start = [struct.unpack_from('<H', data, i*2)[0] for i in range(3)]
            if fmt == 0 and count == 0 and start == 0: return None
            name = None
            for n, idxs in self.pwt_name_to_entries.items():
                if file_idx in idxs: name = n.title(); break
            out = [f"{'PKMN Trainer ' + name if name else f'Trainer #{file_idx}'} | Picks {count} | Start: {start}"]
            try:
                ro = self.get_narc(self.PWT_ROSTERS_B_PATH)
                pool = self.get_narc(self.PWT_CHAMPIONS_PATH)
                if file_idx < len(ro.files):
                    rd = bytes(ro.files[file_idx])
                    if len(rd) >= 4:
                        r_count = struct.unpack_from('<H', rd, 2)[0]
                        for i in range(r_count):
                            o = 4 + i * 2
                            if o + 2 > len(rd): break
                            pi = struct.unpack_from('<H', rd, o)[0]
                            if pi < len(pool.files):
                                line = self._decode_pwt_pool_entry(bytes(pool.files[pi]))
                                if line: out.append(f"  {line.replace(chr(10), '  |  ')}")
            except: pass
            return "\n".join(out)

        # Tournament def (everything else under a/2/5/)
        if len(data) < 0x60: return None
        tid = struct.unpack_from('<H', data, 0)[0]
        trainer_count = struct.unpack_from('<H', data, 4)[0]
        bf = struct.unpack_from('<H', data, 6)[0]
        pool_type = struct.unpack_from('<H', data, 8)[0]
        bt = {1:"Single", 2:"Double", 3:"Triple", 4:"Rotation"}.get(bf, f"Type {bf}")
        tourn_names = tt.get('tournament_names', [])
        tname = ''
        if tid < len(tourn_names):
            r = tourn_names[tid]
            if isinstance(r, str): tname = re.sub(r'[^ -~]', '', r).strip()
        if not tname or tname == '???': tname = f"Tournament #{tid}"
        out = [f"Tournament #{tid} — {tname}", f"Trainers: {trainer_count} | Battle: {bt} | Pool: {pool_type}"]
        tis = set()
        for rs, re_ in [(0xA0, 0x130), (0x160, 0x1A8)]:
            if len(data) < re_: continue
            for off in range(rs, re_, 2):
                val = struct.unpack_from('<H', data, off)[0]
                if 1 <= val <= 68: tis.add(val)
        if tis:
            out.append(f"Trainer pool: {sorted(tis)}")
            try:
                pool = self.get_narc(self.PWT_CHAMPIONS_PATH)
                ro = self.get_narc(self.PWT_ROSTERS_B_PATH)
                for ti in sorted(tis):
                    if ti >= len(ro.files): continue
                    rd = bytes(ro.files[ti])
                    if len(rd) >= 6:
                        rc = struct.unpack_from('<H', rd, 2)[0]
                        first = struct.unpack_from('<H', rd, 4)[0]
                        if first < len(pool.files):
                            line = self._decode_pwt_pool_entry(bytes(pool.files[first]))
                            if line: out.append(f"  pwttr[{ti}]: {line.split(chr(10))[0]}  (+{rc-1} more)")
            except: pass
        return "\n".join(out)

    def bootstrap_locations(self):
        """Discover gym/league trainer locations from ROM data. Called at spotlight."""
        import ndspy.narc
        tr_narc = self.get_narc(self.TRAINER_PATH)
        if not tr_narc:
            return

        # Gym leaders: known index pairs (normal, challenge) -> city
        self._gym_locations = (
            ((156, 764), "Aspertia Gym"),
            ((157, 765), "Virbank Gym"),
            ((158, 766), "Castelia Gym"),
            ((159, 767), "Nimbasa Gym"),
            ((160, 768), "Driftveil Gym"),
            ((161, 769), "Mistralton Gym"),
            ((162, 770), "Opelucid Gym"),
            ((163, 771), "Humilau Gym"),
        )

        self._challenge_start = 764

        # E4/Champion: read byte 1 of known challenge files, scan all trdata
        e4_champ_classes = set()
        for idx in (772, 773, 774, 775, 776):
            e4_champ_classes.add(bytes(tr_narc.files[idx])[1])

        self._league_indices = set()
        self._initial_indices = set()
        self._rematch_indices = set()

        # Scan all trdata for E4/Champion class bytes
        for i, f in enumerate(tr_narc.files):
            d = bytes(f)
            if len(d) >= 2 and d[1] in e4_champ_classes:
                self._league_indices.add(i)

        # Initial vs Rematch: split within each mode, not across modes
        # 764 boundary separates Normal from Challenge
        by_class = {}
        for idx in self._league_indices:
            cls = bytes(tr_narc.files[idx])[1]
            by_class.setdefault(cls, []).append(idx)
        for cls, indices in by_class.items():
            normal = sorted(i for i in indices if i < 764)
            challenge = sorted(i for i in indices if i >= 764)
            # Within each mode: lower index = First Battle, higher = Rematch
            for group in (normal, challenge):
                if len(group) >= 2:
                    self._initial_indices.add(group[0])
                    self._rematch_indices.add(group[1])
                elif len(group) == 1:
                    self._initial_indices.add(group[0])


    # PWT pool roles — these decode as individual pokemon entries (16B each)
    _PWT_POOL_ROLES = {
        'pwt_rental', 'pwt_rental_b', 'pwt_champions', 'pwt_champions_b', 'pwt_mix',
    }

    # PWT role relationships: trainer role → (roster role, pool role)
    _PWT_ROLE_CHAINS = {
        'pwt_trainers':   ('pwt_rosters',   'pwt_rental'),
        'pwt_trainers_b': ('pwt_rosters_b', 'pwt_champions'),
        'pwt_trainers_2': ('pwt_rosters_2', 'pwt_rental'),
    }

    # Roster role → pool role (includes non-PWT facilities that share the format)
    _PWT_ROSTER_POOLS = {
        'pwt_rosters':           'pwt_rental',
        'pwt_rosters_b':         'pwt_champions',
        'pwt_rosters_2':         'pwt_rental',
        'subway_trainers':       'subway_pokemon',
        'battle_tower_trainers': 'battle_tower_pokemon',
    }

    TRAINER_LOCATIONS = {
        "IRE": {
            ("Leader", "Cheren"): "Aspertia Gym",
            ("Leader", "Roxie"): "Virbank Gym",
            ("Leader", "Burgh"): "Castelia Gym",
            ("Leader", "Elesa"): "Nimbasa Gym",
            ("Leader", "Clay"): "Driftveil Gym",
            ("Leader", "Skyla"): "Mistralton Gym",
            ("Leader", "Drayden"): "Opelucid Gym",
            ("Leader", "Marlon"): "Humilau Gym",
            ("Elite Four", "Shauntal"): "Pokémon League",
            ("Elite Four", "Grimsley"): "Pokémon League",
            ("Elite Four", "Caitlin"): "Pokémon League",
            ("Elite Four", "Marshal"): "Pokémon League",
            ("Champion", "Iris"): "Pokémon League",
            ("Subway Boss", "Ingo"): "Battle Subway",
            ("Subway Boss", "Emmet"): "Battle Subway",
        },
        "IRD": "IRE",
    }

    CLASS_LOCATIONS = {
        "IRE": {
            "Elite Four": "Pokémon League", "Champion": "Pokémon League", "Subway Boss": "Battle Subway",
            "Brock": "Pokémon World Tournament", "Misty": "Pokémon World Tournament",
            "Lt. Surge": "Pokémon World Tournament", "Erika": "Pokémon World Tournament",
            "Sabrina": "Pokémon World Tournament", "Blaine": "Pokémon World Tournament",
            "Giovanni": "Pokémon World Tournament", "Falkner": "Pokémon World Tournament",
            "Bugsy": "Pokémon World Tournament", "Whitney": "Pokémon World Tournament",
            "Morty": "Pokémon World Tournament", "Chuck": "Pokémon World Tournament",
            "Jasmine": "Pokémon World Tournament", "Pryce": "Pokémon World Tournament",
            "Clair": "Pokémon World Tournament", "Janine": "Pokémon World Tournament",
            "Roxanne": "Pokémon World Tournament", "Brawly": "Pokémon World Tournament",
            "Wattson": "Pokémon World Tournament", "Flannery": "Pokémon World Tournament",
            "Norman": "Pokémon World Tournament", "Winona": "Pokémon World Tournament",
            "Tate": "Pokémon World Tournament", "Liza": "Pokémon World Tournament",
            "Juan": "Pokémon World Tournament", "Roark": "Pokémon World Tournament",
            "Gardenia": "Pokémon World Tournament", "Fantina": "Pokémon World Tournament",
            "Maylene": "Pokémon World Tournament", "Wake": "Pokémon World Tournament",
            "Byron": "Pokémon World Tournament", "Candice": "Pokémon World Tournament",
            "Volkner": "Pokémon World Tournament", "Blue": "Pokémon World Tournament",
            "Lance": "Pokémon World Tournament", "Steven": "Pokémon World Tournament",
            "Wallace": "Pokémon World Tournament", "Red": "Pokémon World Tournament",
            "Cynthia": "Pokémon World Tournament", "Alder": "Pokémon World Tournament",
        },
        "IRD": "IRE",
    }
