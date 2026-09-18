# Baking and Lightmaps

## Principle

Baking transfers a result from a source configuration into asset or scene data. The baked result is only correct for the geometry, UVs, scale, lighting, and settings used during the bake. Treat a bake as a reproducible build artifact, not as a permanent substitute for dynamic lighting.

## Bake Contract

Record:

- geometry and scene revision;
- lightmap UV set, charting rules, padding, and resolution/texel-density target;
- static/baked participation flags;
- direct and indirect lighting settings, bounce count, environment, exposure, and color space;
- shadow, ambient occlusion, emissive, probe, and denoising settings;
- target platform and compression/encoding;
- ownership and invalidation conditions for baked data.

If geometry, UVs, materials, lights, scale, or relevant settings change, determine whether the bake is stale before judging the scene.

## UV and Chart Quality

Check for:

- missing or overlapping lightmap UVs;
- insufficient chart padding for the target mip chain;
- excessive seams or fragmented charts;
- stretched charts and poor texel allocation;
- mirrored or tiled layouts accidentally used for unique baked data;
- lightmap resolution that does not match asset scale or visual importance.

Lightmap artifacts may come from UV layout, resolution, geometry normals, lightmap compression, shadow bias, insufficient samples, or stale data. Diagnose the source before increasing resolution globally.

## Bake Validation

Inspect:

- seams, bleeding, splotches, gradients, and low-frequency discontinuities;
- contact shadows and indirect-light behavior;
- emissive contribution and material response;
- light probes for dynamic objects;
- baked data memory and load time;
- representative close, mid, and distant views;
- the oldest supported platform and quality tier.

Use a clean rebuild and compare timestamps or hashes when stale data is suspected. Keep static and dynamic lighting ownership explicit so that an object is not accidentally lit twice or left without a valid source.
