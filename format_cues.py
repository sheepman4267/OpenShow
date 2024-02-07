# A python script to test logic (and hopefully be useful) for auto-formatting text into cues for decks.

with open('cues.txt', 'r') as cuefile:
    cuelines = cuefile.readlines()

for line in cuelines:
    cuewords = line.split(' ')
    if len(cuewords) > 12:
        print(f'{cuewords[0]} {cuewords[1]} {cuewords[2]} (...) {cuewords[-3]} {cuewords[-2]} {cuewords[-1]}'.strip('\n'))
    else:
        print(line.strip('\n'))
    print('~~')