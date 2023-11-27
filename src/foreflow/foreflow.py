from __future__ import annotations

import typing
from typing import Any
from typing import Callable
from typing import TypeVar

import pydantic

from . import types

S = TypeVar("S", bound=pydantic.BaseModel)
R = TypeVar("R", bound=pydantic.BaseModel)
ResourceFn = Callable[[S], R]

T_ResourceFn = TypeVar("T_ResourceFn", bound=ResourceFn[Any, Any])


class Foreflow:
    def __init__(self) -> None:
        self._resources: dict[str, ResourceFn[Any, Any]] = {}

    def resource(self, name: str) -> Callable[[T_ResourceFn], T_ResourceFn]:
        def decorator(fn: T_ResourceFn) -> T_ResourceFn:
            self._resources[name] = fn
            return fn

        return decorator

    def execute(
        self,
        state_machine: types.StateMachine,
        inpt: dict[str, Any],
    ) -> dict[str, Any]:
        if not state_machine.start_at in state_machine.states:
            raise ValueError(f"StartAt state '{state_machine.start_at}' not found")

        cur_inpt = inpt
        cur_state = state_machine.states[state_machine.start_at]

        while cur_state.type not in ["Succeed", "Fail"]:
            if cur_state.type == "Task":
                if cur_state.resource not in self._resources:
                    raise ValueError(f"Resource '{cur_state.resource}' not found")

                resource = self._resources[cur_state.resource]

                resource_fn_hints = typing.get_type_hints(resource)
                inpt_model = resource_fn_hints["inpt"]
                outpt_model = resource_fn_hints["return"]

                if not isinstance(inpt_model, type):
                    raise ValueError(
                        f"Resource '{cur_state.resource}' missing 'inpt' type hint",
                    )

                if not issubclass(inpt_model, pydantic.BaseModel):
                    raise ValueError(
                        f"Resource '{cur_state.resource}' 'inpt' type hint is not a subclass of pydantic.BaseModel",
                    )

                if not isinstance(outpt_model, type):
                    raise ValueError(
                        f"Resource '{cur_state.resource}' missing 'return' type hint",
                    )

                if not issubclass(outpt_model, pydantic.BaseModel):
                    raise ValueError(
                        f"Resource '{cur_state.resource}' 'return' type hint is not a subclass of pydantic.BaseModel",
                    )

                ret = resource(inpt_model.model_validate(cur_inpt))

                if not isinstance(ret, outpt_model):
                    raise ValueError(
                        f"Resource '{cur_state.resource}' returned value is not an instance of '{outpt_model.__name__}'",
                    )

                cur_state = state_machine.states[cur_state.next]
                cur_inpt = ret.model_dump(by_alias=True)

            else:
                raise ValueError(f"Unknown state type '{cur_state.type}'")

        return cur_inpt