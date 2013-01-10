# -*- coding: utf-8 *-*

from random import Random
import datetime
import threading
import time

from nibbles.server.engine import *
from nibbles.client.ai.simon.ai import AI
from nibbles.client.ai.simon.matrixoperations import *
from nibbles.nibblelogger import NibbleStreamLogger


class DarwinDevice(threading.Thread):
    """Class that controls world population, evolution and the engine."""
    def __init__(self):
        threading.Thread.__init__(self)
        self.enginerunning = threading.Condition()
        self.lock = threading.RLock()
        self.logger = NibbleStreamLogger("nibbles.ai.simon.darwindevice")
        self.logger.setLevel(logging.WARNING)
        # settings of the darwin device
        self.maxpopulation = 30
        self.mutationchance = 0.5
        self.lifecycles = 3
        self.lifecycleduration = 10
        self.fieldspernibble = 1
        self.foodpernibble = 1
        self.turntimeout = 10
        # list that holds all nibbles
        self.population = []
        # dictionary that holds id -> nibble pairs.
        self.nibbleids = {}

        self.engine = None
        # tuple which holds data recieved from the engine
        self.data = None

    def run(self):
        for i in range(0, self.lifecycles):
            # Set up new engine
            self.engine = Engine(Random())
            self.engine._logger.setLevel(logging.WARNING)
            self.engine.setcmp(self)
            self.engine.setfieldspernibble(self.fieldspernibble)
            self.engine.setfoodpernibble(self.foodpernibble)
            self.engine.setrounds(self.lifecycleduration)
            self.engine.setturntimeout(self.turntimeout)
            # Set up population
            self.repopulate()
            self.registernibbles()
            # Run the engine
            #td = datetime.timedelta(0, 3)
            self.engine.setgamestart(datetime.datetime.now())
            time.sleep(0.1)

            while self.engine.getgamestatus() == RUNNING:
                if self.data is not None:
                    self.lock.acquire()
                    self.logger.info("Execute ai.think")
                    move = self.nibbleids[self.data[0]].think(
                        self.data[1], self.data[2])
                    self.logger.info("ai wants to move to: %d" % move)
                    self.engine.execturn(self.data[0], move)
                    self.logger.info("Executed ai move. continuing...")
                    self.lock.release()
            self.logger.info("Lifecycle %d ended." % i)
        self.logger.info("All lifecycles ended.")

    def send(self, nibbleid, view, energy, end=False):
        """Implementation of interface to engine. It receives data
            from the engine and saves them."""
        self.lock.acquire()
        if end is False:
            self.data = (nibbleid, view, energy, end)
        self.lock.release()
            #time.sleep(1)
            #move = self.nibbleids[nibbleid].think(view, energy)
            #self.engine.execturn(nibbleid, move)
        #try:
            #self.enginerunning.notifyAll()
        #except:
            #pass

    def mutatenibble(self, nibble):
        """Takes a nibble and mutates its genome.
            Arguments:
                nibble -- (simon.ai) Instance of a nibble ai."""
        for k in nibble.genome.keys():
            mutatematrix(nibble.genome[k], self.mutationchance)

    def reproduce(self, n1, n2):
        """Takes a mother and father nibble and recombines their genomes.
            Arguments:
                n1, n2 -- (simon.ai) Instances of nibble ais.
            Return:
                simon.ai instance which is the children of n1 and n2."""
        child = AI()
        for k in child.genome.keys():
            child.genome[k] = recombinematrcices(n1[k], n2[k])
            self.mutatenibble(child)
        return child

    def repopulate(self):
        """Creates nibbles until the maximum population is reached."""
        if len(self.population) == 0:
            while len(self.population) <= self.maxpopulation:
                nibble = AI()
                self.mutatenibble(nibble)
                self.population.append(nibble)
        else:
            while len(self.population) <= self.maxpopulation:
                n1 = random.choice(self.population)
                n2 = random.choice(self.population)
                self.population.append(reproduce(n1, n2))

    def registernibbles(self):
        """This function registers all nibbles of population to the engine."""
        self.nibbleids = {}
        for n in self.population:
            newid = self.engine.register()
            self.nibbleids[newid] = n
