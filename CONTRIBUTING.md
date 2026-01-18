# Contributing to 100 AI-Native Python Projects

Thank you for your interest in building the pattern library for the human-in-the-loop era!

## Philosophy
This is not a script dump. We are building **infrastructure patterns**.
- **No Scripts**: Don't contribute a single file script. Contribute a *system*.
- **No Happy Paths**: Every project must handle failure, rate limits, and bad inputs.
- **Ethics First**: Every contribution must include an `ETHICS.md` discussing failure modes.

## Project Structure
New projects must follow the strict template:

```
project-name/
├── README.md           # Problem statement, mental model
├── DESIGN.md           # Architecture, tradeoffs, diagrams
├── ETHICS.md           # Safety, bias, misuse
├── src/                # Implementation
├── tests/              # Unit and integration tests
├── evals/              # Golden datasets and scoring logic
└── traces/             # Example logs/traces
```

## Standards
1. **Type Hints**: All code must be strictly typed (mypy compliant).
2. **Schema Validation**: Use Pydantic for all IO.
3. **Observability**: All complex logic must be traced (OpenTelemetry or similar).
4. **Dependencies**: Prefer raw clients (`openai`) over heavy frameoworks (`langchain`) unless the project *is* about the framework. We want to teach the *mechanics*.

## Pull Request Process
1. Open an issue proposing the Pattern.
2. Receive approval on the architecture.
3. Submit PR with full test coverage and an Eval run.
