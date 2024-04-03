
def solvepart1():
    #read data into 2 dictionaries
    data = fileRead("input.txt")
    global modules
    modules = {"button": ("*", ("broadcaster",)), "rx": ("*", ())}
    global modulesState
    modulesState = {"button": {}}
    for row in data:
        splitRow = row.split(" -> ")
        nameType = splitRow[0]
        destinationsStr = splitRow[1]
        if ("%" in nameType) or ("&" in nameType):
            name = nameType[1:]
            moduleType = nameType[0]
        else:
            name = nameType
            moduleType = "*"
        destinations = tuple(destinationsStr.strip().split(", "))
        modules[name] = (moduleType, destinations)
        modulesState[name] = {}
    for module, data in modules.items():
        for outModule in data[1]:
            if outModule != "rx":
                modulesState[outModule][module] = 0

    # #press button 1000 times
    lowPulses = 0
    highPulses = 0
    for _ in range(1000):
        low, high = pressButton()
        lowPulses += low
        highPulses += high

    print(lowPulses * highPulses)

#propogate signal through modules, breadth-first, updating global modules state as it goes
def pressButton():
    totalLow = 0
    totalHigh = 0
    queue = [("broadcaster",0,"button")]
    while len(queue) > 0:
        currentModule = queue.pop(0)
        moduleName = currentModule[0]
        incomingSignal = currentModule[1]
        prevModule = currentModule[2]
        moduleType = modules[moduleName][0]
        outModules = modules[moduleName][1]

        if incomingSignal == 0: totalLow += 1
        else: totalHigh += 1

        if moduleName == "rx": continue

        if moduleType == "%":
            if incomingSignal == 0:
                state = modulesState[moduleName].get(0, 0)
                state = 1-state
                modulesState[moduleName][0] = state
                for module in outModules:
                    queue.append((module, state, moduleName))
        elif moduleType == "&":
            modulesState[moduleName][prevModule] = incomingSignal
            allHigh = True
            for value in modulesState[moduleName].values():
                if value == 0:
                    allHigh = False
                    break
            if allHigh: outState = 0
            else: outState = 1
            for module in outModules:
                    queue.append((module, outState, moduleName))
        else:
            for module in outModules:
                queue.append((module, incomingSignal, moduleName))

    return totalLow, totalHigh

def fileRead(name):
    data = []
    f = open(name, "r")
    for line in f:
        data.append(line);
    return data

solvepart1()