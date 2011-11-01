#!/usr/bin/env python
import random 
from random import shuffle
from ants import *
from DataStructs import *
import DataStructs
# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us
class MyBot:
    def __init__(self):
        # define class level variables, will be remembered between turn
       self.enemyList = [] # List of enemy ants 
       self.foodList = []
       # self.attackRadius = ants.attackradius2
       
    # do_setup is run once at the start of the game
    # after the bot has received the game settings
    # the ants class is created and setup by the Ants.run method
    def do_setup(self, ants):
        # initialize data structures after learning the game settings
        self.hills = []
        self.visitedList = []
        self.counter = 0
        self.foodList = ants.food()
       # self.unseen = []
       # self.undiscovered = []
       # self.undiscovered = aStar(ants.my_hills()[0]) # CHECK
      #  self.undiscovered = aStar((0,0))
       # for row in range(ants.rows):
       #     for col in range(ants.cols):
          #      self.unseen.append((row, col))
         
    # do turn is run once per turn
    # the ants class has the game state and is updated by the Ants.run method
    # it also has several helper methods to use
    def do_turn(self, ants):
        # track all moves, prevent collisions
        orders = {}
       # print ants.my_hills()[0]
        enemyList = ants.enemy_ants()

        
        def do_move_direction(loc, direction):
            new_loc = ants.destination(loc, direction)
            if not ants.passable(new_loc): # Can't move to location because it is water
                return False       
            for enemy in enemyList:
                   if ants.visible(enemy[0]):
                        enemyDist = ants.distance(new_loc, enemy[0]) # Store distance between current location and enemy location
                        if len(ants.my_hills()) != 0: # We have a hill
                            if enemyDist < 5 and ants.distance(loc, ants.my_hills()[0]) > 5 : # FIX DISTANCE Will avoid moving within attacking range of another ant
                                return False
            
            if (ants.unoccupied(new_loc) and new_loc not in orders and loc not in orders.values()): # checks if location is unoccupied and no ant has been assigned to move to that location
                ants.issue_order((loc, direction)) # Tells the ant to move in a given direction, loc is the current ant location 
                orders[new_loc] = loc # The orders list now includes an ant going to the new location 
                return True
            else:
                return False
        
        def do_move_direction_lite(loc, direction):
            new_loc = ants.destination(loc, direction)
            if not ants.passable(new_loc):
                return False 
            if (ants.unoccupied(new_loc) and new_loc not in orders and loc not in orders.values()):       
                ants.issue_order((loc, direction)) # Tells the ant to move in a given direction, loc is the current ant location 
                orders[new_loc] = loc # The orders list now includes an ant going to the new location 
                return True
            else:
                return False

            
        targets = {}
        def do_move_location(loc, dest):
            directions = ants.direction(loc, dest) # determine the 1 or 2 fastest (closest) directions to reach a location
            for direction in directions:
                if do_move_direction(loc, direction): # If possible to move there and another ant is not already ordered to move there
                    targets[dest] = loc # Key = successor location Value = current ant location
                    return True
            return False
        
        def do_move_location_lite(loc, dest):
            directions = ants.direction(loc, dest) # determine the 1 or 2 fastest (closest) directions to reach a location
            for direction in directions:
                if do_move_direction_lite(loc, direction): # If possible to move there and another ant is not already ordered to move there
                    targets[dest] = loc # Key = successor location Value = current ant location
                    return True
            return False
        
        def exploreMap():
            distList = []
            #foodArray = []
            for ant_loc in ants.my_ants():
                if ant_loc in self.foodList:
                    self.foodList.remove(ant_loc)
                undiscovered = aStar(ant_loc)
                #distList = []
                if ant_loc not in orders.values() and undiscovered != None: # Ant has not been assigned an order yet
                    for loc, isFood in undiscovered:
                        if (ants.passable(loc)):
                            if (isFood == True):  
                                foodArray.append((ants.distance(ant_loc, loc), loc, ant_loc)) # 0 because food is more important than exploring
                            else:
                                distList.append((ants.distance(ant_loc, loc), loc, ant_loc))
            distList.sort()
           # foodArray.sort()
                      #  if distance < minDistance:
                           # minDistance = distance
                          #  closestLoc = loc
            #for dist, loc, ant_location in foodArray:
             #   if loc not in targets and ant_location not in targets.values():
              #      if do_move_location(ant_location, loc): # Attempt to move to the closest undiscovered location
               #         break
            for dist, loc, ant_location in distList:
                if loc not in targets and ant_location not in targets.values():
                    if do_move_location(ant_location, loc): # Attempt to move to the closest undiscovered location
                        break 
                    
        directionList = ['s', 'n', 'w', 'e']
        shuffle(directionList)

        
        def aStar(ant_loc):
            visitedList = []
            undiscovered = []
            foodDisc = []
            parent = None # First node doesn't have a parent
            direct = None # First node doesn't have a parent
            pathCost = 0 # start with 0 pathCost
            myPQ = DataStructs.PriorityQueue()
            myPQ.push((ant_loc, parent, direct, pathCost), pathCost)
            level = 0
            # self.foodList = ants.food()
            
            while not myPQ.isEmpty() and level < 100:
                level += 1
                shuffle(directionList)
                currNode = myPQ.pop()
                #if currNode[0] in self.foodList: # Found a space with food
                 #    if currNode[0] not in targets and ant_loc not in targets.values():
                  #      foodDisc.append((currNode[0], True)) # (Food Loc, True if food location False otherwise)
                     #if len(foodDisc) > 2:
                   #     return foodDisc # Return food location
                if not ants.visible(currNode[0]): # Check if current state is visible - this is a goal state
                    #undiscovered.append(ants.distance(ant_loc, currNode), currNode)
                    undiscovered.append((currNode[0], False))
                    #if len(undiscovered) > 50:
                        #if len(foodDisc) != 0:
                         #   return foodDisc
                        #else:
#                    return undiscovered
                if currNode[0] not in visitedList:
                    visitedList.append(currNode[0])
                    for direction in directionList: #('s','e','w','n'):
                        new_loc = ants.destination(currNode[0], direction)
                        dist = ants.distance(currNode[0], new_loc)
                        if ants.passable(new_loc) and new_loc not in visitedList:
                            myPQ.push ((new_loc, currNode[0], direction, currNode[3] + dist), currNode[3] + dist) # Push new location, direction, parent, with a heuristic
            return undiscovered                 #myPQ.push ((new_loc, currNode[0], direction, dist), dist)
        
        # prevent stepping on own hill
        def avoidOwnHill():
            if len(ants.my_ants()) > 1:
                for hill_loc in ants.my_hills():
                    orders[hill_loc] = None # So no ants are ordered to step on the hill
            
        
                # Update foodList
        def updateFoodList():
            for food in ants.food():
                if food not in self.foodList:
                    self.foodList.append(food)
                
        # Move Towards Closest Known Food
        def moveFood():
            ant_dist = [] # Holds the distance between an ant and food, as well as the ants current location and the food location
            for food_loc in ants.food(): # for every food location in the food list
                for ant_loc in ants.my_ants(): # for every ant we control
                    dist = ants.distance(ant_loc, food_loc) # find distance between ant and food
                    ant_dist.append((dist, ant_loc, food_loc))
            ant_dist.sort() # Put ants closest to food first in list
            for dist, ant_loc, food_loc in ant_dist:
                if food_loc not in targets and ant_loc not in targets.values(): # check to see if a food item already has an ant gathering it. 
                    do_move_location(ant_loc, food_loc)
                
         
        # attack hills
        def attackHills():
            for hill_loc, hill_owner in ants.enemy_hills():
                if hill_loc not in self.hills: # Hill has yet to be discovered in previous turns
                    self.hills.append(hill_loc)        
            ant_dist = []
            for hill_loc in self.hills:
                for ant_loc in ants.my_ants():
                    shuffle(directionList)
                    if (ant_loc in self.hills):
                        self.hills.remove(ant_loc)
                    if ant_loc not in orders.values(): # Current ant has not been assigned an order
                         dist = ants.distance(ant_loc, hill_loc) # Find distance between ant and enemy hill
                         ant_dist.append((dist, ant_loc))
            ant_dist.sort() # Closest ant to hill at beginning of list
            for dist, ant_loc in ant_dist: 
                do_move_location_lite(ant_loc, hill_loc) # Move towards enemy hill


        # unblock own hill
        def unblockHill():
            for hill_loc in ants.my_hills():
                if hill_loc in ants.my_ants() and hill_loc not in orders.values():
                    for direction in directionList: #('s','e','w','n'):
                        if do_move_direction(hill_loc, direction):
                            break        
        
        # Random Move
        def randomMove():
            for ant_loc in ants.my_ants():
                shuffle(directionList)
                if ant_loc not in orders.values():
                    for direction in directionList:#('s','e','w','n'):
                        if do_move_direction(ant_loc, direction):
                            break                 
                            
        updateFoodList()
        avoidOwnHill()
        unblockHill() 
        moveFood()
        attackHills()
        exploreMap()    # explore the map using aStar search
        randomMove()                 
if __name__ == '__main__':
    # psyco will speed up python a little, but is not needed
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    
    try:
        # if run is passed a class with a do_turn method, it will do the work
        # this is not needed, in which case you will need to write your own
        # parsing function and your own game state class
        Ants.run(MyBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
