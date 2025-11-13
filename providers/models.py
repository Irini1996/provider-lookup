from django.db import models

# Create your models here.
from django.db import models
# Provider Model
# Stores basic provider (doctor / organization) information
# Data source: NPI Registry API

class Provider(models.Model):

    npi_number = models.CharField(max_length=20, unique=True)
    enumeration_type = models.CharField(max_length=30, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    organization_name = models.CharField(max_length=100, blank=True)
    address_purpose = models.CharField(max_length=50, blank=True)  
    address_line = models.CharField(max_length=100, blank=True)     
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=150, blank=True)
    country_code = models.CharField(max_length=100, blank=True)
    telephone_number = models.CharField(max_length=100, blank=True)
    fax_number = models.CharField(max_length=100, blank=True)


    class Meta:  ## Meta gives special instructions to Django about how to handle this model
             db_table = "provider"    # Use this exact table name ("provider") in the database
             indexes = [
            models.Index(fields=["first_name"]),
            models.Index(fields=["last_name"]),
            models.Index(fields=["organization_name"]),
            models.Index(fields=["npi_number"]),
            models.Index(fields=["address_line"]),
            models.Index(fields=["city"]),
            models.Index(fields=["state"]),
            models.Index(fields=["postal_code"]),
        ]

    def __str__(self):  #self refers to the current instance of the class
        # This method defines how each Provider object will be displayed as text
        # When you print a Provider or see it in the Django Admin, this text appears
        return f"{self.first_name} {self.last_name} ({self.npi_number})"
    

# Taxonomy Model
# Defines medical specialties (NUCC taxonomy data)
class Taxonomy(models.Model):
    
    taxonomy_code = models.CharField(max_length=10, unique=True)    # NUCC Code (unique)
    taxonomy_classification = models.CharField(max_length=255, blank=True)
    taxonomy_specialization = models.CharField(max_length=255, blank=True)

class Meta:
    db_table = "taxonomy"
    indexes = [
        models.Index(fields=["taxonomy_code"]),
        models.Index(fields=["taxonomy_classification"]),
        models.Index(fields=["taxonomy_specialization"]),
    ]


    def __str__(self):
        # Shows how each Taxonomy will appear as text (in Admin or shell)
        return f"{self.taxonomy_code} - {self.taxonomy_classification}"
    


# Provider ↔ Taxonomy Join Table (Many-to-Many Relationship)
# A provider may have multiple taxonomy specialties
# A taxonomy code may belong to multiple providers

class ProviderTaxonomy(models.Model):

    provider = models.ForeignKey(  # Creates a link to a Provider 
        Provider, on_delete=models.CASCADE  # If a Provider is deleted, remove related links automatically
    )

    taxonomy = models.ForeignKey(  # Creates a link to a Taxonomy 
        Taxonomy, on_delete=models.CASCADE  # If a Taxonomy is deleted, remove related links automatically
    )

    is_primary = models.BooleanField(default=False)  # True if this is the provider’s main specialty

class Meta:
    db_table = "provider_taxonomy"
    indexes = [
        models.Index(fields=["provider"]),
        models.Index(fields=["taxonomy"]),
    ]
    def __str__(self):
        return f"{self.provider.npi_number} → {self.taxonomy.taxonomy_code}"

    #Notes
# blank=True --> If the user leaves first_name empty in a form, Django won’t throw a validation error — it will accept it as blank ("").
# For text fields (CharField, TextField): use only blank=True, because we want an empty string, not NULL.
# null=True --> If the provider doesn’t have a taxonomy,the database will store NULL (nothing at all)
# For relations or non-text fields I can use both null=True and blank=True
# The class Meta was added to define simple database table names, making the models cleaner and easier to manage.