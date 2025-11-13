from django.core.management.base import BaseCommand
from providers.models import Provider, Taxonomy, ProviderTaxonomy
import csv
from pathlib import Path

class Command(BaseCommand):
    help = "Import provider-taxonomy links using bulk inserts"

    def handle(self, *args, **kwargs):
        file_path = Path("Original_data/npidata_pfile_20050523-20251109.csv")  

        if not file_path.exists():
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        taxonomies = {t.taxonomy_code: t for t in Taxonomy.objects.all()}
        providers = {p.npi_number: p for p in Provider.objects.all()}

        self.stdout.write(self.style.SUCCESS(f"✅ Loaded {len(taxonomies)} taxonomy definitions."))
        self.stdout.write(self.style.SUCCESS(f"✅ Loaded {len(providers)} providers into memory."))

        buffer = []
        batch_size = 10000
        total = 0

        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                npi = row.get("NPI")
                if not npi:
                    continue

                provider = providers.get(npi)
                if not provider:
                    continue

                # 🔹 Διαβάζει όλες τις 15 στήλες Taxonomy Code
                taxonomy_codes = [
                    row.get(f"Healthcare Provider Taxonomy Code_{i}", "").strip()
                    for i in range(1, 16)
                ]
                taxonomy_codes = [code for code in taxonomy_codes if code]

                for taxonomy_code in taxonomy_codes:
                    taxonomy = taxonomies.get(taxonomy_code)
                    if taxonomy:
                        buffer.append(ProviderTaxonomy(provider=provider, taxonomy=taxonomy))

                if len(buffer) >= batch_size:
                    ProviderTaxonomy.objects.bulk_create(buffer, ignore_conflicts=True)
                    total += len(buffer)
                    buffer.clear()
                    self.stdout.write(f"Linked {total} provider-taxonomy records...")

        if buffer:
            ProviderTaxonomy.objects.bulk_create(buffer, ignore_conflicts=True)
            total += len(buffer)

        self.stdout.write(self.style.SUCCESS(f" Successfully linked {total} provider-taxonomy records in total!"))
