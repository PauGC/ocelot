__author__ = 'Sergey Tomin'
#from e_optics import *
from numpy.random import normal
from numpy import abs, append
from ocelot.cpbd.elements import *
import copy


class Errors:
    def __init__(self):
        self.sigma_x = 100e-6
        self.sigma_y = 100e-6

def tgauss(mu = 0, sigma = 1, trunc = 2):
    if sigma == 0:
        return mu
    err = normal(mu, sigma, size = 50)
    err_ok = err[abs(err) < trunc*sigma]
    return err_ok[0]

def create_copy(lattice, nsuperperiods):

    lat_copy_seg = []
    #print "errors: ", len(lattice.sequence)
    for i in xrange(nsuperperiods):

        for n, elem in enumerate(lattice.sequence):
            lat_copy_seg.append(copy.deepcopy(elem))
            if lat_copy_seg[-1].id == None:
                lat_copy_seg[-1].id = lat_copy_seg[-1].type[:2] + "_sp" +str(i)+"_"+str(n)
            else:
                if elem.type != "sextupole":
                    lat_copy_seg[-1].id = lat_copy_seg[-1].id+ "_sp" +str(i)+"_"+str(n)
    #print "errors: ", len(lattice.sequence)
    return MagneticLattice(lat_copy_seg, energy= lattice.energy)

#class Errors:


def errors_seed(lattice, er_list):

    #lat_seq_err = create_copy(lattice, nsuperperiods = nsuperperiods)
    dx = []
    dy = []
    dtilt = []
    the_same = 0
    elem_dx = 0.
    elem_dy = 0.
    elem_dtilt = 0.
    for elem in lattice.sequence:
        elem.dx = 0
        elem.dy = 0
        elem.dtilt = 0
        if elem.type == "quadrupole":
            elem.dx = tgauss(sigma = er_list[elem.type]["offset"])
            elem.dy = tgauss(sigma = er_list[elem.type]["offset"])
            elem.dtilt = tgauss(sigma = er_list[elem.type]["dtilt"])
            if the_same == 1:
                elem.dx = elem_dx
                elem.dy = elem_dy
                elem.dtilt = elem_dtilt
                the_same = 0

            elem_dx = elem.dx
            elem_dy = elem.dy
            elem_dtilt = elem.dtilt

        elif elem.type == "sbend" or elem.type == "rbend" or elem.type == "bend":
            elem.dx = 0
            elem.dy = 0
            if the_same == 1:
                elem.dtilt = elem_dtilt
                the_same = 0
            else:
                elem.dtilt = tgauss(sigma = er_list[elem.type]["dtilt"])

        #elem_dx = elem.dx
        #elem_dy = elem.dy
        #elem_dtilt = elem.dtilt

        dx = append(dx, elem.dx)
        dy = append(dy, elem.dy)
        dtilt = append(dtilt, elem.dtilt)
        if elem.l == 0:
            the_same = 1
        else:
            the_same = 0

    return lattice.update_transfer_maps(), (dx, dy, dtilt)

if __name__ == "__main__":
    for i in range(1):
        rv = tgauss()
        if abs(rv)>2.99:
            print (rv)