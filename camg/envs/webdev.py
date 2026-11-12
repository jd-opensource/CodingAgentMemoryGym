from __future__ import annotations

from .agentgeneral import (
    AGENTGENERAL_CONTEXT_COMPACTION_REQUEST,
    AgentGeneralEnvClient,
)
from .filesystem_checkpoint import (
    FILESYSTEM_CHECKPOINT_PATH,
    FILESYSTEM_CHECKPOINT_REQUEST,
)
from .verl_qwen_tool_parser import QWEN_SINGLE_TOOL_CALL_CONTRACT

WEBDEV_COMPACTION_CONTRACT = "policy_filesystem_checkpoint_then_client_replace_v2"
WEBDEV_REWARD_CONTRACT = "webdev_vision_rubric_outcome_finish_only_v1"

WEBDEV_TOOLS_CONTRACT = (
    "Workspace bash takes exactly one parameter: command. bash commands "
    "already run from the container working directory /workspace, so bash "
    "may use paths relative to that directory. "
    "Put multi-line file content for bash in one quoted here-document: "
    "append with `cat >> path <<'EOF'` and overwrite with `cat > path <<'EOF'`, "
    "placing every pending line in the same block instead of one line per "
    "call. Do not assemble multi-line text with inline printf or echo "
    "arguments. Chaining with `&&` or `||` inside one bash command is "
    "allowed; prefer write-then-read-back verification."
)


_TC_OPEN = "<tool" + "_call>"
_TC_CLOSE = "</tool" + "_call>"

_BASH_EXAMPLE = (
    _TC_OPEN + "\n<function=bash>\n<parameter=command>\n"
    "ls -la dist\n"
    "</parameter>\n</function>\n" + _TC_CLOSE
)
_FINISH_EXAMPLE = (
    _TC_OPEN + "\n<function=finish>\n<parameter=answer>\n"
    "The requested site is delivered under dist/.\n"
    "</parameter>\n</function>\n" + _TC_CLOSE
)

_PREVIEW_EXAMPLE = (
    _TC_OPEN + "\n<function=render_preview>\n</function>\n" + _TC_CLOSE
)

_WEBDEV_DUAL_EXAMPLE = (
    _TC_OPEN + "\n<function=bash>\n<parameter=command>\n"
    "mkdir -p dist/assets\n"
    "</parameter>\n</function>\n" + _TC_CLOSE + "\n"
    + _TC_OPEN + "\n<function=bash>\n<parameter=command>\n"
    "find dist -type f | head -20\n"
    "</parameter>\n</function>\n" + _TC_CLOSE
)

WEBDEV_SYSTEM_PROMPT = (
    QWEN_SINGLE_TOOL_CALL_CONTRACT
    + "\n"
    + WEBDEV_TOOLS_CONTRACT
    + " Reasoning belongs inside think tags before the tool call.\n\n"
) + f"""
You are building a website inside a persistent container workspace. The task
message states the design brief and the delivery contract: build the
requested site and deliver it under dist/ with its entry point at
dist/index.html, unless the task message names a different delivery
directory. The fixed workspace tools are bash, plus render_preview for
screenshots of the delivered page and the finish tool. The workspace
persists for the whole episode, so files you write survive every context
compaction.

For a workspace command, use this complete form:

{_BASH_EXAMPLE}

To see how the delivered page actually looks, call render_preview: it
renders the current delivery and returns one screenshot of the page as an
image. Review it against the design brief and fix what looks wrong before
finishing; at most four screenshots per episode:

{_PREVIEW_EXAMPLE}

When the site is fully delivered under the task's delivery directory, call
finish so the delivered pages are rendered and graded:

{_FINISH_EXAMPLE}

Grading renders the delivered pages and judges them against the design
brief, so fulfil the brief's explicit requirements (sections, text, and
behaviour it names) before polishing style.

Your continuing memory lives in {FILESYSTEM_CHECKPOINT_PATH}: when the
conversation is compacted, write the checkpoint exactly as requested, then
read it back with one bash call when instructed.

The episode's turn budget is measured in policy responses: every response
spends exactly one turn, however many tool calls it carries, and the task's
opening message states how many turns the episode has. When several
independent build steps are useful together, emit them as consecutive
envelopes in the same response, for example:

{_WEBDEV_DUAL_EXAMPLE}
"""

WEBDEV_CONTEXT_COMPACTION_REQUEST = (
    FILESYSTEM_CHECKPOINT_REQUEST
    + " For this task, preserve the design brief's outstanding requirements, "
    "the delivery directory, the pages and files already written, and the "
    "next concrete build action."
)


class WebdevEnvClient(AgentGeneralEnvClient):


    _system_prompt = WEBDEV_SYSTEM_PROMPT


    _POLICY_BUDGET_FOOTER_LABEL = "Webdev"

    def __init__(
        self,
        env_server_base: str,
        data_len: int | None = None,
        *args,
        timeout: int = 900,
        **kwargs,
    ) -> None:


        from camg.controller import BaseEnvClient

        BaseEnvClient.__init__(self, *args, **kwargs)
        self.env_server_base = env_server_base.rstrip("/")
        self.timeout = timeout
        self.invalid_action_reward = 0.0
        self.invalid_action_budget = None
        self._exploration_milestones = {}
        metadata = self._request("GET", "metadata")
        if metadata.get("domain_id") != "webdev":
            raise RuntimeError("Webdev endpoint reports the wrong domain")
        if metadata.get("compaction_contract") != WEBDEV_COMPACTION_CONTRACT:
            raise RuntimeError(
                "Webdev endpoint reports the wrong compaction contract"
            )
        if metadata.get("reward_contract") != WEBDEV_REWARD_CONTRACT:
            raise RuntimeError(
                "Webdev endpoint reports the wrong reward contract"
            )
        if not str(metadata.get("reward_judge", "")).strip():
            raise RuntimeError("Webdev endpoint does not name its reward judge")
        max_policy_steps = metadata.get("max_policy_steps")
        if type(max_policy_steps) is not int or max_policy_steps <= 0:
            raise RuntimeError("Webdev endpoint reports invalid max_policy_steps")
        if metadata.get("max_policy_steps_enforced_by") != "shared_policy_runner":
            raise RuntimeError(
                "Webdev endpoint reports the wrong policy-step owner"
            )
        prompt_policy_turns = metadata.get("prompt_policy_turns", max_policy_steps)
        if type(prompt_policy_turns) is not int or prompt_policy_turns <= 0:
            raise RuntimeError("Webdev endpoint reports invalid prompt_policy_turns")
        if prompt_policy_turns > max_policy_steps:
            raise RuntimeError("Webdev endpoint reports prompt turns above the action cap")
        self.max_policy_steps = prompt_policy_turns
        self._policy_action_headroom = max_policy_steps
        task_count = int(metadata["task_count"])
        if data_len is not None and int(data_len) > task_count:
            raise ValueError(
                f"Webdev data_len {data_len} exceeds task_count {task_count}"
            )
        self.data_len = task_count if data_len is None else int(data_len)
        created = self._request("POST", "create", json={})
        self.env_id = int(created["id"])
        self.info = created
        self.metadata = metadata
        self._reset_policy_transition_state()


    def policy_turn_candidate(self) -> str | None:
        if not self._policy_context_bound or self._pending_checkpoint_read is not None:
            return None
        return WEBDEV_CONTEXT_COMPACTION_REQUEST

    def prepare_policy_turn(self, pressure) -> str | None:


        selected = super().prepare_policy_turn(pressure)
        if selected is None:
            return None
        if selected == AGENTGENERAL_CONTEXT_COMPACTION_REQUEST:
            return WEBDEV_CONTEXT_COMPACTION_REQUEST
        return selected
