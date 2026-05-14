# tests/test_tax_calculator.py
import pytest
from payment_system.tax_calculator import TaxCalculator

class TestTaxCalculator:

    def setup_method(self):
        """ARRANGE global: instancia reutilizada en cada test."""
        self.calc = TaxCalculator()

    # --- Pruebas de cálculo estándar (IGV 18%) ---
    def test_general_tax_is_18_percent(self):
        # Arrange
        amount = 100.0
        # Act
        tax = self.calc.calculate_tax(amount, 'general')
        # Assert
        assert tax == 18.0

    def test_food_product_is_tax_exempt(self):
        # Arrange & Act
        tax = self.calc.calculate_tax(500.0, 'food')
        # Assert: alimentos no pagan IGV
        assert tax == 0.0

    def test_luxury_product_tax_is_30_percent(self):
        tax = self.calc.calculate_tax(1000.0, 'luxury')
        assert tax == 300.0

    def test_medicine_is_tax_exempt(self):
        tax = self.calc.calculate_tax(200.0, 'medicine')
        assert tax == 0.0

    def test_unknown_type_defaults_to_general_rate(self):
        # Tipo desconocido debe usar 18% (IGV general)
        tax = self.calc.calculate_tax(100.0, 'electronics')
        assert tax == 18.0

    # --- Boundary Testing ---
    def test_zero_amount_returns_zero_tax(self):
        # Límite inferior: monto = 0
        tax = self.calc.calculate_tax(0.0, 'general')
        assert tax == 0.0

    def test_negative_amount_raises_value_error(self):
        # Valor fuera de límite debe lanzar excepción
        with pytest.raises(ValueError, match='negativo'):
            self.calc.calculate_tax(-10.0, 'general')

    def test_total_with_tax_general(self):
        total = self.calc.calculate_total_with_tax(100.0, 'general')
        assert total == 118.0

    def test_total_with_tax_food_unchanged(self):
        total = self.calc.calculate_total_with_tax(50.0, 'food')
        assert total == 50.0
