import random

def getword():
    index = random.randint(1,500)
    wordfile = open('hangman\\words.txt','r')
    words = [w.strip('\n') for w in wordfile.readlines()]
    return words[index]


def main(word=getword()):
    #letters to censor

    letters = list(dict.fromkeys(list(word)))
    letters_used = []
    censor = random.sample(letters,int(len(letters)/2))
    lives = len(censor) * 2

    def concat(letter):
        return f"Words Used - |{'| |'.join(letter).upper()}|"

    def display(words,c):
        replaced = [w if not w in c else '_' for w in word]
        replaced = f"|{'| |'.join(replaced).upper()}|"
        return replaced
    
    print(f'Initializing Hangman Game. You have {lives} lives.\n')

    #loop input
    while True:
        censored_word = display(word,censor)
        answer = input(f'{censored_word}\n> ')
        while True:
            if len(answer) > 1:
                print('Invalid input, try again.')
                answer = input(f'{censored_word}\n> ')
            else:
                break
        if answer in censor:
            censor.remove(answer)
            remaining = display(word,censor).count("_")
            print(f'Good guess! [{remaining}] letters left.')
        else:
            lives = lives - 1
            print(f'Wrong! Try again.')

        if not censor:
            print(display(word,censor))
            print(f'The word is {word}. You win!')
            break
        elif not lives:
            print(f'The word is {word}. You lose!')
            break

        letters_used.append(answer)
        print(f'You have {lives} lives left.')
        print(concat(letters_used))
        print()
main()