# Naming Audit Workflow

## 1. Start from the point of entry

Use the asset or location specified by the user as the point of entry. Inspect the dependencies required to understand that entry point instead of scanning the entire project.

Examples:

- For a 3D model, inspect its meshes.
- For a material, inspect the textures assigned to it.
- For a shader, inspect its default values and referenced files.

## 2. Check names in the selected zone

Check the names of the entry point and its relevant dependencies within the selected zone. Do not first infer or validate a project-wide naming convention.

## 3. Identify the applicable naming system

Compare the names with the recommended convention or identify an analogous acceptable naming system in the selected zone.

The recommended convention is a reference for orientation, not a convention that must be imposed on every project.

- If the selected zone has an acceptable naming system, use that system when analyzing the task.
- If the selected zone has no recognizable naming system and contains substantial naming noise, warn the user immediately.

## 4. Determine the asset context

When the naming system is missing or unclear, ask the user whether the selected assets are:

- a rapid prototype; or
- real production assets used in the project.

This is the key workflow branch. After the user answers, continue in either Rapid Prototype mode or Production mode.

## 5. Apply the selected mode

### Rapid Prototype mode

Prioritize obtaining a visible prototype result. Deliberately skip naming-convention work and other design work that is not required to demonstrate the prototype.

### Production mode

Propose establishing a naming convention when one is missing or inadequate. Warn the user that this work is important even though it may feel tedious.

A naming convention is the skeleton of the project: it helps the users and AI tools orient themselves within the project.

## 6. Return to the user's request

After applying the selected mode, continue according to the user's original request. The mode determines priorities, warnings, and constraints; it does not replace or expand the user's requested task.

If no naming convention exists, warn that the analysis may be less accurate, then continue analyzing the user's original problem. Do not turn the task into a naming-convention task unless the user asks for that separately.

## 7. Check dependency integrity

Before analyzing the technical problem, check the quality and integrity of the point of entry's dependencies.

Look for:

- `null` references;
- `missing` references or assets.

Record all such findings in the report and continue with the full analysis. Do not stop the workflow unless the user asks for a partial check or the missing dependency makes further analysis impossible.

## 8. Categorize the problem

After checking dependency integrity, determine which technical-art problem category applies. Use the relevant knowledge in the repository's `knowledge/` directory to guide the categorization and subsequent analysis.

The knowledge categories are defined separately and should be expanded from the user's technical-art experience.
