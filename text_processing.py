def clean_token(token, misc):
    """
    :param token:
    :param misc:
    :return:
    """
    out_token = token.strip().replace(' ', '')
    if token == 'Файл' and 'SpaceAfter=No' in misc:
        return None
    return out_token

def clean_lemma(lemma, pos, lowercase=True):
    """
    :param lemma:
    :param pos:
    :return:
    """
    out_lemma = lemma.strip().replace(' ', '').replace('_', '')
    if lowercase:
        out_lemma = out_lemma.lower()
    if '|' in out_lemma or out_lemma.endswith('.jpg') or out_lemma.endswith('.png'):
        return None
    if pos != 'PUNCT':
        if out_lemma.startswith('«') or out_lemma.startswith('»'):
            out_lemma = ''.join(out_lemma[1:])
        if out_lemma.endswith('«') or out_lemma.endswith('»'):
            out_lemma = ''.join(out_lemma[:-1])
        if out_lemma.endswith('!') or out_lemma.endswith('?') or out_lemma.endswith(',') \
                or out_lemma.endswith('.'):
            out_lemma = ''.join(out_lemma[:-1])
    return out_lemma
def num_replace(word):
    newtoken = 'x' * len(word)
    nw = newtoken + '_NUM'
    return nw
