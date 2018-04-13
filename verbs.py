from collections import namedtuple
from utils import group_iterable


Verb = namedtuple('Verb', ['infinitif', 'type'])
VerbType = namedtuple("VerbType", ['ending', 'présent', 'passé_composé',
                                   'imparfait', 'passé_simple', 'futur_simple',
                                   'conditionnel', 'sujonctif'])

tenses = ['présent', 'passé_composé', 'imparfait', 'passé_simple',
          'futur_simple', 'conditionnel', 'sujonctif', 'passé_sujonctif',
          'passé_conditionnel', 'futur_antérieur']

verb_types = []
verbs = []


def get_verb_type(verb):
    match_len = 0
    verb_type = None
    for possbile_verb_type in verb_types:
        if possbile_verb_type.ending == verb[-len(possbile_verb_type.ending):] \
                and len(possbile_verb_type.ending) > match_len:
            verb_type = possbile_verb_type
            match_len = len(possbile_verb_type.ending)
    return verb_type


def conjugate_verb(verb, tense, person, number, verb_type=None, gender=0):
    if type(verb) is Verb:
        verb_type = verb.type
        verb = verb.infinitif
    elif verb_type is None:
        verb_type = get_verb_type(verb)
    elif verb_type not in verb_types:
        raise ValueError('Unrecognized verb type: ', verb_type)
    if verb_type is None:
        raise ValueError('Verb of no known type: '+verb)
    stem = verb[:-len(verb_type.ending)]
    if tense in ('passé_composé', 'passé_sujonctif',
                 'passé_conditionnel', 'futur_antérieur'):
        if tense == 'passé_composé':
            if verb in etre_passé_verbs:
                aux = conjugate_verb('être', 'présent', person, number)
            else:
                aux = conjugate_verb('avoir', 'présent', person, number)
            conjugated = aux + ' ' + stem + verb_type.passé_composé[0]
            if verb in etre_passé_verbs:
                if gender:
                    conjugated += 'e'
                if number > 1:
                    conjugated += 's'
            return conjugated
        elif tense == 'futur_antérieur':
            if verb in etre_passé_verbs:
                return conjugate_verb('être', 'futur_simple', person, number) \
                      + ' ' + stem + verb_type.passé_composé[0]
            else:
                return conjugate_verb('avoir', 'futur_simple', person, number) \
                      + ' ' + stem + verb_type.passé_composé[0]
        if verb in etre_passé_verbs:
            return conjugate_verb('être', tense[6:], person, number) \
                  + ' ' + stem + verb_type.passé_composé[0]
        else:
            return conjugate_verb('avoir', tense[6:], person, number) \
                  + ' ' + stem + verb_type.passé_composé[0]
    ending = getattr(verb_type, tense)[person + 3*min(2, number) - 4]
    if ending.count('.'):
        ending = ending.replace('.', verb[-len(verb_type.ending)])
    return stem + ending


etre_passé_verbs = ['devenir', 'revenir', 'montrer', 'rentrer', 'sortir',
                    'venir', 'aller', 'naître', 'descendre', 'entrer', 'rester',
                    'tomber', 'retourner', 'arriver', 'mourir', 'partir']

with open('verbs.txt', encoding='utf-8') as f:
    for verb_file in group_iterable(5, f):
        v = verb_file.strip().split('\n')
        next_type = VerbType(*[v[1]]+list(x.split(',')
                                          for x in v[2].split(';')))
        verb_types.append(next_type)
        verbs += (Verb(verb, next_type) for verb in v[3].split(','))

if __name__ == '__main__':
    print(*verb_types, sep='\n')
    print([verb.infinitif for verb in verbs])
