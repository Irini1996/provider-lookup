from django.core.management.base import BaseCommand
from providers.models import Provider
import csv
from pathlib import Path
from django.db import transaction

class Command(BaseCommand):
    help = "Efficiently import providers from large NPI CSV in batches"

    def handle(self, *args, **kwargs):
        csv_path = Path("Original_data/npidata_pfile_20050523-20251109.csv")



        if not csv_path.exists():
            self.stdout.write(self.style.ERROR(f"File not found: {csv_path}"))
            return

        batch_size = 10000  # number of records to insert per batch
        providers = []
        total = 0

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for i, row in enumerate(reader, start=1):
                provider = Provider(
                    npi_number=row.get("NPI", "").strip(),
                    enumeration_type=row.get("Entity Type Code", "").strip(),
                    first_name=row.get("Provider First Name", "").strip(),
                    last_name=row.get("Provider Last Name (Legal Name)", "").strip(),
                    organization_name=row.get("Provider Organization Name (Legal Business Name)", "").strip(),
                    address_purpose=row.get("Provider Business Mailing Address Address Purpose", "").strip(),
                    address_line=row.get("Provider Business Mailing Address Line 1", "").strip(),
                    city=row.get("Provider Business Mailing Address City Name", "").strip(),
                    state=row.get("Provider Business Mailing Address State Name", "").strip(),
                    postal_code=row.get("Provider Business Mailing Address Postal Code", "").strip(),
                )
                providers.append(provider)

                # Bulk insert every batch_size rows
                if i % batch_size == 0:
                    with transaction.atomic():
                        Provider.objects.bulk_create(providers, ignore_conflicts=True)
                    total += len(providers)
                    self.stdout.write(f"✅ Inserted {total:,} providers...")
                    providers.clear()

            # Insert remaining
            if providers:
                with transaction.atomic():
                    Provider.objects.bulk_create(providers, ignore_conflicts=True)
                total += len(providers)

        self.stdout.write(self.style.SUCCESS(f"🎉 Done! Imported {total:,} providers."))
