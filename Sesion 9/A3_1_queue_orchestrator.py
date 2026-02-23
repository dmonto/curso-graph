from persistqueue import SQLiteQueue # pip install persist-queue
import json
from datetime import datetime
import threading  # Thread-safe

class QueueOrchestrator:
    def __init__(self, queue_name, db_path="./queues"):
        """
        queue_name: "orders-queue"
        db_path: "./queues/orders-queue.db" (auto-crea)
        """
        self.queue_name = queue_name
        self.db_path = f"{db_path}/{queue_name}.db"
        self.queue = SQLiteQueue(self.db_path, auto_commit=True, multithreading=True)
    
    def enqueue(self, message_data, priority=0):
        """Añade mensaje a la cola (misma API)."""
        message = {
            "priority": priority,
            "data": message_data,
            "timestamp": datetime.now().isoformat()
        }
        self.queue.put(json.dumps(message))
        return True
    
    def dequeue(self, visibility_timeout=300):
        """Obtiene mensaje (simula visibility con lock temporal)."""
        if not self.queue.empty():
            message_str = self.queue.get()
            self.queue.task_done()  # Marca como "processing"
            return {
                "id": hash(message_str),  # Pseudo-ID
                "body": json.loads(message_str),
                "pop_receipt": f"temp_{datetime.now().timestamp()}"  # Simulado
            }
        return None
    
    def delete_message(self, message_id, pop_receipt):
        """"Elimina" ya consumido (task_done previo)."""
        # No-op ya que dequeue ya lo "elimina" de queue
        print(f"Message {message_id} completed.")
        return True
    
    def get_queue_stats(self):
        """Estadísticas (pending + total)."""
        pending = self.queue.qsize()
        return {
            "approximate_message_count": pending,
            "metadata": {"queue_name": self.queue_name, "db_path": self.db_path}
        }

# USO (IDÉNTICO)
queue = QueueOrchestrator("orders-queue")

# Productor
queue.enqueue({"order_id": "ORD-001", "items": [1, 2, 3]}, priority=1)

# Consumidor
message = queue.dequeue()
if message:
    print(f"Processing: {message['body']}")
    # Procesar Graph/Dataverse...
    queue.delete_message(message['id'], message['pop_receipt'])
    print(queue.get_queue_stats())
