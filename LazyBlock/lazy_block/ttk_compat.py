"""Compatibility helpers for ttkbootstrap imports.

This project styles the UI with ``ttkbootstrap``.  The package is small, but it
isn't always available in the execution environment that runs the automated
checks for this kata.  Previously ``import ttkbootstrap`` raised a
``ModuleNotFoundError`` and prevented the rest of the code base from running at
all.  To make the demo usable everywhere we try to import the real library and
fall back to the standard :mod:`tkinter.ttk` widgets when it is missing.

The fallback still exposes a ``Window`` class so that the rest of the code does
not need to change.  When ``ttkbootstrap`` is installed nothing changes – the
library is used exactly as before.
"""

from __future__ import annotations

from typing import Any

try:  # pragma: no cover - exercised indirectly when ttkbootstrap is present
    import ttkbootstrap as ttk  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - default path in CI
    import tkinter as tk
    from tkinter import ttk as _ttk

    class _Window(tk.Tk):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            kwargs.pop("themename", None)
            super().__init__(*args, **kwargs)

    class _BootstrapShim:
        """Expose a subset of ttkbootstrap's API backed by tkinter.ttk."""

        Window = _Window

        def __getattr__(self, name: str) -> Any:
            return getattr(_ttk, name)

    ttk = _BootstrapShim()  # type: ignore

__all__ = ["ttk"]