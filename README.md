# Foreflow

A lightweight Python implementation of AWS Step Functions state machines.

Foreflow lets you define and execute state machine workflows locally using familiar AWS Step Functions syntax. It is built on Pydantic for robust type validation and supports YAML-based workflow definitions.

## Installation

```bash
pip install foreflow
```

## Quick Start

Define resources using decorators and execute state machines with type-safe inputs and outputs:

```python
import yaml
import foreflow
from foreflow import types

app = foreflow.Foreflow()


@app.resource("Foreflow::Callable::Invoke")
def invoke(inpt: Inpt) -> Outpt:
    return Outpt(payload={"status": "SUCCESS"})


state_machine = """
StartAt: ProcessTask
States:
  ProcessTask:
    Type: Task
    Resource: Foreflow::Callable::Invoke
    Next: Done
  Done:
    Type: Succeed
"""

machine = types.StateMachine.model_validate(yaml.safe_load(state_machine))
result = app.execute(machine, {})
```

## Features

- **AWS Step Functions Syntax**: Use familiar state machine definitions with Task and Succeed states
- **Type Safety**: Pydantic-based input and output validation for resources
- **YAML Workflows**: Define state machines in readable YAML format
- **JMESPath Support**: Extract and transform data using JMESPath expressions in parameters
- **Decorator API**: Register resources with a clean decorator pattern

## State Types

Foreflow currently supports the following state types:

| State Type | Description |
|------------|-------------|
| Task | Execute a registered resource function |
| Succeed | Mark successful completion of the workflow |

## Parameters

Use JMESPath expressions in parameters to extract data from the input:

```yaml
States:
  ProcessData:
    Type: Task
    Resource: MyResource
    Parameters:
      userId.$: "$.user.id"
      staticValue: "constant"
    Next: Done
```

Keys ending with `.$` are evaluated as JMESPath expressions against the current input.

## Requirements

- Python 3.11+
- pydantic
- pyyaml
- jmespath

## License

Apache-2.0
