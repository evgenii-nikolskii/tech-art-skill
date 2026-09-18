# Materials and Shaders

## Principle

A material is a data instance consumed by a shader. A shader defines the rendering algorithm, while the material supplies textures, numeric parameters, keywords, render state, and ownership. A scene audit or asset review must separate shader capability from material configuration and from the intended artistic result.

## Material Contract

Before changing a material, identify:

- the shader and render pipeline it targets;
- required textures, channel layout, color space, and normal-map convention;
- scalar/vector ranges and defaults;
- transparency, culling, depth, sorting, and shadow behavior;
- whether parameters are shared, per-material, per-instance, or per-vertex;
- whether the material is project-owned, generated, imported, or a temporary look-development asset.

Do not create duplicate materials to solve a per-object variation that should be an instanced property, vertex color, or material variant. Conversely, do not force unrelated assets into one material when they require different render states or texture contracts.

## Shader Review

Check:

- supported render pipeline and shader model/API requirements;
- vertex and fragment complexity, texture samples, branches, loops, and additional passes;
- shader keywords and variant count;
- SRP Batcher compatibility where applicable;
- GPU Instancing compatibility where repeated geometry needs it;
- depth, shadow, motion-vector, meta/lightmap, and distortion passes;
- platform fallbacks and behavior when an optional feature is unavailable;
- whether properties are declared in the expected constant buffers and exposed with stable names.

An apparently simple material can be expensive because of transparent overdraw, shadow passes, variants, or multiple texture samples. An apparently complex shader may be acceptable for a small number of objects. Use captures and profiler data when making performance claims.

## Transparency and Render State

Treat opaque, alpha-clipped, transparent, additive, premultiplied, and refractive materials as different technical contracts. Validate:

- blend factors and alpha interpretation;
- depth test and depth write;
- render queue/sorting order;
- backface culling and double-sided normal handling;
- shadow casting and receiving;
- fog, motion vectors, refraction, and post-processing interaction.

Do not fix sorting problems by changing queue values blindly. Identify the competing surfaces, depth policy, camera order, and whether the asset should be opaque or alpha-tested instead.

## Variants and Ownership

Track which keywords are required by content and which are accidental. Excess variants increase build time, memory, warm-up cost, and risk of unsupported combinations. Missing variants can produce fallback shaders or incorrect runtime behavior.

Materials should have a clear owner and reimport policy. Imported or generated materials must not silently replace project-authored materials. A material validation report should include shader, keywords, render state, referenced textures, missing properties, and intended owner.

## Validation

Use a neutral diagnostic scene and test:

- albedo, roughness, metallic, normal, AO, opacity, and emission inputs independently;
- extreme parameter values and missing optional maps;
- directional lighting, environment reflections, shadows, and camera distance;
- opaque, clipped, and transparent sorting cases;
- target-platform shader compilation and representative frame timings.

Record confirmed technical failures separately from subjective differences between the DCC preview and the engine.
