# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 18:31:56 2021

@author: mark
"""

import matplotlib.pyplot as plt
import numpy as np

def flipPoints(a_votes, b_votes):
    """
    Returns the array of points where the step function of the Seats-Vote plot steps
    a_votes: an array of votes for party A indexed by district
    b_votes: an array of votes for party B indexed by district 
    """
    a_votes_adjusted = np.copy(a_votes) 
    b_votes_adjusted = np.copy(b_votes)
    flip_points = []
    
    a_vote_share_adjusted = (np.sum(a_votes_adjusted)) / (np.sum(a_votes_adjusted) + np.sum(b_votes_adjusted))
    
    while a_vote_share_adjusted != 1:
        for i in range(num_districts):
            if b_votes_adjusted[i] != 0:
                a_votes_adjusted[i] += 1
                b_votes_adjusted[i] -= 1
                
            if a_votes_adjusted[i] == b_votes_adjusted[i] or a_votes_adjusted[i] == b_votes_adjusted[i] + 1:
                flip_points.append(a_vote_share_adjusted)

        a_vote_share_adjusted = (np.sum(a_votes_adjusted)) / (np.sum(a_votes_adjusted) + np.sum(b_votes_adjusted))        

    a_votes_adjusted = np.copy(a_votes) 
    b_votes_adjusted = np.copy(b_votes)
    
    a_vote_share_adjusted = (np.sum(a_votes_adjusted)) / (np.sum(a_votes_adjusted) + np.sum(b_votes_adjusted))
    
    while a_vote_share_adjusted != 0:
        for i in range(num_districts):
            if a_votes_adjusted[i] != 0:
                a_votes_adjusted[i] -= 1
                b_votes_adjusted[i] += 1
                
            if a_votes_adjusted[i] == b_votes_adjusted[i] or a_votes_adjusted[i] == b_votes_adjusted[i] + 1:
                flip_points.append(a_vote_share_adjusted)

        a_vote_share_adjusted = (np.sum(a_votes_adjusted)) / (np.sum(a_votes_adjusted) + np.sum(b_votes_adjusted)) 
    return flip_points

def SeatsVotePlot(a_votes, b_votes):
    """
    Constructs a Vote-Seat Plot for the given election results
    a_votes: an array of votes for party A indexed by district
    b_votes: an array of votes for party B indexed by district 
    """
    x = np.linspace(0, 1, 1000)
    const = np.empty(1000)
    const.fill(0.5)
    
    plt.xlim(left = 0, right = 1)
    plt.ylim(bottom = 0, top =1.01)
    plt.xlabel("Vote Share")
    plt.ylabel("Seat Share")
    plt.axis
    
    plt.plot(a_vote_share, a_seat_share, 'bo', markersize = 4)
    
    plt.plot(x,const, 'black')
    plt.plot(const,x, 'black')
    
    flips = flipPoints(a_votes, b_votes)
    flips.sort()
    
    for i in range(len(flips)-1):
        constant = np.empty(1000)
        constant.fill((i+1)/num_districts)
        plt.plot(np.linspace(flips[i], flips[i+1],1000),constant,'r')
        
        vconstant = np.empty(1000)
        vconstant.fill(flips[i])
        plt.plot(vconstant, np.linspace(i/num_districts,(i+1)/num_districts,1000),'r')
    
        
    ones = np.empty(1000)
    zeros = np.empty(1000)
    last_verticle = np.empty(1000)
    
    ones.fill(1)
    zeros.fill(0)
    last_verticle.fill(flips[-1])
    
    plt.plot(last_verticle,np.linspace((num_districts-1)/num_districts,1,1000) ,'r')
    plt.plot(np.linspace(0,flips[0],1000),zeros, 'r')
    plt.plot(np.linspace(flips[-1],1,1000),ones, 'r')
    
    return total_votes

if __name__ == '__main__':
    #Virginia 2020 House of Representatives - a_votes are democrat and b_votes are republican
    #a_votes = np.array([186923,185733,233326,241142,190315,134729,230893,301454,0,268734,280725])
    #b_votes = np.array([260614,165031,107299,149625,210988,246606,222623,95365,271851,206253,111380,])
    
    #Wisconsin 2020 House of Representatives - a_votes are democrat and b_votes are republican
    #a_votes = np.array([163170,318523,199870,232668,175902,164239,162761,149558])
    #b_votes = np.array([238271,138306,189524,70769,265434,238874,252048,268173])
    
    #Wisconsin 2020 House of Representatives - a_votes are democrat and b_votes are republican
    a_votes = np.array([143877,224836,260358,282119,274210,215540,237084,274716])
    b_votes = np.array([250901,106335,112117,71671,123525,143599,92825,127157])
    
    num_districts = len(a_votes)
    a_votes_sum = np.sum(a_votes)
    b_votes_sum = np.sum(b_votes)
    total_votes = a_votes_sum + b_votes_sum
    
    seats_won_a = np.zeros(num_districts)
    
    for i in range(num_districts):
        if a_votes[i] > b_votes[i]:
            seats_won_a[i] = 1

    a_vote_share = a_votes_sum / total_votes
    a_seat_share = np.sum(seats_won_a) / num_districts
    
    SeatsVotePlot(a_votes, b_votes)

    
