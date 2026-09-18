# Mesh Processing

## Principle

Mesh processing changes the representation of geometry while preserving an intended visual, deformation, collision, or baking result. Topology, vertex splits, normals, tangents, UVs, skinning, and morph deltas are coupled; changing one can invalidate the others.

## Geometry Contract

Before processing, define whether the mesh is for rendering, deformation, baking, collision, navigation, simulation, or export. Record:

- coordinate system, scale, pivot, and transform policy;
- topology and triangulation ownership;
- normals, smoothing groups, hard edges, and tangent convention;
- UV sets, vertex colors, skin weights, morphs, and custom attributes;
- material slots and submesh boundaries;
- LOD and collision requirements.

## Normals, Tangents, and Splits

Inspect hard-edge placement, smoothing angles, mirrored UVs, tangent handedness, and vertex splits. A vertex may need to split at a UV seam, material boundary, hard edge, or tangent discontinuity. Reducing vertex count without understanding these boundaries can produce shading seams or break normal-map decoding.

Keep baker and runtime tangent generation compatible. If authored normals/tangents are replaced, rebake or validate the normal map and inspect under directional lighting.

## Optimization

Use reduction, welding, reordering, quantization, mesh compression, and vertex-cache optimization only against a measurable budget. Check silhouette, screen-space error, deformation, shadows, collision, UV density, and material boundaries after each operation.

Do not merge meshes merely to reduce object count if it harms culling, LOD, streaming, material ownership, or instancing. Do not split meshes merely for organization if it creates excessive draw submissions or duplicated vertices.

## Validation

Compare before/after counts, bounds, screen-space error, normals/tangents, UVs, skin weights, morphs, collisions, material slots, and runtime memory. Test extreme poses and representative lighting, not only a static beauty view.
