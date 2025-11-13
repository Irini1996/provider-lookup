from django.contrib import admin
from .models import Provider, Taxonomy, ProviderTaxonomy

admin.site.register(Provider)
admin.site.register(Taxonomy)
admin.site.register(ProviderTaxonomy)