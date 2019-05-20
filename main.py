import gym
from gym import spaces
import numpy as np
import random
import sys


env = gym.make("Blackjack-v0")
state = None
round_counter = 0
reward_counter = 0
debug = 1 # set to 1 to print exceptions
cardbot = 0  # Set cardbot to 1 to train an RL agent, leave at zero to interact
cumuward = 0 # Cumulative reward for all rounds
round_count = 0 # number of total rounds

# state = 32*32*2 array
# 1.) Players current sum
# 2.) Dealers current sum
# 3.) Player has usable ace
# 4.) List of [player hand numeric values, dealer hand numeric values]


def step(hit_or_stay):
    global env
    global state

    try:
        if hit_or_stay == 0 or hit_or_stay == 1:
            state, reward, done = env.step(hit_or_stay)

            if not cardbot:
                print("player card total: {} {} ({} Ace), Dealer visible card sum: {}".format(state[0], state[3][0],
                                                                                   "Yes" if state[2] is True else
                                                                               "No usable", state[1]))
            if done is True:
                if state[0] > 21:
                    if not cardbot:
                        print("Bust! {}".format(state[3][0]))
                if not cardbot:
                    if reward > 0:
                        print("Round complete.  You Won! {} ({}) Dealer hand: {} ({})".format(state[0], state[3][0],
                                                                                         state[1], state[3][1]))
                    else:
                        print("Round complete.  You Lost {} ({}) Dealer hand: {} ({})".format(state[0], state[3][0],
                                                                                            state[1], state[3][1]))

                    try:
                        new_round = str(input("Deal another round? y/n:"))
                        if new_round.lower() == "y":
                            deal_new_round()
                        elif new_round.lower() == "n":
                            sys.exit()
                        else:
                            print("please use y or n")
                            deal_new_round()
                    except KeyboardInterrupt:
                        sys.exit()
                else:
                    deal_new_round()
            else:
                prompt()
        else:
            prompt()
    except Exception as err:
        if debug:
            print("Error! (def step()): {}".format(err))


def prompt():
    hit_or_stay = 0
    try:
        if not cardbot:
            hit_or_stay = int(input("Choose an action: enter 0 for stay, 1 for hit: "))
        else:
            hit_or_stay = env.action_space.sample()

        step(hit_or_stay)
    except KeyboardInterrupt:
        sys.exit()
    except Exception as err:
        print("Error (def prompt): {}".format(err))
        prompt()


def deal_new_round():
    global round_count

    round_count = round_count + 1

    if not cardbot:
        print("\nStarting round #{} of BlackJack\n Dealer stands on 17".format(round_count))
        print("---------------------\n")

    player_hand_sum, dealer_face_up, usable_ace, hands = env.reset()

    if not cardbot:
        print("player hand value: {} ({} {} Ace), Dealer face-up card: {}".format(player_hand_sum, hands[0],
                                                                           "With" if usable_ace is True else
                                                                          "No", dealer_face_up))
    if player_hand_sum == 21:
        if not cardbot:
            print("Natural Black Jack! You Won\n\n")
            try:
                new_round = str(input("Deal another round? y/n:"))
                if new_round.lower() == "y":
                    deal_new_round()
                elif new_round.lower() == "n":
                    sys.exit()
                else:
                    print("please use y or n")
                    deal_new_round()
            except KeyboardInterrupt:
                sys.exit()
        else:
            deal_new_round()
    else:
        prompt()



deal_new_round()

