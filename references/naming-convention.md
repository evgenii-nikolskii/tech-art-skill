# Recommended Naming Convention

The skill may use this convention as an alternative when the project does not have a clear or consistent naming convention.

## Rules

1. Do not use abbreviations.
2. Do not include the file extension in the file name.
3. Use numbering starting at `00`.
4. Use lowercase for all names.
5. Keep names as short as possible.
6. Use the following general structure:

   ```text
   prefix_type_object_variant-number
   ```

## Component definitions

- `prefix` is a universal organizational separator used across the project.
- `type` is an internal separator within the prefix.
- `object` answers the question: what is this?
- `variant-number` is the number of the asset variation.

## Examples

### Character asset

```text
npc-human-adam-00
```

- `npc` — prefix
- `human` — type
- `adam` — object
- `00` — default variation

This means the default variation of a non-player human character named Adam.

### Environment asset

```text
enemy-buildings-house-02
```

- `enemy` — prefix
- `buildings` — type
- `house` — object
- `02` — variation number

This means the third variation of a house structure for the enemy faction.

## Proposed texture map and material examples

Texture maps inherit the complete mesh name and then add their own map-purpose and variation components. This keeps the relationship between the mesh and its texture maps explicit while allowing texture variations to be numbered independently.

### Texture maps

```text
npc-human-adam-00-basecolor-00
npc-human-adam-00-normal-00
npc-human-adam-00-roughness-00
npc-human-adam-00-metallic-00
npc-human-adam-00-ambientocclusion-00
```

For the mesh:

```text
npc-human-adam-00
```

For the texture map:

```text
npc-human-adam-00-basecolor-00
```

- `npc-human-adam-00` — complete mesh name
- `basecolor` — map purpose
- `00` — texture map variation number

### Materials

```text
npc-human-adam-material-00
enemy-buildings-house-material-02
```

- `npc` or `enemy` — prefix
- `human` or `buildings` — type
- `adam` or `house` — object
- `material` — asset purpose
- `00` or `02` — variation number

The texture-map example extends the mesh name with an explicit purpose and an independent texture-map variation number.
