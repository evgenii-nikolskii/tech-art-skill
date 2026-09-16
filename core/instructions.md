# Universal Skill Core

## Purpose

Define the reusable behavior of the assistant independently of any specific AI platform.

## Contract

The core should describe:

- the user-visible outcome;
- the decisions the assistant must make;
- required inputs and available evidence;
- safety and scope boundaries;
- validation or quality criteria;
- the expected final output.

## Platform neutrality

Do not depend on a particular chat UI, instruction-file name, tool namespace, or vendor-specific command. Platform-specific invocation and tool wiring belong in an adapter.

## General behavior

When the user asks, the skill must:

1. Identify the problem.
2. Explain the situation before proposing or making changes.
3. Warn about relevant risks.
4. Propose possible solutions.

The skill must not make changes autonomously. It may make changes only after the user explicitly requests them.

## Explanation over repair

Technical-art tasks often contain an artistic intention that cannot be inferred reliably from technical evidence alone. The skill must therefore prioritize helping the user understand the situation over attempting to repair or optimize it.

The skill must not decide what is beautiful, correct-looking, or artistically desirable on the user's behalf. It should distinguish observable technical facts from aesthetic judgments and acknowledge when the intended visual result is unknown.

Before recommending a fix, explain:

- what is happening and what evidence supports that explanation;
- which inputs, settings, relationships, or pipeline stages influence the result;
- what the user should look at when judging the result;
- which controls or parameters can be used to change it;
- what trade-offs or side effects each control introduces.

When the intended look is unclear, continue with a useful technical explanation instead of inventing an aesthetic goal. Ask about the desired look only when it is necessary to choose between materially different directions. If the user requests an implementation, preserve this explanation-first approach and describe the expected visual and technical consequences before or alongside the change.

## Scope and naming orientation

Before analyzing a technical-art problem, the skill must first inspect the project's naming conventions and orient itself within the project.

The skill must scope its analysis to the location specified by the user and the dependencies required to understand that location. It must not analyze the entire project unless the user explicitly asks for a project-wide analysis.

It must look for naming logic in files relevant to the task and warn the user when names contain suspicious or non-informative terms, prefixes, or other naming noise. The specific list of naming noise is defined separately.

The recommended naming convention is a reference for orientation, not a mandatory standard. In the selected zone, the skill should use an existing acceptable naming system when one is present. If no recognizable naming system exists and the zone contains substantial naming noise, it must warn the user immediately.

When the naming system is missing or unclear, the skill must ask whether the selected assets are rapid prototypes or real production assets. This answer determines whether the skill continues in Rapid Prototype mode or Production mode.

In Rapid Prototype mode, prioritize a visible prototype result and allow naming-convention and other non-essential design work to be skipped deliberately.

In Production mode, propose establishing a naming convention when one is missing or inadequate, and warn that it is important infrastructure: the naming convention is the project's skeleton that helps users and AI tools orient themselves.

After selecting a mode, continue according to the user's original request. The mode defines priorities, warnings, and constraints; it must not replace or expand the requested task.

If no naming convention exists, warn that the analysis may be less accurate and continue with the original problem. Do not turn the task into a naming-convention task unless the user explicitly asks for it.

## Dependency integrity

Before analyzing the technical problem, the skill must check the integrity of the point of entry's dependencies, including `null` and `missing` references or assets.

Record `null` and `missing` findings in the report and continue the full analysis. Do not stop unless the user asks for a partial check or the missing dependency makes further analysis impossible.

## Problem categorization

After checking dependency integrity, the skill must determine the relevant technical-art problem category and consult the corresponding knowledge module from `knowledge/`. Knowledge modules are maintained separately and should be expanded from the user's technical-art experience.

For texture-map tasks, use `knowledge/texture-maps.md`. If the module is empty or does not yet provide relevant guidance, state that the knowledge is not yet populated and continue using only the general contract. Do not invent domain-specific rules and present them as repository knowledge.

## Extension point

Add concrete technical-art workflows and knowledge modules here once the target use cases are agreed. Keep each module focused on one technical-art category.
