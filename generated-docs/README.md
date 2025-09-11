# Generated Documentation

This directory contains the documentation scaffold for Nexus projects. Each subdirectory represents a different type of document that can be generated.

## Document Types

- **[arch/](arch/)** - Architecture documents and system design
- **[exec/](exec/)** - Execution plans and operational guides  
- **[impl/](impl/)** - Implementation details and technical specs
- **[int/](int/)** - Integration guides and API documentation
- **[prd/](prd/)** - Product requirements and specifications
- **[rules/](rules/)** - Coding standards and guidelines
- **[task/](task/)** - Task management and project planning
- **[tests/](tests/)** - Test documentation and QA processes

## Usage

This scaffold is automatically created when you run `nexus init-project`. Each directory contains an `index.md` file that serves as a template for the document type.

To generate documents, use the Nexus CLI commands:

```bash
nexus generate prd --title "Feature Specification"
nexus generate arch --title "System Architecture"
nexus generate impl --title "API Implementation"
```

## Customization

You can customize the document templates by modifying the `index.md` files in each directory, or by creating additional template files in the `.nexus/templates/` directory.
