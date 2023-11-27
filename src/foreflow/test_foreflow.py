from __future__ import annotations

from typing import Any

import yaml

from . import foreflow
from . import types
from . import util


class TestMain:
    def test_5cca9516(self) -> None:
        app = foreflow.Foreflow()

        class Inpt(util.pydantic.PascalModel):
            pass

        class Outpt(util.pydantic.PascalModel):
            payload: dict[str, Any]

        @app.resource("Foreflow::Callable::Invoke")
        def invoke(inpt: Inpt) -> Outpt:
            return Outpt(
                payload={
                    "Status": "SUCCESS",
                },
            )

        inpt = """\
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

        state_machine = types.StateMachine.model_validate(yaml.safe_load(inpt))

        assert app.execute(state_machine, {}) == expected
