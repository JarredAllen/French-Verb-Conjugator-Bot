import discord
import secrets
import random
from verbs import verbs, tenses, conjugate_verb
from prompt import get_prompt

discord_client = discord.Client()

@discord_client.event
async def on_message(message):
    if starts_with(message.content, 'fvb!play'):
        next_verb = random.choice(verbs)
        tense = random.choice(tenses)
        person = random.randrange(1,4)
        number = random.randrange(1,3)
        prompt = get_prompt(next_verb.infinitif, tense, person, number)
        await client.send_message(message.channel, prompt)
        correct = conjugate_verb(next_verb, tense, person, number, gender=prompt.lower().count('elle'))
        response = await client.wait_for_message(channel=message.channel, author=message.author)
        if correct == response.content.strip():
            await client.send_message(message.channel, 'Correct, %s!' % (message.author.name))
        else:
            await client.send_message(message.channel, 'Sorry, %s, but that isn\'t right.\n'
                                      'The answer is %s.' % (message.author.name, correct))

class Client:
    def __init__(self, api_key=secrets.discord_key):
        self.api_key = secrets.discord_key

    def run(self):
        discord_client().run(self.api_key)

client = Client()

def starts_with(str_a, str_b):
    return len(str_a) >= len(str_b) and str_a[:len(str_b)] == str_b
