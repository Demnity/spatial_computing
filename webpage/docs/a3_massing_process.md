# Process

## Behaviour
#### Squareness
This behaviour takes a weight in range <strong>[0, 1] </strong>, representing how rectangular the shape the agent would grow into is.

![Squareness](/img/squareness.jpg)
<i>The only voxel with value 2 (it has 2 neighbours adjacent to it) is the best voxel the agent wants to grow to if it wants to be rectangular.</i>
<table><thead><tr class="header"><th>Pseudocode</th><th></th></tr></thead><tbody><tr class="odd"><td>Input</td><td>Square weight, current agent's free neighbours</td></tr><tr class="even"><td>Output</td><td><p>Change value priority of the free neighbours</p></td></tr>
<tr class="odd"><td>Code</td><td>
<pre>
1> Find neighbours of the current agent (neighbours can be duplicated)

2> Count the number of duplicated neighbours 

3> The more times a neighbour is duplicated, the more probable it is the necessary voxel the agent has to grow to achieve squareness 

4> For each neighbour value:
    value *= count ** input_weight
</pre>
</td></tr></tbody></table>

#### Agent connectiveness
This behaviour takes a weight in range <strong>[0, 1] </strong>, representing how rectangular the shape the agent would grow into is.

<table><thead><tr class="header"><th>Pseudocode</th><th></th></tr></thead><tbody><tr class="odd"><td>Input</td><td>Current agent locations</td></tr><tr class="even"><td>Output</td><td><p>Change value priority of the free neighbours</p></td></tr>
<tr class="odd"><td>Code</td><td>
<pre>
1> Initialize agent seeds​

2> For each agent:​
    Calculate the breath-first distance to the seed​

3> Append them to the field values​

3> Agent growth for-loop:​
    Use weighted products to evaluate the distance field of the neighbouring voxels ​

4> Choose the best voxel out of them​

5> Recalculate the distance field of the current agent since it has grown 1 more voxel
</pre>
</td></tr></tbody></table>

#### Eating and abandoning voxels
When an agent has grown to its max size, if there is a better voxel in the neighbourhood, it will willingly give up its worst-valued voxel to absorb that better one. This way, the max size will still be upheld.

<table><thead><tr class="header"><th>Pseudocode</th><th></th></tr></thead><tbody><tr class="odd"><td>Input</td><td>Current agent locations, current agent values</td></tr><tr class="even"><td>Output</td><td><p>Change agent locations</p></td></tr>
<tr class="odd"><td>Code</td><td>
<pre>
1> Define a max size for each agent​

2> Store the value array of each voxel of each agent​

3> If an agent has reached it max size:​
    Get the best neighbouring voxel​
    If best_neighbour_voxel_value > worst_voxel_value_in_array:​
        Remove the worst voxel in the value array (doing this will reduce the size of the agent, then we can add new voxel in step 4)​
    Else:
        Continue (not adding any new voxels, concluding the growth of this agent)​

4> Continue the agent growth process if the current agent hasn't reached its max size yet (adding the best neighbouring voxel to the agent)
</pre>
</td></tr></tbody></table>

#### Building depth
The behaviour limits the building depth, not allowing it grow further than the predefined maximum depth.
![Depth stencil](/img/building_depth_stencil.jpg)
<i>The stencil created in the x and y direction with the length of max depth 2. It has 4 axis, x, y, -x, -y.</i>
![Depth scenario 1](/img/scenario1_building_depth.jpg)
<i>Here since all the values are 2, each voxel only has 1 of its axis filled (axis = value / max_depth, in this case the number of axis filled = 2 / 2 = 1). Since the number of axis filled is not 2, these voxels can still be considered as neighbours to the current agent.</i>
![Depth scenario 2](/img/scenario2_building_depth.jpg)
<i>The same thing happens here, each voxel only has 1 axis filled, except for one voxel with 1.5 axis filled. Still, these voxels can be considered as neighbours.</i>
![Depth scenario 3](/img/scenario3_building_depth.jpg)
<i>Here there is one voxel with value 4, meaning it has 2 of its axis filled. Therefore, the voxel is ignored and the agent won't grow to this voxel.</i>
<table><thead><tr class="header"><th>Pseudocode</th><th></th></tr></thead><tbody><tr class="odd"><td>Input</td><td>Current agent locations</td></tr><tr class="even"><td>Output</td><td><p>Remove the neighbours that make the agent exceed the max depth</p></td></tr>
<tr class="odd"><td>Code</td><td>
<pre>
1> Define a max depth for each agent​

2>   For each agent:​

2.2>    Create a stencil in the x and y directions with the length of max depth​

2.3>    Set stencil function to sum​

2.4>    Get lattice that contains only the current agent voxels​

2.5>    Apply the stencil to the lattice to get res_lattice (this would calculate how many voxels are surrounding each voxel)​

2.6>    res_lattice = res_lattice / max_depth (to obtain the number of axis filled for each voxel)​

2.7>    If the number of axis filled >= <strong>2</strong>: ​
            Ignore this voxel as a neighbour for the current agent​
        Else:​
            Use it normally
</pre>
</td></tr></tbody></table>

#### Building height
The behaviour limits the building height, not allowing it grow further than the predefined maximum height. Works better in conjunction with squareness. Has the same idea as building depth.

<table><thead><tr class="header"><th>Pseudocode</th><th></th></tr></thead><tbody><tr class="odd"><td>Input</td><td>Current agent locations</td></tr><tr class="even"><td>Output</td><td><p>Remove the neighbours that make the agent exceed the max height</p></td></tr>
<tr class="odd"><td>Code</td><td>
<pre>
1> Define a max depth for each agent​

2>   For each agent:​

2.2>    Create a stencil in the z direction with the length of max height

2.3>    Set stencil function to sum​

2.4>    Get lattice that contains only the current agent voxels​

2.5>    Apply the stencil to the lattice to get res_lattice (this would calculate how many voxels are surrounding each voxel)​

2.6>    res_lattice = res_lattice / max_depth (to obtain the number of axis filled for each voxel)​

2.7>    If the number of axis filled >= <strong>1</strong>: ​
            Ignore this voxel as a neighbour for the current agent​
        Else:​
            Use it normally
</pre>
</td></tr></tbody></table>