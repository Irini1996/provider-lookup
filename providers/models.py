from django.db import models

# Create your models here.
class Taxonomy(models.Model):
 pass
class Provider(models.Model):
    
    npi_number = models.CharField(max_length=20, unique=True, db_index=True) # NPI unique identifier. 
# Not use Integerfield because NPI numbers can start with 0, unique=true --> No two providers in the table can have the same NPI number.
# db_index=True --> Create an index in the database for this field to make lookups faster so the database will jump straight to that provider instantly instead of searching every row one by one

    enumeration_type = models.CharField(max_length=30, blank=True) # "NPI-1" (individual) or "NPI-2" (organization).
    first_name = models.CharField(max_length=120, blank=True) 
    last_name = models.CharField(max_length=120, blank=True) 
    organization_name = models.CharField(max_length=255, blank=True) 
    address_purpose = models.CharField(max_length=50, blank=True) # Purpose of the stored address: "LOCATION" 
    address_line = models.CharField(max_length=255, blank=True) 
    city = models.CharField(max_length=120, blank=True) 
    state = models.CharField(max_length=10, blank=True) 
    postal_code = models.CharField(max_length=15, blank=True) 
    country_code = models.CharField(max_length=10, blank=True) 
    telephone_number = models.CharField(max_length=30, blank=True) # Phone number can have (+)
    fax_number = models.CharField(max_length=30, blank=True) # Fax number can have (+), (-)
 
     #Creates a field in Provider that points to another model (Taxonomy).
     #This establishes a relationship between the two tables.
     #In the database, this will become a column named taxonomy_id 
    taxonomy = models.ForeignKey(
    Taxonomy,   #This is the target model the foreign key refers to
    on_delete=models.SET_NULL, #If a Taxonomy is deleted, do not delete the Provider, just set the provider’s taxonomy_id field to NULL.”
    null=True, #Tells the database that the field can be empty so it’s okay for a Provider to have no taxonomy assigned
    blank=True, #Tells Django that this field is optional during validation
)
       
    class Meta:
        indexes = [
            models.Index(fields=["last_name", "first_name"]), #Creates an index on last_name and first_name to make name-based lookups faster.
            models.Index(fields=["taxonomy"]), #Creates an index on the taxonomy field to speed up searches by specialty
        ]
      
    
    #Notes
# blank=True --> If the user leaves first_name empty in a form, Django won’t throw a validation error — it will accept it as blank ("").
#For text fields (CharField, TextField): use only blank=True, because we want an empty string, not NULL.
# null=True --> If the provider doesn’t have a taxonomy,the database will store NULL (nothing at all)
# For relations or non-text fields I can use both null=True and blank=True