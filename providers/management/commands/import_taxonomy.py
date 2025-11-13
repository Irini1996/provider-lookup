from django.core.management.base import BaseCommand
from providers.models import Taxonomy
import csv
from pathlib import Path

class Command(BaseCommand):
    help = "Import taxonomy codes from NUCC taxonomy CSV file"

    def handle(self, *args, **kwargs):
        file_path = Path("providers/data/nucc_taxonomy.csv")

        if not file_path.exists():
            self.stdout.write(self.style.ERROR(f"❌ File not found: {file_path}"))
            return

        taxonomies = []
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                taxonomies.append(Taxonomy(
                    taxonomy_code=row.get("Code", "").strip(),
                    taxonomy_classification=row.get("Classification", "").strip(),
                    taxonomy_specialization=row.get("Specialization", "").strip(),
                ))

        Taxonomy.objects.bulk_create(taxonomies, batch_size=1000)
        self.stdout.write(self.style.SUCCESS(f"✅ Imported {len(taxonomies)} taxonomies."))

