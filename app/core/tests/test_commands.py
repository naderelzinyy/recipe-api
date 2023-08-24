"""
Test Django commands.
"""

from unittest.mock import patch

from django.test import SimpleTestCase
from django.core.management import call_command


@patch('core.management.commands.await_db.Command.check')
class CommandTest(SimpleTestCase):
    """Test management command."""

    def test_await_db_ready(self, patched_check):
        """Test await_db command."""
        patched_check.return_value = True
        call_command('await_db')
        patched_check.assert_called_once_with(databases=['default'])

    # @patch("time.sleep")
    # def test_await_db_delay(self, patched_sleep, patched_check):
    #     """Test waiting for DB when getting errors."""
    #     patched_check.side_effect = [Error] * 2 + \
    #     [OperationalError] * 3 + [True]
    #     call_command("await_db")
    #     self.assertEqual(patched_check.call_count, 6)
    #     patched_check.assert_called_with(databases=["default"])
