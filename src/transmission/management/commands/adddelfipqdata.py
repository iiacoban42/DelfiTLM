"""Custom command for populating DelfiPQ buckets.
Run with 'python manage.py adddelfipqdata' """
from django.core.management.base import BaseCommand
from transmission.processing.add_dummy_data import add_dummy_tlm_raw_data
from transmission.processing.process_raw_bucket import process_raw_bucket
# pylint: disable=all
class Command(BaseCommand):
    """Django command class"""

    def handle(self, *args, **options):
        """Populate DelfiPQ influxdb buckets"""
        add_dummy_tlm_raw_data("delfi_pq", "delfipq/delfi-pq.txt")
        process_raw_bucket("delfi_pq", "downlink")
