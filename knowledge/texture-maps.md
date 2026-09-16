## Definition

Texture maps are raster information: precise, artist-friendly, and the most expensive.

They can be used as information storage.

They are most often used in combination with the UV(W) coordinates of model geometry.

## PBR Texture Maps

### Albedo vs. Diffuse

**Albedo** is the intrinsic color or reflectance of a surface, excluding lighting, shadows, highlights, ambient occlusion, and other illumination information.

**Diffuse** is a legacy and broader term. It often refers to the color texture used by a non-PBR diffuse shader and may contain baked lighting, shadows, or ambient occlusion, depending on the project and its authoring workflow.

In a PBR workflow, use an albedo/base-color map for surface color and keep lighting information in the lighting model or dedicated maps. Do not assume that a texture named `diffuse` is a valid PBR albedo map without inspecting its content and shader context.

Multiplying or overlaying an ambient-occlusion (AO) map onto the albedo or diffuse color is an error in a PBR workflow. AO is lighting-related technical data, not intrinsic surface color; it should be supplied through the material's AO input and combined by the shader's lighting model. Baking AO into albedo makes the result too dark, duplicates the occlusion when the shader also applies AO, and prevents the map from responding correctly to changes in lighting, exposure, or environment.

An AO map exists to support lighting calculations. It passes occlusion information to the lighting system so the shader can reduce ambient or indirect light where nearby surfaces block it. The map does not paint or create darkness by itself; the shader interprets its values in the context of the scene's lighting. Without a lighting calculation, an AO texture is only a grayscale data map.

### Gamma Correction and Color Space

Gamma correction is a transfer between a linear representation of light and a nonlinear representation used for storage and display. In practice, game workflows commonly use the sRGB transfer function rather than a simple mathematical gamma curve. sRGB allocates more stored precision to the darker visual range, matching how people perceive brightness and how display devices represent color.

The important distinction is between **visual color data** and **technical data**:

- Visual color maps, such as albedo/base color and the color component of emission, are authored and stored in sRGB so they look correct to artists and are converted back to linear values before lighting calculations.
- Technical maps, such as normal, roughness, metallic, ambient occlusion, height, opacity masks, and packed data, contain numeric instructions rather than displayed color. They must remain linear and must not receive sRGB/gamma conversion.

Applying gamma correction to a technical map changes its numeric values. This can alter normal directions, roughness response, mask thresholds, metalness, displacement height, or packed channels even when the texture preview looks acceptable. Conversely, treating a visual color map as linear makes its color and brightness wrong in the material.

The texture import setting and shader sampler must agree. Mark visual color maps as sRGB and technical maps as linear data; for packed textures, disable sRGB for the entire texture because every channel is technical data. When diagnosing a mismatch, verify the actual imported color-space setting rather than relying on the file name or preview.

### Roughness and Metallic

#### Roughness

Roughness describes how irregular the microscopic surface is. It controls the distribution of reflected light rays rather than simply making a material brighter or darker:

- Low roughness produces a narrow, concentrated reflection. Light rays are reflected in similar directions, creating a sharp highlight or a clear environment reflection.
- High roughness produces a wide, scattered reflection. Light rays leave the surface across a broader range of directions, creating a soft, broad highlight and a blurred environment reflection.

Roughness is usually stored as a linear grayscale value, where `0` means smooth and `1` means rough. Some workflows use a glossiness/smoothness map instead; those are inverse representations and must not be treated as roughness without conversion.

#### Metallic

Metallic describes whether the surface behaves as a conductor or a dielectric. It changes what happens to the incoming light rays:

- A dielectric (`metallic = 0`) has a colored diffuse response beneath a generally neutral specular reflection. Light enters the surface response, scatters, and returns as diffuse light.
- A metal (`metallic = 1`) has no traditional diffuse response. Light is reflected at the surface, and the reflected specular color is tinted by the metal's base color.

Metallic is usually a linear mask with values close to `0` or `1`; intermediate values should represent an intentional material boundary or a filtered transition, not a way to make a material partially metallic. Roughness still controls the spread of the reflected rays on both metals and dielectrics, while metallic controls the type and color of the surface response.

### Ambient Occlusion (AO)

An ambient-occlusion map stores how accessible each surface point is to ambient or indirect light. It is usually a linear grayscale map where white means little or no occlusion and black means strong occlusion from nearby geometry.

The shader uses AO to reduce ambient or indirect illumination in creases, contact areas, and other places where surrounding geometry blocks the environment. It does not replace shadows and should not be used to darken direct light, paint surface color, or simulate a complete lighting bake. AO is a supporting input to the lighting model, not a standalone visual effect.

AO may be baked from the asset's surrounding geometry or generated dynamically by the engine. A baked AO map represents the conditions used during baking, so it can become incorrect when the asset's scale, nearby geometry, lighting model, or intended placement changes. Use dynamic occlusion when the scene requires the result to respond to changing geometry or lighting.

Keep AO separate from albedo and sample it as linear data. If the material uses a packed texture, document the AO channel explicitly and verify that the shader reads the same channel without sRGB conversion.

### Normal Maps and Tangent Space

A normal map stores surface direction information in RGB instead of storing actual geometry. The encoded color is decoded into a vector, usually in the range `-1` to `1`, and used by the shader to change how lighting reacts across the surface. This creates the appearance of small geometric detail without adding vertices.

Most normal maps use **tangent space**. The vector is defined relative to the surface at each point:

- **X** points along the mesh tangent, usually in the direction of increasing U;
- **Y** points along the mesh bitangent, usually in the direction of increasing V;
- **Z** points away from the surface, along the vertex normal.

The shader builds a TBN basis from the tangent, bitangent, and normal vectors, then transforms the sampled tangent-space normal into world space or another lighting space. Because of this, the mesh tangents, UV orientation, baker, and shader must use compatible conventions. A correct-looking normal texture can produce incorrect shading when any part of this basis differs.

#### DirectX and OpenGL Y Convention

The main difference between common DirectX and OpenGL tangent-space normal-map conventions is the direction of the green channel, which represents the tangent-space Y component:

- **OpenGL:** the green channel conventionally represents `+Y`;
- **DirectX:** the green channel conventionally represents `-Y` relative to the OpenGL convention.

When converting a normal map between the conventions, invert the green channel. Do not flip the texture's UV Y coordinate as a substitute; that changes texture addressing rather than the encoded normal direction. Always verify the result on the target mesh under directional lighting, because the required convention is determined by the baker and the target renderer together.
