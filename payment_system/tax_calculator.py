# payment_system/tax_calculator.py

TAX_RATES = {
    'general':   0.18,   # IGV estándar 18%
    'food':      0.00,   # Alimentos básicos exentos
    'luxury':    0.30,   # Productos de lujo 30%
    'medicine':  0.00,   # Medicamentos exentos
}

class TaxCalculator:
    """Calcula el impuesto aplicable a un monto según el tipo de producto."""

    def calculate_tax(self, amount: float, product_type: str) -> float:
        if amount < 0:
            raise ValueError('El monto no puede ser negativo')
        rate = TAX_RATES.get(product_type, TAX_RATES['general'])
        return round(amount * rate, 2)

    def calculate_total_with_tax(self, amount: float, product_type: str) -> float:
        tax = self.calculate_tax(amount, product_type)
        return round(amount + tax, 2)
