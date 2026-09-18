# VFX and Particle Systems

## Principle

VFX cost is a combination of simulation, rendering, overdraw, memory, synchronization, and content density. A visually small effect can be expensive when it uses large transparent surfaces, distortion, many texture samples, or frequent CPU updates.

## Audit Contract

For each effect, identify:

- CPU or GPU simulation and update frequency;
- spawn rate, lifetime, particle count, burst behavior, and pooling;
- render mode, mesh/quad complexity, trails, ribbons, lights, and distortion;
- blend mode, depth policy, sorting, soft particles, and shadow behavior;
- texture samples, flipbooks, VAT data, shader variants, and per-particle attributes;
- bounds, culling, LOD, off-screen simulation, and camera coverage;
- target platform and acceptable frame/memory budget.

## Overdraw

Warn about overdraw when effects contain many transparent layers or cover a large portion of the screen. Smoke, fog, fire, additive glows, distortion, ribbons, decals, and fullscreen effects are common risks.

Particle count alone is insufficient evidence. Measure or visualize overdraw from representative cameras and include GPU timing. Reducing spawn rate may not help if a few large particles dominate fill rate; reducing size, overlap, shader passes, or screen coverage may be more effective but can change the intended look.

## Simulation and Memory

Check for unbounded emission, long lifetimes, duplicate systems, runtime allocation, unnecessary collision events, and effects that continue while invisible. Prefer pooling and bounded lifetimes where the runtime architecture supports them. Validate that GPU buffers, flipbooks, mesh data, and audio/VFX dependencies fit the platform memory budget.

## Validation

Test warm-up, looping, interruption, pooling reuse, camera cuts, low-end devices, and multiple simultaneous effects. Verify sorting with opaque geometry, correct bounds/culling, motion vectors, lighting, and behavior when textures or optional features are missing.
