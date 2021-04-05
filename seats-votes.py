import matplotlib.pyplot as plt
import numpy as np

def flipPoints(a_votes, b_votes):
    """
    Returns the array of points where the step function of the Seats-Vote plot steps
    a_votes: an array of votes for party A indexed by district
    b_votes: an array of votes for party B indexed by district 
    """
    
    # Create copies of both arrays to adjust and an array to store the flip points
    a_votes_adjusted = np.copy(a_votes) 
    b_votes_adjusted = np.copy(b_votes)
    flip_points = []
    
    # Calculate V_0
    a_vote_share_adjusted = (np.sum(a_votes_adjusted)) / (np.sum(a_votes_adjusted) + np.sum(b_votes_adjusted))
    
    # Loop through the states adding votes to party a until they have all votes
    while a_vote_share_adjusted != 1:
        for i in range(num_districts):
            if b_votes_adjusted[i] != 0:
                a_votes_adjusted[i] += 1
                b_votes_adjusted[i] -= 1
                
            if a_votes_adjusted[i] == b_votes_adjusted[i] or a_votes_adjusted[i] == b_votes_adjusted[i] + 1:
                flip_points.append(a_vote_share_adjusted)

        a_vote_share_adjusted = (np.sum(a_votes_adjusted)) / (np.sum(a_votes_adjusted) + np.sum(b_votes_adjusted))        
    
    # Create copies of both arrays to adjust
    a_votes_adjusted = np.copy(a_votes) 
    b_votes_adjusted = np.copy(b_votes)
    
    # Calculate V_0
    a_vote_share_adjusted = (np.sum(a_votes_adjusted)) / (np.sum(a_votes_adjusted) + np.sum(b_votes_adjusted))
    
    # Loop through the states removing votes from party a until they have no votes
    while a_vote_share_adjusted != 0:
        for i in range(num_districts):
            if a_votes_adjusted[i] != 0:
                a_votes_adjusted[i] -= 1
                b_votes_adjusted[i] += 1
                
            if a_votes_adjusted[i] == b_votes_adjusted[i] or a_votes_adjusted[i] == b_votes_adjusted[i] + 1:
                flip_points.append(a_vote_share_adjusted)

        a_vote_share_adjusted = (np.sum(a_votes_adjusted)) / (np.sum(a_votes_adjusted) + np.sum(b_votes_adjusted)) 
    # Return the flip points
    return np.sort(flip_points)

def SeatsVotePlot(a_votes, b_votes, plot_reverse = True):
    """
    Constructs a Vote-Seat Plot for the given election results
    a_votes: an array of votes for party A indexed by district
    b_votes: an array of votes for party B indexed by district 
    """
    # Create arrays to help with plotting
    x = np.linspace(0, 1, 1000)
    const = np.empty(1000)
    const.fill(0.5)
    
    # Plot the basic empty plot
    plt.xlim(left = 0, right = 1)
    plt.ylim(bottom = 0, top =1.01)
    plt.xlabel("Vote Share")
    plt.ylabel("Seat Share")
    plt.axis
    
    # Plot the realised election result
    plt.plot(a_vote_share, a_seat_share, 'ko', markersize = 4)
    
    # Plot the lines seatshare=1/2, voteshare=1/2
    plt.plot(x,const, 'black')
    plt.plot(const,x, 'black')
    
    # Use the function flipPoints to find the flip points
    flips = flipPoints(a_votes, b_votes)
    flips.sort()
    
    # Access the global variables defined in main
    global color1
    global Label1
    global once
    
    # For each of the flip points plot the seats-vote curve
    for i in range(len(flips)-1):
        constant = np.empty(1000)
        constant.fill((i+1)/num_districts)
        plt.plot(np.linspace(flips[i], flips[i+1],1000),constant,color1)
        
        vconstant = np.empty(1000)
        vconstant.fill(flips[i])
        plt.plot(vconstant, np.linspace(i/num_districts,(i+1)/num_districts,1000),color1)
    
    # Plot the last verticle line that does not get plotted by the previous for loop
    ones = np.empty(1000)
    zeros = np.empty(1000)
    last_verticle = np.empty(1000)
    ones.fill(1)
    zeros.fill(0)
    last_verticle.fill(flips[-1])
    plt.plot(last_verticle,np.linspace((num_districts-1)/num_districts,1,1000) ,color1)
    plt.plot(np.linspace(0,flips[0],1000),zeros, color1)
    plt.plot(np.linspace(flips[-1],1,1000),ones, color1, label=Label1)

    # If plot_reverse is true, run the function again to plot the republican
    # seats-vote curve
    if plot_reverse:
        if once == 0:
             once += 1
             color1 = 'r'
             Label1 = 'Republicans'
             SeatsVotePlot(b_votes,a_votes)
    
    # Add a title and legend
    plt.title(Title)
    plt.legend()
    return

def SymmetryMeasures(a_votes, b_votes):
    # Initialize the measures as zero
    PB=0
    PG=0
    MM=0
    
    # Find the flip points for both parties 
    dem_flips = (flipPoints(a_votes, b_votes))
    con_flips = (flipPoints(b_votes, a_votes))
    
    # Construct the vote vector
    vote_vector = a_votes / (a_votes + b_votes)
    vote_vector = np.sort(vote_vector)
    n = len(vote_vector)
    
    # Find the mean and median votes    
    MM = str(round(np.median(vote_vector)-np.mean(vote_vector),10))
    
    # Calculate PB - a warning is printed if the flips is close to 0.5
    for i in range(1,n):
        if dem_flips[i-1] < 0.5 and dem_flips[i] > 0.5:
            gamma_half = i / n
            if dem_flips[i] - 0.5 < 0.01:
                print('Check that PB makes sense here, there is a flip within 1% of 50%')      
    PB = gamma_half - 0.5
    
    # Calculate PG
    for i in range(len(dem_flips)):
        PG += abs(dem_flips[i]-con_flips[i]) * (1/num_districts)
    
    # Return the measures
    return PG, MM, PB

def EfficiencyGap(a_votes, b_votes):
    # Initialize the variables as zero 
    EG = 0
    wasted_a = 0
    wasted_b = 0
    
    # for each district, calculate the wasted votes for each party 
    for i in range(len(a_votes)):
        if a_votes[i] > b_votes[i]: # if party a wins district i 
            wasted_b += b_votes[i]
            wasted_a += a_votes[i] - ((a_votes[i]+b_votes[i]) / 2)
        else:                       # if party b wins district i
            wasted_a += a_votes[i]
            wasted_b += b_votes[i] - ((a_votes[i]+b_votes[i]) / 2)
    
    # Calculate the Efficiency Gap
    EG = (wasted_a - wasted_b) / (sum(a_votes) + sum(b_votes))
    
    return EG


if __name__ == '__main__':
    ##########################################################################
    # 2020 House of Representatives ##########################################
    ##########################################################################
    
    # Body of Project Text
    
    #Virginia
    #Title='Virginia Seat-Vote Plot'
    #a_votes = np.array([186923,185733,233326,241142,190315,134729,230893,301454,0,268734,280725])
    #b_votes = np.array([260614,165031,107299,149625,210988,246606,222623,95365,271851,206253,111380,])
    
    #Virginia Even Test
    #Title='Virginia Seat-Vote Plot Even Test'
    #a_votes = np.array([186922,185733,233325,241141,190314,134728,230893,301453,0,268733,280724])
    #b_votes = np.array([260614,165031,107299,149625,210988,246606,222623,95365,271850,206253,111380,])
    
    #Wisconsin
    #Title='Wisconsin Seat-Vote Plot'
    #a_votes = np.array([163170,318523,199870,232668,175902,164239,162761,149558])
    #b_votes = np.array([238271,138306,189524,70769,265434,238874,252048,268173])
    
    #Maryland
    #Title='Maryland Seat-Vote Plot'
    #a_votes = np.array([143877,224836,260358,282119,274210,215540,237084,274716])
    #b_votes = np.array([250901,106335,112117,71671,123525,143599,92825,127157])
    
    ##########################################################################
    # Indiana - Case Study
    ##########################################################################
    
    # Districting Plan A
        
    # Indiana 2002
    #Title = 'Indiana 2002'
    #a_votes = np.array([90443,86253,50509,41314,45283,63871,77478,88763,96654])
    #b_votes = np.array([41909,95081,92566,112760,129442,118436,64379,98952,87169])
    
    # Indiana 2004
    #Title = 'Indiana 2004'
    #a_votes = np.array([178406,115513,76232,77574,228718,85123,121303,121522,140772])
    #b_votes = np.array([82858,140496,171389,190445,82637,182529,97491,145576,142197])
    
    # Indiana 2006
    #Title = 'Indiana 2006'
    #a_votes = np.array([104195,103561,80357,66986,64362,76812,74750,131019,110454])
    #b_votes = np.array([40146,88300,95421,111057,133118,115266,64304,83704,100469])
    
    # Indiana 2008
    #Title = 'Indiana 2008'
    #a_votes = np.array([199954,187416,112309,129038,123357,94265,172650,188693,181281])
    #b_votes = np.array([76647,84455,155693,192526,234705,180608,92645,102769,120529])
    
    # Indiana 2010
    #Title = 'Indiana 2010'
    #a_votes = np.array([99387,91341,61267,53167,60024,56647,86011,76265,95353])
    #b_votes = np.array([65558,88803,116140,138732,146899,126027,55213,117259,118040])
    
    # Districting Plan B
    
    # Indiana 2012
    #Title = 'Indiana 2012'
    #a_votes = np.array([187743,130113,92363,93015,125347,96678,162122,122325,132848])
    #b_votes = np.array([91291,134033,187872,168688,194570,162613,95828,151533,165332])
    
    # Indiana 2014
    #Title = 'Indiana 2014'
    #a_votes = np.array([86579,55590,39771,47056,49756,45509,61443,61384,55016])
    #b_votes = np.array([51000,85583,97892,94998,105277,102187,46887,103344,101594])
    
    # Indiana 2016
    #Title = 'Indiana 2016'
    #a_votes = np.array([207515,102401,66023,91256,123849,79135,158739,93356,130627])
    #b_votes = np.array([0,164355,201396,193412,221957,204920,94456,187702,174791])
    
    # Indiana 2018
    #Title = 'Indiana 2018'
    #a_votes = np.array([159611,103363,86610,87824,137142,79430,141139,86895,118090])
    #b_votes = np.array([85594,125499,158927,156539,180035,154260,76457,157396,153271])

    # Indiana 2020
    Title = 'Indiana 2020'
    a_votes = np.array([185180,114967,104762,112984,191226,91103,176422,95691,122566])
    b_votes = np.array([132247,183601,220989,225531,208212,225318,106146,214643,222057])
    
    # Initialize some basic variables
    once = 0
    color1 = 'b'
    Label1 = 'Democrats' 
    num_districts = len(a_votes)
    a_votes_sum = np.sum(a_votes)
    b_votes_sum = np.sum(b_votes)
    total_votes = a_votes_sum + b_votes_sum
    seats_won_a = np.zeros(num_districts)
    
    # Calculate the number of seats won by party a
    for i in range(num_districts):
        if a_votes[i] > b_votes[i]:
            seats_won_a[i] = 1

    # Calculate the vote share vectors
    a_vote_share = a_votes_sum / total_votes
    a_seat_share = np.sum(seats_won_a) / num_districts
    
    # Print the election year and state
    print(Title)
    
    # Print the efficiency Gap for party a
    print(EfficiencyGap(a_votes, b_votes)) 
    
    # Print the flip points for party a
    print((flipPoints(a_votes, b_votes)))
    
    # Print the symmetry measures for party a
    print(SymmetryMeasures(a_votes, b_votes)) 
    
    # Plot the seats-vote curve
    SeatsVotePlot(a_votes, b_votes, plot_reverse = False) 
