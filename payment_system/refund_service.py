# payment_system/refund_service.py
from datetime import datetime, timedelta

REFUND_WINDOW_DAYS = 30  # Política: máximo 30 días para solicitar reembolso

class PaymentRepository:
    """Interfaz de acceso a la base de datos de transacciones."""
    def get_payment(self, payment_id: str) -> dict:
        pass  # En producción accede a la BD real

class RefundService:
    """Procesa reembolsos respetando la política de la empresa."""

    def __init__(self, repository: PaymentRepository):
        self.repository = repository

    def process_refund(self, payment_id: str) -> dict:
        payment = self.repository.get_payment(payment_id)
        if not payment:
            return {'success': False, 'reason': 'Pago no encontrado'}
        payment_date = payment['date']
        limit_date   = datetime.now() - timedelta(days=REFUND_WINDOW_DAYS)
        if payment_date < limit_date:
            return {'success': False, 'reason': 'Fuera del plazo de 30 días'}
        if payment.get('refunded'):
            return {'success': False, 'reason': 'Pago ya fue reembolsado'}
        return {'success': True, 'amount': payment['amount'], 'payment_id': payment_id}
