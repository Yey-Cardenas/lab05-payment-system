# tests/test_refund_service.py
import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from payment_system.refund_service import RefundService

class TestRefundService:

    def setup_method(self):
        self.repo_mock = MagicMock()
        self.service   = RefundService(self.repo_mock)

    def test_refund_within_30_days_is_successful(self):
        # Arrange: pago de hace 10 días (dentro del plazo)
        self.repo_mock.get_payment.return_value = {
            'amount':   250.0,
            'date':     datetime.now() - timedelta(days=10),
            'refunded': False
        }
        # Act
        result = self.service.process_refund('PAY-100')
        # Assert
        assert result['success'] is True
        assert result['amount'] == 250.0

    def test_refund_after_30_days_is_rejected(self):
        # Arrange: pago de hace 35 días (fuera del plazo)
        self.repo_mock.get_payment.return_value = {
            'amount':   100.0,
            'date':     datetime.now() - timedelta(days=35),
            'refunded': False
        }
        result = self.service.process_refund('PAY-200')
        assert result['success'] is False
        assert 'plazo' in result['reason']

    def test_already_refunded_payment_is_rejected(self):
        # Arrange: pago reciente pero ya reembolsado
        self.repo_mock.get_payment.return_value = {
            'amount':   80.0,
            'date':     datetime.now() - timedelta(days=5),
            'refunded': True
        }
        result = self.service.process_refund('PAY-300')
        assert result['success'] is False
        assert 'reembolsado' in result['reason']

    def test_nonexistent_payment_returns_not_found(self):
        # Arrange: repositorio no encuentra el pago
        self.repo_mock.get_payment.return_value = None
        result = self.service.process_refund('PAY-999')
        assert result['success'] is False
        assert 'no encontrado' in result['reason']

    # --- Boundary Testing: exactamente en el límite de 30 días ---
    def test_refund_exactly_at_day_30_boundary(self):
        # Arrange: pago de exactamente 29 días 23 horas → dentro del plazo
        self.repo_mock.get_payment.return_value = {
            'amount':   120.0,
            'date':     datetime.now() - timedelta(days=29, hours=23),
            'refunded': False
        }
        result = self.service.process_refund('PAY-400')
        assert result['success'] is True
