from matplotlib import pyplot
from numpy import average
from sys import argv

xlabel = ["50", "100", "150", "200"]
x = [1,2,3,4]
y = {}
colors = ["blue", "red", "green", "yellow"]

if len(argv) == 1:
    exit()

for epifix in argv[1:]:
    y[epifix] = []

for key, value in y.items():
    for i in xlabel:
        f = open("./Tex/"+i+"_"+key+".txt")
        tmp = f.read().split("\n")
        arr = [int(n) for n in tmp if n != ""]
        y[key].append(average(arr))

fig = pyplot.figure()

i = 0
for key, value in y.items():
    print(key+str(value))
    pyplot.bar([n-0.15+i*0.3 for n in x], value, width=0.3, color=colors[i], align="center", label=key)
    i += 1
pyplot.xticks(x, xlabel)
pyplot.legend()

fig.savefig("./output.png")