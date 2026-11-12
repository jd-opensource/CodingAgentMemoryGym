from abc import ABCMeta, abstractmethod
from typing import Any, Mapping, Sequence

from .types import (
    ActionFormat,
    ConversationMessage,
    PolicyContextPressure,
    StepOutput,
)


class BaseEnvClient(metaclass=ABCMeta):
    _conversation_start: dict[ActionFormat, tuple[ConversationMessage]]

    def __init__(self, action_format: ActionFormat = "react") -> None:
        self.action_format = ActionFormat(action_format)

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def observe(self) -> str:
        pass

    @abstractmethod
    def step(self, action) -> StepOutput:
        pass

    @abstractmethod
    def reset(self, idx: int) -> None:
        pass

    def policy_turn_candidate(self) -> str | None:


        return None

    def policy_framing(self) -> Sequence[Mapping[str, str]] | None:


        return None

    def policy_tool_schemas(self) -> Sequence[Mapping[str, Any]] | None:


        return None

    def normalize_initial_policy_context(
        self,
        messages: Sequence[Mapping[str, str]],
    ) -> Sequence[Mapping[str, str]]:


        return messages

    def bind_policy_context(
        self,
        messages: Sequence[Mapping[str, str]],
        *,
        initial: bool = False,
    ) -> None:


        del messages, initial

    def begin_policy_turn(self, turn_index: int, turn_budget: int) -> None:


        del turn_index, turn_budget

    def prepare_policy_turn(
        self, pressure: PolicyContextPressure | None
    ) -> str | None:


        del pressure
        return None

    def finalize_policy_horizon(self) -> StepOutput | None:


        return None
