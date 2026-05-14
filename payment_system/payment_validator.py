# payment_system/payment_validator.py

MIN_PAYMENT_AMOUNT = 1.00     # Monto mínimo S/ 1.00
DAILY_LIMIT        = 5000.00  # Límite diario S/ 5,000.00

class PaymentValidator:
    """Valida restricciones de pago antes de procesar."""

    def is_amount_valid(self, amount: float) -> bool:
        """Verifica que el monto sea mayor o igual al mínimo permitido."""
        return amount >= MIN_PAYMENT_AMOUNT

    def is_within_daily_limit(self, amount: float, spent_today: float) -> bool:
        """Verifica que la suma no supere el límite diario."""
        return (spent_today + amount) <= DAILY_LIMIT

    def validate_payment(self, amount: float, spent_today: float) -> dict:
        """Devuelve un dict con el resultado completo de validación."""
        errors = []
        if not self.is_amount_valid(amount):
            errors.append(f'Monto S/{amount:.2f} es menor al mínimo S/{MIN_PAYMENT_AMOUNT:.2f}')
        if not self.is_within_daily_limit(amount, spent_today):
            errors.append(f'Supera el límite diario de S/{DAILY_LIMIT:.2f}')
        return {'valid': len(errors) == 0, 'errors': errors}
