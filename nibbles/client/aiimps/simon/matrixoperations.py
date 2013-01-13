# -*- coding: utf-8 *-*

# Following functions are special purpose helper functions.
# Very specific implementations!

from random import randrange, random


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
    offset = (destpos[0] - 2, destpos[1] - 2)
#    print "offset: %d/%d" % (offset[0], offset[1])
    # x and y are the coordinates on src.
    for x in range(0, 5):
        for y in range(0, 5):
#            print "beeing at %d/%d" % (x, y)
            srcval = src[x][y]
#            print "srcvalue: %d" % srcval
            (destx, desty) = (x + offset[0], y + offset[1])
#            print "destcoord: %d/%d" % (destx, desty)
            if(0 <= destx <= 4 and 0 <= desty <= 4):
                destval = dest[destx][desty]
#                print "destval: %d" % destval
                dest[destx][desty] = destval + srcval
#                print "new destval: %d" % (dest[destx][desty])


#def tuplesum(t1, t2):
    #"""Summates two tuples: (x, y) + (a, b) = (x+a, y+b)
        #Arguments:
            #t1, t2 -- (tuple) Should be tuples of length 2 and contain
                      #only numbers.
        #Return:
            #Touple which contains the result."""
    #return (t1[0] + t2[0], t1[1] + t2[1])

def mutatematrix(dest, mutationchance=1.0, mutationrange=(-1, 1)):
    """This function "mutates" a given 2d-list by adding random
        numbers between -1 and 1 to each element.
        Arguments:
            dest -- (iterable) A 5x5 list that only contains numbers.
            mutationchance -- (float) Specifies the chance with which
                              one element of the matrix mutates.
            mutationrange -- (tuple(lr, hr)) Tuple which contains lower and
                             upper boundaries of the mutation."""
    #print "before mutation: %s" % dest
    for x in xrange(0, 2):
        for y in xrange(0, 2):
            mutation = 0
            if random() <= mutationchance:
                mutation = randrange(mutationrange[0], mutationrange[1])
                dest[x][y] += mutation
                dest[-x-1][y] += mutation
                dest[x][-y-1] += mutation
                dest[-x-1][-y-1] += mutation

    # Hardcoded mutation for the middle lines to avoid redundancy.
    if random() <= mutationchance:
        mutation = randrange(mutationrange[0], mutationrange[1])
        dest[0][2] += mutation
        dest[2][0] += mutation
        dest[2][4] += mutation
        dest[4][2] += mutation

    if random() <= mutationchance:
        mutation = randrange(mutationrange[0], mutationrange[1])
        dest[2][1] += mutation
        dest[1][2] += mutation
        dest[2][3] += mutation
        dest[3][2] += mutation

    if random() <= mutationchance:
        mutation = randrange(mutationrange[0], mutationrange[1])
        dest[2][2] += mutation
    #print "after mutation: %s" % dest

   # matrixintersection(mutationmatrix, dest, (2, 2))
            #dest[x][y] = round(dest[x][y], 2)


def copymatrix(m):
    """Copies a given matrix.
        Arguments:
            m -- (iterable) the matrix to copy
        Returns:
            newmatrix -- (iterable) copy of m"""
    newmatrix = []
    linenumber = 0
    for line in m:
        newmatrix.append([])
        for entry in line:
            newmatrix[linenumber].append(entry)
        linenumber += 1
    return newmatrix

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

