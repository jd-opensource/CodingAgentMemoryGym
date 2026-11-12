"""Register the on-policy distillation training components."""
from camp import token_gae
from .agent_loop import AMGTaskNeutralAgentLoop
from .trainer import AMGPPOTrainerSeparateAsync
