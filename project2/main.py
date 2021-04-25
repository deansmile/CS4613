class csp:
    def __init__(self):
        self.gtConstraints = set()  # data type: ((x1,y1),(x2,y2))   --> a>b

    def addConstraint(self, x1, y1, x2, y2):
        '''
        add gt constraint
        :param x1: row coordinate of greater element
        :param y1: col coordinate of greater element
        :param x2: row coordinate of smaller element
        :param y2: col coordinate of smaller element
        :return:
        '''
        self.gtConstraints.add((x1, y1), (x2, y2))


class Assignment:
    def __init__(self):
        '''
        board size:6
        '''
        self.domain = [1, 2, 3, 4, 5, 6]
        self.rowSet = [set(domain) for i in range(6)]
        self.colSet = [set(domain) for i in range(6)]
        self.m = [0]*6
        for i in range(6):
            self.m[i] = [0]*6

    def set(self, x, y, val):
        if not val in [1, 2, 3, 4, 5, 6]:
            raise ValueError("Illegal Value")
        # keep row set and col set to dynamically track domains with O(1)
        if self.m[x][y] != 0:
            self.rowSet[x].remove(self.m[x][y])
            self.colSet[y].remove(self.m[x][y])
        if val != 0:
            self.rowSet[x].add(val)
            self.colSet[y].add(val)
        self.m[x][y] = val

    def remove(self, x, y):
        self.set(x, y, 0)

    def getDomain(self, x, y, csp):
        domain = self.rowSet[x].union(self.colSet[y])
        checks = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        for item in checks:  # total iterations in this loop <24
            # find if checked cell has been filled
            if (self.m[item[0]][item[1]] != 0):
                # deal with smaller constriants
                # would be beter to go reversed order, but set does not allow reversed() method
                if (item, (x, y)) in csp.gtConstraints:
                    for element in domain:
                        if element >= self.m[item[0]][item[1]]:
                            domain.remove(value)
                # deal with greater constraints
                elif ((x, y), item) in csp.gtConstraints:
                    for element in domain:
                        if element <= self.m[item[0]][item[1]]:
                            domain.remove(value)
        return domain

    def selectUnassignedValue(self, csp):
        minDomainSize = 6
        targets = []
        # minimum value left heuristic
        # find smallest domains
        for i in range(6):
            for j in range(6):
                if self.m[i][j] == 0:
                    currDomain = self.getDomain(i, j, csp)
                    if len(currDomain) < minDomainSize:
                        minDomainSize = len(currDomain)
                        targets = [(i, j)]
                    elif len(currDomain) == minDomainSize:
                        targets.append((i, j))
        # degree heuristic
        maxdegree = -1

        for i, j in targets:
            # degree num = # of unfilled cell in same row+ ... in same col
            currdegree = (5-len(self.rowSet[i]))+(5-len(self.colSet[j]))
            if currdegree > maxdegree:
                maxdegree = currdegree
                result = (i, j)
        return result

    def orderDomainValues(self, x, y, csp):
        '''

        :param val: (x,y)
        :param domain:
        :return:
        '''
        return self.getDomain(x, y, csp)


def backTrackSearch(domains):
    '''

    :param domains: matrix of arrays
    :return: assignment
    '''
    # use csp.addConstraint to load the inequalities.
    # use assignment.set to load initial data

