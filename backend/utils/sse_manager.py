import asyncio
from typing import Dict


class SSEManager:
    """SSE 连接池管理器"""

    def __init__(self):
        self._queues: Dict[int, list] = {}

    def subscribe(self, assignment_id: int) -> asyncio.Queue:
        if assignment_id not in self._queues:
            self._queues[assignment_id] = []
        q = asyncio.Queue()
        self._queues[assignment_id].append(q)
        return q

    def unsubscribe(self, assignment_id: int, q: asyncio.Queue):
        if assignment_id in self._queues:
            self._queues[assignment_id] = [x for x in self._queues[assignment_id] if x is not q]

    async def publish(self, assignment_id: int, data: dict):
        if assignment_id in self._queues:
            for q in self._queues[assignment_id]:
                await q.put(data)


sse_manager = SSEManager()
