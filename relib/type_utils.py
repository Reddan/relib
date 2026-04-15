from typing import Any
from .types import T, T1, T2

__all__ = [
  "as_any",
  "coalesce",
  "ensure_tuple",
  "non_none",
]

def as_any(obj: Any) -> Any:
  return obj

def coalesce(obj: T1 | None, default: T2) -> T1 | T2:
  return default if obj is None else obj

def non_none(obj: T | None) -> T:
  assert obj is not None
  return obj

def ensure_tuple(value: T | tuple[T, ...]) -> tuple[T, ...]:
  return value if isinstance(value, tuple) else (value,)
