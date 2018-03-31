from random import choice


prompts = dict()
subjects = [lambda: "je/j'", lambda: 'tu', lambda: choice(('il', 'elle', 'on')),
            lambda: 'nous', lambda: 'vous', lambda: choice(('ils', 'elles'))]


def register(tense):
    def decorator(func):
        prompts[tense] = func
        return func
    return decorator


def get_prompt(verb, tense, person, number):
    if tense in prompts:
        prompt = prompts[tense](verb, person, number)
        return prompt[0].upper() + prompt[1:]
    else:
        prompt = get_default_prompt(verb, tense, person, number)
        return prompt[0].upper() + prompt[1:]


def get_default_prompt(verb, tense, person, number):
    subject = subjects[number*3+person - 4]()
    return subject+' __________ '+str((verb, tense))


sujonctifs = ["c'est "+x+' que ' for x in ('important', 'bon', 'intéressant',
                                           'impossible', 'juste', 'normal',
                                           'possible', 'rare', 'utile')]
sujonctifs += ['il '+x+' que ' for x in ('faut', 'semble', 'vaut mieux',
                                          'suffit', 'doute')]

sujonctifs += ['je ne pense pas que ', 'nous ne pensons pas que ',
               'je doute que ', 'nous doutons que ']


@register('sujonctif')
def _(verb, person, number):
    return choice(sujonctifs) + subjects[number*3+person - 4]() + \
           ' __________ ('+verb+')'


passés = ["L'été passé, ", "Hier, ", "L'année passé, ", "La dernière semaine, ",
          "Le printemps passé, ", "L'hiver passé, ",
          "Un jour il y a deux ans, "]


@register('passé_composé')
def _(verb, person, number):
    return choice(passés) + subjects[number*3+person - 4]() + \
           ' __________ ('+verb+')'


@register('imparfait')
def _(verb, person, number):
    return choice(['Habituellement, ', "D'habitude, ", "Normalement, "]) \
           + subjects[number*3+person - 4]() + ' __________ ('+verb+')'
