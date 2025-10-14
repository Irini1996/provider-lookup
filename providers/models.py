from django.db import models

# Create your models here.


class Provider(models.Model):
    
    npi_number = models.CharField(max_length=20, unique=True, db_index=True) # NPI unique identifier. 

    enumeration_type = models.CharField(max_length=30, blank=True) # "NPI-1" (individual) or "NPI-2" (organization).

    first_name = models.CharField(max_length=120, blank=True) # Individual's first name. 

    last_name = models.CharField(max_length=120, blank=True) # Individual's last name. API: results[i].basic.last_name

    organization_name = models.CharField(max_length=255, blank=True) # Organization name (for NPI-2). 

    address_purpose = models.CharField(max_length=50, blank=True) # Purpose of the stored address: "LOCATION" 

    address_line1 = models.CharField(max_length=255, blank=True) # Street line 1 

    address_line2 = models.CharField(max_length=255, blank=True) # Street line 2 

    city = models.CharField(max_length=120, blank=True) # City of the stored address. 

    state = models.CharField(max_length=10, blank=True) # State/Province 

    postal_code = models.CharField(max_length=15, blank=True) # ZIP/Postal code. 

    country_code = models.CharField(max_length=10, blank=True) # Country code 

    telephone_number = models.CharField(max_length=30, blank=True) # Phone number for the stored address. 

    fax_number = models.CharField(max_length=30, blank=True) # Fax number for the stored address (if any).

    taxonomy_code = models.CharField(max_length=20, blank=True) # NUCC taxonomy code 

   
