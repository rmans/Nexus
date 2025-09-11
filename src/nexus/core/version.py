"""Centralized version configuration for Nexus."""

# Core version information
VERSION = "1.0.0"
TEMPLATE_VERSION = "1.0.0"

# Version metadata
VERSION_INFO = {
    "version": VERSION,
    "template_version": TEMPLATE_VERSION,
    "major": 1,
    "minor": 0,
    "patch": 0,
    "release": "stable",
    "build_date": "2024-01-15",
    "compatibility": {
        "python": ">=3.8",
        "setuptools": ">=40.0.0"
    }
}

# Version comparison utilities
def version_compare(version1: str, version2: str) -> int:
    """Compare two version strings. Returns -1, 0, or 1.
    
    Args:
        version1: First version string (e.g., "1.0.0")
        version2: Second version string (e.g., "1.1.0")
        
    Returns:
        -1 if version1 < version2
         0 if version1 == version2
         1 if version1 > version2
    """
    v1_parts = [int(x) for x in version1.split('.')]
    v2_parts = [int(x) for x in version2.split('.')]
    
    # Pad with zeros to same length
    max_len = max(len(v1_parts), len(v2_parts))
    v1_parts.extend([0] * (max_len - len(v1_parts)))
    v2_parts.extend([0] * (max_len - len(v2_parts)))
    
    for v1, v2 in zip(v1_parts, v2_parts):
        if v1 < v2:
            return -1
        elif v1 > v2:
            return 1
    return 0

def is_newer_version(version1: str, version2: str) -> bool:
    """Check if version1 is newer than version2."""
    return version_compare(version1, version2) > 0

def is_older_version(version1: str, version2: str) -> bool:
    """Check if version1 is older than version2."""
    return version_compare(version1, version2) < 0

def get_version_string() -> str:
    """Get the main version string."""
    return VERSION

def get_template_version() -> str:
    """Get the template version string."""
    return TEMPLATE_VERSION

def get_version_info() -> dict:
    """Get complete version information."""
    return VERSION_INFO.copy()

# Convenience functions for common use cases
def get_nexus_version() -> str:
    """Get Nexus version for configuration."""
    return VERSION

def get_current_template_version() -> str:
    """Get current template version for updater."""
    return TEMPLATE_VERSION
