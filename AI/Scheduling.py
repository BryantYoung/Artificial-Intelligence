def getinput():
    filename = "input.txt"
    inputfile = open(filename, "r")
    airport = Airport(inputfile.next().split())



    airport.numplanes = inputfile.next().split()[0]
    count = 0

    for line in inputfile:
        airport.planes.append(Plane(line.split(),count))
        count = count + 1
    return airport
    #size = int(next(inputfile))
    #gameboard = []
    #for line in inputfile:
    #       gameboard.append([x for x in line[:size]])
    #return gameboard

# contains 5 positive integers,  R M S O C , separated by spaces.
# R is the maximum number of minutes that this plane can keep hovering based on its remaining fuel.
# M is the number of minutes it takes the plane to reach its gate after initiating its landing.
# S is the number of minutes it takes the gate crew to serve the plane
#   (unload passengers, refuel, board new passengers, etc.).
# O is the number of minutes it takes the plane to complete takeoff after leaving the gate.
# C is the maximum number of minutes that a plane can stay at the gate before passengers start complaining.


class Plane:

    dependents = []
    restrictions = []

    def __init__(self, vals, order):
        self.R = int(vals[0])
        self.M = int(vals[1])
        self.S = int(vals[2])
        self.O = int(vals[3])
        self.C = int(vals[4])
        self.order = int(order)
        self.time = int(self.R)
        self.A = 0
        self.B = 0
        self.E = self.M + self.S
        self.values = vals[:]

    def totaltime(self):
        return self.M + self.S + self.O


# contains 3 integers,  L G T , separated by spaces.
# The first is the maximum number of planes that can be landing at the same time.
# The second is the number of boarding gates in the airport, each capable of serving only a single plane.
# The third is the maximum number of planes that can be taking off at the same time.
# <NUMBER OF PLANES>:  contains one integer  N specifying the number of planes.
# The next  N lines will provide the information about each of the planes currently hovering over the airport.


class Airport:
    planes = []
    def __init__(self, vals):
        self.L = int(vals[0])
        self.G = int(vals[1])
        self.T = int(vals[2])


class State:
    def __init__(self, *args):
        if len(args) > 0:
            x = args[0]
            self.inAir = PriorityQueue()
            self.landing = PriorityQueue()
            self.inGate = PriorityQueue()
            self.readytotakeoff = PriorityQueue()
            self.takingoff = PriorityQueue()
            self.end = x.end[:]
            self.airport = x.airport
            self.time = 0
        else:
            self.inAir = PriorityQueue()
            self.landing = PriorityQueue()
            self.inGate = PriorityQueue()
            self.readytotakeoff = PriorityQueue()
            self.takingoff = PriorityQueue()
            self.end = OrderPriorityQueue()
            self.airport = getinput()
            self.time = 0

    def output(self):
        outputstr = ""
        for x in self.airport.planes:
            outputstr = outputstr + str(x.A) + " " + str(x.B)+"\n"
        filename = "output.txt"
        outputfile = open(filename, "w")
        outputfile.write(outputstr)


def gone(state):
    while state.takingoff.length() > 0 and int(state.takingoff.peek().time) <= int(state.time):
        x = state.takingoff.pop()
        state.end.push(x)


def ready(state):
    while state.inGate.length() > 0 and state.inGate.peek().time <= state.time:
            x = state.inGate.pop()
            x.time = x.time - x.S + x.C
            state.readytotakeoff.push(x)


def descending(state):
    while state.landing.length() > 0 and state.landing.peek().time <= state.time:
        x = state.landing.pop()
        x.time = state.time + x.S
        state.inGate.push(x)


def valid(state):
    a = state.airport
    #if there are more airplanes in gate then available gates
    if a.G < len(state.readytotakeoff) + len(state.inGate):
       return False
    #if customers are mad
    for x in state.readytotakeoff:
        if x.time <= state.time:
            return False
    #if planes crash
    for x in state.inAir:
        if x.time <= state.time:
            return False
    return True


class PriorityQueue(object):
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

        # for checking if the queue is empty

    def isEmpty(self):
        return len(self.queue) == []

        # for inserting an element in the queue
    def length(self):
        return len(self.queue)

    def push(self, data):
        self.queue.append(data)

        # for popping an element based on Priority

    def pop(self):
        try:
            minimum = 0
            for i in range(len(self.queue)):
                if self.queue[i].time < self.queue[minimum].time:
                    minimum = i
            item = self.queue[minimum]
            del self.queue[minimum]
            return item
        except IndexError:
            exit()

    def peek(self):
        try:
            minimum = 0
            for i in range(len(self.queue)):
                if self.queue[i].time < self.queue[minimum].time:
                    minimum = i
            item = self.queue[minimum]
            return item
        except IndexError:
            exit()


class OrderPriorityQueue(object):
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

        # for checking if the queue is empty

    def isEmpty(self):
        return len(self.queue) == []

        # for inserting an element in the queue
    def length(self):
        return len(self.queue)

    def push(self, data):
        self.queue.append(data)

        # for popping an element based on Priority

    def pop(self):
        try:
            minimum = 0
            for i in range(len(self.queue)):
                if int(self.queue[i].order) < int(self.queue[minimum].order):
                    minimum = i
            item = self.queue[minimum]
            del self.queue[minimum]
            return item
        except IndexError:
            exit()

    def peek(self):
        try:
            minimum = 0
            for i in range(len(self.queue)):
                if int(self.queue[i].order) < int(self.queue[minimum].order):
                    minimum = i
            item = self.queue[minimum]
            return item
        except IndexError:
            exit()


def TakeOff(state):
    while state.takingoff.length() < state.airport.T and state.readytotakeoff.length() > 0:
        temp = state.readytotakeoff.pop()
        temp.B = state.time
        temp.time = temp.B + temp.O
        state.takingoff.push(temp)


def takeOffInTime(plane,state):
    if plane.R == state.time:
        return True
    else:
        onRunWay = 0
        mytime = plane.M + state.time + plane.S
        gone = []
        for x in range(state.airport.T - state.takingoff.length()):
            gone.append(state.time)
        for x in state.takingoff.queue:
            if int(state.time) + int(plane.M) > int(x.time):
                gone.append(x.time)
        templist = PriorityQueue()
        templist.queue = state.readytotakeoff.queue[:]
        planeCopy = Plane(plane.values, plane.order)
        planeCopy.time = mytime
        templist.push(planeCopy)
        for x in state.inGate.queue:
            if x.time < mytime:
                templist.push(x)
        for x in state.landing.queue:
            if x.time + x.S < mytime:
                y = Plane(x.values, x.order)
                y.time = x.time + y.S
                templist.push(y)
        for x in gone:
            if templist.length() > 0:
                temp = templist.pop()
                if temp.order == plane.order:
                    return True
                nextTime = max(int(temp.O) + int(x), int(temp.O) + int(temp.time))
                if nextTime <= (int(state.time) + int(plane.M) + int(plane.C)):
                    gone.append(nextTime)

        #mytime = plane.M + state.time + plane.C
        #for x in state.landing.queue:
        #    if x.time + x.C + x.O > mytime:
        #        onRunWay += 1
        #for x in state.inGate.queue:
        #    if x.time + x.C + x.O > mytime:
        #       onRunWay += 1
        #for x in state.readytotakeoff.queue:
        #    if x.time + x.O > mytime:
        #        onRunWay += 1
        return False


def canland(plane, state):
    ingatealso = 0
    if int(plane.time) == int(state.time):
        return True
    for x in state.landing.queue:
        if ((int(state.time) + int(plane.M) < int(x.time)) and (state.time + plane.M + plane.S > x.time)) or \
                ((int(state.time) + int(plane.M) > int(x.time)) and (state.time + plane.M < x.time + x.S)) or \
                    (int(state.time) + int(plane.M) == int(x.time)): #plane lands after x
            ingatealso += 1
    for x in state.inGate.queue:
        if int(state.time) + int(plane.M) < int(x.time):
            ingatealso += 1
    if state.airport.T == state.takingoff.length():
        gone = []
        for x in state.takingoff.queue:
            if int(state.time) + int(plane.M) > int(x.time):
                gone.append(x.time)
        templist = PriorityQueue()
        templist.queue = state.readytotakeoff.queue[:]
        for x in gone:
            if templist.length() > 0:
                temp = templist.pop()
                if temp.O + int(x) < int(state.time) + int(plane.M):
                    gone.append(temp.O + x)
            else:
                break
        ingatealso += templist.length()
    return (state.landing.length() < state.airport.L) and (ingatealso < state.airport.G) and takeOffInTime(plane, state)


def Land(state):
    while state.inAir.length() > 0 and canland(state.inAir.peek(), state):
        temp = state.inAir.pop()
        temp.A = state.time
        temp.time = temp.A + temp.M
        state.landing.push(temp)


def SchedulePlanes():
    currentState = State()
    airport = currentState.airport
    if airport.L >= airport.numplanes and airport.T >= airport.numplanes and airport.G >= airport.numplanes:
        simpleCase(currentState)
        currentState.output()
    else:

        for x in currentState.airport.planes:
            currentState.inAir.push(x)

        while currentState.takingoff.length() + currentState.end.length() < int(airport.numplanes):
            TakeOff(currentState)
            Land(currentState)
            currentState.time += 1
            gone(currentState)
            ready(currentState)
            descending(currentState)
        currentState.output()


def simpleCase(currentState):
    planes = currentState.airport.planes
    for plane in planes:
        plane.A = 0
        plane.B = int(plane.M) + int(plane.S)


SchedulePlanes()