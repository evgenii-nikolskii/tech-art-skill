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

## Extension point

Add the concrete technical-art workflows here once the target use cases are agreed.
