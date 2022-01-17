import numpy as np
import trimesh as tm
import topogenesis as tg

def streetview (agn_locs,avail_lattice,street_g,context_mesh):
    # duplicating the ocuupied lattice from the agent growth process
    occupied_lattice = tg.to_lattice(np.copy(avail_lattice), avail_lattice)
    # setting the values of the occupied lattice to 0
    occupied_lattice[occupied_lattice==1]=0

    # retrieving the agent locations
    for i in range(len(agn_locs)):
        for loc in agn_locs[i]:
            occupied_lattice[tuple(loc)]=1

    # create a transformation matrix for each agent location 
    def transformation_matrix (arr):
        return [[1,0,0,int(arr[0])],[0,1,0,int(arr[1])],[0,0,1,int(arr[2])],[0,0,0,1]]


    # collecting center points of agent voxels
    agn_cens = occupied_lattice.centroids_threshold(0)

    # creating a box mesh and transforming it to each centroid of the agent voxels with the transformation matrix above
    meshes = [tm.creation.box(extents=avail_lattice.unit,transform=transformation_matrix(agn_cens[i])) for i in range(len(agn_cens))]
    agent_mesh = tm.util.concatenate(meshes)
    # creating neighborhood definition
    stencil = tg.create_stencil("von_neumann", 1, 1)
    # setting the center to zero
    stencil.set_index([0,0,0], 0)
    stencil.set_index([0,0,1], 0)
    stencil.set_index([0,0,-1], 0)
    stencil.function = tg.sfunc.sum

    # collecting neighbours count for occupied lattice
    occupied_lat_sten=occupied_lattice.apply_stencil(stencil)

    facade_lattice=avail_lattice*0
    # seperating the voxels with neighbours and excluding the occupied agents to retain only facade voxels
    facade_lattice[occupied_lat_sten>0]=1
    facade_lattice[occupied_lattice==1]=0

    # collecting center points of facade voxels
    fcd_cens = facade_lattice.centroids_threshold(0)

    # inputting the street grid


    # combining the surrounding building meshes with the agent meshes
    context_mesh_complete=context_mesh+agent_mesh

    # Extracting the vector between the facade centroid and the street points. 
    ray_dir=[]
    run_count=0
    for i in range(len(fcd_cens)):
        for f in range(len(street_g)):
            ray_dir1=street_g[f]-fcd_cens[i]
            ray_dir.append(ray_dir1)
            run_count+=1
    ray_dir=np.array(ray_dir)

    # all the ray origins for each sky directions (vectorization format)
    ray_srcs = np.tile(fcd_cens, [1, len(street_g)]).reshape(-1, 3)

    # all the ray directions for each centroid
    ray_dirs = np.tile(street_g, [len(fcd_cens), 1])

    # computing the intersections of rays with the context mesh
    tri_id, ray_id = context_mesh.ray.intersects_id(ray_origins=ray_srcs, ray_directions=ray_dir, multiple_hits=False)

    # initialize the 'hits' array with 0
    hits = np.array([0] * len(ray_dirs))
    # rays that hit the context mesh are set to 1
    hits[ray_id] = 1

    hits=hits.astype(float)

    good_ray=[]
    good_ray_id=[]
    for i in range(len(hits)):
        if hits[i]==0:
            good_ray.append(ray_dir[i])
            good_ray_id.append(i)

    good_ray=np.array(good_ray)
    good_ray_id=np.array(good_ray_id)

    z_n=[0,0,-1]

    angle_deg=[]
    area_cross=[]
    ray_len=[]
    for i in range(len(good_ray)):
        ray2=good_ray[i]
        ray_l=np.linalg.norm(ray2)
        angle2=(180/np.pi)*np.arccos(np.dot(z_n,(ray2/ray_l)))
        area_p2=np.linalg.norm(np.cross((ray2/np.linalg.norm(ray2)),z_n))
        angle_deg.append(angle2)
        area_cross.append(area_p2)
        ray_len.append(ray_l)


    area_cross2=area_cross
    angle_deg2=angle_deg
    angle_deg=np.array(angle_deg)
    area_cross=np.array(area_cross)
    ray_len=np.array(ray_len)


    cross_product_score=1/np.exp(area_cross)
    length_score=np.exp(ray_len/100)
    total_score=(cross_product_score*length_score)

    score_hits=hits*0

    for i in range(len(good_ray_id)):
        score_hits[good_ray_id[i]]=total_score[i]
        
    # reshape the 'hits' array to (len(centroids), len(directions))
    score = score_hits.reshape(len(fcd_cens), -1)

    # sum up all the scores per centroid
    vox_score=np.sum(score,axis=1)

    # flatten the facade_lattice to retrieve the 1 dimensional lattice id
    facade_lattice_flat=facade_lattice.flatten()
    # retrieving 
    fcd_id=np.array(np.argwhere(facade_lattice_flat==1))
    for i in range(len(fcd_id)):
        facade_lattice_flat[fcd_id[i]]=vox_score[i]
        
    facade_streetview = facade_lattice_flat.reshape(facade_lattice.shape)

    facade_streetview_lat= tg.to_lattice(facade_streetview, facade_lattice)

    return facade_streetview_lat