class AI(object):
    def __init__(self):
        self.values = {'.' : 0 , '*' : 1 , '=' : 12 , '>' : -1 , '<' : 6}
        self.enemy = [[-1, -2, -3, -2, -1],
                      [-2, -4, -5, -4, -2],
                      [-3, -5, -6, -5, -3],
                      [-2, -4, -5, -4, -2],
                      [-1, -2, -3, -2, -1]]
        self.costPrio = [[1, 2, 3, 2, 1],
                         [2, 4, 5, 4, 2],
                         [3, 5, 6, 5, 3],
                         [2, 4, 5, 4, 2],
                         [1, 2, 3, 2, 1]]
        self.prio = [[0 for col in range(5)] for row in range (5)]

    def think(self,env, energy):

        for x in range(0, 5):
            for y in range(0, 5):
                self.prio[x][y] = self.values.get(env[x*5+y])
        self.prio[2][2] = 0.5

        if ">" in env:
            self.enemyPos = []
            for i in range(len(env)):
                if ">" is env[i]:
                    self.enemyPos.append(i)
            for p in self.enemyPos:
                row = p/5
                col = p-row*5

                for x in range(0, 5):
                    for y in range(0, 5):
                        if -2 <= row - x <= 2 and -2 <= col - y <= 2:
                            self.prio[x][y] = self.prio[x][y] + self.enemy[2-(row-x)][2-(col-y)]
                        else:
                            self.prio[x][y] = self.prio[x][y]
            print self.enemyPos

        for y in range(1, 4):
            self.prio[0][y] = self.prio[0][y] + self.prio[1][2]
            self.prio[4][y] = self.prio[4][y] + self.prio[3][2]
            self.prio[y][0] = self.prio[y][0] + self.prio[2][1]
            self.prio[y][4] = self.prio[y][4] + self.prio[3][2]

        self.prio[0][0] = self.prio[0][0] + self.prio[1][1]
        self.prio[0][4] = self.prio[0][4] + self.prio[1][3]
        self.prio[4][0] = self.prio[4][0] + self.prio[3][1]
        self.prio[4][4] = self.prio[4][4] + self.prio[3][3]

        for x in range(0, 5):
            for y in range(0, 5):
                self.prio[x][y] = self.prio[x][y] * self.costPrio[x][y]

        for x in self.prio:
            print x

        self.pos = 0
        self.max = self.prio[0][0]
        for x in range(0, 5):
            for y in range(0, 5):
                if self.prio[x][y] > self.max:
                    self.pos = x*5+y
                    self.max = self.prio[x][y]
        return self.pos

if __name__ == "__main__":


    boardtestview = "............a............"
    boardtestview2 = ">......<....a.....=....>*"
    boardtestview3 = "*...........a...........*"
    boardtestview4 = "......*.....a...........*"

    testenergy = "30"
    print boardtestview2
    ai = AI()
    move = ai.think(boardtestview4, testenergy)
    print move