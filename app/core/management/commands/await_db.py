"""
Command that waits till DB is active.
"""
import time
from typing import Any
from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to wait for DB."""

    def handle(self, *args: Any, **options: Any):
        """Command starting point."""
        self.stdout.write("Waiting for database...")
        is_db_up = False
        while not is_db_up:
            try:
                self.check(databases=["default"])
                is_db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write(
                    self.style.ERROR("Database unavailable,"
                                     " will try again in 1 second...")
                )
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
