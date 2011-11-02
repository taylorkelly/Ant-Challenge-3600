#!/usr/bin/env python
from ants import *
import heapq, random

class PriorityQueue:
    """
        Implements a priority queue data structure. Each inserted item
        has a priority associated with it and the client is usually interested
        in quick retrieval of the lowest-priority item in the queue. This
        data structure allows O(1) access to the lowest-priority item.
        
        Note that this PriorityQueue does not allow you to change the priority
        of an item.  However, you may insert the same item multiple times with
        different priorities.
        """  
    def  __init__(self):  
        self.heap = []
    
    def push(self, item, priority):
        pair = (priority,item)
        heapq.heappush(self.heap,pair)
    
    def pop(self):
        (priority,item) = heapq.heappop(self.heap)
        return item
    
    def isEmpty(self):
        return len(self.heap) == 0


class SolutionNode:
    def __init__(self, parent, state, action, cost):
        self.parent = parent
        self.state = state
        self.action = action
        self.cost = cost
    
    def childNode(self, state, action, cost):
        return SolutionNode(self, state, action, cost)
    
    def path(self):
        path = []
        currNode = self
        
        while 1 == 1:
            if currNode.action is None:
                return path
            
            path.insert(0, currNode.action)
            
            if currNode.parent is None:
                return path
            
            currNode = currNode.parent


class MyBot:
    def __init__(self):
        # define class level variables, will be remembered between turns
        pass
    
    # do_setup is run once at the start of the game
    # after the bot has received the game settings
    # the ants class is created and setup by the Ants.run method
    def do_setup(self, ants):
        # initialize data structures after learning the game settings
        self.unseen = []
        self.enemyHills = []
        for row in range(ants.rows):
            for col in range(ants.cols):
                self.unseen.append((row, col))
    
    # do turn is run once per turn
    # the ants class has the game state and is updated by the Ants.run method
    # it also has several helper methods to use
    def do_turn(self, ants):
        orders = {}
        targets = {}

        # Check hills
        for hill_loc in ants.my_hills():
            orders[hill_loc] = None
        
        # Gather foods
        ant_dist = []
        for food_loc in ants.food():
            for ant_loc in ants.my_ants():
                dist = ants.distance(ant_loc, food_loc)
                ant_dist.append((dist, ant_loc, food_loc))
        ant_dist.sort()
        for dist, ant_loc, food_loc in ant_dist:
            if food_loc not in targets and ant_loc not in targets.values():
                self.do_move_location(ants, targets, orders, ant_loc, food_loc)

        # explore unseen areas
        for loc in self.unseen[:]:
            if ants.visible(loc):
                self.unseen.remove(loc)
        for ant_loc in ants.my_ants():
            if ant_loc not in orders.values():
                unseen_dist = []
                for unseen_loc in self.unseen:
                    dist = ants.distance(ant_loc, unseen_loc)
                    unseen_dist.append((dist, unseen_loc))
                unseen_dist.sort()
                for dist, unseen_loc in unseen_dist:
                    if self.simple_do_move_location(ants, targets, orders, ant_loc, unseen_loc):
                        break
                    
        # attack hills
        for hill_loc, hill_owner in ants.enemy_hills():
            if hill_loc not in self.enemyHills:
                self.enemyHills.append(hill_loc)        
        ant_dist = []
        for hill_loc in self.enemyHills:
            for ant_loc in ants.my_ants():
                if ant_loc not in orders.values():
                    dist = ants.distance(ant_loc, hill_loc)
                    ant_dist.append((dist, ant_loc, hill_loc))
        ant_dist.sort()
        for dist, ant_loc, hill_loc in ant_dist:
            self.do_move_location(ants, targets, orders, ant_loc, hill_loc)

        # unblock own hill
        for hill_loc in ants.my_hills():
            if hill_loc in ants.my_ants() and hill_loc not in orders.values():
                for direction in ('s','e','w','n'):
                    if self.do_move_direction(ants, orders, hill_loc, direction):
                        break


    def do_move_direction(self, ants, orders, loc, direction):
        new_loc = ants.destination(loc, direction)
        if(ants.unoccupied(new_loc) and new_loc not in orders):
            ants.issue_order((loc, direction))
            orders[new_loc] = loc
            return True
        else:
            return False

    def do_move_location(self, ants, targets, orders, loc, dest):
        dir = self.aStarSearch(ants, targets, orders, loc, dest, self.distHeuristic)
        if self.do_move_direction(ants, orders, loc, dir):
            targets[dest] = loc
            return True
        return False

    def simple_do_move_location(self, ants, targets, orders, loc, dest):
        directions = ants.direction(loc, dest)
        for direction in directions:
            if self.do_move_direction(ants, orders, loc, direction):
                targets[dest] = loc
                return True
            return False
    

    def aStarSearch(self, ants, targets, orders, loc, dest, heuristic=None):
        "Search the node that has the lowest combined cost and heuristic first."
        if (heuristic is None):
            heuristic = self.nullHeuristic
        fringe = []
        explored = []
        queue = PriorityQueue()
        
        currNode = SolutionNode(None, loc, None, 0)
                
        queue.push(currNode, heuristic(ants, currNode.state, dest))
        fringe.append(currNode.state)
        
        while 1 == 1:
            if queue.isEmpty():
                print "Error: Empty stack"
                sys.exit(1)
            currNode = queue.pop()
            if (currNode.state == dest):
                return currNode.path()[0]
            explored.append(currNode.state)
            for direction in ('s','e','w','n'):
                #if self.do_move_direction(ants, orders, hill_loc, direction):
                newLoc = ants.destination(currNode.state, direction)
                if (ants.passable(newLoc)):
                    successorNode = currNode.childNode(newLoc, direction, currNode.cost + 1)
                    if successorNode.state not in explored and successorNode.state not in fringe:
                        queue.push(successorNode, successorNode.cost + heuristic(ants, successorNode.state, dest))
                        fringe.append(successorNode.state)

    def nullHeuristic(self, ants, loc, dest):
        """
            A heuristic function estimates the cost from the current state to the nearest
            goal in the provided SearchProblem.  This heuristic is trivial.
            """
        return 0

    def distHeuristic(self, ants, loc, dest):
        """
            A heuristic function estimates the cost from the current state to the nearest
            goal in the provided SearchProblem.  This heuristic is trivial.
            """
        return ants.distance(loc, dest)


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
