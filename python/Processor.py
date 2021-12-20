class Processor:
    def __init__(self):
         self._makespan = 0

    def schedule(self, nodes):
        timer = 0

        while(len(nodes) != 0):
            node = nodes.pop(0)
            self._makespan = timer + node

            timer += 1

    def makespan(self):
        return self._makespan