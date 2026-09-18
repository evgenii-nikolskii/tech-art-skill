## Definition

Texture maps are raster information: precise, artist-friendly, and the most expensive.

They can be used as information storage.

They are most often used in combination with the UV(W) coordinates of model geometry.

Any other information can be encoded as grayscale pixel values. A texture map is not limited to visible color or surface properties; it is a raster container for data. With an agreed encoding, range, precision, channel layout, and decoding process, it can carry almost anything the consuming material or system needs.

Vertex Animation Textures (VAT) are a practical example: animation data such as vertex positions, normals, or other per-vertex attributes can be encoded into textures and read by a shader over time. The texture is not “an animation” by itself—it is an information carrier, and the shader gives the stored values meaning.

Understanding texture maps as general-purpose information carriers is an important step toward using them effectively in technical art.

A color pixel expands this idea from a single scalar to a three-component vector. Its red, green, and blue channels can be read as `Vector3` values, which makes vector addition, subtraction, multiplication, interpolation, normalization, and other mathematical operations available in the shader. The channels do not have to represent a visible color; they can represent any three related values defined by the data contract.

Lookup tables (LUTs) are a practical example. A LUT texture stores a mapping from an input value to an output value, allowing a shader to retrieve a precomputed result instead of performing the full calculation at runtime. A color-grading LUT maps input colors to corrected output colors; a 3D LUT is commonly flattened into a 2D texture for storage and sampling. This demonstrates how a color texture can function as a mathematical data structure rather than an image intended only for display.

### Swizzling

Swizzling is a standard mathematical operation for selecting, reordering, duplicating, or replacing vector components. Shader languages commonly expose it through component names such as `r`, `g`, `b`, `a` or `x`, `y`, `z`, `w`.

For example, a sampled value can be transformed by:

- passing only one channel, such as `texture.r`;
- reordering channels, such as `texture.bgr`;
- duplicating a channel, such as `texture.rrr`;
- filling a component with a constant, such as `float4(texture.rgb, 1)` or `float3(texture.rg, 0)`;
- combining channels from different values into a new vector.

This simple operation solves a wide range of technical-art problems: adapting one texture layout to another shader input, supplying a required `0` or `1`, unpacking or repacking data, creating masks, and constructing vectors for further mathematical processing. Swizzling changes how the stored information is read; it does not change the texture data itself.

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

## Texture Import

Texture import settings are part of the map's data contract. The same image file can be correct or incorrect depending on how the engine interprets its channels, color space, mip levels, alpha, and compression.

Before importing, classify the map:

- **Visual color:** albedo/base color and the color component of emission. Enable sRGB decoding.
- **Technical data:** normal, roughness, metallic, AO, height, opacity, masks, packed maps, LUTs, and VAT data. Disable sRGB decoding.
- **HDR data:** environment, reflection, and HDR emission maps. Preserve the required HDR range and use a format that supports it.

Recommended import checks:

1. Confirm the texture type and intended channel layout. A packed map must document which property is in each channel, including whether a channel is unused and should be filled with `0` or `1`.
2. Enable the engine's normal-map import/decode path for tangent-space normals. Do not treat a normal map as ordinary color data or apply artistic color correction to it.
3. Preserve alpha semantics. Straight alpha, premultiplied alpha, opacity masks, and alpha-tested coverage are different contracts; the shader and importer must agree.
4. Generate mipmaps for world-space surfaces and sampling across distance unless the texture is a UI element, a lookup/data texture with deliberate no-mip sampling, or another explicitly controlled exception. Validate alpha-tested assets at mip levels, not only at full resolution.
5. Set wrap and filter modes according to use: repeat for tiled materials, clamp for atlases/LUTs, and point filtering for deliberately discrete data. Avoid filtering across unrelated atlas regions or packed data boundaries.
6. Set maximum size per platform and verify the imported result rather than assuming the source resolution is resident on the GPU. Non-power-of-two textures and block-compressed formats may introduce platform-specific padding or restrictions.
7. Inspect the actual GPU format and memory footprint in the target build. File size is not the same as runtime texture memory.

For packed maps, disable sRGB for the whole texture even when one channel originated from a color-looking source. If a shader needs a different layout, use explicit swizzling or repacking; do not rely on an editor preview to communicate channel meaning.

## GPU Compression by Platform

Choose compression for the GPU family and the map's error sensitivity, not only for download size. Block compression is fixed-rate: a smaller file does not automatically mean a better result, and a visually acceptable albedo setting can be destructive for a normal or mask map.

| Target | Preferred families | Practical starting point | Important constraints |
| --- | --- | --- | --- |
| Windows/Linux/macOS with modern desktop GPUs | BCn | BC7 for high-quality LDR RGBA, BC1 for opaque RGB, BC4 for one-channel masks, BC5 for two-channel normals, BC6H for HDR | BC7/BC6H need modern GPU support. Use BC3/DXT5 as a compatibility fallback, not as the default for every map. |
| PlayStation/Xbox and other desktop-class consoles | Platform-native BC-family formats where supported | Use the console SDK/profile and the same semantic split as desktop: BC7/BC5/BC4/BC6H where available | Verify the exact SDK and GPU profile; do not ship a PC format assumption without a console build capture. |
| Modern iOS/tvOS and modern Android | ASTC | 4x4 for high sensitivity, 6x6 as a balanced default, 8x8 or larger for less sensitive maps | ASTC block size changes quality and bitrate. Confirm the minimum device generation; unsupported formats may be decompressed at runtime. |
| Android with broad OpenGL ES 3 coverage | ETC2/EAC | ETC2 RGB/RGBA for color, EAC R/RG for single/two-channel data | ETC1 has no native alpha. Use ETC1 only with a deliberate split-alpha path or legacy fallback. |
| Older Apple devices or legacy mobile targets | PVRTC or the platform's required fallback | PVRTC 4 bpp before 2 bpp when quality matters | PVRTC has stricter shape/quality constraints and is a legacy compatibility choice; test square/non-square assets and alpha carefully. |
| WebGL/WebGPU | Formats exposed by the browser/device | Provide capability-based variants such as BC, ETC2, or ASTC where supported; keep a defined uncompressed fallback | Browser support is not uniform. Select the format at runtime/build time instead of assuming one compressed format for all clients. |

For the most common map types:

- **Base color/albedo:** BC7 or ASTC 6x6 are good quality-oriented starting points. BC1 is suitable for opaque RGB when the quality budget is lower. Keep it sRGB.
- **Tangent-space normal:** BC5 or EAC/RG two-channel formats are preferred when the shader reconstructs Z. ASTC 4x4–6x6 is a common mobile choice. Keep it linear and verify the green-channel convention after compression.
- **Roughness, metallic, AO, and masks:** use BC4/EAC R for one channel, BC5/EAC RG for two channels, or a higher-quality RGBA format for packed channels. Keep them linear. Avoid using a color-oriented low-quality setting merely because the preview looks acceptable.
- **HDR environment or emission:** use BC6H on supported desktop targets and ASTC HDR where the target device/API supports it; otherwise use an appropriate higher-precision fallback and measure memory.
- **Alpha-tested foliage and sprites:** evaluate alpha coverage through mipmaps and compression. If the alpha edge is important, increase quality or use a format with adequate alpha precision rather than hiding artifacts with a sharpen or threshold change.

Crunch or similar secondary compression reduces package/download size; it is not a GPU texture format and does not reduce the final resident GPU memory by itself. The runtime still needs to decode the texture into a supported GPU format.

### Compression Validation

For every platform profile, validate at least:

- the imported GPU format and runtime memory size;
- albedo gradients and alpha edges at native and mip levels;
- normal-map shading under a moving directional light;
- roughness response on both smooth and rough materials;
- packed-channel values in a debug shader or numeric inspector;
- fallback behavior on the oldest supported device/API.

If a map carries gameplay, deformation, lookup, or other non-visual data, validate decoded numeric error—not just the texture preview. The acceptable compression choice depends on how that error affects the consuming shader or system.
