'''
File: project1
Author: Dean Sheng and Songyang Guo
Purpose: Source code for CS4613 Project 1: 15-Puzzle
'''

import copy
import heapq
BLANK_TOKEN = '0'


class State:
    class Coord:
        def __init__(self,x,y):
            self.x=x
            self.y=y
        def __eq__(self, other):
            return self.x==other.x and self.y==other.y
        def __ne__(self, other):
            return not self.__eq__(other)
        def __repr__(self):
            return "({}, {})".format(self.x,self.y)
        def copy(self):
            newCoord=State.Coord(self.x,self.y)
            return newCoord

    def __init__(self,m,blank):
        '''
        load state
        :param m: matrix
        :param blank: blank coord
        '''
        self.blank=blank.copy()
        self.m=copy.deepcopy(m)

    def move(self,x,y):
        '''
        move state
        :param x:-1,0,1
        :param y: -1,0,1
        :return: void
        '''
        #print(self.blank)
        self.m[self.blank.x][self.blank.y] = self.m[self.blank.x+x][self.blank.y+y]
        self.m[self.blank.x+x][self.blank.y+y] = BLANK_TOKEN
        self.blank.x += x
        self.blank.y += y

    def moveCheck(self,x,y):
        '''
        check legal state
        :param x:-1,0,1
        :param y: -1,0,1
        :return: -1:error 0:fail, 1:success
        '''
        if x < -1 or x > 1:
            raise ValueError("Cant move x grid more than 1")
        if y < -1 or y > 1:
            raise ValueError("Cant move y grid more than 1")
        if self.blank.x + x >= len(self.m) or self.blank.x + x < 0:
            return 0
        if self.blank.y + y >= len(self.m[0]) or self.blank.y + y < 0:
            return 0
        return 1
    
    def heuristic(self, goalMap):
        '''
        heuristic function by chessboard distance
        :param goalMap: location map of goal state. item->Coord
        :return: h(s)
        '''
        result=0
        for i in range(len(self.m)):
            for j in range(len(self.m[0])):
                if self.m[i][j]!=BLANK_TOKEN:
                    result+=max(abs(i-goalMap[self.m[i][j]].x),abs(j-goalMap[self.m[i][j]].y))
        return result

    def genMap(self):
        coordMap={}
        for i in range (len(self.m)):
            for j in range(len(self.m[0])):
                coordMap[self.m[i][j]]=State.Coord(i,j)
        return coordMap

    def __copy__(self):
        return State(self.m,self.blank)

    def __hash__(self):
        return hash(str(self.m))

    def __eq__(self, other):
        '''
        Check Repeated States
        :param other: State
        :return: bool
        '''
        return str(self.m)==str(other.m)

    def __ne__(self,other):
        return not State.__eq__(other)

    def __repr__(self):
        return str(self.m)
    def __str__(self):
        return '\n'.join([' '.join(self.m[i]) for i in range(len(self.m[0]))])
    

class Node:
    def __init__(self,state,goalMap,parent=None,action=None,path_cost=0):
        # initialize a node with state, parent, action, path cost, and estimated total cost
        self.state=state
        self.parent=parent
        self.action=action
        self.path_cost=path_cost
        self.f=path_cost+state.heuristic(goalMap)
    
    def __lt__(self,other):
        return self.f < other.f
    
    def expand(self, goalMap):
        # expand a node by returning all child nodes
        s=self.state
        actions = [[0, -1], [-1, -1], [-1, 0], [-1, 1],
              [0, 1], [1, 1], [1, 0], [1, -1]]
        for i in range(len(actions)):
            #check legal
            if self.state.moveCheck(actions[i][0], actions[i][1]) == 1:
                newState = State(self.state.m, self.state.blank)
                newState.move(actions[i][0], actions[i][1])
                new_path_cost=self.path_cost+1
                yield Node(newState,goalMap,self,i+1,new_path_cost)
    
    def __repr__(self):
        return str(self.state)
    
def search(initialState, goalState):
    #store goal map for optimization
    goalMap=goalState.genMap()
    node=Node(initialState,goalMap)
    n=1
    frontier=[node]
    # use heap queue to represent the priority queue
    heapq.heapify(frontier)
    reached={initialState:node}
    while frontier:
        node=heapq.heappop(frontier)
        if node.state == goalState:
            return node,n
        for child in node.expand(goalMap):
            s=child.state
            # check repeated state
            if s not in reached or child.f<reached[s].f:
                reached[s]=child
                heapq.heappush(frontier,child)
                n+=1
    return None,-1

def io(inputFileName, outPutFileName):
    #read initial state from input file
    fi=open(inputFileName,'r')
    m=[]
    for i in range(4):
        ls=fi.readline().strip().split()
        m.append(ls)
        for j in range(4):
            if ls[j]=='0':
                blank=State.Coord(i,j)
    initialState=State(m,blank)
    fi.readline()

    #read goal state
    m=[]
    for i in range(4):
        ls=fi.readline().strip().split()
        m.append(ls)
        for j in range(4):
            if ls[j]=='0':
                blank=State.Coord(i,j)
    fi.close()
    goalState=State(m,blank)
    fo=open(outPutFileName,'w')
    # output initial state and goal state
    fo.write(str(initialState)+'\n\n')
    fo.write(str(goalState)+'\n\n')
    goalNode, n=search(initialState,goalState)

    def solution(node,sol):
        '''
        get solution path
        :param node: goal node
        :param sol: output array
        :return: void
        '''
        if node.parent:
            solution(node.parent,sol)
        sol.append(node)

    sol=[]
    solution(goalNode,sol)
    # output the depth level of the shallowest goal node, total number of nodes, solution, and f(n) values
    fo.write(str(len(sol)-1)+'\n')
    fo.write(str(n)+'\n')
    for i in range(1,len(sol)):
        fo.write(str(sol[i].action)+' ')
    fo.write('\n')
    for node in sol:
        fo.write(str(node.f)+' ')
    fo.close()

def main():
    print("Make sure file names are correct, or you have to rerun the program")
    inputFileName=input("Please enter input file name: ")
    outputFileName=input("Please enter output file name: ")
    io(inputFileName,outputFileName);

if __name__ == '__main__':
    main()
