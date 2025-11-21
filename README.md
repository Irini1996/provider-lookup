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

    %% ----------- STYLE DEFINITIONS -----------
    classDef box fill:#E0F7F7,stroke:#0d9488,stroke-width:2px,color:#064f43,rx:12,ry:12;
    classDef title fill:#0d9488,color:white,stroke:#0d9488,stroke-width:2px,rx:12,ry:12;

    %% ----------- DIAGRAM -----------
    A[Download NPPES CSV data]:::box --> B[Create Django project & providers app]:::box

    B --> C[Design database models<br/>Provider, Taxonomy, ProviderTaxonomy]:::box
    C --> D[Create & run migrations<br/>(PostgreSQL schema)]:::box

    D --> E[Import taxonomy codes<br/>from CSV]:::box
    E --> F[Import provider records<br/>(batch loading)]:::box
    F --> G[Link providers to taxonomy codes]:::box

    G --> H[Clean & update provider addresses]:::box
    H --> I[Add indexes<br/>NPI, names, ZIP, taxonomy, state]:::box

    I --> J[Implement serializers]:::box
    J --> K[Implement views & search logic]:::box

    K --> L[Create HTML search page<br/>and results template]:::box
    L --> M[Add pagination & performance optimizations]:::box

    M --> N[Redesign UI<br/>colors, gradients, layout]:::box
    N --> O[Fix .gitignore & remove large files]:::box

    O --> P[Push final project to GitHub]:::box
