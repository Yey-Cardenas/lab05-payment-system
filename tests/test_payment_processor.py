# tests/test_payment_processor.py
import pytest
from unittest.mock import MagicMock
from payment_system.payment_processor import PaymentProcessor

class TestPaymentProcessor:

    def setup_method(self):
        # ARRANGE: Mock de la pasarela de pagos externa
        self.gateway_mock = MagicMock()
        self.processor = PaymentProcessor(self.gateway_mock)

    def test_successful_payment_returns_success_true(self):
        # Arrange: gateway aprueba el pago
        self.gateway_mock.charge.return_value = {
            'status': 'approved',
            'transaction_id': 'TXN-001'
        }
        # Act
        result = self.processor.process_payment(150.0, 'PEN', 'token_abc')
        # Assert
        assert result['success'] is True
        assert result['transaction_id'] == 'TXN-001'
        assert result['amount'] == 150.0

    def test_rejected_payment_returns_success_false(self):
        # Arrange: gateway rechaza el pago
        self.gateway_mock.charge.return_value = {
            'status': 'rejected',
            'transaction_id': None
        }
        # Act
        result = self.processor.process_payment(200.0, 'PEN', 'token_xyz')
        # Assert
        assert result['success'] is False
        assert result['transaction_id'] is None

    def test_gateway_is_called_with_correct_arguments(self):
        # Arrange
        self.gateway_mock.charge.return_value = {'status': 'approved', 'transaction_id': 'T1'}
        # Act
        self.processor.process_payment(75.0, 'USD', 'token123')
        # Assert: verificar que se llamó con los parámetros exactos
        self.gateway_mock.charge.assert_called_once_with(75.0, 'USD', 'token123')

    def test_zero_amount_raises_value_error(self):
        with pytest.raises(ValueError):
            self.processor.process_payment(0.0, 'PEN', 'token')

    def test_negative_amount_raises_value_error(self):
        with pytest.raises(ValueError):
            self.processor.process_payment(-50.0, 'PEN', 'token')

    def test_gateway_not_called_on_invalid_amount(self):
        # Si el monto es inválido, la gateway NO debe ser invocada
        try:
            self.processor.process_payment(-10.0, 'PEN', 'token')
        except ValueError:
            pass
        self.gateway_mock.charge.assert_not_called()
