# -*- coding: utf-8 *-*

from random import random, choice, Random
import datetime
import threading
import time
import re

from nibbles.client.aiimps.simon.serverengine import *
from nibbles.client.aiimps.simon.ai import AI
from nibbles.client.aiimps.simon.matrixoperations import *

class DarwinDevice(threading.Thread):
    """Class that controls world population, evolution and the engine."""
    def __init__(self):
        """Creates a new darwin device. If filename is set, create first
            population from the content of the given file.
            Arguments:
                filename -- (string) name of the file from which nibbles
                            are loaded. The file has to be in the given
                            format (see simon.ai.AI.genometostring())."""
        threading.Thread.__init__(self)
        self.enginerunning = threading.Condition()
        self.lock = threading.RLock()
        self.infofilename = str(datetime.datetime.now()) + ".txt"

        # settings of the darwin device
        # The maximum population
        self.maxpopulation = 30
        # The number of nibbles that survive selection process
        self.minsurvivors = 15
        # Variables used by matrixoperations.mutatematrix()
        self.mutationchance = 0.5
        self.mutationrange = (-10, 10)
        # Number of simulation cycles
        self.lifecycles = 100
        # Number of rounds to be computed by engine
        self.lifecycleduration = 1000
        # Settings for the engine.
        self.fieldspernibble = 1
        self.foodpernibble = 1
        self.turntimeout = 10
        # List that holds all nibbles
        self.population = []
        # Dictionary that holds id -> nibble pairs.
        self.nibbleids = {}

        self.engine = None
        # tuple which holds data recieved from the engine
        self.data = None

    def run(self):
        print "Began training..."
        self.infofile = open(self.infofilename, "w")
        for i in range(0, self.lifecycles):
            self.starttime = datetime.datetime.now()
            self.engine = Engine(Random())
            self.engine.setcmp(self)
            self.engine.setfieldspernibble(self.fieldspernibble)
            self.engine.setfoodpernibble(self.foodpernibble)
            self.engine.setrounds(self.lifecycleduration)
            self.engine.setturntimeout(self.turntimeout)
            # Set up population
            self.repopulate()
            self.registernibbles()
            # Run the engine
            self.engine.setgamestart(datetime.datetime.now())
            time.sleep(0.1)
            while self.engine.getgamestatus() == RUNNING:
                if self.data is not None:
                    self.lock.acquire()

                    move = self.nibbleids[self.data[0]].think(
                        self.data[1], self.data[2])
                    self.engine.execturn(self.data[0], move)

                    self.lock.release()
            # Lifecycle ended
            self.selectbestnibbles()
            self.savelifecycle(i)
            print "Lifecycle %d/%d done (%s)." % (i + 1,
                  self.lifecycles, datetime.datetime.now() - self.starttime)
        self.infofile.flush()
        self.infofile.close()
        print "Training DONE."

    def send(self, nibbleid, view, energy, end=False):
        """Implementation of interface to engine. It receives data
            from the engine and saves them."""
        self.lock.acquire()
        if end is False:
            self.data = (nibbleid, view, energy, end)
        self.lock.release()

    def mutatenibble(self, nibble):
        """Takes a nibble and mutates its genome.
            Arguments:
                nibble -- (simon.ai) Instance of a nibble ai."""
        for k in nibble.genome.keys():
            mutatematrix(nibble.genome[k], self.mutationchance,
                self.mutationrange)

    def selectbestnibbles(self):
        energydict = {}
        k = energydict.keys()
        # Arrange nibbles by their energy.
        for n in self.population:
            # If no other nibble with same energy is saved, create new list
            if n.energy not in k:
                energydict[n.energy] = []
                k = energydict.keys()
            # Append nibble to the list with same energy.
            energydict[n.energy].append(n)

        # Now take the nibbles with the best energy until
        # population is restored.
        self.population = []
        keys = energydict.keys()
        # Remove zero energy.
        if 0 in keys:
            keys.remove(0)

        # Take the best nibbles and save them back to the population.
        while (len(self.population) < self.minsurvivors
              and len(keys) > 0):
            maxkey = max(keys)
            for nibble in energydict[maxkey]:
                self.population.append(nibble)
            keys.remove(maxkey)

    def reproduce(self, n1, n2):
        """Takes a mother and father nibble and recombines their genomes.
            Arguments:
                n1, n2 -- (simon.ai) Instances of nibble ais.
            Return:
                simon.ai instance which is the children of n1 and n2."""
        child = AI()
        for k in child.genome.keys():
            # Either take genome of mother or father
            if random() < 0.5:
                child.genome[k] = n1.genome[k]
            else:
                child.genome[k] = n2.genome[k]
        return child

    def repopulate(self):
        """Creates nibbles until the maximum population is reached."""
        # Create population for the first time
        if len(self.population) == 0:
            while len(self.population) < self.maxpopulation:
                nibble = AI()
                self.mutatenibble(nibble)
                self.population.append(nibble)
        # Repopulate world from existing population.
        else:
            while len(self.population) < self.maxpopulation:
                n1 = choice(self.population)
                n2 = choice(self.population)
                nibble = self.reproduce(n1, n2)
                self.mutatenibble(nibble)
                self.population.append(nibble)

    def registernibbles(self):
        """This function registers all nibbles of population to the engine."""
        self.nibbleids = {}
        for n in self.population:
            newid = self.engine.register()
            self.nibbleids[newid] = n

    def savelifecycle(self, number):
        """Saves information about the lifecycle to a file.
            Arguments:
                number -- (int) The number of last lifecycle."""
        self.infofile.write("Information after lifecycle %s:\n" % (number + 1))
        for n in self.population:
            self.infofile.writelines("   AI with %s HP:\n" % n.energy)
            text = n.genometostring()
            self.infofile.writelines(text + "\n")
