"""Register the task-reward RL training components."""
from camp import token_gae
from .agent_loop import AMGTaskNeutralAgentLoop
from .trainer import AMGPPOTrainerSeparateAsync
