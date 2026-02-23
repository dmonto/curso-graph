import asyncio
from typing import List, Callable, Dict, Any
from datetime import datetime, timedelta

class BatchProcessor:
    """Procesa mensajes en lotes."""
    
    def __init__(self, batch_size: int = 100, timeout_seconds: int = 5):
        self.batch_size = batch_size
        self.timeout = timeout_seconds
        self.batch = []
        self.lock = asyncio.Lock()
        self.last_flush = datetime.now()
    
    async def add(self, item: Any) -> bool:
        """Añade item al lote."""
        async with self.lock:
            self.batch.append(item)
            
            # Check si debe procesarse
            should_flush = (
                len(self.batch) >= self.batch_size or
                (datetime.now() - self.last_flush).seconds >= self.timeout
            )
            
            return should_flush
    
    async def flush(self, process_func: Callable) -> Dict[str, Any]:
        """Procesa lote actual."""
        async with self.lock:
            if not self.batch:
                return {"processed": 0, "status": "empty"}
            
            batch_copy = self.batch.copy()
            self.batch.clear()
            self.last_flush = datetime.now()
        
        # Procesar fuera del lock
        try:
            result = await process_func(batch_copy)
            return {
                "processed": len(batch_copy),
                "status": "success",
                "result": result
            }
        except Exception as e:
            return {
                "processed": 0,
                "status": "error",
                "error": str(e),
                "batch": batch_copy  # Para retry
            }
    
    async def run(self, process_func: Callable):
        """Ejecuta procesamiento continuo."""
        while True:
            # Check timeout
            if (datetime.now() - self.last_flush).seconds >= self.timeout:
                await self.flush(process_func)
            
            # Check size (sin lock)
            async with self.lock:
                if len(self.batch) >= self.batch_size:
                    await self.flush(process_func)
            
            await asyncio.sleep(1)

# USO CORREGIDO
async def process_batch(items: List[Any]) -> Dict[str, Any]:
    """Procesa lote de items."""
    print(f"Processing batch of {len(items)} items")
    # Proceso
    return {"saved": len(items)}

async def main():
    processor = BatchProcessor(batch_size=5, timeout_seconds=3)  # Pequeño para demo
    
    # Añadir items
    for i in range(15):  # Reducido para demo rápida
        should_flush = await processor.add({"id": i, "data": f"item_{i}"})
        if should_flush:
            result = await processor.flush(process_batch)
            print(f"Flush result: {result}")
    
    # Procesar restantes
    await asyncio.sleep(4)  # Esperar timeout
    result = await processor.flush(process_batch)
    print(f"Final flush: {result}")

if __name__ == "__main__":
    asyncio.run(main())
