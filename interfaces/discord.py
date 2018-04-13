import discord
import secrets
import random
from verbs import verbs, tenses, conjugate_verb
from prompt import get_prompt

discord_client = discord.Client()

@discord_client.event
async def on_message(message):
    print('Received message:', str(message))
    if starts_with(message.content, 'fvb!play'):
        play = True
        loop = False
        death = False
        rounds = 0
        wins = 0
        limit = 0

        cmd = message.content.split(' ')[1:]
        if not cmd:
            play = False
            print('Single game')
        elif cmd[0] == 'death':
            death = True
            print('Sudden death game')
        elif is_int_str(cmd[0]):
            limit = int(cmd[0])
            print('%d-round game' % limit)
        else:
            play = False
            discord_client.send_message(message.channel, 'Unrecognized play args: [%s]' % ' '.join(cmd))

        while play or not rounds:
            next_verb = random.choice(verbs)
            tense = random.choice(tenses)
            person = random.randrange(1,4)
            number = random.randrange(1,3)
            prompt = get_prompt(next_verb.infinitif, tense, person, number)
            await discord_client.send_message(message.channel, prompt)
            correct = conjugate_verb(next_verb, tense, person, number, gender=prompt.lower().count('elle'))
            response = await discord_client.wait_for_message(channel=message.channel, author=message.author)
            rounds += 1
            if correct == response.content.strip():
                wins += 1
                await discord_client.send_message(message.channel, 'Correct, %s!' % (message.author.name))
            else:
                await discord_client.send_message(message.channel, 'Sorry, %s, but that isn\'t right.\n'
                                                  'The answer is %s.' % (message.author.name, correct))
                if death:
                    await discord_client.send_message(message.channel, 'Your final streak is %d!' % wins)
                    break
            if limit:
                print('%d rounds left' % (limit - rounds))
                if limit == rounds:
                    await discord_client.send_message(message.channel, 'That\'s all for your game. You won %d/%d (%.1f%%)!' %
                                                      (wins, rounds, 100 * wins/rounds))
                    break
        print('Game finished')

class Client:
    def __init__(self, api_key=secrets.discord_key):
        self.api_key = secrets.discord_key

    def run(self):
        print('Connecting...')
        discord_client.run(self.api_key)
        print('Done!')

client = Client()

def starts_with(str_a, str_b):
    return len(str_a) >= len(str_b) and str_a[:len(str_b)] == str_b

def is_int_str(string):
    try:
        int(string)
        return True
    except:
        return False

