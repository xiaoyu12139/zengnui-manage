from typing import Callable, Dict, List, Any, Tuple
import threading

class EventBus:
    def __init__(self):
        self._subs: Dict[str, List[Tuple[Callable[..., Any], bool]]] = {}
        self._lock = threading.RLock()

    def subscribe(self, topic: str, handler: Callable[..., Any], *, once: bool = False) -> None:
        with self._lock:
            lst = self._subs.setdefault(topic, [])
            if not any(h is handler for h, _ in lst):
                lst.append((handler, once))

    def unsubscribe(self, topic: str, handler: Callable[..., Any]) -> None:
        with self._lock:
            lst = self._subs.get(topic)
            if not lst:
                return
            self._subs[topic] = [(h, o) for (h, o) in lst if h is not handler]
            if not self._subs[topic]:
                del self._subs[topic]

    def publish(self, topic: str, *args, **kwargs) -> None:
        with self._lock:
            lst = list(self._subs.get(topic, []))
        to_remove: List[Callable[..., Any]] = []
        for handler, once in lst:
            try:
                handler(*args, **kwargs)
            finally:
                if once:
                    to_remove.append(handler)
        for h in to_remove:
            self.unsubscribe(topic, h)

    def request(self, topic: str, *args, **kwargs) -> Any:
        with self._lock:
            lst = list(self._subs.get(topic, []))
        result = None
        for handler, once in lst:
            result = handler(*args, **kwargs)
            if once:
                self.unsubscribe(topic, handler)
            if result is not None:
                break
        return result

