<!-- # Forming

> Here you should include the process and product of your 4th activity: **Forming**

| Title     | Forming (process): Form (product)                                                                                                                                                                                                                                                                                       |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Objective | Document the process and products and provide explanations to ensure reusability of materials.                                                                                                                                                                                                                          |
| Procedure | Finalize the plans and the forms of all functional units. Optionally, choose a way to alter the jaggedness of voxels in the final form by partially bringing in contrasting curvy shapes, for instance as a shell around the building, e.g. through smoothing, relaxation, iso-surfaces, or topological transformation. | -->

# Forming Product

## Forming the first model

The model is created by using the first tileset and the final mesh (all agents combined). The result looks like this:

<img src="/img/a4_3.1.png"width="700">

<img src="/img/a4_3.2.png"width="700">

<img src="/img/a4_3.3.png"width="700">

## Forming the second model

For a new model, it would be interesting to use multiple tilesets for the same building. We have already created a seperate mesh per agent. We ran this for an updated script with an extra field. This leads to the building that is seen below. All living spaces have been colore red, all other spaces have been colored black.

<img src="/img/a4_5.1.png"width="700">

By manually puting the tiles on this building, we get the following image. This is done manually because the new tilesets do not work in code (the balconies are turned upside down on all voxels on the ground floor). The problem probably lies in the used symetry stencil.

<img src="/img/a4_5.2.png"width="700">

Visually, we prefer the first model. It looks a lot more clean. For future projects, the second version offers a lot more potential.