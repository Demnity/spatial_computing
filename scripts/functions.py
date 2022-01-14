import numpy as np
from scipy.interpolate import RegularGridInterpolator
import topogenesis as tg

def interpolate(info_lowres, base_highres):
    # line spaces
    x_space = np.linspace(info_lowres.minbound[0], info_lowres.maxbound[0],info_lowres.shape[0])
    y_space = np.linspace(info_lowres.minbound[1], info_lowres.maxbound[1],info_lowres.shape[1])
    z_space = np.linspace(info_lowres.minbound[2], info_lowres.maxbound[2],info_lowres.shape[2])

    # interpolation function
    interpolating_function = RegularGridInterpolator((x_space, y_space, z_space), info_lowres, bounds_error=False, fill_value=None)

    # high_res lattice
    envelope_lattice = base_highres + 1
    
    # sample points
    sample_points = envelope_lattice.centroids
    #print(envelope_lattice)
    # interpolation
    interpolated_values = interpolating_function(sample_points)

    # lattice construction
    info_highres = tg.to_lattice(interpolated_values.reshape(base_highres.shape), base_highres)

    # nulling the unavailable cells
    info_highres *= base_highres

    return info_highres

def squareness(square_weight, free_neighs, a_eval):
    free_neighs_count = []
    for free_neigh in free_neighs:
        free_neighs_count.append(free_neighs.count(free_neigh))
    a_weighted_square = np.array(free_neighs_count) ** square_weight
    a_eval *= a_weighted_square

def normalize_excel(excel):
    excel.iloc[:, 1:] = excel.iloc[:, 1:].div(excel.iloc[:, 1:].sum(axis=1), axis=0)
    excel.iloc[:, 1:] = excel.iloc[:, 1:].fillna(0)

def breath_first_traversal(starting_locs, envelope_lattice):
    # creating neighborhood definition
    stencil = tg.create_stencil("von_neumann", 1, 1)
    # setting the center to zero
    stencil.set_index([0,0,0], 0)
    # retrieve the neighbour list of each cell
    neighs = starting_locs.find_neighbours(stencil)

    # set the maximum distance to sum of the size of the lattice in all dimensions.
    max_dist = np.sum(starting_locs.shape)

    # initialize the street network distance lattice with all the street cells as 0, and all other cells as maximum distance possible
    mn_dist_lattice = 1 - starting_locs
    mn_dist_lattice[mn_dist_lattice==1] = max_dist

    # flatten the distance lattice for easy access
    mn_dist_lattice_flat = mn_dist_lattice.flatten()

    # flatten the envelope lattice
    env_lat_flat = envelope_lattice.flatten()

    # main loop for breath-first traversal
    for i in range(1, max_dist):
        # find the neighbours of the previous step
        next_step = neighs[mn_dist_lattice_flat == i - 1]
        # find the unique neighbours
        next_unq_step = np.unique(next_step.flatten())
        # check if the neighbours of the next step are inside the envelope
        validity_condition = env_lat_flat[next_unq_step]
        # select the valid neighbours
        next_valid_step = next_unq_step[validity_condition]
        # make a copy of the lattice to prevent overwriting in the memory
        mn_nex_dist_lattice_flat = np.copy(mn_dist_lattice_flat)
        # set the next step cells to the current distance
        mn_nex_dist_lattice_flat[next_valid_step] = i
        # find the minimum of the current distance and previous distances to avoid overwriting previous steps
        mn_dist_lattice_flat = np.minimum(mn_dist_lattice_flat, mn_nex_dist_lattice_flat)
        
        # check how many of the cells have not been traversed yet
        filled_check = mn_dist_lattice_flat * env_lat_flat == max_dist
        # if all the cells have been traversed, break the loop
        if filled_check.sum() == 0:
            break

    # reshape and construct a lattice from the street network distance list
    mn_dist_lattice = mn_dist_lattice_flat.reshape(mn_dist_lattice.shape)
    return mn_dist_lattice