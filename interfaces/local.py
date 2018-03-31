#!/usr/bin/python3

import random
from verbs import verbs, tenses, conjugate_verb
from prompt import get_prompt


class LocalClient:
    def run():
        while True:
            next_verb = random.choice(verbs)
            tense = random.choice(tenses)
            person = random.randrange(1, 4)
            number = random.randrange(1, 3)
            prompt = get_prompt(next_verb.infinitif, tense, person, number)
            print(prompt)
            guess = input()
            correct = conjugate_verb(next_verb, tense, person, number,
                                     gender=prompt.lower().count('elle '))
            if guess == correct:
                print('Correct')
            else:
                print('Incorrect, the correct answer is', correct)

client = LocalClient()
