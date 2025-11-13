from django.shortcuts import render
from django.db.models import Q, Prefetch
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.core.paginator import Paginator
from .models import Provider, Taxonomy, ProviderTaxonomy
from .serializers import ProviderSerializer, TaxonomySerializer
from django.db.models import Prefetch


#  HTML VIEW — MAIN SEARCH PAGE

def find_provider(request):
    # # Read all search parameters sent via GET request

    first_name = request.GET.get("first_name", "").strip()
    last_name = request.GET.get("last_name", "").strip()
    organization = request.GET.get("organization", "").strip()
    npi = request.GET.get("npi", "").strip()
    address = request.GET.get("address", "").strip()
    city = request.GET.get("city", "").strip()
    state = request.GET.get("state", "").strip()
    postal_code = request.GET.get("postal_code", "").strip()
    taxonomy = request.GET.get("taxonomy", "").strip()

    # Check if user searched something
    searched = any([
        first_name, last_name, organization, npi,
        address, city, state, postal_code, taxonomy
    ])
# Start with all providers before applying filters
    providers = Provider.objects.all()
# Apply filters one-by-one only if each field is provided
    if first_name:
        providers = providers.filter(first_name__icontains=first_name)

    if last_name:
        providers = providers.filter(last_name__icontains=last_name)

    if organization:
        providers = providers.filter(organization_name__icontains=organization)

    if npi:
        providers = providers.filter(npi_number__icontains=npi)

    if address:
        providers = providers.filter(address_line__icontains=address)

    if city:
        providers = providers.filter(city__icontains=city)

    if state:
        providers = providers.filter(state__iexact=state)

    if postal_code:
        clean_zip = postal_code.replace("-", "")
        providers = providers.filter(postal_code__icontains=clean_zip)

    if taxonomy:
        providers = providers.filter(
            Q(providertaxonomy__taxonomy__taxonomy_classification__icontains=taxonomy) |
            Q(providertaxonomy__taxonomy__taxonomy_specialization__icontains=taxonomy)
        )
 # Efficiently load all taxonomy data with a single additional query
    providers = providers.prefetch_related(
        Prefetch(
            "providertaxonomy_set",
            queryset=ProviderTaxonomy.objects.select_related("taxonomy"),
        )
    ).distinct()
    # Pagination: show only 50 providers per page for performance

    paginator = Paginator(providers, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
# Render the page and return all parameters so the form remembers them
    return render(request, "providers/find_provider.html", {
        "providers": page_obj,
        "page_obj": page_obj,
        "searched": searched,

        # RETURN THEM BACK SO TEMPLATE WILL HAVE VALUES
        "first_name": first_name,
        "last_name": last_name,
        "organization": organization,
        "npi": npi,
        "address": address,
        "city": city,
        "state": state,
        "postal_code": postal_code,
        "taxonomy": taxonomy,
    })


  #  API VIEWSETS — These return JSON responses (used for APIs or frontend)

class ProviderViewSet(viewsets.ReadOnlyModelViewSet):
    
    # API endpoint for searching providers with pagination & filters.
    
    queryset = Provider.objects.all() # Base queryset of all providers
    serializer_class = ProviderSerializer  # Convert Provider model instances → JSON fields
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] # Enable filtering + search features from Django REST Framework
    filterset_fields = ["city", "state"] # Fields that can be filtered directly 
    # Fields that can be filtered directly 
    search_fields = [
        "first_name",
        "last_name",
        "organization_name",
        "npi_number",
        "providertaxonomy__taxonomy__taxonomy_classification",
        "providertaxonomy__taxonomy__taxonomy_specialization",
    ]

    def get_queryset(self): # Fields that can be filtered directly 
        query = self.request.query_params.get("q", "").strip()
        taxonomy = self.request.query_params.get("taxonomy", "").strip()

        providers = Provider.objects.all()
# Text search across basic provider fields
        if query:
            providers = providers.filter(
                Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(organization_name__icontains=query)
                | Q(npi_number__icontains=query)
            )
# Taxonomy search 
        if taxonomy:
            providers = providers.filter(
                providertaxonomy__taxonomy__taxonomy_classification__icontains=taxonomy
            )

        return providers.distinct()


class TaxonomyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for taxonomy codes with autocomplete search.
    """

    serializer_class = TaxonomySerializer
    filter_backends = [filters.SearchFilter]
    # These fields are searchable in the autocomplete API
    search_fields = [
        "taxonomy_code",
        "taxonomy_classification",
        "taxonomy_specialization",
    ]
    queryset = Taxonomy.objects.all().order_by("taxonomy_classification") # Return all taxonomy codes, ordered alphabetically

    @action(detail=False, methods=["get"], url_path="autocomplete")
    def autocomplete(self, request):
        """
        Custom endpoint for live taxonomy autocomplete
        """
        term = request.query_params.get("q", "").strip()
        qs = Taxonomy.objects.all()
# Return all taxonomy codes, ordered alphabetically
        if term:
            qs = qs.filter(
                Q(taxonomy_classification__icontains=term)
                | Q(taxonomy_specialization__icontains=term)
                | Q(taxonomy_code__icontains=term)
            )
# Return all taxonomy codes, ordered alphabetically
        data = list(qs.values("taxonomy_code", "taxonomy_classification")[:20])
        return Response(data)
