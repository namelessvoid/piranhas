class AI(object):
    def __init__(self):
        self.eyes = []
        self.eyes.append(eye(6,0))
        self.eyes.append(eye(7,1))
        self.eyes.append(eye(7,2))
        self.eyes.append(eye(7,3))
        self.eyes.append(eye(8,4))
        self.eyes.append(eye(13,9))
        self.eyes.append(eye(13,14))
        self.eyes.append(eye(13,19))
        self.eyes.append(eye(18,24))
        self.eyes.append(eye(17,23))
        self.eyes.append(eye(17,22))
        self.eyes.append(eye(17,21))
        self.eyes.append(eye(16,20))
        self.eyes.append(eye(11,15))
        self.eyes.append(eye(11,10))
        self.eyes.append(eye(11,5))
        self.cost = {'0' : 7, '1' : 6, '2' : 5, '3' : 6,   '4' : 7,  
                          '5' : 6, '6' : 2, '7' : 2, '8' : 3, '9' : 6, 
                        '10' : 5, '11' : 3, '12' : 1, '13' : 2, '14' : 5 , 
                        '15' : 6 , '16' : 2, '17' : 2, '18' : 3, '19' : 6,
                        '20' : 7, '21' : 6, '22' : 5, '23' : 6, '24' : 7}

    def think(self,env, energy):
        move = 12
        self.impression = []
        for i in range(len(self.eyes)):
            x,y = self.eyes[i].getfields()
            loc, weight = (self.eyes[i].investigate(env[x],env[y]))
            self.impression.append([loc,weight])
        self.hungry(energy)
        move = self.getbest()
        return move

    def hungry(self, energy):
        for i in self.impression:
            if self.cost.get(i[0]) > energy:
                self.impression.remove(i)

    def getbest(self):
        bestattraction = 0
        bestpos = 12
        for i in self.impression:
            if  i[1] > bestattraction:
                bestattraction = i[1]
                bestpos = i[0]
        return bestpos

class eye(object):
    def __init__(self, closerange, widerange):
        self.closerange = closerange
        self.widerange = widerange
        self.innerweight = 1.0
        self.outerweight = 0.75
        self.dict = {'.'  : 0.0 , '*' : 0.5 , '<' : 1.0 , '>' : -1.0, '=' : 1.0}

    def getfields(self):
        return self.closerange, self.widerange

    def investigate(self, innerfield, outerfield):
        closeattraction = self.dict.get(innerfield) * self.innerweight
        wideattraction = self.dict.get(outerfield) * self.outerweight
        if  closeattraction == -1.0 or wideattraction == -0.75:
            return -1 , -1
        elif closeattraction > wideattraction :
            return self.closerange, closeattraction
        elif wideattraction > closeattraction :
            return self.widerange, wideattraction
        else:
            return 12 , 0
