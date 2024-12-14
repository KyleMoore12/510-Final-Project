class STSfloor1:
    def __init__(self):
        self.deck = {'s': 5, 'd': 4, 'b': 1}  # Represents each card in the starting deck
        self.stack = []  # Stack to track played cards also used for transitioning between turns
        self.damage = 0  # Total damage dealt
        self.turn = 1 #tracks what turn the player is on
        self.energy = 0 #tracks how much energy the player has used 

    def play_card(self, card):
        if self.deck[card] <= 0:
            print(f"Invalid move: {card} not available in deck.")
            return False

        # Update damage and energy counter after player plays a card
        if card == 's':  # Strike deals 6 damage
            self.damage += 6
            self.energy += 1
        elif card == 'b':  # Bash deals 12 damage also costs 2 energy
            self.energy += 2
            self.damage += 12
            if self.energy > 3:
                print(f"Invalid move: not enough energy to play {card}")
        else:
            self.energy += 1 # defends also cost 1 energy
            
        self.stack.append(card) # Push the card to the stack so that the PDA knows what to shuffle back into the starting deck 
        self.deck[card] -= 1  # Decrease card availability in the deck
        print(f"Played {card}. Current damage: {self.damage}.")

        #check if the play transitions to the next turn
        self.__end_turn()
        return True

    def __end_turn(self):
        if self.turn == 2 and self.energy == 3:  # Reshuffle played cards into the deck at the end of Turn 2
            while self.stack:
                card = self.stack.pop()
                self.deck[card] += 1
            print("Reshuffled played cards back into the deck.")
        if self.turn == 4 and self.energy == 3:
            self.__end_game()
        
        elif self.energy == 3:
            self.turn += 1 
            self.energy = 0 # Reset the energy spent preparing for the new turn
            print(f"\nMoving on to turn {self.turn}")
        else:
            print("waiting on next card")
            
    def __check_win_condition(self):
        if self.damage >= 48:
            print("Win condition met: Damage is greater than or equal to 48!")
            return True
        else:
            print("Win condition not met: Insufficient damage.")
            return False

    def __end_game(self):
        print(f"Game Over. Total damage: {self.damage}")
        win_damage = self.__check_win_condition()
        if win_damage:
            print("Victory! You defeated the Cultist.")
        else:
            print("Defeat. Better luck next time.")


'''
This funciton tests whether the given string results in a win in the STSfloor 1 class
each character in the string represent the card that the player play on that turn
returns either accept and then the state path if the string results in a win else it returns reject
'''
def accept(PDA, string):
    state_path = []  # Track the sequence of states by turn number and damage dealt
    
    for card in string:
        # Record the current state before playing the card
        #Transitioning from trun 1 to turn 2 is recorded as turn 2 and same for any transition between turns
        #This is why it looks like more than 4 cards were played on some turns or 3 cards were played on a turn where bash was played.
        state_path.append((PDA.turn, PDA.damage))
        
        # Attempt to play the card
        if not PDA.play_card(card):
            print(f"Rejected: Unable to play {card} due to invalid move.")
            return 'reject', []  # Invalid card play
        
        # Check for a win condition after each play
        if PDA.damage >= 48:
            state_path.append((PDA.turn, PDA.damage))
            return 'accept', state_path
    
    # If all cards are played but no win condition is met, return reject
    return 'reject', []


#Testing game1
game1 = STSfloor1()
string1 = "sdddbssdsddd" 
print("Game 1")
result1 = accept(game1, string1)
print(result1)

#Testing game2
game2 = STSfloor1()
string2 = "ssddddbsbd"
print("Game 2")
result2 = accept(game2, string2)
print(result2)

#Testing game3
game3 = STSfloor1()
string3 = "bddssddsbs"
print("Game 3")
result3 = accept(game3, string3)
print(result3)