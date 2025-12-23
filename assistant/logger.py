from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Iterable, List

from .models import ConversationMessage


class ConversationLogger:
    """Simple JSONL logger for assistant conversations."""

    def __init__(self, log_path: str | Path = "conversation_log.jsonl") -> None:
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, message: ConversationMessage) -> None:
        record = {
            "role": message.role,
            "content": message.content,
            "timestamp": message.timestamp.isoformat(),
        }
        with self.log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    def load(self) -> List[ConversationMessage]:
        if not self.log_path.exists():
            return []

        messages: List[ConversationMessage] = []
        with self.log_path.open("r", encoding="utf-8") as fh:
            for line in fh:
                if not line.strip():
                    continue
                payload = json.loads(line)
                messages.append(
                    ConversationMessage(
                        role=payload["role"],
                        content=payload["content"],
                        timestamp=datetime.fromisoformat(payload["timestamp"]),
                    )
                )
        return messages

    def extend(self, messages: Iterable[ConversationMessage]) -> None:
        for msg in messages:
            self.append(msg)
