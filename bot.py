#!/usr/bin/python3

from sys import argv

if len(argv) == 2:
    if argv[1] == '--help':
        print('Runs the bot, to the specified interface. There must be a specified interface.')
        print('The currently supported interfaces are: local')
    elif argv[1] == 'local':
        import interfaces.local
        interfaces.local.client.run()
    elif argv[1] == 'discord':
        import interfaces.discord
        interfaces.discord.client.run()
    else:
        print('Unrecognized option: %s' % argv[1])
        print('Recognized options: local, --help')
else:
    print('Expected format: 1 argument, containing the channel to run it in.')
