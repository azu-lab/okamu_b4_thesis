from matplotlib import pyplot
from sys import argv
import pandas
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

methods = argv[3:]

data = pandas.DataFrame({method: [] for method in methods})
#colors = ["#40ff40", "#40c0ff", "#ffc0c0", "#c0ffff"]

idx = 0
for x in xlabel:
    y = []

    for m in [m for m in methods if m != "Equivalence"]:
        f = open("./DATA/"+x+"_"+m+".txt")
        tmp = f.read().split("\n")
        y.append([int(n) for n in tmp if n != ""])

    eva = [0 for m in methods]

    for t in zip(*y):
        t = list(t)
        argmax = [i for i, n in enumerate(t) if min(t) == n]

        if len(argmax) != 1:
            if "Equivalence" in methods:
                eva[-1] += 1
        else:
            eva[argmax[0]] += 1

    data.loc[x] = eva

print(data)

pyplot.figure()

data.plot(y=methods)
data.plot.bar(stacked=True, edgecolor="black", linewidth=1, cmap="Blues")
pyplot.subplots_adjust(bottom=0.2)

pyplot.savefig("./Image/"+argv[2]+".png")
pyplot.savefig("./Image/"+argv[2]+".eps")