THAWAI_HTOO = '\u1031'
VIRAMA = '\u1039'
MEDIAL_YA = '\u103b'
MEDIAL_RA = '\u103c'
MEDIAL_WA = '\u103d'
MEDIAL_HA = '\u103e'
NA = '\u1014'
RA = '\u101b'
SIGN_U = '\u102f'
SIGN_UU = '\u1030'

THAWAI_SET = {MEDIAL_YA, MEDIAL_RA, MEDIAL_WA, MEDIAL_HA}
MEDIAL_RA_BASES = {
    '\u1000', '\u1003', '\u100f', '\u1006', '\u1010', '\u1011',
    '\u1018', '\u101a', '\u101c', '\u101e', '\u101f', '\u1021',
}
U_SET = {SIGN_U, SIGN_UU}
KINZI = '\ue390'
KINZI_MAP = {
    '\u102e': '\ue392',
    '\u102d': '\ue391',
    '\u1032': '\ue396',
    '\u1036': '\ue393',
}
SUB_MAP = {
    '\u1000': '\ue000', '\u1001': '\ue001', '\u1002': '\ue002',
    '\u1003': '\ue003', '\u1005': '\ue005', '\u1006': '\ue006',
    '\u1007': '\ue007', '\u1008': '\ue008', '\u100a': '\ue00a',
    '\u100b': '\ue00b', '\u100c': '\ue00c', '\u100e': '\ue00e',
    '\u100f': '\ue00f', '\u1010': '\ue010', '\u1011': '\ue011',
    '\u1012': '\ue012', '\u1013': '\ue013', '\u1014': '\ue014',
    '\u1015': '\ue015', '\u1016': '\ue016', '\u1017': '\ue017',
    '\u1018': '\ue018', '\u1019': '\ue019', '\u101c': '\ue01c',
    '\u101e': '\ue01e', '\u101f': '\ue553', '\u1021': '\ue021',
}
TONE_I = {'\u102d', '\u102e', '\u1032'}
MYANMAR_CONSONANTS = {chr(cp) for cp in range(0x1000, 0x1022)}
COMBINED_YA = '\ue1b2'
SPECIAL_THAWAI = '\u001d' + THAWAI_HTOO


def reshape_myanmar_word(mm_word):
    mm_letters = list(mm_word)
    length = len(mm_letters)

    def has(i, chars):
        return 0 <= i < length and mm_letters[i] in chars

    # Special: န္ဒြ
    pattern = [NA, VIRAMA, '\u1012', MEDIAL_RA]
    for i in range(length - 3):
        if mm_letters[i:i + 4] == pattern:
            mm_letters[i:i + 4] = ['\u200c', MEDIAL_RA, '\ue107', '\ue012']

    # Step 1: reorder ThaWaiHtoo
    for i in range(length):
        if mm_letters[i] != THAWAI_HTOO:
            continue

        if mm_letters[i - 3:i] == [MEDIAL_RA, '\ue107', '\ue012'] and i >= 3:
            mm_letters[i - 3:i + 1] = [THAWAI_HTOO, MEDIAL_RA, '\ue107', '\ue012']
            continue

        for offset in range(1, 4):
            if not has(i - offset, THAWAI_SET):
                break
            mm_letters[i - offset], mm_letters[i - offset + 1] = (
                mm_letters[i - offset + 1],
                mm_letters[i - offset],
            )

    # Reorder YaYit
    for i in range(length):
        if mm_letters[i] != MEDIAL_RA:
            continue

        if i > 1 and mm_letters[i - 1] == THAWAI_HTOO:
            mm_letters[i - 2:i + 1] = [SPECIAL_THAWAI, mm_letters[i], mm_letters[i - 2]]
        elif i > 0:
            mm_letters[i - 1], mm_letters[i] = mm_letters[i], mm_letters[i - 1]

    # Step 2: YaYit substitution
    for i in range(length):
        if mm_letters[i] == MEDIAL_RA and has(i + 1, MEDIAL_RA_BASES):
            mm_letters[i] = COMBINED_YA

    # One-to-one substitutions
    for i in range(length):
        v = mm_letters[i]

        if v == NA:
            if has(i + 1, {SIGN_U, SIGN_UU, MEDIAL_WA, MEDIAL_HA}) or has(i + 2, U_SET):
                mm_letters[i] = '\ue107'

            if has(i + 1, {THAWAI_HTOO}) and has(
                i + 2, {SIGN_U, SIGN_UU, MEDIAL_WA, MEDIAL_HA}
            ):
                mm_letters[i:i + 3] = [SPECIAL_THAWAI, '\ue107', mm_letters[i + 2]]

        elif v == RA:
            if any(has(i + d, U_SET) for d in (1, 2, 3)):
                mm_letters[i] = '\ue108'

        elif v in {SIGN_U, SIGN_UU}:
            if (
                has(i - 1, {MEDIAL_YA})
                or has(i - 2, {MEDIAL_YA})
                or has(i - 2, {MEDIAL_RA, COMBINED_YA})
                or has(i - 3, {MEDIAL_RA, COMBINED_YA})
            ):
                mm_letters[i] = '\ue2f1' if v == SIGN_U else '\ue2f2'

        elif v == '\u1037':
            if has(i - 1, U_SET) or has(i - 1, {NA}) or has(i - 2, {NA}):
                mm_letters[i] = '\ue037'

            if (
                has(i - 1, {'\ue2f1', '\ue2f2', MEDIAL_WA})
                or has(i - 1, {MEDIAL_YA})
                or has(i - 2, {MEDIAL_YA})
            ):
                mm_letters[i] = '\ue137'

            if has(i - 1, {MEDIAL_HA}) or has(i - 2, {MEDIAL_HA}):
                mm_letters[i] = '\ue137' if has(i - 3, {RA}) else '\ue037'

        elif v == MEDIAL_HA and has(i - 2, {MEDIAL_RA, COMBINED_YA}):
            mm_letters[i] = '\ue1f3'

    # Two-to-one substitutions
    pair_map = {
        '\u102d': {'\u1036': '\ue2d1', '\u1032': '\ue12d'},
        '\u102b': {'\u103a': '\ue02d', '\u1032': '\ue52c', '\u1036': '\ue52b'},
        MEDIAL_YA: {MEDIAL_WA: '\ue1a4', MEDIAL_HA: '\ue1a3'},
        MEDIAL_WA: {MEDIAL_HA: '\ue1d1'},
    }

    for i in range(length):
        v = mm_letters[i]

        if v in pair_map and has(i + 1, pair_map[v]):
            mm_letters[i], mm_letters[i + 1] = pair_map[v][mm_letters[i + 1]], ''

            if v == MEDIAL_YA and mm_letters[i] == '\ue1a4' and has(i + 2, {MEDIAL_HA}):
                mm_letters[i:i + 3] = ['\ue1d1', MEDIAL_YA, '']

        elif v in {SIGN_U, SIGN_UU}:
            replacement = '\ue1f2' if v == SIGN_U else '\ue430'
            if has(i - 1, {MEDIAL_HA}):
                mm_letters[i - 1], mm_letters[i] = replacement, ''
            elif has(i - 2, {MEDIAL_HA}):
                mm_letters[i - 2], mm_letters[i] = replacement, ''

    # Virama / subjoined consonants
    for i in range(length):
        if mm_letters[i] != VIRAMA:
            continue

        if has(i - 1, {'\u103a'}) and has(i - 2, {'\u1004'}):
            mm_letters[i - 2:i + 1] = ['', '', KINZI]

            if has(i + 1, {MEDIAL_RA}):
                mm_letters[i:i + 3] = ['\ue1b6', mm_letters[i + 2], mm_letters[i]]
            elif has(i + 1, {COMBINED_YA}):
                mm_letters[i:i + 3] = ['\ue1b7', mm_letters[i + 2], mm_letters[i]]
            elif i + 1 < length:
                mm_letters[i], mm_letters[i + 1] = (mm_letters[i + 1], mm_letters[i])
            continue

        if has(i + 1, SUB_MAP):
            mm_letters[i], mm_letters[i + 1] = SUB_MAP[mm_letters[i + 1]], ''

        if has(i - 1, {'\u100f'}) and has(i + 1, {'\u100d'}):
            mm_letters[i - 1:i + 2] = ['\ue105', '', '']
        elif has(i + 1, {'\u100d'}):
            mm_letters[i:i + 2] = ['\ue00d', '']

        if i + 2 < length:
            if mm_letters[i + 2] == SIGN_U:
                mm_letters[i + 2] = '\ue2f1'
            elif mm_letters[i + 2] == SIGN_UU:
                mm_letters[i + 2] = '\ue2f2'

        if has(i - 1, {NA}):
            mm_letters[i - 1] = '\ue107'

    # KinZi variants + KinZi/ThaWaiHtoo reorder
    for i in range(length - 1):
        if mm_letters[i] != KINZI:
            continue

        if has(i + 1, {MEDIAL_YA}) and has(i + 2, KINZI_MAP):
            mm_letters[i:i + 3] = [KINZI_MAP[mm_letters[i + 2]], MEDIAL_YA, '']
        elif has(i + 1, KINZI_MAP):
            mm_letters[i], mm_letters[i + 1] = (KINZI_MAP[mm_letters[i + 1]], '')

        if (
            mm_letters[i] == KINZI
            and mm_letters[i + 1] in {THAWAI_HTOO, SPECIAL_THAWAI}
            and has(i + 2, {'\u102b', '\u102c', '\ue02d'})
        ):
            mm_letters[i], mm_letters[i + 1] = (mm_letters[i + 1], mm_letters[i])

    # YaYit variants
    for i in range(length):
        if mm_letters[i] not in {MEDIAL_RA, COMBINED_YA}:
            continue

        glyph = '\ue1b6' if mm_letters[i] == MEDIAL_RA else '\ue1b7'

        if has(i + 2, TONE_I):
            mm_letters[i] = glyph
        elif has(i + 2, {MEDIAL_WA}):
            mm_letters[i] = '\ue1bb' if mm_letters[i] == MEDIAL_RA else '\ue1bc'
            if has(i + 3, TONE_I):
                mm_letters[i] = glyph

    # Remove placeholders only after all index-based transformations.
    mm_letters = [c for c in mm_letters if c]

    # Insert Zero Width Non-Joiner between consonant and special ThaWaiHtoo.
    i = 0
    while i < len(mm_letters) - 1:
        if mm_letters[i] in MYANMAR_CONSONANTS and mm_letters[i + 1] == SPECIAL_THAWAI:
            mm_letters.insert(i + 1, '\u200c')
            i += 1
        i += 1

    return ''.join(mm_letters)
