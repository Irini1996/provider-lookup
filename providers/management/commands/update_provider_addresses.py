from django.core.management.base import BaseCommand
from providers.models import Provider
from django.db import connection
from pathlib import Path
import csv, time, re, tempfile


class Command(BaseCommand):
    help = "⚡ Ultra-fast provider address loader using PostgreSQL COPY + single UPDATE"

    def handle(self, *args, **kwargs):
        file_path = Path("Original_data/npidata_pfile_20050523-20251109.csv")
        if not file_path.exists():
            self.stdout.write(self.style.ERROR(f"❌ File not found: {file_path}"))
            return

        tmp_csv = Path(tempfile.gettempdir()) / "provider_addresses.csv"

        # ✅ Cache NPIs για lookup
        provider_npis = set(Provider.objects.values_list("npi_number", flat=True))
        self.stdout.write(self.style.SUCCESS(f"✅ Loaded {len(provider_npis):,} provider NPIs into memory."))

        count = 0
        start = time.time()

        # 🧹 Δημιουργία cleaned CSV
        with open(file_path, newline="", encoding="utf-8") as src, open(tmp_csv, "w", newline="", encoding="utf-8") as dst:
            reader = csv.DictReader(src)
            writer = csv.writer(dst)
            writer.writerow(["npi", "address", "city", "state", "postal", "phone"])

            for row in reader:
                npi = row.get("NPI", "").strip()
                if npi not in provider_npis:
                    continue

                addr1 = row.get("Provider First Line Business Practice Location Address", "").strip()
                addr2 = row.get("Provider Second Line Business Practice Location Address", "").strip()
                address = re.sub(r"\s+", " ", f"{addr1} {addr2}".strip())[:255]

                city = row.get("Provider Business Practice Location Address City Name", "").strip()[:100]
                state = row.get("Provider Business Practice Location Address State Name", "").strip()[:10]
                postal = re.sub(r"[^0-9A-Za-z-]", "", row.get("Provider Business Practice Location Address Postal Code", ""))[:10]
                phone = re.sub(r"\D", "", row.get("Provider Business Practice Location Address Telephone Number", ""))[:15]

                if not any([address, city, state, postal, phone]):
                    continue

                writer.writerow([npi, address, city, state, postal, phone])
                count += 1

        elapsed = time.time() - start
        self.stdout.write(self.style.SUCCESS(f"✅ Prepared {count:,} cleaned rows in {elapsed:.1f}s"))
        self.stdout.write("📥 Loading into PostgreSQL via COPY...")

        # 🚀 COPY + single UPDATE (super fast)
        start_copy = time.time()
        with connection.cursor() as cursor:
            # Drop + recreate safely
            cursor.execute("DROP TABLE IF EXISTS tmp_provider_addr;")
            cursor.execute("""
                CREATE TEMP TABLE tmp_provider_addr (
                    npi varchar(20),
                    address varchar(255),
                    city varchar(100),
                    state varchar(10),
                    postal varchar(10),
                    phone varchar(20)
                );
            """)

            # COPY directly from file
            with open(tmp_csv, "r", encoding="utf-8") as f:
                next(f)  # skip header
                cursor.copy_expert("COPY tmp_provider_addr FROM STDIN WITH CSV", f)

            self.stdout.write(self.style.SUCCESS("📦 Data copied to PostgreSQL temp table."))

            # Add index on npi for ultra-fast join
            cursor.execute("CREATE INDEX idx_tmp_npi ON tmp_provider_addr(npi);")

            # Update in one SQL
            self.stdout.write("⚙️ Updating provider table (please wait)...")
            cursor.execute("""
                UPDATE provider p
                   SET address_line = t.address,
                       city = t.city,
                       state = t.state,
                       postal_code = t.postal,
                       telephone_number = t.phone
                  FROM tmp_provider_addr t
                 WHERE p.npi_number = t.npi;
            """)

            updated_rows = cursor.rowcount

        total_time = time.time() - start
        copy_time = time.time() - start_copy
        self.stdout.write(self.style.SUCCESS(f"✅ PostgreSQL COPY finished in {copy_time:.1f}s"))
        self.stdout.write(self.style.SUCCESS(f"🏁 Done! Updated {updated_rows:,} providers in {total_time:.1f}s total."))
