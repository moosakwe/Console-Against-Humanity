import random
import json

# Load JSON with card objects (format follows JSON Against Humanity)
with open("scigeek-cah-cards-full.json", "r", encoding="utf-8") as CAH:
    packs = json.load(CAH)
# Separate cards across all chosen CAH packs in JSON file by type
black_pack = [pack['black'] for pack in packs]
white_pack = [pack['white'] for pack in packs]
# Flatten nested list of cards across packs in single combined list by type
blist = sum(black_pack, [])
wlist = sum(white_pack, [])
# Extract only the card text from each card dictionary
white_cards = [card['text'] for card in wlist]
black_cards = [card['text'] for card in blist]
# Flag for restarting game after a single go
quit_game = False

while True:
    # Start every round by shuffling black and white cards, then serve a hand of 10
    random.shuffle(black_cards)
    random.shuffle(white_cards)
    hand = white_cards[:10]
    del white_cards[:10]
    # Set max number of turns a player using total number of black cards or 1/2 of white (whichever is bigger)
    max_turns = min(len(white_cards) // 2, len(black_cards))

    while True:
        turns = input("How many rounds do you want to play?")
        try:
            turns = int(turns)
        except ValueError:
            print("Please enter a number")
            continue

        if 1 <= turns <= max_turns:
            break

        else:
            print(f"Please pick a number above 0 and under {max_turns + 1}")
# loop for setting total number of turns per game
    for turn in range(turns):
        prompt = black_cards.pop()
        blank = prompt.count("_")
        question = prompt.count("?")
        print(prompt + "\n")
# create an index of all cards in player's hand and print it
        indexed_hand = {i: card for i, card in enumerate(hand, start=1)}
        for key, value in indexed_hand.items():
            print(f"{key}: {value}")
# Conditions for displaying selected white card(s)
        if blank == 1 or question == 1:
            while True:
                player_choice = input("Choose your card!")
                try:
                    player_choice = int(player_choice)
                except ValueError:
                    print("You must enter a number between 1 and 10!")
                    continue

                if 1 <= player_choice <= 10:
                    break
                else:
                    print("You must enter a number between 1 and 10!")

        elif blank == 2:
            while True:
                player_choice, player_choice2 = input("Choose your first card!"), input("Choose a second card!")
                try:
                    player_choice = int(player_choice)
                    player_choice2 = int(player_choice2)
                except ValueError:
                    print("You must enter numbers between 1 and 10!")
                    continue

                if player_choice == player_choice2:
                    print("You cannot use the same card twice!")
                    continue

                if 1 <= player_choice <= 10 and 1 <= player_choice2 <= 10:
                    break
                else:
                    print("You must enter numbers between 1 and 10!")
# conditions for displaying user's input every turn
        if question == 1:
            print(f"{prompt} {indexed_hand[player_choice]}" + "\n")
            hand.pop(player_choice - 1)
            hand.append(white_cards.pop())
            indexed_hand = {i: card for i, card in enumerate(hand, start=1)}

        elif blank == 1:
            blank_index_finder = prompt.find("_")
            if prompt[blank_index_finder - 2].islower():
                printed_white_card = indexed_hand[player_choice]
                printed_white_card = printed_white_card[0].lower() + printed_white_card[1:]
                print(prompt.replace("_", printed_white_card.strip(".")) + "\n")
            else:
                print(prompt.replace("_", indexed_hand[player_choice].strip(".")) + "\n")
            hand.pop(player_choice - 1)
            hand.append(white_cards.pop())
            indexed_hand = {i: card for i, card in enumerate(hand, start=1)}

        elif blank == 2:
            blank_index_finder = prompt.find("_", 0)
            blank_index_finder2 = prompt.find("_", blank_index_finder + 1)
            if prompt[blank_index_finder - 2].islower() and prompt[blank_index_finder2 - 2].islower():
                printed_white_card = indexed_hand[player_choice]
                printed_white_card = printed_white_card[0].lower() + printed_white_card[1:]
                printed_white_card2 = indexed_hand[player_choice2]
                printed_white_card2 = printed_white_card2[0].lower() + printed_white_card2[1:]
                prompt = prompt.replace("_", printed_white_card.strip("."), 1)
                prompt = prompt.replace("_", printed_white_card2.strip("."), 1)
                print(prompt + "\n")
            elif not prompt[blank_index_finder - 2].islower():
                printed_white_card2 = indexed_hand[player_choice2]
                printed_white_card2 = printed_white_card2[0].lower() + printed_white_card2[1:]
                prompt = prompt.replace("_", indexed_hand[player_choice].strip("."), 1)
                prompt = prompt.replace("_", printed_white_card2.strip("."), 1)
                print(prompt + "\n")
            elif not prompt[blank_index_finder2 - 2].islower():
                printed_white_card = indexed_hand[player_choice]
                printed_white_card = printed_white_card[0].lower() + printed_white_card[1:]
                prompt = prompt.replace("_", printed_white_card.strip("."), 1)
                prompt = prompt.replace("_", indexed_hand[player_choice2].strip("."), 1)
                print(prompt + "\n")
            else:
                prompt = prompt.replace("_", indexed_hand[player_choice].strip("."), 1)
                prompt = prompt.replace("_", indexed_hand[player_choice2].strip("."), 1)
                print(prompt + "\n")
            selection = sorted([player_choice, player_choice2], reverse=True)
            hand.pop(selection[0] - 1)
            hand.pop(selection[1] - 1)
            hand.append(white_cards.pop())
            hand.append(white_cards.pop())
            indexed_hand = {i: card for i, card in enumerate(hand, start=1)}
# Loop to ask player if they want to replay
    while True:
        replay = input("Would you like to play again, (y/n):").lower()
        if replay == "yes" or replay == "y":
            break
        elif replay == "no" or replay == "n":
            quit_game = True
            break
        else:
            print("Enter y/n to continue.")

    if quit_game:
        break

    ''' 
    1. Black card must be drawn
    2. White cards must be drawn (a traditional hand is 10)
    3. Player must choose a white card
    4. Player must choose a second white card if black card has two blanks or says "choose two"
    5. Player sees their white card(s) added to the black card or printed alone if black card is just a question (have to use enmueration and new variable then use replace function)
    X 6. (Optional) voting occurs
    7. A new Black card is issued, depletes total pool of black cards
    8. A new white card is issued, depletes total pool of white cards
    9. (Optional) Set a limit of turns.
    '''
