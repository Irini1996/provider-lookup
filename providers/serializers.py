from rest_framework import serializers
from .models import Provider, Taxonomy, ProviderTaxonomy


class TaxonomySerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxonomy
        fields = ["taxonomy_code", "taxonomy_classification", "taxonomy_specialization"]


class ProviderTaxonomySerializer(serializers.ModelSerializer):
    taxonomy = TaxonomySerializer(read_only=True)

    class Meta:
        model = ProviderTaxonomy
        fields = ["taxonomy", "is_primary"]


class ProviderSerializer(serializers.ModelSerializer):
    taxonomies = ProviderTaxonomySerializer(
        source="providertaxonomy_set", many=True, read_only=True
    )

    class Meta:
        model = Provider
        fields = [
            "id",
            "npi_number",
            "first_name",
            "last_name",
            "organization_name",
            "city",
            "state",
            "postal_code",
            "telephone_number",
            "fax_number",
            "taxonomies",
        ]
