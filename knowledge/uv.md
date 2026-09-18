# UV and Texel Density

## Principle

UVs are a mapping contract between surface points and texture space. A valid UV layout depends on its consumer: material textures, lightmaps, decals, trim sheets, atlases, procedural masks, and runtime data may require different layouts.

## UV Set Contract

Document the purpose and index of every UV set:

- material/base UVs;
- lightmap or baked-lighting UVs;
- decal/detail/trim-sheet UVs;
- simulation, VAT, or other data UVs.

Do not assume UV1 is always a lightmap set or that UV0 is always the only set. The importer, shader, baker, and runtime must use the same index and orientation.

## Layout Checks

Audit:

- missing UV sets and incorrect channel assignment;
- overlaps, stacking, mirroring, and whether each consumer permits them;
- shell padding and bleed at the target mip levels;
- shell orientation, distortion, stretching, and wasted space;
- coordinates outside the 0–1 range when tiling or UDIM behavior is not intentional;
- consistent texel density across assets that should share material detail;
- hard seams where filtering, normal baking, or lightmap charts require them.

Overlapping UVs are not automatically wrong: trim sheets, mirrored details, decals, and tiled materials may require them. Report the conflict between the layout and its consumer instead of applying a universal no-overlap rule.

## Texel Density

Texel density is the texture resolution assigned per unit of world or asset scale. Establish a project or asset-class target, then compare representative surfaces rather than forcing every surface to one value. Intentional exceptions include hero assets, small props, UI-like surfaces, decals, and detail masks.

When density is inconsistent, determine whether the cause is object scale, UV scale, texture resolution, material tiling, or an intentional visual priority. Changing UV scale can alter the apparent detail and may break trim-sheet or bake relationships.

## Validation

Use checker, grid, gradient, and texel-density diagnostic materials. Inspect at native resolution and through mip levels. For baked data, validate the exact UV set used by the baker and engine, including padding, chart seams, and lightmap resolution.
