from typing import Dict, Any
from datetime import datetime
import redis
import time

class VisitCounterService:
    def __init__(self):
        """Initialize the visit counter service with Redis and cache"""

        self._visit_counts: Dict[str, int] = {}
  
        self.redis_client = redis.Redis(
            host='redis1',
            port=6379,
            decode_responses=True
        )
        
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.cache_ttl = 5 
        
        self.use_redis = True  

    async def increment_visit(self, page_id: str) -> Dict[str, Any]:
        """
        Increment visit count for a page and return the response
        All writes go directly to Redis, then update cache
        """
        if self.use_redis:
            count = self.redis_client.incr(f"page:{page_id}")
            
            self._cache[page_id] = {
                'count': count,
                'timestamp': time.time()
            }
            
            return {
                "visits": count,
                "served_via": "redis"
            }
        else:
            if page_id not in self._visit_counts:
                self._visit_counts[page_id] = 0
            self._visit_counts[page_id] += 1
            return {
                "visits": self._visit_counts[page_id],
                "served_via": "in_memory"
            }

    async def get_visit_count(self, page_id: str) -> Dict[str, Any]:
        """
        Get current visit count for a page
        First check cache, then fall back to Redis
        """
        if not self.use_redis:
            count = self._visit_counts.get(page_id, 0)
            return {
                "visits": count,
                "served_via": "in_memory"
            }

        cached_data = self._cache.get(page_id)
        current_time = time.time()
        
        if cached_data and (current_time - cached_data['timestamp']) < self.cache_ttl:

            return {
                "visits": cached_data['count'],
                "served_via": "in_memory"
            }
        
        count = self.redis_client.get(f"page:{page_id}")
        count = int(count) if count else 0
        
        self._cache[page_id] = {
            'count': count,
            'timestamp': current_time
        }
        
        return {
            "visits": count,
            "served_via": "redis"
        }