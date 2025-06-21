# Definitions

This document collects recurring terms and concepts used across the project.

## SPECLANG

SpecLang refers to a natural-language specification approach championed by GitHub Next.  In this repository it means our specs under `./specs` are treated as the primary source of truth for plotting behavior.  Each spec should be precise enough that an LLM or developer can implement the described logic in any programming language without referring back to the Python code.

Working with SpecLang guides us to:

- Describe data columns, configuration objects and algorithm steps in straightforward prose.
- Keep plotting details implementation agnostic while noting necessary calculations or relationships.
- Maintain the specs in lockstep with code changes so new agents always understand the expected behavior.

This approach allows multiple language implementations or AI agents to share the same understanding of the plotting services built here.

Additional points distilled from the SpecLang research prototype:

- Specs evolve through an iterative feedback loop where running code informs new sections or clarifies ambiguous behavior.
- Natural language is used as "prose code": concise yet precise instructions that assume a programmer's mindset.
- The model may suggest refinements, so treat the spec as a conversation rather than a static document.
