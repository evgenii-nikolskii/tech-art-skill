# Platform adapters

Adapters translate the universal core into the instruction and packaging format expected by a specific AI system. These are AI-platform adapters, not game-engine integrations.

Add one file or directory per platform. Keep platform-specific commands, tool names, invocation syntax, and packaging details here; keep reusable behavior in `core/`.

The AI workflow is intended to apply across game engines. Engine-specific guidance belongs in clearly scoped knowledge sections and must only be applied when relevant. Providing structured project data through the optional snapshot contract is outside the required AI adapter behavior.
