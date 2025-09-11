try:
    from setuptools import setup, find_packages
except ImportError:
    # Fallback for environments where setuptools is not available
    import os
    import sys
    
    def find_packages(where='.', exclude=()):
        """Simple find_packages implementation for setuptools fallback"""
        out = []
        stack = [(os.path.abspath(where), '')]
        while stack:
            where, prefix = stack.pop(0)
            try:
                for name in os.listdir(where):
                    fn = os.path.join(where, name)
                    if ('.' not in name and os.path.isdir(fn) and
                        os.path.isfile(os.path.join(fn, '__init__.py'))):
                        out.append(prefix + name)
                        stack.append((fn, prefix + name + '.'))
            except (OSError, IOError):
                # Skip directories that can't be read
                continue
        return out
    
    def setup(**kwargs):
        """Minimal setup function fallback"""
        print("Warning: Using fallback setup function. Install setuptools for full functionality.")
        # This is a minimal fallback - in practice, setuptools should always be available
        # for modern Python packaging
        sys.exit(1)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nexus-context",
    version="0.1.0",
    description="AI context orchestration system for Cursor and other coding assistants",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Nexus Team",
    author_email="contact@nexus-project.dev",
    url="https://github.com/rmans/Nexus",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "isort>=5.0.0",
            "pre-commit>=2.0.0",
        ],
        "docs": [
            "mkdocs>=1.4.0",
            "mkdocs-material>=8.0.0",
            "mkdocs-mermaid2-plugin>=0.6.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "nexus=nexus.__main__:main",
        ],
    },
    include_package_data=True,
    package_data={
        "nexus": [
            "commands/*.md",
            "instructions/*.md", 
            "templates/**/*",
            "docs/readmes/*.md",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: Markup",
    ],
    keywords="ai, context, documentation, cursor, coding-assistant, nexus",
    project_urls={
        "Bug Reports": "https://github.com/rmans/Nexus/issues",
        "Source": "https://github.com/rmans/Nexus",
        "Documentation": "https://github.com/rmans/Nexus#readme",
    },
)
