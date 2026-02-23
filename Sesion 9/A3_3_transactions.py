from enum import Enum
from typing import Callable, List, Dict, Any
import json
import asyncio

class TransactionStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    COMPENSATED = "compensated"

class SagaOrchestrator:
    """Orquesta transacciones distribuidas con compensación."""
    
    def __init__(self, saga_id: str):
        self.saga_id = saga_id
        self.steps: List[Dict[str, Any]] = []
        self.current_step = 0
        self.status = TransactionStatus.PENDING
    
    def add_step(
        self,
        name: str,
        execute_func: Callable[[], Any],
        compensate_func: Callable[[Any], Any]
    ):
        """Añade paso a la saga."""
        self.steps.append({
            "name": name,
            "execute": execute_func,
            "compensate": compensate_func,
            "status": TransactionStatus.PENDING,
            "result": None
        })
    
    async def execute(self) -> Dict[str, Any]:
        """Ejecuta la saga con compensación automática."""
        try:
            # Ejecutar todos los pasos
            for i, step in enumerate(self.steps):
                self.current_step = i
                
                print(f"[{step['name']}] Executing...")
                result = await step['execute']()
                
                step['status'] = TransactionStatus.COMPLETED
                step['result'] = result
                
                print(f"[{step['name']}] ✓ Completed")
            
            self.status = TransactionStatus.COMPLETED
            return {
                "saga_id": self.saga_id,
                "status": "success",
                "steps": [
                    {
                        "name": s['name'],
                        "status": s['status'].value,
                        "result": s['result']
                    }
                    for s in self.steps
                ]
            }
        
        except Exception as e:
            print(f"[ERROR] {str(e)}")
            print(f"[COMPENSATING] Rolling back from step {self.current_step}")
            
            # Compensar en orden inverso
            for i in range(self.current_step, -1, -1):
                step = self.steps[i]
                
                try:
                    print(f"[{step['name']}] Compensating...")
                    await step['compensate'](step['result'])
                    
                    step['status'] = TransactionStatus.COMPENSATED
                    print(f"[{step['name']}] ✓ Compensated")
                
                except Exception as comp_error:
                    print(f"[{step['name']}] ✗ Compensation failed: {comp_error}")
                    # Log para intervención manual
            
            self.status = TransactionStatus.FAILED
            return {
                "saga_id": self.saga_id,
                "status": "failed",
                "error": str(e),
                "steps": [
                    {
                        "name": s['name'],
                        "status": s['status'].value,
                        "result": s['result']
                    }
                    for s in self.steps
                ]
            }

# Funciones de ejemplo (integra con Graph batch aquí)
async def reserve_inventory():
    print("→ Reservando inventario en Planner...")
    # await graph_batch([{"endpoint": "/planner/tasks", ...}])
    return {"reservation_id": "RES-001"}

async def undo_reserve(result):
    print(f"↶ Liberando {result['reservation_id']}")

async def charge_payment():
    print("→ Cargando pago via Stripe/Graph...")
    return {"transaction_id": "TXN-001"}

async def refund_payment(result):
    print(f"↶ Reembolsando {result['transaction_id']}")

async def ship_order():
    print("→ Creando envío en Outlook/Teams...")
    # Simular fallo para demo compensación
    raise Exception("Envío falló: transportista no disponible")

async def cancel_shipment(result):
    print(f"↶ Cancelando {result.get('tracking_id', 'N/A')}")

async def main():
    """Función principal para ejecutar saga."""
    saga = SagaOrchestrator("ORDER-12345")
    saga.add_step("ReserveInventory", reserve_inventory, undo_reserve)
    saga.add_step("ChargePayment", charge_payment, refund_payment)
    saga.add_step("ShipOrder", ship_order, cancel_shipment)
    
    result = await saga.execute()
    print(json.dumps(result, indent=2, default=str))

if __name__ == "__main__":
    asyncio.run(main())
