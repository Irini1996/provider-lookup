# Provider Lookup Project

The objective of this project is to create a system that allows users to search for and locate Healthcare providers.

## Data Sources

- **NPI Registry Search**  
  https://npiregistry.cms.hhs.gov/search
- **NPPES NPI Files**  
  https://download.cms.gov/nppes/NPI_Files.html
- **Provider Taxonomy Codes**  
  https://www.nucc.org/index.php/code-sets-mainmenu-41/provider-taxonomy-mainmenu-40/csv-mainmenu-57


## Project Workflow

```mermaid
flowchart TD

    A[Download NPPES data: CSV files + documentation]
        --> B[Create Django project and app: provider-lookup / providers]

    B --> C[Design database models: Provider, Taxonomy, ProviderTaxonomy]
    C --> D[Create and run migrations → PostgreSQL schema]

    D --> E[Import taxonomy codes from CSV]
    E --> F[Import provider records (batch loading)]
    F --> G[Link providers with taxonomy codes]

    G --> H[Update provider addresses using cleaned data]
    H --> I[Add database indexes: NPI, names, taxonomy, ZIP, state]

    I --> J[Implement serializers]
    J --> K[Implement views and search logic]

    K --> L[Create HTML template: search form + results]
    L --> M[Add pagination + query optimizations]

    M --> N[Redesign UI: gradients, colors, layout]
    N --> O[Fix .gitignore + remove large data files]

    O --> P[Initialize clean Git repo + push to GitHub]

