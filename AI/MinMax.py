BLOCK = 3
ME = 1
ENEMY = 2
CROSS = 6
NMES = 5
MINE = 4
LIMIT = 2


def score(gameboard):
    count = 0
    for row in gameboard:
        for col in row:
            if int(col) == int(NMES):
                count -= 1
            elif int(col) == int(MINE):
                count += 1
    return count


def directions(gameboard, a, b, laser, x, y):
    length = len(gameboard)
    for i in range(1, 4):
        j = x + (i * a)
        k = y + (i * b)
        if int(j) < 0 or int(k) < 0 or int(j) >= int(length) or int(k) >= int(length):
            break
        else:
            #print(str(j) + " " + str(k) )
            sqr = gameboard[j][k]
            if int(sqr) == int(BLOCK):
                break
            elif int(sqr) == int(0):
                gameboard[j][k] = str(laser)
            elif int(sqr) != int(laser):
                gameboard[j][k] = str(CROSS)
        #return gameboard


def getinput():
    filename = "input.txt"
    inputfile = open(filename, "r")
    size = int(next(inputfile))
    gameboard = []
    for line in inputfile:
            gameboard.append([x for x in line[:size]])
    return gameboard


def output(x, y, gameboard):
    filename = "output.txt"
    outputfile = open(filename, "w")
    #for i in gameboard:
     #   outputfile.write(str(i) + "\n")

    outputfile.write(str(x) + " " + str(y))


def lasers(gameboard, x, y, mine):
    if mine:
        laser = MINE
    else:
        laser = NMES

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == j and i == 0:
                continue
            else:
                directions(gameboard, i, j, laser, x, y)
    return gameboard


def putinlasers(gameboard):
    length = len(gameboard)
    for i in range(0,length):
        for j in range(0,length):
            sqr = gameboard[i][j]
            if int(sqr) == int(ME):
                gameboard = lasers(gameboard, i, j, True)
            elif int(sqr) == int(ENEMY):
                gameboard = lasers(gameboard, i, j, False)
            #elif sqr == 0:  add to map
    return(gameboard)


def minvalue(gameboard, turn, alpha, beta):
    value = float(len(gameboard)*len(gameboard))
    length = len(gameboard)
    terminated = True
    for row in range(0,length):
        for col in range(0,length):
            if int(gameboard[row][col]) == 0:
                terminated = False
                temp = [x[:] for x in gameboard]
                temp[row][col] = ENEMY
                lasers(temp, row, col, False)
                value = min(value, float(maxvalue(list(temp), turn+1, alpha, beta)))
                if float(value) <= float(alpha):
                    return value
                beta = min(float(beta), float(value))

                #if value == float(len(gameboard)*len(gameboard)):
                 #   if turn < LIMIT:
                  #      value = maxvalue(list(temp), turn + 1)
                   # else:
                    #    value = score(temp)
                #else:
                    #if turn < LIMIT:
                     #   value = min(value, maxvalue(list(temp), turn + 1))
                    #else:
                     #   value = min(value, score(temp))
    if terminated:
        return score(gameboard)
    else:
        return value


def maxvalue(gameboard, turn, alpha, beta):
    if turn >= LIMIT:
        return score(gameboard)
    value = float(len(gameboard)*len(gameboard)*-1)
    length = len(gameboard)
    terminated = True
    for row in range(0,length):
        for col in range(0,length):
            if int(gameboard[row][col]) == 0:
                temp = [x[:] for x in gameboard]
                terminated = False
                temp[row][col] = ME
                lasers(temp, row, col, True)
                value = max(float(value), float(minvalue(list(temp), turn, alpha, beta)))
                #print (score(gameboard))
                if float(value) >= float(beta):
                    return value
                alpha = max(float(alpha), float(value))
                #if value == float(len(gameboard)*len(gameboard)):
                 #   value = minvalue(list(temp), turn)
                #else:
                 #   value = max(value, minvalue(list(temp), turn))
    if terminated:
        return score(gameboard)
    else:
        return value


def minmax(gameboard):
    x = -1
    y = -1
    value = float(len(gameboard)*len(gameboard))*-1
    length = len(gameboard)
    alpha = float(len(gameboard)*len(gameboard)*-1)
    beta = float(len(gameboard)*len(gameboard))
    for row in range(0, length):
        for col in range(0, length):
            if int(gameboard[row][col]) == 0:
                temp = putinlasers(getinput())
                temp[row][col] = ME
                lasers(temp, row, col, True)
                tempval = minvalue(temp, 0, alpha, beta)
                if tempval > value:
                    value = tempval
                    x = row
                    y = col
                alpha = max(alpha, value)
    output(x, y, gameboard)


minmax(putinlasers(getinput()))


