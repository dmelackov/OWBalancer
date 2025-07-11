from redis.asyncio import Redis, ConnectionPool

class AsyncRedisEngine:
    def __init__(self, redis_url: str):
        self.redis_pool = ConnectionPool.from_url(redis_url, max_connections=10)
    
    async def close(self):
        if self.redis_pool is None:
            return
        await self.redis_pool.disconnect()
        self.redis_pool = None

    async def get_connection(self):
        return Redis(connection_pool=self.redis_pool)

def get_redis_url(ip="localhost", port=6379, db="0"):
    return f"redis://{ip}:{port}/{db}"