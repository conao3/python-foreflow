from __future__ import annotations

from typing import Any

import yaml

from . import foreflow
from . import types
from . import util


class Inpt_5cca9516(util.pydantic.PascalModel):
    pass


class Outpt_5cca9516(util.pydantic.PascalModel):
    payload: dict[str, Any]


class TestMain:
    def test_5cca9516(self) -> None:
        app = foreflow.Foreflow()

        @app.resource("Foreflow::Callable::Invoke")
        def invoke(inpt: Inpt_5cca9516) -> Outpt_5cca9516:
            return Outpt_5cca9516(
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
        ret = app.execute(state_machine, {})

        assert ret.model_dump(mode="json", by_alias=True) == expected
