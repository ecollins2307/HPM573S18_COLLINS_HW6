# HW 6, Problems 1, 2, and 3

# load NumPy, requires Anaconda to be installed locally and chosen as the interpreter
import numpy as numpy

# load StatisticalClasses from SupportLib, requires newest version of SupportLib to be loaded in content root
import scr.StatisticalClasses as Stat

# Modified HW 4 code to complete HW 6, Problems 1 and 2
# create Game class
class Game(object):
    def __init__(self, flip_probability):
        self.flip_probability = flip_probability #probability of heads

    # create Simulate function
    def Simulate(self, number_of_flips, number_of_realizations):
        self.number_of_flips = number_of_flips
        self.number_of_realizations = number_of_realizations

        gamecost = -250 # cost of playing the game
        totalwinnings = 0 # initialize total winnings
        winningslist = [] # empty list to place each game's winnings into for CI construction
        loselist = [] # empty list to place a 1 in if you lost a game and a 0 in if you won a game

        for j in range(0, self.number_of_realizations):
            fliplist = "" # create an empty string

            for i in range(0, self.number_of_flips): # iterate through 20 flips, treating 1's as heads and 0's as tails
                fliplist = fliplist + str((numpy.random.binomial(1, self.flip_probability))) #per https://docs.scipy.org/doc/numpy/reference/generated/numpy.random.binomial.html, add each flip to fliplist

            winnings = gamecost+(100*(fliplist.count("001"))) # find the number of Tails, Tails, Heads, multiply by fifty, add to cost of game to find winnings
            winningslist.append(winnings) # append winningslist with each games winnings
            if winnings < 0:
                loselist.append(1) # if winnings are less than 0, append 1 to loselist
            if winnings >= 0:
                loselist.append(0) # if winnings are equal to or greater than 0, append 0 to lost list
            totalwinnings = totalwinnings + winnings # add all the realizations of winnings together


        # Problem 1
        print("Problem 1:")
        # Expected reward confidence intervals
        winings_summarystats = Stat.SummaryStat('Game winnings', winningslist)
        print("95% t-based confidence intervals for the expected reward:",winings_summarystats.get_t_CI(0.05))

        # Probablitiy of loss
        loss_summarystats = Stat.SummaryStat('Loss probability', loselist)
        print("95% t-based confidence intervals for the probability of loss:",loss_summarystats.get_t_CI(0.05),'\n')

        # Problem 2
        print("Problem 2:")
        print("The first confidence interval (expected reward) can be interpreted as containing 95% of the confidence intervals "
              "produced by continuous game runs which themselves contain the true mean value of the reward.")
        print("The second confidence interval (probability of loss) can be interpreted as containing 95% of the confidence intervals"
              "produced by continuous game runs which themselves contain the true probabiltiy of loss.",'\n')


    # Modified HW 4 code to complete HW 6, Problem 3
    # create Simulate function which differentiates between owner and gambler
    def Simulate_by_player_type(self, number_of_flips, number_of_realizations, player_type):
        self.number_of_flips = number_of_flips
        self.number_of_realizations = number_of_realizations
        self.player_type = player_type # player type must be either 'owner' or 'gambler'

        gamecost = -250 # cost of playing the game
        totalwinnings = 0 # initialize total winnings
        winningslist = [] # empty list to place each game's winnings into for CI construction

        for j in range(0, self.number_of_realizations):
            fliplist = "" # create an empty string

            for i in range(0, self.number_of_flips): # iterate through 20 flips, treating 1's as heads and 0's as tails
                fliplist = fliplist + str((numpy.random.binomial(1, self.flip_probability))) #per https://docs.scipy.org/doc/numpy/reference/generated/numpy.random.binomial.html, add each flip to fliplist

            winnings = gamecost+(100*(fliplist.count("001"))) # find the number of Tails, Tails, Heads, multiply by fifty, add to cost of game to find winnings
            winningslist.append(winnings) # append winningslist with each games winnings

            totalwinnings = totalwinnings + winnings # add all the realizations of winnings together
        averagewinnings = '${:,.2f}'.format((totalwinnings/self.number_of_realizations)) # find the average winnings

        print("Problem 3:")
        # Construct CIs for casino owner
        if self.player_type == "owner":
            owner_summarystats = Stat.SummaryStat('Owner game winnings', winningslist)
            print("Casino Owner:")
            print("Expected reward from 1000 games (from perspective of player):", averagewinnings)
            print("95% t-based confidence intervals for the expected reward:",owner_summarystats.get_t_CI(0.05))
            print("As the casino owner gets to play the game many times, the game should be viewed as a steady-state system. Thus, "
                  "confidence intervals should be constructed. Based on 1000 games, the casino owner should expect a player "
                  "to earn the amount of money displayed in 'Expected reward', with an associated 95% confidence interval "
                  "interpreted as containing 95% of the confidence intervals produced by continuous game runs which themselves contain the true mean value of the reward."
                  " As the confidence intervals do not cross 0, this is a good game for the owner!",'\n')

        # Construct PIs for player
        if self.player_type == "player":
            player_summarystats = Stat.SummaryStat('Player game winnings', winningslist)
            print("Player:")
            print("Expected reward from 10 games:", averagewinnings)
            print("95% prediction intervals for the expected reward:",player_summarystats.get_PI(0.05))
            print("As the player can only play the game a handful of times and the expected reward may vary widely, "
                  "the game should be viewed as a transient-state system. Thus, a prediction interval should be constructed. "
                  "The prediction interval can be interpreted as 'The next game reward will fall within the given prediction interval "
                  "with 95% probability.'")

# Running above code

# Problems 1 and 2
# Initialize an even 50-50 game
fiftyfiftyflip = Game(0.5)
# Run the simulation
fiftyfiftyflip.Simulate(20, 1000)

# Problem 3
# Casino owner run
fiftyfiftyflip.Simulate_by_player_type(20, 1000, player_type="owner")
# Player run
fiftyfiftyflip.Simulate_by_player_type(20, 10, player_type="player")



