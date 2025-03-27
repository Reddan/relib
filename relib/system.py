import asyncio
import contextvars
import functools
import json
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Awaitable, Callable, Iterable, ParamSpec, TypeVar
from .utils import noop

P = ParamSpec("P")
R = TypeVar("R")
default_num_workers = min(32, (os.cpu_count() or 1) + 4)
_default_json: Any = {}

def read_json(path: Path, default=_default_json) -> Any:
  if default is not _default_json and not path.exists():
    return default
  with path.open("r") as f:
    return json.load(f)

def write_json(path: Path, obj: Any, indent: None | int = None) -> None:
  with path.open("w") as f:
    return json.dump(obj, f, indent=indent)

def clear_console() -> None:
  os.system("cls" if os.name == "nt" else "clear")

def console_link(text: str, url: str) -> str:
  return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"

async def worker[T](task: Awaitable[T], semaphore: asyncio.Semaphore, update=noop) -> T:
  async with semaphore:
    result = await task
    update()
    return result

async def roll_tasks[T](tasks: Iterable[Awaitable[T]], workers=default_num_workers, progress=False) -> list[T]:
  semaphore = asyncio.Semaphore(workers)
  if not progress:
    return await asyncio.gather(*[worker(task, semaphore) for task in tasks])

  from tqdm import tqdm
  tasks = tasks if isinstance(tasks, list) else list(tasks)
  with tqdm(total=len(tasks)) as pbar:
    update = functools.partial(pbar.update, 1)
    return await asyncio.gather(*[worker(task, semaphore, update) for task in tasks])

def as_async(workers=default_num_workers) -> Callable[[Callable[P, R]], Callable[P, Awaitable[R]]]:
  executor = ThreadPoolExecutor(max_workers=workers)

  def on_fn(func: Callable[P, R]) -> Callable[P, Awaitable[R]]:
    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
      loop = asyncio.get_running_loop()
      ctx = contextvars.copy_context()
      fn_call = functools.partial(ctx.run, func, *args, **kwargs)
      return await loop.run_in_executor(executor, fn_call)
    return wrapper
  return on_fn

def async_limit(workers=default_num_workers) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
  semaphore = asyncio.Semaphore(workers)

  def on_fn(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
      async with semaphore:
        return await func(*args, **kwargs)
    return wrapper
  return on_fn
