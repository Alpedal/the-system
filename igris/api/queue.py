"""Request queue serializer for sequential GPU processing."""

from __future__ import annotations

import asyncio

# Global asyncio lock to serialize access to the Ollama endpoint.
gpu_lock = asyncio.Lock()
