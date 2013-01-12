
import math

def tangential(x):
    """Anti-symmetrische sigmoide Aktivierungsfunktion."""
    return math.tanh(x)

class KNN(object):

    def __init__(self):
        self.values = {'.' : 0 , '*' : 1 , '=' : 12 , '>' : -1 , '<' : 6}
        self.eingabeNeuronen = []
        for i in range(25):
            self.eingabeNeuronen.append(Neuron())

        self.ausgabeNeuronen = []
        for i in range(25):
            self.ausgabeNeuronen.append(Neuron())
            a1 = Axon()
            a1.neuron = self.eingabeNeuronen[i]
            self.ausgabeNeuronen[i].axone.append(a1)

    def think(self, env, energy):
        eingabewerte = []
        for x in range(0, 5):
            for y in range(0, 5):
                eingabewerte.append(self.values.get(env[x*5+y]))
        eingabewerte[12] = 0.5

        for i in range(len(eingabewerte)):
            self.eingabeNeuronen[i].wert = eingabewerte[i]

        for ausgabeNeuron in self.ausgabeNeuronen:
            ausgabeNeuron.berechne()

        # Alle Werte der Ausgabeneuronen als Liste zurueckgeben
        return [neuron.wert for neuron in self.ausgabeNeuronen]

class Axon(object):
    """ein kpnstliches Axon, das eine Kante in einem KNN darstellt."""
    def __init__(self):
        self.gewicht = 1.0
        self.neuron = None

class Neuron(object):
    """Ein kuenstliches Neuron, das einen Knoten in einem KNN darstellt."""
    def __init__(self, wert=0.0):
        self.wert = wert
        self.axone = []  # Kanten zu anderen (Eingabe-)Neuronen
        self.aktivierung = tangential

    def berechne(self):
        # Aufsummieren
        summe = 0.0
        for axon in self.axone:
            summe += axon.gewicht*axon.neuron.wert

        # Aktivierungsfunkrion anwenden
        self.wert = self.aktivierung(summe)

def trainiere(knn, trainingsdatensatz, lernrate=0.1):
    # Alle Trainingsdaten durchspielen
    for eingabedaten, ausgabeErwartet in trainingsdatensatz:
        # Ergebnis des KNN berechnen
        ausgabeBerechnet = knn.berechne(eingabedaten)
        # Netz veraendern
        for i, neuron in enumerate(knn.ausgabeNeuronen):
            differenz = ausgabeErwartet[i] - ausgabeBerechnet[i]
            # Gewichte der anliegenden Axone anpassen;
            # die Differenz bestimmt, in welche Richtung
            for axon in neuron.axone:
                axon.gewicht += lernrate*differenz*axon.neuron.wert

if __name__ == '__main__':

    knn = KNN()

    boardtestview2 = ">......<....a.....=....>*"
    energy = "30"
    print knn.think(boardtestview2, energy)


    """
    # Logisches Oder
    trainingsdatensatz = [
        (0.0, 0.0, 0.0),
        (0.0, 1.0, 1.0),
        (1.0, 0.0, 1.0),
        (1.0, 1.0, 1.0),
    ]


    # Logisches Und
    trainingsdatensatz = [
        ([0.0, 0.0], [0.0]),
        ([0.0, 1.0], [0.0]),
        ([1.0, 0.0], [0.0]),
        ([1.0, 1.0], [1.0]),
        ]



    print "Vor dem Training:"
    for eingabewerte, ausgabewerte in trainingsdatensatz:
        knn.think(eingabewerte, "30")
        print round(knn.ausgabeNeuronen[0].wert), ausgabewerte[0]

    # Training
    #for i in range(100):
        #trainiere(knn, trainingsdatensatz)

    print "Nach dem Training:"
    for eingabewerte, ausgabewerte in trainingsdatensatz:
        knn.think(eingabewerte, "30")
        print round(knn.ausgabeNeuronen[0].wert), ausgabewerte[0]

    """
