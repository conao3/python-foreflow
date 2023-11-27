# python-foreflow

## Install

```bash
pip install foreflow
```

## Description

Subset of [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-states.html) implemented in Python.

```python
app = foreflow.Foreflow()

@app.resource("Foreflow::Callable::Invoke")
def invoke(inpt: Inpt_5cca9516) -> Outpt_5cca9516:
    return Outpt_5cca9516(
        payload={
            "Status": "SUCCESS",
        },
    )

state_machine = """\
StartAt: FirstState
States:
  FirstState:
    Type: Task
    Resource: Foreflow::Callable::Invoke
    Next: End
  End:
    Type: Succeed
"""

expected = {
    "Payload": {
        "Status": "SUCCESS",
    },
}

state_machine = types.StateMachine.model_validate(yaml.safe_load(state_machine))
ret = app.execute(state_machine, {})

assert ret.model_dump(mode="json", by_alias=True) == expected
```
