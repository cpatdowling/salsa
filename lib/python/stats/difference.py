#Chase Dowling, chase.dowling@pnnl.gov, June 2014
#options for side are left and right, and adds a 0

def difference(inVector, side=False):
    for i in range(len(inVector)):
        if i == len(inVector) - 1:
            break
        inVector[i] = inVector[i + 1] - inVector[i]
    if side == "left":
        inVector = [0] + inVector
    if side == "right":
        inVector = inVector + [0]
    return(inVector)

