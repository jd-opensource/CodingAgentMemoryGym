"""Keep lightweight tests independent of optional training dependencies."""
import os

# Explicitly opt in after installing the complete Linux training environment.
collect_ignore_glob = [] if os.environ.get("CAMP_TEST_TRAINING") == "1" else ["training/test_*.py"]
