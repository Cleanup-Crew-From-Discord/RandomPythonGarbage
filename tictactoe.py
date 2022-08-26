#import some BS because apparently code needs stuff to run and can't just interpret my will alone
from curses.ascii import isdigit
import os
#create the board from string of values
def update(values):
    print("\n")
    print("\t {} | {} | {}".format(values[0], values[1], values[2]))
    print('\t---|---|---')
    print("\t {} | {} | {}".format(values[3], values[4], values[5]))
    print('\t---|---|---')
    print("\t {} | {} | {}".format(values[6], values[7], values[8]))
    print("\n")
#Clean player input and edit values. Send back an exit code if the player chooses to exit
def user_choice(values,playerCurrent,stupidity):
    px='placeholder'
    while True:
        px=(input("Player {name}, Select square 1-9 or type {exit} to exit game: ".format(name=str(stupidity[playerCurrent]),exit='"exit"')))
        if px=='exit':
            values[0]=3
            return values,playerCurrent
        elif px.isdigit() == False or int(px) > 9 or int(px) < 1:
            pass
        else:
            if values[int(px)-1] != ' ':
                print('Space already occupied, try again.')
                px='redo'
            else:
                values[int(px)-1]=stupidity[playerCurrent]
                playerCurrent=not playerCurrent
                return values,playerCurrent
                break
#Check for a win. If the board is full with no win, return a draw
def wincheck(values,p,stupidity):
    z=['']
    a=stupidity[not p]
    z[0]=stupidity[not p]
    #I specifically hate these 3 lines. I have to go through so much stupidity to output 'z' instead of z because the quotes stay attached in a list.
    #Whatever, saves lines on checking for X and O
    vset=set(values)
    if values[0]==values[3]==values[6]==z[0] or values[1]==values[4]==values[7]==z[0] or values[2]==values[5]==values[8]==z[0]:
        print('3 Down! Player {name} wins!'.format(name=a))
        return True,z[0]
    elif values[0]==values[1]==values[2]==z[0] or values[3]==values[4]==values[5]==z[0] or values[6]==values[7]==values[8]==z[0]:
        print('3 Across! Player {name} wins!'.format(name=a))
        return True,z[0]
    elif values[0]==values[4]==values[8]==z[0] or values[2]==values[4]==values[6]==z[0]:
        print('3 Diagonal! Player {name} wins!'.format(name=a))
        return True,z[0]
    elif vset=={'X','O'}:
        print('Draw!')
        return True,3
    else:
        return False,z[0]
#Non function area
print('\nWelcome to Tic Tac Toe! Now only 30% janky!\n')
update('123456789')
values=[' ',' ',' ',' ',' ',' ',' ',' ',' ']
playerCurrent=bool(0)
stupidity=['X','O']
xwins=owins=nowins=0
while True:
    z=['X']
    values,playerCurrent=user_choice(values,playerCurrent,stupidity)
    if values[0]==3:
        break
    os.system('cls' if os.name == 'nt' else 'clear')
    update(values)
    winner,z=wincheck(values,playerCurrent,stupidity)
    if winner == True:
        redo=input('Input "n" to exit, or click enter to play again: ')
        if redo!='n':
            if z=='X':
                xwins=xwins+1
            elif z=='O':
                owins=owins+1
            elif z==3:
                nowins=nowins+1
            os.system('cls' if os.name == 'nt' else 'clear')
            print('\nRound {round}! FIGHT!!'.format(round=xwins+owins+nowins+1))
            print('X:{xw}  O:{ow}'.format(xw=xwins,ow=owins))
            update('123456789')
            values=[' ',' ',' ',' ',' ',' ',' ',' ',' ']
            playerCurrent=bool(0)
            pass
        else:
            break