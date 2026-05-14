# payment_system/payment_processor.py

class PaymentGateway:
    """Interfaz simulada de la pasarela de pagos externa (Ej: Niubiz, PayPal)."""
    def charge(self, amount: float, currency: str, token: str) -> dict:
        # Llamada real a la API externa (simulada en tests con Mock)
        pass

class PaymentProcessor:
    """Procesa el pago usando la pasarela externa."""

    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway

    def process_payment(self, amount: float, currency: str, token: str) -> dict:
        if amount <= 0:
            raise ValueError('Monto debe ser mayor a cero')
        response = self.gateway.charge(amount, currency, token)
        return {
            'success':        response.get('status') == 'approved',
            'transaction_id': response.get('transaction_id'),
            'amount':         amount,
            'currency':       currency,
        }
