"""Keep SWE-bench package imports limited to the pinned grading surface."""

from pkgutil import extend_path


__version__ = "4.1.0"
__path__ = extend_path(__path__, __name__)
