# Project Documentation

This directory contains generated documentation for the project.

## Structure
- `prd/` - Define what needs to be built and why
- `arch/` - Document system design decisions and technical approach
- `impl/` - Detailed technical implementation guidance
- `int/` - External system integrations and API documentation
- `exec/` - Runtime behavior and operational procedures
- `rules/` - Codified learnings that prevent past mistakes
- `task/` - Executable work items with full traceability
- `tests/` - Validate that rules are being followed and prevent regressions

## Usage
# Generate specific document types
nexus generate-prd "New User Authentication"
nexus generate-arch "Microservices Architecture" 
nexus generate-task "Implement OAuth Integration"

# Generate comprehensive documentation
nexus generate-docs --all
nexus generate-docs --type prd,arch,impl

# Use with Cursor for AI-assisted development
@rules/generate-prd        # Create product requirements
@rules/execute-tasks       # Execute development tasks
@rules/analyze-project     # Analyze current codebase
@rules/project-status      # Check project health

# Serve documentation locally
nexus serve-docs --port 8080

# View specific documentation types
nexus list-docs --type rules
nexus validate-docs --check-links

# Analyze and improve the learning system
nexus analyze-failures      # Identify patterns in task failures
nexus generate-rules        # Auto-generate rules from patterns
nexus validate-rules        # Check rule effectiveness
nexus update-tests          # Update tests based on new rules
