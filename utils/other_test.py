import random
def sumup():
    list = random.sample(range(1,9), 4)
    comp1 = str(list[0])+str(list[1])
    comp2 = str(list[2])+str(list[3])
    comp3 = str(list[0])+str(list[2])
    comp4 = str(list[1])+str(list[3])
    sum = int(comp1) + int(comp2) + int(comp3) + int(comp4)
    print(list)
    return sum

print(sumup())