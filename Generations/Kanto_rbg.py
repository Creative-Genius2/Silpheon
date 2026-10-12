"""Kanto_rbg.py: Red/Blue/Green — Gen I structural baseline.

Inherits SDK. First game in the chain. Everything Gen I defined lives here.
"""
from sdk import SDK
import struct


class Kanto_rbg(SDK):
    """Red/Blue/Green (EN + JP). Gen I baseline."""

    GAME_CODES = ('PMR', 'PMB', 'PMG', 'PKMRJ', 'PMBJP')
    TITLES = ('POKÉMON RED', 'POKÉMON BLUE', 'POCKET MONSTERS GREEN', 'POCKET MONSTERS RED', 'POCKET MONSTERS BLUE')
    YEAR = 1996

    PLATFORM = 'Game Boy'
    GEN = 1
    CONTAINER = 'gb'

    ENC_ANCHOR_LEVELS = (2, 5)  # Route 1 grass level range; anchors the wild encounter table scan

    STAT_COUNT = 5
    STAT_ORDER = ('HP', 'Atk', 'Def', 'Spe', 'Special')

    EOS = 0x50
    SPECIES_COUNT = 151

    # Gen I (GB) character map — English Red/Blue/Yellow
    # Space=0x7F, EOS=0x50, A-Z=0x80-0x99, a-z=0xA0-0xB9, 0-9=0xF6-0xFF
    CHARMAP_EN: dict = {0x7F: ' '}
    for _i, _c in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        CHARMAP_EN[0x80 + _i] = _c
    for _i, _c in enumerate('abcdefghijklmnopqrstuvwxyz'):
        CHARMAP_EN[0xA0 + _i] = _c
    for _i, _c in enumerate('0123456789'):
        CHARMAP_EN[0xF6 + _i] = _c
    CHARMAP_EN.update({0xE8: '.', 0xE9: 'l', 0xEA: 's', 0xEB: 't', 0xEC: 'v',
                              0xE0: "'", 0xE3: ' ',   # apostrophe + space variant
                              0xEF: '♂', 0xF5: '♀',  # gender symbols (Gen II trainer classes)
                              0xE6: 'é',   # accented e (Pokémon, Poké Ball etc.)
                              0xE7: "'",   # apostrophe (FARFETCH'D)
                              0x4A: '',    # control code — skip silently
                              0x54: ''})

    # Gen I (GB) character map — Japanese Red/Green/Blue/Yellow
    # From Bulbapedia Character encoding (Generation I):
    # Rows 8-A: unvoiced katakana. ヘ is absent from the katakana block (no byte for it).
    # Gen I JP charmap — verified against pokegreen disassembly constants/charmap.asm
    CHARMAP_JP: dict = {0x7F: ' '}
    # Main katakana block 0x80-0xAF (ヘ absent — lives at 0xCD; リ via 0xD8 normalization)
    _KATAKANA = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフホマミムメモヤユヨラルレロワヲンッャュョ'
    for _i, _c in enumerate(_KATAKANA):
        CHARMAP_JP[0x80 + _i] = _c
    CHARMAP_JP.update({
        # Voiced katakana
        0x05: 'ガ', 0x06: 'ギ', 0x07: 'グ', 0x08: 'ゲ', 0x09: 'ゴ',
        0x0A: 'ザ', 0x0B: 'ジ', 0x0C: 'ズ', 0x0D: 'ゼ', 0x0E: 'ゾ',
        0x0F: 'ダ', 0x10: 'ヂ', 0x11: 'ヅ', 0x12: 'デ', 0x13: 'ド',
        0x19: 'バ', 0x1A: 'ビ', 0x1B: 'ブ', 0x1C: 'ボ', 0x1D: 'ベ',  # 0x1C=ボ 0x1D=ベ
        # Semi-voiced katakana パ行 (0x43=ポ)
        0x40: 'パ', 0x41: 'ピ', 0x42: 'プ', 0x43: 'ポ',
        # Semi-voiced hiragana
        0x44: 'ぱ', 0x45: 'ぴ', 0x46: 'ぷ', 0x47: 'ぺ', 0x48: 'ぽ',
        # Voiced hiragana
        0x14: 'ば', 0x15: 'び', 0x16: 'ぶ', 0x17: 'べ', 0x18: 'ぼ',
        0x26: 'が', 0x27: 'ぎ', 0x28: 'ぐ', 0x29: 'げ', 0x2A: 'ご',
        0x2B: 'ざ', 0x2C: 'じ', 0x2D: 'ず', 0x2E: 'ぜ', 0x2F: 'ぞ',
        0x30: 'だ', 0x31: 'ぢ', 0x32: 'づ', 0x33: 'で', 0x34: 'ど',
        0x35: 'ば', 0x36: 'び', 0x37: 'ぶ', 0x38: 'べ', 0x39: 'ぼ',
        0x3A: 'ば', 0x3B: 'び', 0x3C: 'ぶ', 0x3D: 'べ', 0x3E: 'ぼ',
        # Small kana + long vowel mark
        0xE0: 'ゃ', 0xE1: 'ゅ', 0xE2: 'ょ', 0xE3: 'ー',
        # Small katakana vowels
        0xB0: 'ィ', 0xE9: 'ァ', 0xEA: 'ゥ', 0xEB: 'ェ', 0xF4: 'ォ',
        # Gender symbols
        0xEF: '♂', 0xF5: '♀',
        # Hiragana block 0xB1-0xDF
        0xB1: 'あ', 0xB2: 'い', 0xB3: 'う', 0xB4: 'え', 0xB5: 'お',
        0xB6: 'か', 0xB7: 'き', 0xB8: 'く', 0xB9: 'け', 0xBA: 'こ',
        0xBB: 'さ', 0xBC: 'し', 0xBD: 'す', 0xBE: 'せ', 0xBF: 'そ',
        0xC0: 'た', 0xC1: 'ち', 0xC2: 'つ', 0xC3: 'て', 0xC4: 'と',
        0xC5: 'な', 0xC6: 'に', 0xC7: 'ぬ', 0xC8: 'ね', 0xC9: 'の',
        0xCA: 'は', 0xCB: 'ひ', 0xCC: 'ふ', 0xCD: 'へ', 0xCE: 'ほ', 0xCF: 'ま',
        0xD0: 'み', 0xD1: 'む', 0xD2: 'め', 0xD3: 'も', 0xD4: 'や',
        0xD5: 'ゆ', 0xD6: 'よ', 0xD7: 'ら', 0xD8: 'り', 0xD9: 'る',
        0xDA: 'れ', 0xDB: 'ろ', 0xDC: 'わ', 0xDD: 'を', 0xDE: 'ん', 0xDF: 'っ',
    })

    # Hiragana → Katakana normalization for species name splitting
    JP_H2K: dict = {}
    for _h, _k in zip(
        'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんっぁゃゅょ',
        'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンッァャュョ',
    ):
        JP_H2K[_h] = _k
    for _h, _k in [('が','ガ'),('ぎ','ギ'),('ぐ','グ'),('げ','ゲ'),('ご','ゴ'),
                   ('ざ','ザ'),('じ','ジ'),('ず','ズ'),('ぜ','ゼ'),('ぞ','ゾ'),
                   ('だ','ダ'),('ぢ','ヂ'),('づ','ヅ'),('で','デ'),('ど','ド'),
                   ('ば','バ'),('び','ビ'),('ぶ','ブ'),('べ','ベ'),('ぼ','ボ'),
                   ('ぱ','パ'),('ぴ','ピ'),('ぷ','プ'),('ぺ','ペ'),('ぽ','ポ')]:
        JP_H2K[_h] = _k

    @staticmethod
    def _jp_normalize(s, _h2k=JP_H2K):
        return ''.join(_h2k.get(c, c) for c in s)

    JP_DISASM = [
        'サイドン','ガルーラ','ニドラン♂','ピッピ','オニスズメ','ビリリダマ','ニドキング','ヤドラン',
        'フシギソウ','ナッシー','ベロリンガ','タマタマ','ベトベター','ゲンガー','ニドラン♀','ニドクイン',
        'カラカラ','サイホーン','ラプラス','ウインディ','ミュウ','ギャラドス','シェルダー','メノクラゲ',
        'ゴース','ストライク','ヒトデマン','カメックス','カイロス','モンジャラ','けつばん','けつばん',
        'ガーディ','イワーク','オニドリル','ポッポ','ヤドン','ユンゲラー','ゴローン','ラッキー',
        'ゴーリキー','バリヤード','サワムラー','エビワラー','アーボック','パラセクト','コダック',
        'スリープ','ゴローニャ','けつばん','ブーバー','けつばん','エレブー','レアコイル','ドガース',
        'けつばん','マンキー','パウワウ','ディグダ','ケンタロス','けつばん','けつばん','けつばん',
        'カモネギ','コンパン','カイリュー','けつばん','けつばん','けつばん','ドードー','ニョロモ',
        'ルージュラ','ファイヤー','フリーザー','サンダー','メタモン','ニャース','クラブ','けつばん',
        'けつばん','けつばん','ロコン','キュウコン','ピカチュウ','ライチュウ','けつばん','けつばん',
        'ミニリュウ','ハクリュー','カブト','カブトプス','タッツー','シードラ','けつばん','けつばん',
        'サンド','サンドパン','オムナイト','オムスター','プリン','プクリン','イーブイ','ブースター',
        'サンダース','シャワーズ','ワンリキー','ズバット','アーボ','パラス','ニョロゾ','ニョロボン',
        'ビードル','コクーン','スピアー','けつばん','ドードリオ','オコリザル','ダグトリオ','モルフォン',
        'ジュゴン','けつばん','けつばん','キャタピー','トランセル','バタフリー','カイリキー','けつばん',
        'ゴルダック','スリーパー','ゴルバット','ミュウツー','カビゴン','コイキング','けつばん','けつばん',
        'ベトベトン','けつばん','キングラー','パルシェン','けつばん','マルマイン','ピクシー','マタドガス',
        'ペルシアン','ガラガラ','けつばん','ゴースト','ケーシィ','フーディン','ピジョン','ピジョット',
        'スターミー','フシギダネ','フシギバナ','ドククラゲ','けつばん','トサキント','アズマオウ',
        'けつばん','けつばん','けつばん','けつばん','ポニータ','ギャロップ','コラッタ','ラッタ',
        'ニドリーノ','ニドリーナ','イシツブテ','ポリゴン','プテラ','けつばん','コイル','けつばん',
        'けつばん','ヒトカゲ','ゼニガメ','リザード','カメール','リザードン','けつばん','けつばん',
        'けつばん','ゴースト','ナゾノクサ','クサイハナ','ラフレシア','マダツボミ','ウツドン','ウツボット',
    ]
    JP_REF = sorted(set(map(_jp_normalize, JP_DISASM)), key=len, reverse=True)
    JP_NORM_TO_ORIG = dict(zip(map(_jp_normalize, JP_DISASM), JP_DISASM))

    _jp_normalize = staticmethod(_jp_normalize)


    # Gen I JP species names for splitting merged ROM entries
    JP_SPECIES = {'フシギダネ','フシギソウ','フシギバナ','ヒトカゲ','リザード','リザードン',
    'ゼニガメ','カメール','カメックス','キャタピー','トランセル','バタフリー','ビードル',
    'コクーン','スピアー','ポッポ','ピジョン','ピジョット','コラッタ','ラッタ','オニスズメ',
    'オニドリル','アーボ','アーボック','ピカチュウ','ライチュウ','サンド','サンドパン',
    'ニドラン♀','ニドリーナ','ニドクイン','ニドラン♂','ニドリーノ','ニドキング','ピッピ',
    'ピクシー','ロコン','キュウコン','プリン','プクリン','ズバット','ゴルバット','ナゾノクサ',
    'クサイハナ','ラフレシア','パラス','パラセクト','コンパン','モルフォン','ディグダ',
    'ダグトリオ','ニャース','ペルシアン','コダック','ゴルダック','マンキー','オコリザル',
    'ガーディ','ウインディ','ニョロモ','ニョロゾ','ニョロボン','ケーシィ','ユンゲラー',
    'フーディン','ワンリキー','ゴーリキー','カイリキー','マダツボミ','ウツドン','ウツボット',
    'メノクラゲ','ドククラゲ','イシツブテ','ゴローン','ゴローニャ','ポニータ','ギャロップ',
    'ヤドン','ヤドラン','コイル','レアコイル','カモネギ','ドードー','ドードリオ','パウワウ',
    'ジュゴン','ベトベター','ベトベトン','シェルダー','パルシェン','ゴース','ゴースト',
    'ゲンガー','イワーク','スリープ','スリーパー','クラブ','キングラー','ビリリダマ',
    'マルマイン','タマタマ','ナッシー','カラカラ','ガラガラ','サワムラー','エビワラー',
    'ベロリンガ','ドガース','マタドガス','サイホーン','サイドン','ラッキー','モンジャラ',
    'ガルーラ','タッツー','シードラ','トサキント','アズマオウ','ヒトデマン','スターミー',
    'バリヤード','ストライク','ルージュラ','エレブー','ブーバー','カイロス','ケンタロス',
    'コイキング','ギャラドス','ラプラス','メタモン','イーブイ','シャワーズ','サンダース',
    'ブースター','ポリゴン','オムナイト','オムスター','カブト','カブトプス','プテラ',
    'カビゴン','フリーザー','サンダー','ファイヤー','ミニリュウ','ハクリュー','カイリュー',
    'ミュウツー','ミュウ','けつばん'}

    @staticmethod
    def _split_jp_species(text: str) -> list:
        """Split merged JP species names using known name dictionary."""
        if not text: return []
        result, sorted_names = [], sorted(Kanto_rbg.JP_SPECIES, key=len, reverse=True)
        while text:
            for sp in sorted_names:
                if text.startswith(sp):
                    result.append(sp)
                    text = text[len(sp):]
                    break
            else:
                text = text[1:]  # Skip unknown char
        return result

    @staticmethod
    def _scan_gen1_trainer_classes_jp(rom_data: bytes, charmap: dict, eos: int, text_tables: dict):
        """Scan JP Gen I trainer class names. Anchors at オーキドせんせい (Professor Oak).

        Table at 0x39DDE in Green/Red JP — 16 entries including all gym leaders by name.
        Names are normalized (hiragana → katakana) before storing so dowse matches work.
        """
        if 'trainer_classes' in text_tables:
            return

        reverse = {v: k for k, v in charmap.items() if isinstance(v, str) and len(v) == 1}
        anchor = 'オーキドせんせい'
        try:
            enc = bytes([reverse[c] for c in anchor]) + bytes([eos])
        except KeyError:
            return

        table_start = rom_data.find(enc)
        if table_start < 0:
            return

        names = []
        i = table_start
        while i < len(rom_data) and len(names) < 64:
            chars = []
            while i < len(rom_data) and rom_data[i] != eos:
                b = rom_data[i]
                ch = charmap.get(b)
                if ch:
                    chars.append(ch)
                elif b >= 0x80:
                    break
                elif b < 0x60:
                    pass  # control code
                i += 1
            name = Kanto_rbg._jp_normalize(''.join(chars)).strip()
            if i < len(rom_data) and rom_data[i] == eos:
                if len(name) >= 2:
                    names.append(name)
                elif not name and len(names) > 4:
                    break
                i += 1
            else:
                break

        if len(names) > 4:
            text_tables['trainer_classes'] = names

    @staticmethod
    def _scan_gen1_trainer_classes_en(rom_data: bytes, charmap: dict, eos: int, text_tables: dict):
        """Scan EN Gen I trainer class names. Anchors at YOUNGSTER (class 0).
        From pret/pokered: trainer class names are consecutive EOS-terminated strings.
        """
        if 'trainer_classes' in text_tables:
            return

        reverse = {v: k for k, v in charmap.items() if isinstance(v, str) and len(v) == 1}
        try:
            enc = bytes([reverse[c] for c in 'YOUNGSTER']) + bytes([eos])
        except KeyError:
            return

        table_start = rom_data.find(enc)
        if table_start < 0:
            return

        # Names are consecutive EOS-terminated strings. Some names contain '.', '♂', '♀', 'é'
        # — bytes that may be unknown to charmap. Scan to EOS regardless, only collect known chars.
        names = []
        i = table_start
        while i < len(rom_data) and len(names) < 64:
            chars = []
            while i < len(rom_data) and rom_data[i] != eos:
                ch = charmap.get(rom_data[i])
                if ch:
                    chars.append(ch)
                # Unknown bytes: skip (don't break — keep scanning to EOS)
                i += 1
            name = ''.join(chars).strip()
            if i < len(rom_data) and rom_data[i] == eos:
                if len(name) >= 2:
                    names.append(name)
                elif not name and len(names) > 8:
                    break
                i += 1
            else:
                break

        if len(names) > 8:
            text_tables['trainer_classes'] = names

    @staticmethod
    def _scan_gen1_items(rom_data: bytes, charmap: dict, eos: int, text_tables: dict):
        """Scan Gen I item names. Anchors on Master Ball (item 1).
        Works for both JP (マスターボール) and EN (MASTER BALL).
        Populates text_tables['items'] with a dummy at index 0.
        """
        if 'items' in text_tables:
            return

        reverse = {v: k for k, v in charmap.items() if isinstance(v, str) and len(v) == 1}
        # Try JP anchor first, then EN
        for anchor in ('マスターボール', 'MASTER BALL', 'MASTER\xa0BALL'):
            try:
                enc = bytes([reverse[c] for c in anchor if c in reverse])
                if len(enc) < 4:
                    continue
                p = rom_data.find(enc)
                if p >= 0:
                    table_start = p
                    break
            except Exception:
                continue
        else:
            return

        names = ['']  # dummy at index 0
        i = table_start
        while i < len(rom_data) and len(names) < 260:
            chars = []
            while i < len(rom_data) and rom_data[i] != eos:
                b = rom_data[i]
                ch = charmap.get(b)
                if ch:
                    chars.append(ch)
                elif b >= 0x80:
                    break
                elif b < 0x60:
                    pass
                i += 1
            name = Kanto_rbg._jp_normalize(''.join(chars)).strip()
            if i < len(rom_data) and rom_data[i] == eos:
                names.append(name)
                i += 1
            else:
                break

        if len(names) > 5:
            text_tables['items'] = names

    @staticmethod
    def _scan_gen1_moves_jp(rom_data: bytes, charmap: dict, eos: int, text_tables: dict):
        """Scan JP Gen I move names. Anchors at はたく (Pound, index 0).
        Skips unknown control bytes (< 0x60) within names so fragments join correctly.
        Sets text_tables['moves'] directly.
        """
        if 'moves' in text_tables:
            return

        reverse = {v: k for k, v in charmap.items() if isinstance(v, str) and len(v) == 1}
        try:
            anchor = bytes([reverse[c] for c in 'はたく']) + bytes([eos])
        except KeyError:
            return

        pos = rom_data.find(anchor)
        if pos < 0:
            return

        names = []
        i = pos
        while i < len(rom_data) and len(names) < 200:
            j, chars = i, []
            while j < len(rom_data) and j < i + 16 and rom_data[j] != eos:
                b = rom_data[j]
                ch = charmap.get(b)
                if ch is not None:
                    chars.append(ch)
                elif b >= 0x60:
                    break  # unknown displayable byte = end of table
                j += 1
            name = ''.join(chars).strip()
            if rom_data[j] == eos:
                if len(name) >= 2:
                    names.append(name)
                i = j + 1
                if len(names) > 10 and not name:
                    break
            else:
                break

        if len(names) > 10:
            text_tables['moves'] = names

    @staticmethod
    def _scan_gen12_moves_en(rom_data: bytes, charmap: dict, eos: int, text_tables: dict, count: int = 165):
        """Scan EN Gen I/II move names: variable-length, eos-terminated, POUND first.
        0-indexed like the JP table (Pound = 0, so move id = index + 1)."""
        if 'moves' in text_tables:
            return
        reverse = {}
        for k, v in sorted(charmap.items()):  # first byte wins: space is 0x7F, not a later alias
            if isinstance(v, str) and len(v) == 1: reverse.setdefault(v, k)
        try:
            enc = lambda s: bytes([reverse[ch] for ch in s]) + bytes([eos])
            anchor = enc('POUND') + enc('KARATE CHOP')
        except KeyError:
            return
        i = rom_data.find(anchor)
        if i < 0:
            return
        names = []
        while len(names) < count:
            j = rom_data.index(eos, i)
            names.append(''.join(charmap.get(b, '?') for b in rom_data[i:j]))
            i = j + 1
        text_tables['moves'] = names

    @staticmethod
    def _scan_gen1_species_varlen(rom_data: bytes, charmap: dict, eos: int,
                                  text_tables: dict,
                                  anchor_pair: tuple = ('サイドン', 'ガルーラ')):
        """Scan Gen I JP species names — packed variable-length EOS-terminated table.

        Anchors on サイドン+ガルーラ (internal indices 0-1), reads all EOS groups
        forward, then splits packed entries via normalization against the
        disassembly-verified reference (JP_DISASM).
        """
        if 'species' in text_tables:
            return

        reverse = {v: k for k, v in charmap.items() if isinstance(v, str) and len(v) == 1}
        name1, name2 = anchor_pair
        try:
            enc1 = bytes([reverse[c] for c in name1]) + bytes([eos])
            enc2_start = bytes([reverse[c] for c in name2])
        except KeyError:
            return

        search = 0
        table_start = -1
        while True:
            p = rom_data.find(enc1, search)
            if p < 0:
                break
            if rom_data[p + len(enc1): p + len(enc1) + len(enc2_start)] == enc2_start:
                table_start = p
                break
            search = p + 1

        if table_start < 0:
            return

        # Scan forward collecting raw EOS-terminated groups
        raw = []
        i = table_start
        while i < len(rom_data) and len(raw) < 250:
            chars = []
            while i < len(rom_data) and rom_data[i] != eos:
                b = rom_data[i]
                ch = charmap.get(b)
                if ch:
                    chars.append(ch)
                elif b >= 0x60:
                    break  # unknown displayable = end of table
                # b < 0x60: control code, skip silently
                i += 1
            if i < len(rom_data) and rom_data[i] == eos:
                raw.append(''.join(chars))
                i += 1
            else:
                break

        # Split packed groups using normalization + disassembly reference
        all_species = []
        for group in raw:
            text = Kanto_rbg._jp_normalize(group)
            while text:
                found = False
                for name in Kanto_rbg.JP_REF:
                    if text.startswith(name):
                        all_species.append(Kanto_rbg.JP_NORM_TO_ORIG[name])
                        text = text[len(name):]
                        found = True
                        break
                if not found:
                    text = text[1:]

        if len(all_species) > 5:
            text_tables['species'] = [''] + all_species  # dummy at index 0

    @staticmethod
    def _scan_gen1_species(rom_data: bytes, charmap: dict, eos: int,
                           text_tables: dict,
                           anchor_pair: tuple = ('RHYDON', 'KANGASKHAN'),
                           max_entries: int = 191,
                           dex_sig: bytes = None,
                           skip_reorder: bool = False):
        """Scan Gen I/II species names starting from RHYDON (internal index 1).

        Gen I stores species names as fixed-width 10-byte entries padded with 0x50 (EOS).
        The names are in INTERNAL index order, not Pokédex order.
        We find RHYDON, read 190 entries, then reorder to Pokédex order using the
        internal→dex mapping table also stored in the ROM.

        Works for both EN and JP ROMs — tries EN anchors first (RHYDON/KANGASKHAN),
        falls back to JP anchors (サイホーン/ガルーラ). Same internal order, same function.
        """
        if 'species' in text_tables:
            return

        SLOT = 10  # Gen I/II species names are always 10 bytes

        name1, name2 = anchor_pair
        reverse = {v: k for k, v in charmap.items() if isinstance(v, str) and len(v) == 1}
        try:
            enc1 = bytes([reverse[c] for c in name1])
            enc2 = bytes([reverse[c] for c in name2])
        except KeyError:
            return

        anchor1 = enc1 + bytes([eos] * (SLOT - len(enc1)))
        anchor2 = (enc2 + bytes([eos] * (SLOT - len(enc2))))[:SLOT]

        table_start = -1
        search = 0
        while True:
            pos = rom_data.find(anchor1, search)
            if pos < 0:
                break
            if rom_data[pos + SLOT: pos + SLOT + SLOT] == anchor2:
                table_start = pos
                break
            search = pos + 1

        if table_start < 0:
            return

        # Read backwards one slot for index 0 (MissingNo / dummy)
        start = max(0, table_start - SLOT)

        # Read entries (index 0..max_entries-1): 0=dummy, 1=RHYDON, ...
        internal_names = []
        for idx in range(max_entries):
            off = start + idx * SLOT
            if off + SLOT > len(rom_data):
                break
            chars = []
            for b in rom_data[off: off + SLOT]:
                if b == eos:
                    break
                ch = charmap.get(b)
                if ch is None:
                    break
                chars.append(ch)
            internal_names.append(''.join(chars).rstrip())

        if len(internal_names) < 10:
            return

        if skip_reorder:
            text_tables['species'] = internal_names
            return

        # Now find the internal→Pokédex mapping table to reorder into dex order.
        # dex_sig identifies the table: first 3 entries' dex numbers.
        # Gen I default: [112, 115, 29] (Rhydon, Kangaskhan, Nidoran♀)
        # Gen II:        [112, 113, 114] (Rhydon, Chansey, Tangela)
        if dex_sig is None:
            dex_sig = bytes([112, 115, 29])
        dex_table_off = rom_data.find(dex_sig)
        if dex_table_off < 0:
            # Can't find the mapping — store in internal order with a dummy at 0
            text_tables['species'] = internal_names
            return

        # Read mapping table (max_entries - 1 bytes, one per internal ID 1..N)
        n_internal = max_entries - 1
        dex_map = rom_data[dex_table_off: dex_table_off + n_internal]

        # Build Pokédex-ordered list: species[0] = dummy, species[1] = Bulbasaur, ...
        max_dex = n_internal
        dex_names = [''] * (max_dex + 1)
        for internal_id in range(1, min(len(internal_names), n_internal + 1)):
            if internal_id - 1 < len(dex_map):
                dex_num = dex_map[internal_id - 1]
                if 1 <= dex_num <= max_dex:
                    dex_names[dex_num] = internal_names[internal_id]

        # Trim trailing empty slots
        while dex_names and not dex_names[-1]:
            dex_names.pop()

        if len(dex_names) > 10:
            text_tables['species'] = dex_names


    # ── Base decoders (Gen I format) ──
    # Personal: 28 bytes. [dex][HP][Atk][Def][Spe][Spc][T1][T2][catch][exp][dim][fptr(2)][bptr(2)][mv1-4][growth][TM(7)]
    def decode_personal(self, data, file_idx, text_tables, **kw):
        import struct
        if len(data) < 28: return None
        dex, hp, atk, dfn, spe, spc = struct.unpack_from('<6B', data, 0)
        t1, t2 = data[6], data[7]
        catch, base_exp = data[8], data[9]
        moves = [data[15], data[16], data[17], data[18]]
        growth = data[19]
        sp = text_tables.get('species', [])
        mv = text_tables.get('moves', [])
        name = sp[dex] if dex < len(sp) else f'#{dex}'
        lines = [f"#{dex} {name}"]
        lines.append(f"HP {hp} / Atk {atk} / Def {dfn} / Spe {spe} / Spc {spc}")
        t1n = self.TYPE_NAMES.get(t1, f'?{t1}')
        t2n = self.TYPE_NAMES.get(t2, f'?{t2}')
        lines.append(f"Type: {t1n}" + (f"/{t2n}" if t1 != t2 else ""))
        lines.append(f"Catch rate: {catch}  Base Exp: {base_exp}")
        lines.append(f"Growth: {self.GROWTH_RATES.get(growth, f'?{growth}')}")
        start_moves = [mv[m] if m < len(mv) else f'#{m}' for m in moves if m != 0]
        if start_moves:
            lines.append(f"Starting moves: {', '.join(start_moves)}")
        return '\n'.join(lines)

    # Move data: 6 bytes. [anim][effect][power][type][accuracy][pp]
    def decode_move(self, data, file_idx, text_tables, **kw):
        if len(data) < 6: return None
        anim, effect, power, mtype, acc, pp = data[0], data[1], data[2], data[3], data[4], data[5]
        mv = text_tables.get('moves', [])
        name = mv[file_idx] if file_idx < len(mv) else f'Move #{file_idx}'
        tn = self.TYPE_NAMES.get(mtype, f'?{mtype}')
        lines = [f"{name} ({tn})"]
        lines.append(f"Power: {power}  Accuracy: {acc}  PP: {pp}")
        if effect: lines.append(f"Effect: {effect}")
        return '\n'.join(lines)

    # Evolution: uses _extract_gen12_evo_learnset, returns evo part
    def decode_evolution(self, data, file_idx, text_tables, **kw):
        evos, _ = self._extract_gen12_evo_learnset(file_idx, self._current_rom_ref(), text_tables)
        if not evos: return "No evolutions"
        sp = text_tables.get('species', [])
        name = sp[file_idx] if file_idx < len(sp) else f'#{file_idx}'
        return f"{name}\n" + '\n'.join(evos)

    # Learnset: uses _extract_gen12_evo_learnset, returns learnset part
    def decode_learnset(self, data, file_idx, text_tables, **kw):
        _, ldata = self._extract_gen12_evo_learnset(file_idx, self._current_rom_ref(), text_tables)
        if ldata is None: return None
        mv = text_tables.get('moves', [])
        sp = text_tables.get('species', [])
        name = sp[file_idx] if file_idx < len(sp) else f'#{file_idx}'
        lines = [f"{name} — Learnset"]
        i = 0
        while i + 1 < len(ldata):
            lvl, mid = ldata[i], ldata[i+1]
            mname = mv[mid] if mid < len(mv) else f'#{mid}'
            lines.append(f"  Lv. {lvl}: {mname}")
            i += 2
        return '\n'.join(lines) if len(lines) > 1 else f"{name} — No moves learned by level"

    # Trainer: wraps existing decode_trainer_class with consistent signature
    def decode_trainer(self, data, file_idx, text_tables, **kw):
        return self.decode_trainer_class(file_idx, self._current_rom_ref(), text_tables)

    def _current_rom_ref(self):
        """Build a minimal current_rom dict from self for Gen I/II decoders."""
        return {
            'data': bytes(self.rom) if self.rom else b'',
            'header': self.header or {},
            'type': self.rom_type or 'gb',
            'gen1_offsets': getattr(self, '_gen1_offsets', {}),
        }

    def decode_encounters(self, map_idx: int, current_rom: dict, text_tables: dict) -> str:
        """Decode Gen I/II wild encounters for a given map index.
        Format: [rate][species,level]×10[water_rate][species,level]×10 = 42 bytes per map.
        Species are internal constants; convert via dex_table → species text table."""
        if not current_rom:
            return ''
        g1off    = current_rom.get('gen1_offsets', {})
        table    = g1off.get('enc_table_base', 0)
        bank_base = g1off.get('enc_bank_base', 0)
        if not table or not bank_base:
            return ''
        rom_data = bytes(current_rom.get('data') or b'')
        ptr_off  = table + map_idx * 2
        if ptr_off + 2 > len(rom_data):
            return ''
        ptr_val  = int.from_bytes(rom_data[ptr_off: ptr_off + 2], 'little')
        if not (0x4000 <= ptr_val <= 0x7FFF):
            return ''
        addr = bank_base + (ptr_val - 0x4000)
        if addr + 42 > len(rom_data):
            return ''

        sp_list   = text_tables.get('species', [])
        dex_tb    = g1off.get('dex_table_base', 0)
        dex_table = list(rom_data[dex_tb: dex_tb + 190]) if dex_tb else []

        def sp_name(const):
            # sp_list[0] is a dummy; sp_list[const] = species at internal const
            if 0 < const < len(sp_list) and sp_list[const]:
                return sp_list[const]
            return f'sp#{const}'

        grass_rate = rom_data[addr]
        water_rate = rom_data[addr + 21]

        if grass_rate == 0 and water_rate == 0:
            return ''

        lines = [f'Map #{map_idx}']

        if grass_rate > 0:
            lines.append('Grass:')
            seen = {}
            for j in range(10):
                lv = rom_data[addr + 1 + j * 2]
                sp = rom_data[addr + 2 + j * 2]
                name = sp_name(sp)
                seen.setdefault(name, []).append(lv)
            for name, lvs in seen.items():
                lv_str = f'Lv. {min(lvs)}-{max(lvs)}' if min(lvs) != max(lvs) else f'Lv. {min(lvs)}'
                lines.append(f'  {name:<20}{lv_str}')

        if water_rate > 0:
            lines.append('Surf:')
            seen = {}
            for j in range(10):
                lv = rom_data[addr + 22 + j * 2]
                sp = rom_data[addr + 23 + j * 2]
                name = sp_name(sp)
                seen.setdefault(name, []).append(lv)
            for name, lvs in seen.items():
                lv_str = f'Lv. {min(lvs)}-{max(lvs)}' if min(lvs) != max(lvs) else f'Lv. {min(lvs)}'
                lines.append(f'  {name:<20}{lv_str}')

        return '\n'.join(lines)

    def _g1_scan(self):
        """Map names + static/gift mons, all found by shape.
        Names: town-map entries (one 3-byte entry per outdoor map, then 4-byte 'first map id past this name' entries, 0xFF end).
        Objects: header -> object data; text byte bit 0x40 = battle object, next byte < 200 = species (else trainer class).
        ASM: 'lb bc, sp/lv; call GivePokemon' and 'ld a, sp; ld [wCurOpponent]; ld a, lv; ld [wCurEnemyLevel]' -- the
        call target / RAM pair is whichever one the ROM uses most inside map scripts."""
        import re, bisect, collections
        r = bytes(self._current_rom_ref().get('data') or b'')
        if getattr(self, '_g1_key', None) == r[0x134:0x150]: return
        self._g1_key, self._g1_names, self._g1_statics = r[0x134:0x150], {}, []
        u = lambda o: r[o] | r[o + 1] << 8
        A = lambda bk, p: bk * 0x4000 + p - 0x4000 if 0x4000 <= p < 0x8000 else None
        S = lambda bk, p: (lambda a: a if a is not None and a < r.find(b'\x50', a, a + 24) else None)(A(bk, p))
        cm = (next((getattr(self, k) for k in dir(self) if 'CHARMAP' in k and 'JP' in k), None) if r[0x14A] == 0 else None) or self.CHARMAP_EN
        for o in range(0x4003, len(r) - 8):
            bk, n = o // 0x4000, 0
            while o + 4 * n + 4 < len(r) and r[o + 4 * n] != 0xFF and (n == 0 or r[o + 4 * n] > r[o + 4 * n - 4]) and S(bk, u(o + 4 * n + 2)) is not None: n += 1
            if n < 20 or r[o + 4 * n] != 0xFF: continue
            k = 0
            while S(bk, u(o - 3 * k - 2)) is not None: k += 1
            if 20 <= k < r[o]: break
        else: return
        dec = lambda a: ''.join(cm.get(ch, ' ' if ch == 0x4E else '') for ch in r[a:r.find(b'\x50', a)]).strip()
        for i in range(k): self._g1_names[i] = dec(S(bk, u(o - 3 * k + 3 * i + 1)))
        j = 0
        for mi in range(k, 256):
            while j < n and mi >= r[o + 4 * j]: j += 1
            if j < n: self._g1_names[mi] = dec(S(bk, u(o + 4 * j + 2)))
        # Map header table: 248-ish u16 pointers + a parallel bank-byte table (any bank); keep the pairing that yields the longest run of sane headers
        nb, best = len(r) // 0x4000, (0, 0, 0)
        def hdr(b, P, i):
            h = A(b, u(P + 2 * i)) if 0 < b < nb else None
            if h is None or h + 60 > len(r) or r[h] >= 0x20 or not 0 < r[h + 1] <= 0x40 or not 0 < r[h + 2] <= 0x40 or r[h + 9] > 0xF: return None
            ob = A(b, u(h + 10 + 11 * bin(r[h + 9]).count('1')))
            if ob is None or A(b, u(h + 5)) is None or ob + 200 > len(r): return None
            q = ob + 1; nw = r[q]; q += 1  # object data must parse: warp dests are map ids / 0xFF, <=16 signs and objects, sprites nonzero
            if nw > 0x20 or any(r[q + 4 * k + 3] not in range(256 - 8) and r[q + 4 * k + 3] != 0xFF for k in range(nw)): return None
            q += 4 * nw; ns = r[q]; q += 1 + 3 * ns; no = r[q]; q += 1
            if ns > 16 or no > 16: return None
            for _ in range(no):
                if not 0 < r[q] < 0x80: return None
                q += 8 if r[q + 5] & 0x40 else 7 if r[q + 5] & 0x80 else 6
            return h
        Ps = [q for q in range(0, len(r) - 500) if all(0x40 <= r[q + 2 * i + 1] < 0x80 for i in range(240))]
        Bs = [q for q in range(0x4000, len(r) - 256) if all(0 < r[q + i] < nb for i in range(240))]
        for P in Ps:
            for B in Bs:
                if any(hdr(r[B + k], P, k) is None for k in range(8)): continue  # real table: first maps (towns) all valid; unused slots later are junk, so score the whole table
                best = max(best, (sum(hdr(r[B + k], P, k) is not None for k in range(256)), -P, B))
        best = (best[0], -best[1], best[2])
        N, P, B = 256, best[1], best[2]
        starts, seen = [], set()
        for mi in range(N):
            b = r[B + mi]; h = hdr(b, P, mi)
            if h is None or h in seen: continue
            seen.add(h)
            ob = A(b, u(h + 10 + 11 * bin(r[h + 9] & 0xF).count('1')))
            if ob is None: continue
            q = ob + 1; q += 1 + 4 * r[q]; ns = r[q]; q += 1 + 3 * ns; no = r[q]; q += 1
            for _ in range(no):
                t = r[q + 5]
                if t & 0x40 and r[q + 6] < 200 and 0 < r[q + 7] <= 100: self._g1_statics.append((mi, 'static', r[q + 6], r[q + 7]))
                q += 8 if t & 0x40 else 7 if t & 0x80 else 6
            tt = A(b, u(h + 5))
            starts += [(a, mi) for a in [A(b, u(h + 7)), tt] + [A(b, u(tt + 2 * i)) for i in range(ns + no) if tt is not None] if a is not None]
        starts.sort(); ks = [a for a, _ in starts]
        def where(x):
            i = bisect.bisect_right(ks, x) - 1
            return starts[i][1] if i >= 0 and x - ks[i] < 0x1000 and x // 0x4000 == ks[i] // 0x4000 else None
        g = [(m.start(), m.group(2)[0], m.group(1)[0], m.group(3)) for m in re.finditer(rb'\x01(.)(.)\xcd(..)', r, re.S)] + [(m.start(), m.group(1)[0], m.group(2)[0], m.group(3)) for m in re.finditer(rb'\x06(.)\x0e(.)\xcd(..)', r, re.S)]
        g = [(where(x), sp, lv, t) for x, sp, lv, t in g if 0 < sp < 200 and 1 < lv <= 100 and where(x) is not None]  # lv 1 = GiveItem (lb bc, item, 1), Gen I never gifts a Lv1 mon
        # GivePokemon (home bank) opens with ld a,b / ld [species],a / ld a,c / ld [level],a; the level address it writes is also what scripted battles store to
        G = {t: r[o + 6:o + 8] for t in {x[3] for x in g} for o in [t[0] | t[1] << 8] if o < 0x3FF0 and r[o] == 0x78 and r[o + 1] == 0xEA and r[o + 4:o + 6] == b'\x79\xea'}
        self._g1_statics += [(mi, 'gift', sp, lv) for mi, sp, lv, t in g if t in G]
        LV = set(G.values())
        w = [(where(m.start()), m.group(1)[0], m.group(3)[0], m.group(2) + m.group(4)) for m in re.finditer(rb'\x3e(.)\xea(..)\x3e(.)\xea(..)', r, re.S)]
        w = [x for x in w if x[0] is not None and 0 < x[1] < 200 and 1 < x[2] <= 100]
        w = [x for x in w if x[3][2:] in LV]
        if w: OPP = collections.Counter(x[3][:2] for x in w).most_common(1)[0][0]; self._g1_statics += [(mi, 'static', sp, lv) for mi, sp, lv, t in w if t[:2] == OPP]  # drops the old man's tutorial (writes battle type, not opponent)

    def map_name(self, mi):
        self._g1_scan(); return getattr(self, '_g1_names', {}).get(mi)

    def iter_encounters(self):
        """(id, species_const, form, lo, hi) per map/area/species. Rate byte 0 = no slots follow (grass skipped -> surf rate is next byte)."""
        ref = self._current_rom_ref(); g, rom = ref.get('gen1_offsets', {}), bytes(ref.get('data') or b'')
        t, bank = g.get('enc_table_base', 0), g.get('enc_bank_base', 0)
        if not t or not bank: return None
        out = []
        for mi in range(248):
            pv = int.from_bytes(rom[t + mi * 2:t + mi * 2 + 2], 'little')
            if not 0x4000 <= pv <= 0x7FFF: continue
            a = bank + pv - 0x4000
            for area in ('grass', 'surf'):
                if a >= len(rom): break
                rate = rom[a]; a += 1
                if not rate: continue
                seen = {}
                for j in range(10): seen.setdefault(rom[a + 2 * j + 1], []).append(rom[a + 2 * j])
                a += 20
                out += [(f"{self.map_name(mi) or 'Map'} [{mi}] {area}", sp, 0, min(l), max(l), {'location': self.map_name(mi) or f'Map [{mi}]', 'method': area}) for sp, l in seen.items()]
        self._g1_scan()
        out += [(f"{self.map_name(mi) or 'Map'} [{mi}] {kind}", sp, 0, lv, lv, {'location': self.map_name(mi) or f'Map [{mi}]', 'method': kind}) for mi, kind, sp, lv in dict.fromkeys(self._g1_statics)]
        return out

    def _discover_gen1_tables(self):
        """Find personal/trainer data offsets in a Gen I/II GB/GBC ROM.

        Anchors on known data signatures — same philosophy as _discover_gen3_tables().
        Results stored in self._gen1_offsets.
        """
        rom_data = getattr(self, 'rom', b'')
        if not rom_data:
            return None
        rom_data = bytes(rom_data)
        text_tables = getattr(self, 'text_tables', {})

        offsets = {}

        # ── Personal data: Bulbasaur's stats HP=45,Atk=49,Def=49,Spe=45,Spc=65 ──
        # Entry format (28B, Pokédex order): [dex_num][HP][Atk][Def][Spe][Spc][T1][T2]
        #   [catch][base_exp][sprite_dim][front_ptr(2)][back_ptr(2)][mv1-4][growth][TM/HM(7B)]
        bulb_sig = bytes([0x2D, 0x31, 0x31, 0x2D, 0x41])
        idx = rom_data.find(bulb_sig)
        if idx >= 0:
            offsets['personal_base'] = idx - 1  # dex_num byte precedes HP
            # Detect entry size: Gen I=28B, Gen II=32B
            # Verify by checking dex_num of next entry at stride 28 vs 32
            base = idx - 1
            size = 28
            for stride in (32, 28):
                if base + stride < len(rom_data) and rom_data[base + stride] == 2:
                    size = stride
                    break
            offsets['personal_size'] = size

        # ── Dex table: internal_species_constant → Pokédex number ──
        # Anchor: internal[1]=Rhydon(dex112=0x70), [2]=Kangaskhan(115=0x73), [3]=Nidoran♂(32=0x20)
        dex_sig = bytes([0x70, 0x73, 0x20])
        idx = rom_data.find(dex_sig)
        if idx >= 0:
            offsets['dex_table_base'] = idx - 1  # entry[0] is the byte before the match

        # ── Trainer class pointer table ──
        # TrainerDataPointers stores trainer data with FF format prefix.
        # Find Brock's core party bytes, step back 1 for the FF prefix,
        # compute bank pointer, search within same bank, walk back to table start.
        # Red/Blue: FF 0C A9(Geodude) 0E 22(Onix) 00. Yellow: FF 0A A9 0C 22 00.
        brock_abs = -1
        for brock_party in (bytes([0xFF, 0x0C, 0xA9, 0x0E, 0x22, 0x00]),   # Red/Blue
                            bytes([0xFF, 0x0A, 0xA9, 0x0C, 0x22, 0x00])):  # Yellow
            brock_abs = rom_data.find(brock_party)
            if brock_abs >= 0:
                break
        if brock_abs >= 0:
            bank_num   = brock_abs // 0x4000
            bank_base  = bank_num * 0x4000
            ptr_val    = (brock_abs - bank_base) + 0x4000
            ptr_bytes  = ptr_val.to_bytes(2, 'little')
            # Search only within same bank to avoid false positives
            bank_start = bank_num * 0x4000
            bank_end   = bank_start + 0x4000
            ptr_off    = rom_data.find(ptr_bytes, bank_start, bank_end)
            if ptr_off < 0:
                ptr_off = rom_data.find(ptr_bytes)  # fallback: whole ROM
            if ptr_off >= 0:
                start = ptr_off
                while start >= 2:
                    v = int.from_bytes(rom_data[start - 2: start], 'little')
                    if 0x4000 <= v <= 0x7FFF:
                        start -= 2
                    else:
                        break
                offsets['trainer_class_ptr_table'] = start
                offsets['trainer_class_bank_base']  = bank_base
                offsets['gym_brock_class'] = (ptr_off - start) // 2

            # Gym leaders 0-6: sequential in ROM (Brock→Misty→Surge→Erika→Koga→Sabrina→Blaine)
            # Store offset including the FF format prefix — decoder handles it.
            gym_offsets = []
            i = brock_abs  # include FF format byte
            while i < len(rom_data) and len(gym_offsets) < 10:
                gym_offsets.append(i)
                while i < len(rom_data) and rom_data[i] != 0x00:
                    i += 2
                i += 1  # skip 0x00
                if i < len(rom_data) and rom_data[i] == 0xFF:
                    i += 1  # skip 0xFF class terminator
                else:
                    break   # multi-trainer class or data ended
            # Giovanni has 3 fights stored separately — find by his Gym team signature
            # Gym: lv45 Rhyhorn / lv42 Dugtrio / lv44 Nidoqueen / lv45 Nidoking / lv50 Rhydon
            # Level sequence: FF 2D ?? 2A ?? 2C ?? 2D ?? 32 ?? 00
            gio_gym_off = -1
            for j in range(len(rom_data) - 12):
                if (rom_data[j] == 0xFF and rom_data[j+1] == 0x2D and rom_data[j+3] == 0x2A
                        and rom_data[j+5] == 0x2C and rom_data[j+7] == 0x2D and rom_data[j+9] == 0x32):
                    gio_gym_off = j + 1  # skip the 0xFF format flag; decoder starts at first lv byte
                    break
            # Giovanni Rocket Hideout fight is just before the Gym team in ROM
            # Walk backward from Gym to find earlier 0xFF-prefixed entry
            gio_hideout_off = -1
            if gio_gym_off > 1:
                # The previous entry ends just before gio_gym_off - 1 (the 0xFF)
                # Scan backward for the 0xFF that starts it
                j = gio_gym_off - 2  # byte before the 0xFF of Gym entry
                if j > 0 and rom_data[j] == 0x00:  # terminator of previous entry
                    k = j - 1
                    while k > 1 and rom_data[k] != 0xFF:
                        k -= 1
                    if rom_data[k] == 0xFF:
                        gio_hideout_off = k + 1
            if gio_gym_off >= 0:
                if gio_hideout_off >= 0:
                    gym_offsets.extend([gio_hideout_off, gio_gym_off])
                else:
                    gym_offsets.append(gio_gym_off)
            offsets['gym_leader_offsets'] = gym_offsets  # [brock, misty, surge, erika, koga, sabrina, blaine, giovanni...]

        # ── Evo + learnset pointer table ─────────────────────────────────────────
        # Anchor: Bulbasaur evo (01 10 09 00 = level 16 → Ivysaur const 9)
        # Table is DISASM-0-indexed; lookup = table_base + (const-1)*2
        # data_base = (bank-1)*0x4000 where bank = floor(abs_bulba/0x4000)
        bulba_evo_sig = bytes([0x01, 0x10, 0x09, 0x00])
        abs_bulba_evo = rom_data.find(bulba_evo_sig)
        if abs_bulba_evo >= 0:
            bank = abs_bulba_evo // 0x4000
            evo_data_base = (bank - 1) * 0x4000
            ptr_bulba = abs_bulba_evo - evo_data_base
            pb_bytes = ptr_bulba.to_bytes(2, 'little')
            # Also find Ivysaur evo (01 20 XX 00) nearby to confirm table location
            abs_ivy_evo = -1
            for off in range(max(0, abs_bulba_evo - 0x800), abs_bulba_evo + 0x800):
                if (off + 4 <= len(rom_data) and rom_data[off] == 0x01
                        and rom_data[off + 1] == 0x20 and rom_data[off + 3] == 0x00):
                    abs_ivy_evo = off
                    break
            evo_table_base = -1
            if abs_ivy_evo >= 0:
                ptr_ivy = abs_ivy_evo - evo_data_base
                pi_bytes = ptr_ivy.to_bytes(2, 'little')
                # Bulbasaur=DISASM[152], Ivysaur=DISASM[8] → 144 indices = 288 bytes apart
                off = 0
                while True:
                    pi_off = rom_data.find(pi_bytes, off)
                    if pi_off < 0:
                        break
                    expected = pi_off + (152 - 8) * 2
                    if (expected + 2 <= len(rom_data)
                            and rom_data[expected:expected + 2] == pb_bytes):
                        evo_table_base = pi_off - 8 * 2
                        break
                    off = pi_off + 1
            if evo_table_base < 0:
                # Fallback: use Bulbasaur ptr alone
                pb_off = rom_data.find(pb_bytes)
                if pb_off >= 0:
                    evo_table_base = pb_off - 152 * 2
            if evo_table_base >= 0:
                offsets['evo_learnset_table']      = evo_table_base
                offsets['evo_learnset_data_base']  = evo_data_base

        # ── Item name table ───────────────────────────────────────────────────────
        # Anchor: マスターボール (Master Ball) as item 1
        masterball_jp = bytes([0x9D, 0x8C, 0x8F, 0xE3, 0x1C, 0xE3, 0xA6])
        masterball_en = b'MASTER BALL'
        for anchor in (masterball_jp, masterball_en):
            p = rom_data.find(anchor)
            if p >= 0:
                # Scan backward to find table start (item 1 = first entry)
                start = p
                while start > 0 and rom_data[start - 1] == 0x50:
                    start -= 1  # skip leading EOS (item 0 = blank)
                offsets['item_name_table'] = start
                break

        # ── Gen II (GBC) trainer class pointer table ──
        # Structure: one pointer per class, each pointing to [name 0x50 fmt party 0xFF] groups.
        # Ordering (from pret/pokegold): Falkner=0, Whitney=1 ... Rival1=8 ... Champion=15 ... Red=62
        # Anchor: "FALKNER@" is class 0 (first entry) — its pointer appears with no valid ptr before it.
        if self.CONTAINER == 'gbc':
            falkner_name = bytes([0x85, 0x80, 0x8B, 0x8A, 0x8D, 0x84, 0x91, 0x50])
            falkner_abs  = rom_data.find(falkner_name)
            if falkner_abs >= 0:
                bank_num  = falkner_abs // 0x4000
                bank_base = bank_num * 0x4000
                ptr_val   = (falkner_abs - bank_base) + 0x4000
                ptr_bytes = ptr_val.to_bytes(2, 'little')
                search_off = 0
                while True:
                    ptr_off = rom_data.find(ptr_bytes, search_off)
                    if ptr_off < 0:
                        break
                    # Entry 0: byte before must NOT be a valid same-bank pointer
                    prev_val = int.from_bytes(rom_data[ptr_off - 2: ptr_off], 'little') if ptr_off >= 2 else 0
                    if not (0x4000 <= prev_val <= 0x7FFF):
                        end = ptr_off
                        while end + 2 <= len(rom_data):
                            v = int.from_bytes(rom_data[end: end + 2], 'little')
                            if 0x4000 <= v <= 0x7FFF:
                                end += 2
                            else:
                                break
                        count = (end - ptr_off) // 2
                        if count >= 10:
                            silver_class = -1
                            for silver_sig in (bytes([0x05, 0x98, 0xFF]), bytes([0x05, 0x9B, 0xFF]),
                                               bytes([0x05, 0x9E, 0xFF])):
                                s_abs = rom_data.find(silver_sig)
                                if s_abs < 3 or rom_data[s_abs - 2] != 0x50:
                                    continue
                                ns = s_abs - 3
                                while ns > 0 and rom_data[ns - 1] != 0xFF:
                                    ns -= 1
                                spb = ((ns - bank_base) + 0x4000).to_bytes(2, 'little')
                                for ci in range(count):
                                    if rom_data[ptr_off + ci * 2: ptr_off + ci * 2 + 2] == spb:
                                        silver_class = ci
                                        break
                                if silver_class >= 0:
                                    break
                            offsets['trainer_class_ptr_table'] = ptr_off
                            offsets['trainer_class_bank_base']  = bank_base
                            offsets['trainer_class_count']      = count
                            offsets['silver_class']             = silver_class
                            # Build name → class_id index by scanning each group's first trainer name
                            name_to_class = {}
                            b2c = {i: chr(ord('A') + i - 0x80) for i in range(0x80, 0x9A)}
                            b2c.update({i: chr(ord('a') + i - 0xA0) for i in range(0xA0, 0xBA)})
                            for ci in range(count):
                                pv = int.from_bytes(rom_data[ptr_off + ci * 2: ptr_off + ci * 2 + 2], 'little')
                                if not (0x4000 <= pv <= 0x7FFF):
                                    continue
                                ga = bank_base + (pv - 0x4000)
                                name_bytes = []
                                j = ga
                                while j < len(rom_data) and rom_data[j] != 0x50 and len(name_bytes) < 20:
                                    name_bytes.append(rom_data[j])
                                    j += 1
                                name = ''.join(b2c.get(b, '') for b in name_bytes).strip()
                                if name:
                                    name_to_class[name.upper()] = ci
                                    name_to_class[name] = ci
                            offsets['trainer_name_to_class'] = name_to_class
                            break
                    search_off = ptr_off + 1

        # ── Wild encounter table (GB/GBC) ──
        # Gen 1: pointer array, 42 bytes per map [rate][sp,lv]×10 [water_rate][sp,lv]×10
        # Gen 2: flat sequential table, 47 bytes per entry [group][map][3 rates][7 lv,sp ×3 times]
        if rom_data:
            for i in range(len(rom_data) - 42):
                if rom_data[i] != 0x19: continue
                levels = [rom_data[i + 1 + j*2] for j in range(10)]
                if not all(self.ENC_ANCHOR_LEVELS[0] <= l <= self.ENC_ANCHOR_LEVELS[1] for l in levels): continue
                water_rate = rom_data[i + 21]
                if water_rate != 0: continue
                species_set = {rom_data[i + 2 + j*2] for j in range(10)}
                if len(species_set) != 2: continue
                # Found Route 1 data. Find the pointer to it.
                bank_num  = i // 0x4000
                bank_base = bank_num * 0x4000
                ptr_val   = (i - bank_base) + 0x4000
                ptr_bytes = ptr_val.to_bytes(2, 'little')
                # Find pointer table entry
                ptr_off = rom_data.find(ptr_bytes)
                if ptr_off < 0: continue
                # Walk backward to table start
                table_start = ptr_off
                while table_start >= 2:
                    v = int.from_bytes(rom_data[table_start - 2: table_start], 'little')
                    if 0x4000 <= v <= 0x7FFF:
                        table_start -= 2
                    else:
                        break
                route1_idx = (ptr_off - table_start) // 2
                offsets['enc_table_base'] = table_start
                offsets['enc_bank_base']  = bank_base
                offsets['enc_route1_idx'] = route1_idx
                break

        # ── Gen 2 (GBC) flat encounter table ──
        # Format per entry: [map_group][map_number][morn_rate][day_rate][nite_rate]
        #   + 7×[lv,sp] morning + 7×[lv,sp] day + 7×[lv,sp] night = 47 bytes
        # Anchor: Route 29 — group=24(0x18), map=3, rates=25,25,25, first morning = lv2 Pidgey(sp16)
        if self.CONTAINER == 'gbc':
            def _valid_gen2_entry(off):
                if off + 47 > len(rom_data): return False
                r1, r2, r3 = rom_data[off+2], rom_data[off+3], rom_data[off+4]
                if not (1 <= r1 <= 100 and 1 <= r2 <= 100 and 1 <= r3 <= 100): return False
                for period in range(3):
                    for slot in range(7):
                        sp = rom_data[off + 5 + period*14 + slot*2 + 1]
                        if sp == 0 or sp > 251: return False
                return True
            r29_sig = bytes([0x18, 0x03, 0x19, 0x19, 0x19, 0x02, 0x10])
            r29_off = rom_data.find(r29_sig)
            if r29_off >= 0:
                # Walk backward to find table start
                off = r29_off
                while off - 47 >= 0 and _valid_gen2_entry(off - 47):
                    off -= 47
                offsets['enc2_table_base'] = off
                offsets['enc2_route29_offset'] = r29_off - off
                # Also find the Kanto table — anchor on Diglett's Cave (3,75) with Diglett(50) morning
                # Diglett's Cave: rates ~10, first morning sp includes 50(Diglett)
                kanto_sig = bytes([3, 75])  # group=3, map=75 = Diglett's Cave
                kanto_off = rom_data.find(kanto_sig, off)  # Kanto table follows the Johto one; from byte 0 this hits code first
                if kanto_off >= 0 and _valid_gen2_entry(kanto_off):
                    offsets['enc2_kanto_table_base'] = kanto_off

        if offsets:
            self._gen1_offsets = offsets

        return offsets if offsets else None

    TYPE_NAMES = {
        0:'Normal', 1:'Fighting', 2:'Flying', 3:'Poison', 4:'Ground', 5:'Rock',
        7:'Bug', 8:'Ghost', 20:'Fire', 21:'Water', 22:'Grass', 23:'Electric',
        24:'Psychic', 25:'Ice', 26:'Dragon',
    }
    GROWTH_RATES = {0:'Medium Fast', 1:'Fast', 2:'Slow', 3:'Medium Slow'}

    @staticmethod
    def _gen1_resolve_const(key: str, g1off: dict, current_rom: dict, text_tables: dict) -> int:
        """Resolve a species name, dex number, or constant to a game constant (1-based)."""
        sp_list = text_tables.get('species', [])
        if key.isdigit():
            dex_num = int(key)
            # Dex number → game constant via dex_table
            dex_tb = g1off.get('dex_table_base', 0)
            rom_data = bytes((current_rom or {}).get('data') or b'')
            if dex_tb and rom_data:
                dex_table = list(rom_data[dex_tb: dex_tb + 190])
                for const, dex in enumerate(dex_table):
                    if dex == dex_num:
                        return const
            return -1
        # Name → find in species list → index IS the game constant
        for i, n in enumerate(sp_list):
            if n and (n.strip() == key.strip() or
                      Kanto_rbg._jp_normalize(n).strip() == Kanto_rbg._jp_normalize(key).strip()):
                return i
        return -1

    @staticmethod
    def _extract_gen12_evo_learnset(const: int, current_rom: dict, text_tables: dict):
        """Extract raw evo entries + learnset u8 pairs from Gen I/II combined evo+learnset table.
        Returns (evo_lines: list[str], learnset_bytes: bytes) or (None, None) on failure."""
        g1off = (current_rom or {}).get('gen1_offsets', {})
        table, db = g1off.get('evo_learnset_table', 0), g1off.get('evo_learnset_data_base', 0)
        if not table or not db or not current_rom:
            return None, None
        rom_data = bytes(current_rom.get('data') or b'')
        ptr_off = table + (const - 1) * 2
        if ptr_off + 2 > len(rom_data):
            return None, None
        i = db + int.from_bytes(rom_data[ptr_off:ptr_off + 2], 'little')
        sp_list, it_list = text_tables.get('species', []), text_tables.get('items', [])
        # Parse variable-length evo entries
        # Gen I: level/item(+lv)/trade(+1). Gen II (32B personal): all 3 bytes except stat (Tyrogue) = 4.
        _EVO_SIZES = {1: 3, 2: 3, 3: 3, 4: 3, 5: 4} if g1off.get('personal_size') == 0x20 else {1: 3, 2: 4, 3: 3, 4: 4}
        evos = []
        while i < len(rom_data) and rom_data[i] != 0x00:
            method = rom_data[i]
            sz = _EVO_SIZES.get(method, 1)
            if method in (1, 2, 3, 4):
                target = rom_data[i + sz - 1] if i + sz <= len(rom_data) else 0
                tname = sp_list[target] if target < len(sp_list) else f'#{target}'
                if method == 1: evos.append(f'  Level {rom_data[i+1]} \u2192 {tname}')
                elif method == 3: evos.append(f'  Trade \u2192 {tname}')
                else:
                    iid = int.from_bytes(rom_data[i+1:i+3], 'little')
                    iname = it_list[iid] if 0 < iid < len(it_list) else f'Item#{iid}'
                    prefix = 'Trade w/ ' if method == 4 else ''
                    evos.append(f'  {prefix}{iname} \u2192 {tname}')
            i += sz
        i += 1  # skip 0x00 evo terminator
        # Extract learnset as raw bytes (u8 pairs: level, move_id, level, move_id, ..., 0)
        start = i
        while i + 1 < len(rom_data) and rom_data[i] != 0:
            i += 2
        return evos, rom_data[start:i]

    def decode_trainer_class(self, class_id, current_rom: dict, text_tables: dict, direct_off: int = None, label: str = None) -> str:
        """Decode a Gen I or Gen II trainer class. Detects gen from personal_size.
        Gen I: fixed-level or 0xFF individual-levels format, class-terminated by 0xFF.
        Gen II: name+0x50, format byte, party 0xFF-terminated. Format 0-3 controls member size.
        Pass direct_off for gym leaders (Gen I only)."""
        g1off = (current_rom or {}).get('gen1_offsets', {})
        if not current_rom:
            return ''
        rom_data = bytes(current_rom.get('data') or b'')
        is_gen2 = g1off.get('personal_size', 28) == 32
        sp_list = text_tables.get('species', [])
        mv_list = text_tables.get('moves', [])
        it_list = text_tables.get('items', [])

        # Resolve pointer → absolute offset + boundary
        ptr_table = g1off.get('trainer_class_ptr_table', 0)
        bank_base = g1off.get('trainer_class_bank_base', 0x38000)
        data_end = None
        if direct_off is not None:
            data_off = direct_off
        else:
            if not ptr_table: return ''
            ptr_off = ptr_table + class_id * 2
            if ptr_off + 2 > len(rom_data): return ''
            ptr_val = int.from_bytes(rom_data[ptr_off:ptr_off + 2], 'little')
            if not (0x4000 <= ptr_val <= 0x7FFF): return ''
            data_off = bank_base + (ptr_val - 0x4000)
            nxt = ptr_off + 2
            if nxt + 2 <= len(rom_data):
                nv = int.from_bytes(rom_data[nxt:nxt + 2], 'little')
                if 0x4000 <= nv <= 0x7FFF:
                    data_end = bank_base + (nv - 0x4000)

        # Gen 1 species are in internal order — need dex table for names
        dex_tb = g1off.get('dex_table_base', 0)
        dex_table = list(rom_data[dex_tb:dex_tb + 190]) if (dex_tb and not is_gen2) else []

        def sp_name(c):
            if is_gen2:
                return sp_list[c] if 0 < c < len(sp_list) else f'sp#{c}'
            if c < len(sp_list) and sp_list[c]: return sp_list[c]
            if c < len(dex_table): return f'#{dex_table[c]}'
            return f'const#{c}'

        trainers = []
        i, limit = data_off, (data_end or len(rom_data))

        if is_gen2:
            # Gen II: [name 0x50] [fmt] [party entries] [0xFF terminator]
            while i < limit and len(trainers) < 50:
                while i < limit and rom_data[i] != 0x50: i += 1
                if i >= limit: break
                i += 1  # skip 0x50
                if i >= limit: break
                fmt = rom_data[i]
                bpp = {0: 2, 1: 6, 2: 3, 3: 7}.get(fmt, 2)
                i += 1
                party = []
                while i < limit and rom_data[i] != 0xFF and len(party) < 6:
                    lv = rom_data[i]
                    if lv == 0 or lv > 100: break
                    sp = rom_data[i + 1] if i + 1 < limit else 0
                    p = {'header': f'{sp_name(sp)} (Lv. {lv})'}
                    if fmt in (2, 3) and i + 2 < limit:
                        item = rom_data[i + 2]
                        if item and item <= len(it_list): p['item'] = it_list[item - 1]
                    if fmt in (1, 3):
                        mo = 2 if fmt == 1 else 3
                        mvs = [rom_data[i + mo + m] for m in range(4) if i + mo + m < limit]
                        mn = [mv_list[m - 1] if 0 < m <= len(mv_list) else '' for m in mvs]
                        mn = [m for m in mn if m]
                        if mn: p['moves'] = mn
                    party.append(p)
                    i += bpp
                if party: trainers.append(party)
                if i < limit and rom_data[i] == 0xFF: i += 1
        else:
            # Gen I: fixed-level or 0xFF individual-levels, 0x00 party terminator
            while i < limit:
                if rom_data[i] == 0xFF:
                    if data_end is None and trainers: break
                    i += 1
                    party = []
                    while i + 1 < limit and rom_data[i] != 0x00:
                        party.append({'header': f'{sp_name(rom_data[i+1])} (Lv. {rom_data[i]})'})
                        i += 2
                elif rom_data[i] == 0x00:
                    i += 1; continue
                else:
                    lv = rom_data[i]; i += 1
                    party = []
                    while i < limit and rom_data[i] not in (0x00, 0xFF):
                        party.append({'header': f'{sp_name(rom_data[i])} (Lv. {lv})'})
                        i += 1
                if party: trainers.append(party)
                if i < len(rom_data) and rom_data[i] == 0x00: i += 1

        # Shared formatting for both gens
        cls_list = text_tables.get('trainer_classes', [])
        if label: cls_name = label
        elif isinstance(class_id, int) and class_id < len(cls_list): cls_name = cls_list[class_id]
        else: cls_name = f'Class {class_id if class_id is not None else "?"}'
        out = []
        for t_idx, party in enumerate(trainers):
            out.append(f'{cls_name} — Trainer {t_idx + 1}' if len(trainers) > 1 else cls_name)
            out.append('\nTeam:')
            for p in party:
                h = p['header'] + (f'  [{p["item"]}]' if p.get('item') else '')
                out.append(h)
                if p.get('moves'): out.append(' / '.join(p['moves']))
            out.append('\nNo Items')
            if t_idx < len(trainers) - 1: out.append('')
        return '\n'.join(out)

    FLIPNOTE_PAIRS = {
        # Gen I (GB) — US
        'Pokémon Red & Blue': ['PMR', 'PMB'],
        'Pokémon Yellow': ['PMY'],
        # Gen I (GB) — JP
        'Pocket Monsters Red & Green': ['PKMRJ', 'PMG'],
        'Pocket Monsters Blue (JP)': ['PMBJP'],
        'Pocket Monsters Yellow (JP)': ['PMYJ'],
    }

    TABLE_FINGERPRINTS_JP = (
        ('species',    ((1, "フシギダネ"), (4, "ヒトカゲ"))),
        ('moves',      ((0, "はたく"), (4, "メガトンパンチ"))),
        ('items',      ((1, "マスターボール"),)),
        ('natures',    ((0, "がんばりや"), (1, "さみしがり"), (3, "いじっぱり"))),
        ('type_names', ((0, "ノーマル"),)),
    )

    LEARNSET_COUNT = 190  # internal species consts (Rhydon=1), not dex order

    def learnset_moves(self, data):
        """Raw learnset for reverse lookup: [(level, move_idx)]. u8 pairs, Gen I/II.
        Cartridge move ids are 1-based; shifted to index the 0-based moves table."""
        return [(data[i], data[i + 1] - 1) for i in range(0, len(data) - 1, 2)]

    def iter_learnsets(self):
        """Cartridge: learnsets sit in the combined evo+learnset pointer table, not files.
        Gen I keeps Lv1 moves in base stats (0x0F-0x12), so those are prepended."""
        ref = self._current_rom_ref()
        g, rom = ref['gen1_offsets'], ref['data']
        pb, dx = g.get('personal_base', 0), g.get('dex_table_base', 0)
        for c in range(1, self.LEARNSET_COUNT + 1):
            _, d = self._extract_gen12_evo_learnset(c, ref, {})
            if d is None: continue
            ls = self.learnset_moves(d)
            if g.get('personal_size') == 0x1C and pb and dx:
                dex = rom[dx + c]; p = pb + (dex - 1) * 0x1C
                if dex == 151 and rom[p] != dex: p = rom.find(bytes([151, 100, 100, 100, 100, 100]))  # R/B Mew row lives outside the table
                if dex and rom[p] == dex:  # R/B Mew lives outside the table: skip rather than misread
                    ls = [(1, m - 1) for m in rom[p + 0x0F:p + 0x13] if m] + ls
            yield c, ls

    # Clean attribute names for spec-based access
    DISCOVER_TABLES = _discover_gen1_tables
    EXTRACT_EVO_LEARNSET = _extract_gen12_evo_learnset
    RESOLVE_CONST = _gen1_resolve_const
    def bootstrap_text(self, rom_data, region='US'):
        """Scan raw ROM binary for text tables, run game-specific scanners, fingerprint."""
        charmap = self.CHARMAP_JP if region == 'JP' else self.CHARMAP_EN
        eos = self.EOS
        self.text_tables = {}

        candidates = self.scan_rom_text(rom_data, charmap, eos)
        for idx, table in enumerate(candidates):
            self.text_tables[idx] = table

        jp = region == 'JP'
        if jp:
            self._scan_gen1_species_varlen(rom_data, charmap, eos, self.text_tables)
            self._scan_gen1_moves_jp(rom_data, charmap, eos, self.text_tables)
            self._scan_gen1_trainer_classes_jp(rom_data, charmap, eos, self.text_tables)
            self._scan_gen1_items(rom_data, charmap, eos, self.text_tables)
        else:
            self._scan_gen1_species(rom_data, charmap, eos, self.text_tables)
            self._scan_gen1_trainer_classes_en(rom_data, charmap, eos, self.text_tables)
            self._scan_gen1_items(rom_data, charmap, eos, self.text_tables)
            self._scan_gen12_moves_en(rom_data, charmap, eos, self.text_tables, 165)

        self._auto_detect_tables()
        self._map_text_tables()

    SCAN_SPECIES = _scan_gen1_species
    SCAN_SPECIES_VARLEN = _scan_gen1_species_varlen
    SCAN_ITEMS = _scan_gen1_items
    SCAN_MOVES_JP = _scan_gen1_moves_jp
    SCAN_TRAINER_CLASSES_EN = _scan_gen1_trainer_classes_en
    SCAN_TRAINER_CLASSES_JP = _scan_gen1_trainer_classes_jp

