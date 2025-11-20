# Provider Lookup Project

The objective of this project is to create a system that allows users to search for and locate Healthcare providers. 

## Data Sources

- [NPI Registry Search]
npiregistry.cms.hhs.gov/search
- [NPPES NPI Files]
download.cms.gov/nppes/NPI_Files.html
- [Provider Taxonomy Codes]
www.nucc.org/index.php/code-sets-mainmenu-41/provider-taxonomy-mainmenu-40/csv-mainmenu-57

```mermaid
flowchart TD

    A[Download NPPES data<br/>(CSV files & documentation)] --> B[Create Django project & app<br/>provider-lookup / providers]

    B --> C[Design database models<br/>Provider, Taxonomy, ProviderTaxonomy]
    C --> D[Create and run migrations<br/>(PostgreSQL schema)]

    D --> E[Write management command<br/>import_taxonomy<br/>(load taxonomy CSV)]
    E --> F[Write batched provider import<br/>import_providers_batched<br/>(load 9M+ providers)]
    F --> G[Write provider-taxonomy linker<br/>import_provider_taxonomies]

    G --> H[Write bulk address updater<br/>update_provider_addresses<br/>using COPY + temp table]
    H --> I[Add database indexes<br/>on names, NPI, address, taxonomy]

    I --> J[Implement serializers<br/>ProviderSerializer, TaxonomySerializer]
    J --> K[Implement views<br/>find_provider (HTML) + DRF ViewSets]

    K --> L[Create HTML template<br/>find_provider.html<br/>search form + results list]
    L --> M[Add pagination & prefetch_related<br/>(optimize performance)]

    M --> N[Redesign UI<br/>gradient background, colours, layout]
    N --> O[Configure .gitignore<br/>and remove large data files from repo]
    O --> P[Initialize clean Git repo<br/>and push project to GitHub]
```
