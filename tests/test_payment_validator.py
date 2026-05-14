# tests/test_payment_validator.py
import pytest
from payment_system.payment_validator import PaymentValidator

class TestPaymentValidator:

    def setup_method(self):
        self.validator = PaymentValidator()

    # --- Boundary Testing: Monto Mínimo ---
    def test_amount_below_minimum_is_invalid(self):
        # 0.99 < 1.00 → FALLA
        assert self.validator.is_amount_valid(0.99) is False

    def test_amount_at_minimum_is_valid(self):
        # 1.00 == 1.00 → PASA
        assert self.validator.is_amount_valid(1.00) is True

    def test_amount_above_minimum_is_valid(self):
        # 1.01 > 1.00 → PASA
        assert self.validator.is_amount_valid(1.01) is True

    # --- Boundary Testing: Límite Diario ---
    def test_payment_within_daily_limit(self):
        # 3000 + 1999 = 4999 <= 5000 → PASA
        assert self.validator.is_within_daily_limit(1999.0, 3000.0) is True

    def test_payment_exactly_at_daily_limit(self):
        # 3000 + 2000 = 5000 == 5000 → PASA
        assert self.validator.is_within_daily_limit(2000.0, 3000.0) is True

    def test_payment_exceeds_daily_limit(self):
        # 3000 + 2001 = 5001 > 5000 → FALLA
        assert self.validator.is_within_daily_limit(2001.0, 3000.0) is False

    # --- Prueba integral de validate_payment ---
    def test_valid_payment_returns_no_errors(self):
        result = self.validator.validate_payment(100.0, 0.0)
        assert result['valid'] is True
        assert len(result['errors']) == 0

    def test_invalid_amount_returns_error_message(self):
        result = self.validator.validate_payment(0.50, 0.0)
        assert result['valid'] is False
        assert any('mínimo' in e for e in result['errors'])

    def test_exceeded_limit_returns_error_message(self):
        result = self.validator.validate_payment(1000.0, 4500.0)
        assert result['valid'] is False
        assert any('límite diario' in e for e in result['errors'])

    def test_double_failure_returns_two_errors(self):
        # Monto < mínimo Y supera límite
        result = self.validator.validate_payment(0.50, 5000.0)
        assert result['valid'] is False
        assert len(result['errors']) == 2
