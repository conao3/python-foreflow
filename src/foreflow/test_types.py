from __future__ import annotations

import yaml

from . import types


class TestMain:
    def test_ab9ada04(self) -> None:
        inpt = """\
States:
  FirstState:
    Type: Task
    Resource: AWS::Lambda::Invoke
    Parameters:
      FunctionName: abc-function
    Next: End
  End:
    Type: Succeed
"""
        expected = {
            "States": {
                "FirstState": {
                    "Type": "Task",
                    "Resource": "AWS::Lambda::Invoke",
                    "Parameters": {
                        "FunctionName": "abc-function",
                    },
                    "Next": "End",
                },
                "End": {
                    "Type": "Succeed",
                },
            },
        }

        obj = types.StateMachine.model_validate(yaml.safe_load(inpt))
        assert obj.model_dump(mode="json", by_alias=True) == expected
