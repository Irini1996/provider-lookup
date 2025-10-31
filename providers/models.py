from django.db import models

# Create your models here.

class Provider(models.Model):
    
    npi_number = models.CharField(max_length=20, unique=True,) # NPI unique identifier. unique=true --> No two providers in the table can have the same NPI number.
    enumeration_type = models.CharField(max_length=30, blank=True) # "NPI-1" (individual) or "NPI-2" (organization).
    first_name = models.CharField(max_length=50, blank=True) 
    last_name = models.CharField(max_length=50, blank=True) 
    organization_name = models.CharField(max_length=100, blank=True) 
    address_purpose = models.CharField(max_length=50, blank=True) # Purpose of the stored address:"LOCATION" 
    address_line = models.CharField(max_length=100, blank=True) 
    city = models.CharField(max_length=50, blank=True) 
    state = models.CharField(max_length=10, blank=True) 
    postal_code = models.CharField(max_length=15, blank=True) 
    country_code = models.CharField(max_length=10, blank=True) 
    telephone_number = models.CharField(max_length=30, blank=True) # Phone number can have (+)
    fax_number = models.CharField(max_length=30, blank=True) # Fax number can have symbols as (+), (-)
 
    
    class Meta:
        db_table = "provider"   #db_table → sets the exact table name in the database. Without this line, Django would name the table "providers_provider" automatically.
        


class Taxonomy(models.Model):
    taxonomy_code = models.CharField(max_length=10, unique=True) # unique=True → each taxonomy code appears only once in the table.
    taxonomy_classification = models.CharField(max_length=50, blank=True,)
    taxonomy_specialization = models.CharField(max_length=50, blank=True,)
# deleting a Provider or a Taxonomy will automatically delete all related ProviderTaxonomy records.
    class Meta:
        db_table = "taxonomy"  

#Connects providers and taxonomies using foreign keys and includes a Boolean field (is_primary) to mark the provider’s main specialty. 
#Django automatically uses the id of each model as the foreign key.
class ProviderTaxonomy(models.Model):
    provider = models.ForeignKey( Provider, on_delete=models.CASCADE,) #It links each record to a provider through the NPI number. 
    taxonomy = models.ForeignKey( Taxonomy,on_delete=models.CASCADE,)  #It links each record to a specialty (taxonomy).
    is_primary = models.BooleanField(default=False) # Shows whether a taxonomy is the provider’s main specialty, True for primary, False for secondary

    class Meta:
        db_table = "provider_taxonomy"
    
    #Notes
# blank=True --> If the user leaves first_name empty in a form, Django won’t throw a validation error — it will accept it as blank ("").
# For text fields (CharField, TextField): use only blank=True, because we want an empty string, not NULL.
# null=True --> If the provider doesn’t have a taxonomy,the database will store NULL (nothing at all)
# For relations or non-text fields I can use both null=True and blank=True
# The class Meta was added to define simple database table names, making the models cleaner and easier to manage.