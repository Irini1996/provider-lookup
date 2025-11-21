# Provider Lookup Project

The objective of this project is to create a system that allows users to search for and locate Healthcare providers.

## Data Sources

- **NPI Registry Search**  
  https://npiregistry.cms.hhs.gov/search
- **NPPES NPI Files**  
  https://download.cms.gov/nppes/NPI_Files.html
- **Provider Taxonomy Codes**  
  https://www.nucc.org/index.php/code-sets-mainmenu-41/provider-taxonomy-mainmenu-40/csv-mainmenu-57

flowchart TD

    classDef box fill=#E8F6F3,stroke=#0d9488,stroke-width=2,color=#0d4f4a,rx=12,ry=12;

    A[Download NPPES CSV data]:::box --> B[Create Django project & providers app]:::box

    B --> C[Design database models<br/>Provider, Taxonomy, ProviderTaxonomy]:::box
    C --> D[Create and run migrations<br/>PostgreSQL schema]:::box

    D --> E[Import taxonomy codes<br/>from CSV]:::box
    E --> F[Import provider records<br/>(batch loading)]:::box
    F --> G[Link providers to taxonomy codes]:::box

    G --> H[Update provider addresses<br/>with cleaned data]:::box
    H --> I[Add database indexes<br/>NPI, name, taxonomy, ZIP, state]:::box

    I --> J[Implement serializers]:::box
    J --> K[Implement views & search logic]:::box

    K --> L[Create HTML search page<br/>and results template]:::box
    L --> M[Add pagination & performance optimizations]:::box

    M --> N[Redesign UI<br/>gradients, layout, colours]:::box
    N --> O[Fix .gitignore & remove large files]:::box

    O --> P[Push final project to GitHub]:::box
