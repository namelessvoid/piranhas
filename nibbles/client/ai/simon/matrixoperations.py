# -*- coding: utf-8 *-*

# Following functions are special purpose helper functions.
# Very specific implementations!

from random import randrange, choice, random


def matrixintersection(src, dest, destpos):
    """This function takes two 2d-lists instances src and dest.
        It add's the integers on src to the integers on dest.
        destpos is the position of the center of src on dest, the offset
        of the center of src to the center of dest.
        Arguments:
            src, dest -- (list) The lists are supposed to be of size 5x5
            and must contain numbers only!
            destpos -- (touple) which holds (x, y) koordinates"""

    # calculate the offset of src relative to the center of dest.
#    print "destpos: %d/%d" % (destpos[0], destpos[1])
    offset = tuplesum((-2, -2), destpos)
#    print "offset: %d/%d" % (offset[0], offset[1])
    # x and y are the coordinates on src.
    for x in range(0, 5):
        for y in range(0, 5):
#            print "beeing at %d/%d" % (x, y)
            srcval = src[x][y]
#            print "srcvalue: %d" % srcval
            (destx, desty) = tuplesum((x, y), offset)
#            print "destcoord: %d/%d" % (destx, desty)
            if(0 <= destx <= 4 and 0 <= desty <= 4):
                destval = dest[destx][desty]
#                print "destval: %d" % destval
                dest[destx][desty] = destval + srcval
#                print "new destval: %d" % (dest[destx][desty])


def tuplesum(t1, t2):
    """This function takes two touples of numbers and adds
        the according elements of both:
        t1 + t2
        Arguments:
            t1, t2 -- (iterable) Have to be of the same length and
                      must contain numbers only!
        Return:
            Touple which contains the result."""
    result = list()
    for i in range(0, len(t1)):
        result.append(t1[i] + t2[i])
    return result


def mutatematrix(dest, mutationchance=1.0, mutationrange=(-1, 1)):
    """This function "mutates" a given 2d-list by adding random
        numbers between -1 and 1 to each element.
        Arguments:
            dest -- (iterable) A 5x5 list that only contains numbers.
            mutationchance -- (float) Specifies the chance with which
                              one element of the matrix mutates.
            mutationrange -- (tuple(lr, hr)) Tuple which contains lower and
                             upper boundaries of the mutation."""
    for x in range(0, 5):
        for y in range(0, 5):
            mutation = 0
            if random() <= mutationchance:
                mutation = randrange(mutationrange[0] * 10,
                            mutationrange[1] * 10) / 10.0
                print mutation
                dest[x][y] += mutation + dest[x][y]
            #dest[x][y] = round(dest[x][y], 2)


#def recombinematrices(m1, m2):
    #"""Takes two matrices and recombines them by randomly choosing one element
        #out of both and setting it as element of a resulting matrix.
        #Arguments:
            #m1, m2 -- (iterable) A 5x5 list that only contains numbers.
        #Return:
            #The resulting matrix."""
    #result = list()
    #for x in range(0, 5):
        #result.append([])
        #for y in range(0, 5):
            #result[x].append(choice((m1[x][y], m2[x][y])))
    #return result

