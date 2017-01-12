def CoverHLS(Highlight): #乱序版
    coverd = set()
    NewHL = []
    NewHighlight = []
    for i in Highlight:
        for j in range(i[0],i[1]+1):
            coverd.add(j)
    coverd = sorted(list(coverd))
    NewHL.append(coverd[0])
    LastI = coverd[0]-1
    for i in coverd:
        if LastI != i-1:
            NewHL.append(LastI)
            NewHL.append(i)
        LastI = i
    NewHL.append(coverd[-1])
    for i in range(0,len(NewHL)):
            if i % 2 == 0:
                NewHighlight.append((NewHL[i],NewHL[i+1]))
    return NewHighlight

def CoverHL(Highlight):
    minr = Highlight[0][0]
    maxr = Highlight[0][1]
    coverd = []
    NewHL = []
    NewHighlight = []
    for i,j in Highlight:
        if i<= maxr and i> minr:
            NewHL.append(j)
        else:
            NewHL.append(i)
        minr = i
        maxr = j
    for i in range(0,len(NewHL)):
        if i % 2 == 0:
            NewHighlight.append((NewHL[i],NewHL[i+1]))
    return NewHighlight