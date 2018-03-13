def _edit_dist_init(len1, len2):
    lev = []
    for i in range(len1):
        lev.append([0] * len2)  # initialize 2D array to zero
    for i in range(len1):
        lev[i][0] = i           # column 0: 0,1,2,3,4,...
    for j in range(len2):
        lev[0][j] = j           # row 0: 0,1,2,3,4,...
    return lev


def c1_close_to_c2(c1, c2):
    closest = {
    'й': set('цфы'),
    'ц': set('йфыву'),
    'у': set('цывако'),
    'к': set('увапе'),
    'е': set('капрнэи'),
    'н': set('епрог'),
    'г': set('нролш'),
    'ш': set('голдщ'),
    'щ': set('шлджз'),
    'з': set('щджэх'),
    'х': set('зжэъ'),
    'ъ': set('хэ'),
    'ф': set('йцычя]'),
    'ы': set('йцувсчяф'),
    'в': set('цукамсчы'),
    'а': set('укепимсво'),
    'п': set('акенртим'),
    'р': set('енгоьтип'),
    'о': set('нгшлбьтра'),
    'л': set('гшщдюбьо'),
    'д': set('шщзж.юбл'),
    'ж': set('щзхэ.юд'),
    'э': set('зхъже'),
    ']': set('фя'),
    'я': set('фыч'),
    'ч': set('яфывс'),
    'с': set('чывам'),
    'м': set('свапи'),
    'и': set('мапрте'),
    'т': set('ипроь'),
    'ь': set('тролб'),
    'б': set('ьолдю'),
    'ю': set('блдж'),
    '.': set('юджэ')
    }
    return c2 in closest[c1]


def _edit_type_init(len1, len2):
    lev = []
    for i in range(len1):
        lev.append([[]] * len2)  # initialize 2D array to empty arrays
    for i in range(len1):
        lev[i][0] = ['insert']*i           # column 0: 0,1,2,3,4,...
    for j in range(len2):
        lev[0][j] = ['skip']*j          # row 0: 0,1,2,3,4,...
    return lev


def _edit_dist_step(lev, lev_type, i, j, s1, s2, substitution_cost=1, transpositions=True):
    c1 = s1[i - 1]
    c2 = s2[j - 1]

    # skipping a character in s1
    a = lev[i - 1][j] + 1
    # skipping a character in s2
    b = lev[i][j - 1] + 1
    # substitution
    c = lev[i - 1][j - 1] + (0.5 if c1_close_to_c2(c1, c2) else substitution_cost if c1 != c2  else 0)

    # transposition
    d = c + 1  # never picked by default
    if transpositions and i > 1 and j > 1:
        if s1[i - 2] == c2 and s2[j - 2] == c1:
            d = lev[i - 2][j - 2] + 1


    # pick the cheapest
    lev[i][j] = min(a, b, c, d)
    # get its type
    if lev[i][j] == a:
        lev_type[i][j] = lev_type[i - 1][j] + ['insert:{}'.format(c1)]
    elif lev[i][j] == b:
        lev_type[i][j] = lev_type[i][j - 1] + ['skip:{}'.format(c2)]
    elif lev[i][j] == c:
        if c == lev[i - 1][j - 1]:
            lev_type[i][j] = lev_type[i - 1][j - 1]
        else:
            lev_type[i][j] = lev_type[i - 1][j - 1] + ['subst:{}'.format(c2)]
    elif lev[i][j] == d:
        lev_type[i][j] = lev_type[i - 2][j - 2] + ['tr:{}{}'.format(c1, c2)]


def edit_distance(s1, s2, substitution_cost=1.5, transpositions=True):
    """
    Calculate the Levenshtein edit-distance between two strings.
    The edit distance is the number of characters that need to be
    substituted, inserted, or deleted, to transform s1 into s2.  For
    example, transforming "rain" to "shine" requires three steps,
    consisting of two substitutions and one insertion:
    "rain" -> "sain" -> "shin" -> "shine".  These operations could have
    been done in other orders, but at least three steps are needed.

    Allows specifying the cost of substitution edits (e.g., "a" -> "b"),
    because sometimes it makes sense to assign greater penalties to substitutions.

    This also optionally allows transposition edits (e.g., "ab" -> "ba"),
    though this is disabled by default.

    First word is the variant, second one is the correct, existing word

    :param s1, s2: The strings to be analysed
    :param transpositions: Whether to allow transposition edits
    :type s1: str
    :type s2: str
    :type substitution_cost: int
    :type transpositions: bool
    :rtype int
    """
    # set up 2-D arrays for distance and types
    len1 = len(s1)
    len2 = len(s2)
    lev = _edit_dist_init(len1 + 1, len2 + 1)
    lev_type = _edit_type_init(len1 + 1, len2 + 1)

    # iterate over the array
    for i in range(len1):
        for j in range(len2):
            _edit_dist_step(lev, lev_type, i + 1, j + 1, s1, s2,
                            substitution_cost=substitution_cost, transpositions=transpositions)
    return lev[len1][len2], lev_type[len1][len2]
