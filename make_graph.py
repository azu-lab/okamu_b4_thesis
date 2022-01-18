from matplotlib import pyplot
from numpy import average
from sys import argv
import pandas
import numpy
import seaborn

if len(argv) <= 3:
    exit()

if argv[1] == "n":
    xlabel = ["n=1-8", "n=1-16", "n=9-16"]
    x = [1,2,3]
elif argv[1] == "p":
    xlabel = ["p=3", "p=4", "p=5", "p=6"]
    x = [1,2,3,4]
else:
    xlabel = ["node=20", "node=40", "node=60", "node=80", "node=100"]
    x = [1,2,3,4,5]

data = pandas.DataFrame({"method": [], "parameter": [], "makespan": []})
#colors = ["#40ff40", "#40c0ff", "#ffc0c0", "#c0ffff"]

methods = argv[3:]

idx = 0
for method in methods:
    for x in xlabel:
        f = open("./DATA/"+x+"_"+method+".txt")
        tmp = f.read().split("\n")
        for i in [int(n) for n in tmp if n != ""]:
            data.loc[str(idx)] = [method, x, i]
            idx += 1

#print(data)
fig = pyplot.figure()

seaborn.boxplot(x="parameter", y="makespan", hue="method", data=data, palette="Blues")

fig.savefig("./Image/"+argv[2]+".png")
fig.savefig("./Image/"+argv[2]+".eps")

#i = 0
#for key, value in y.items():
#    print(key+str(value))
#    pyplot.bar([n-0.15+i*0.3 for n in x], value, width=0.3, color=colors[i], align="center", label=key)
#    i += 1
#pyplot.xticks(x, xlabel)
#pyplot.legend()