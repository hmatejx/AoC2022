with open('input.txt') as file:
    for line in [line.rstrip() for line in file]: 
        for i in range(0, len(line) - 4):
            if len(set(line[i:(i+4)])) == 4:
                print('Found start-of-packet marker @ {}'.format(i + 4))
                break
        for i in range(0, len(line) - 14):
            if len(set(line[i:(i+14)])) == 14:
                print('Found start-of-message marker @ {}'.format(i + 14))
                break
