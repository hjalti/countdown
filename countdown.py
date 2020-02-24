import letters, numbers

def main():
    print('COUNTDOWN!')
    grouped = letters.init()
    while True:
        try:
            inp = input('Letters or numbers? [L/N]: ')
            if inp.upper() == 'L':
                letters.interact(grouped)
            elif inp.upper() == 'N':
                numbers.interact()
        except (EOFError, KeyboardInterrupt):
            print('\nBye')
            return

if __name__ == '__main__':
    main()
