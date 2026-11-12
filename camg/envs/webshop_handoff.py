from __future__ import annotations

from .filesystem_checkpoint import (
    FILESYSTEM_CHECKPOINT_REQUEST,
    FILESYSTEM_QWEN_CHECKPOINT_CONTINUATION_MARKER,
    FILESYSTEM_QWEN_CHECKPOINT_WRITE_GUIDANCE,
)


WEBSHOP_QWEN_CHECKPOINT_GUIDANCE = FILESYSTEM_QWEN_CHECKPOINT_WRITE_GUIDANCE
WEBSHOP_POLICY_CONTINUATION_MARKER = (
    FILESYSTEM_QWEN_CHECKPOINT_CONTINUATION_MARKER
    + " On this required read turn, do not use search, click, or `rg`. First read "
    "the continuation with the exact `cat` action above. On the following action, "
    "you may inspect other workspace records such as Confirmed entries. Every "
    "later action must remain a complete Qwen XML tool call."
)


WEBSHOP_POST_CHECKPOINT_READ_MARKER = (
    "The required continuation checkpoint read succeeded. The current browser "
    "page shown above did not change during that workspace read. Use the "
    "recovered checkpoint contents shown above and continue shopping now with "
    "a Qwen XML search or click function call. Do not read "
    "`.agent_memory/CONTINUATION.md` again unless a later context-boundary "
    "request explicitly requires it."
)


WEBSHOP_REPEATED_CHECKPOINT_READ_MARKER = (
    "This checkpoint has already been read in the current shopping session. "
    "The browser page above did not change during this repeated workspace read. "
    "Use the recovered checkpoint contents above and continue shopping now with "
    "a Qwen XML search or click function call; do not read "
    "`.agent_memory/CONTINUATION.md` again before browser progress."
)


WEBSHOP_SESSION_HANDOFF_REQUEST = (
    FILESYSTEM_CHECKPOINT_REQUEST
    + WEBSHOP_QWEN_CHECKPOINT_GUIDANCE
    + " For this shopping task, preserve completed purchases and their visible "
    "compatibility-relevant attributes, the current customer requirement, and "
    "the next shopping action. Overwrite the checkpoint even if you also keep "
    "other voluntary notes."
)


WEBSHOP_CONTEXT_COMPACTION_REQUEST = (
    FILESYSTEM_CHECKPOINT_REQUEST
    + WEBSHOP_QWEN_CHECKPOINT_GUIDANCE
    + " For this shopping task, preserve the current session requirement, "
    "decisive product evidence and selections, completed purchases, remaining "
    "budget, and the next shopping action. Overwrite the checkpoint even if "
    "you also keep other voluntary notes."
)
