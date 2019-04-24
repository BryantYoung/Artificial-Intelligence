import time

def loc(o, n):
    return (o - 1) * N + n - 1


def left(l):
    e = P * boardVals[spaces[l][0]]
    e += p * boardVals[spaces[l][1]]
    e += p * boardVals[spaces[l][2]]
    return e


def right(l):
    e = P * boardVals[spaces[l][3]]
    e += p * boardVals[spaces[l][4]]
    e += p * boardVals[spaces[l][5]]
    return e


def down(l):
    e = P * boardVals[spaces[l][6]]
    e += p * boardVals[spaces[l][2]]
    e += p * boardVals[spaces[l][5]]
    return e


def up(l):
    e = P * boardVals[spaces[l][7]]
    e += p * boardVals[spaces[l][4]]
    e += p * boardVals[spaces[l][1]]
    return e


def utility(l):
    return max(left(l), right(l), up(l), down(l))


def iterate():
    while True:
        delta = 0
        global boardVals
        temp = []
        for l in range(N * N):
            if board[l] == "X":
                temp.append(R + Y * utility(l))
                if abs(temp[l] - boardVals[l]) > delta:
                    delta = abs(temp[l] - boardVals[l])
            elif board[l] == "E":
                temp.append(boardVals[l])
            else:
                temp.append("N")
        boardVals = temp[:]
        if delta <= .001 or time.time() - start >= 28:
            break


def getspaces():
    temp = []
    for l in range(E):
        mylist = []
        if l % N == 0 or board[l - 1] == "N":
            mylist.append(l)
        else:
            mylist.append(l - 1)
        if l % N == 0 or l - 1 - N < 0 or board[l - 1 - N] == "N":
            mylist.append(l)
        else:
            mylist.append(l - 1 - N)
        if l % N == 0 or l - 1 + N >= N * N or board[l - 1 + N] == "N":
            mylist.append(l)
        else:
            mylist.append(l - 1 + N)
        if l % N == N - 1 or board[l + 1] == "N":
            mylist.append(l)
        else:
            mylist.append(l + 1)
        if l % N == N - 1 or l + 1 - N < 0 or board[l + 1 - N] == "N":
            mylist.append(l)
        else:
            mylist.append(l + 1 - N)
        if l % N == N - 1 or l + 1 + N >= E or board[l + 1 + N] == "N":
            mylist.append(l)
        else:
            mylist.append(l + 1 + N)
        if l + N >= E or board[l + N] == "N":
            mylist.append(l)
        else:
            mylist.append(l+N)
        if l - N < 0 or board[l - N] == "N":
            mylist.append(l)
        else:
            mylist.append(l - N)
        temp.append(mylist)
    return temp


start = time.time()

filename = "input.txt"
inputfile = open(filename, "r")
N = int(inputfile.next())
E = N * N
board = ["X" for i in range(N * N)]
M = int(inputfile.next())

for m in range(0, M):
    line = inputfile.next()
    x = int(line.split(",")[0])
    y = int(line.split(",")[1])
    board[loc(x, y)] = "N"
T = int(inputfile.next())
boardVals = [0 for i in range(N * N)]

for t in range(0, T):
    line = inputfile.next()
    x = int(line.split(",")[0])
    y = int(line.split(",")[1])
    v = float(line.split(",")[2])
    board[loc(x, y)] = "E"
    boardVals[loc(x, y)] = v

P = float(inputfile.next())
p = (1-P)/2
R = float(inputfile.next())
Y = float(inputfile.next())

spaces = getspaces()
iterate()

for i in range(N * N):
    if board[i] == "X":
        x = utility(i)
        if x == up(i):
            board[i] = "U"
        if x == down(i):
            board[i] = "D"
        if x == left(i):
            board[i] = "L"
        if x == right(i):
            board[i] = "R"

outputstr = ""
for i in range(N * N):
    if i % N != N - 1:
        outputstr += board[i] + ","
    else:
        outputstr += board[i] + "\n"

filename = "output.txt"
with open(filename, "w") as f:
    f.write(outputstr)
