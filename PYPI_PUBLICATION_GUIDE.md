# PyPI Publication Guide for MDSA Framework

**Version**: 1.0.0
**Last Updated**: December 2025
**Goal**: Enable `pip install mdsa-framework` for global distribution

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Account Setup](#account-setup)
3. [Package Preparation](#package-preparation)
4. [Build Package](#build-package)
5. [Test on TestPyPI](#test-on-testpypi)
6. [Publish to Production PyPI](#publish-to-production-pypi)
7. [Post-Publication](#post-publication)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### 1.1 Required Software

Ensure you have the following installed:

```bash
# Python 3.10 or higher
python --version  # Should show 3.10+

# Install build tools
pip install --upgrade pip setuptools wheel build twine

# Verify installations
python -m build --version
twine --version
```

### 1.2 Package Requirements Checklist

- [x] `setup.py` configured with all metadata
- [x] `pyproject.toml` with build system requirements
- [x] `MANIFEST.in` specifies included files
- [x] `README.md` with installation instructions
- [x] `LICENSE` file (Apache 2.0)
- [x] `CHANGELOG.md` version history
- [x] `requirements.txt` with dependencies
- [x] Version set to 1.0.0 in all files
- [x] No hardcoded secrets or API keys in code

### 1.3 Security Audit (CRITICAL)

Before proceeding, verify:

```bash
# Check for hardcoded secrets
cd "j:\ME CSE\Sem III\Research Paper\MDSA Orcherstartion Framework\MDSA\version_1"

# Search for API keys (should return nothing)
grep -r "sk-" mdsa/ --include="*.py" || echo "No API keys found"
grep -r "API_KEY\s*=" mdsa/ --include="*.py" || echo "No hardcoded API keys"

# Check for personal paths (should be minimal)
grep -r "j:\\" mdsa/ --include="*.py" || echo "No Windows paths"
grep -r "/Users/" mdsa/ --include="*.py" || echo "No macOS paths"

# Verify .env is excluded
ls .env 2>/dev/null && echo "WARNING: .env exists" || echo ".env properly excluded"
```

**If any secrets or personal paths are found, STOP and remove them before continuing.**

---

## Account Setup

### 2.1 Create PyPI Account

1. **Production PyPI**:
   - Visit: https://pypi.org/account/register/
   - Username: Choose a unique username
   - Email: Use a valid, monitored email address
   - Password: Strong password (12+ characters)

2. **Enable Two-Factor Authentication (REQUIRED)**:
   - Go to: https://pypi.org/manage/account/
   - Click "Add 2FA with authentication application"
   - Scan QR code with authenticator app (Google Authenticator, Authy, etc.)
   - Save recovery codes in a secure location

3. **Create API Token**:
   - Go to: https://pypi.org/manage/account/token/
   - Token name: "MDSA Framework Upload"
   - Scope: "Entire account" (for first upload) or "Project: mdsa-framework" (for updates)
   - Click "Add token"
   - **COPY THE TOKEN IMMEDIATELY** (shown only once)
   - Format: `pypi-AgEIcHlwaS5vcmc...` (very long string)
   - Store in password manager

### 2.2 Create TestPyPI Account (RECOMMENDED)

TestPyPI is a separate instance for testing package uploads without affecting production.

1. Visit: https://test.pypi.org/account/register/
2. Repeat the same process as production PyPI
3. Create separate API token for TestPyPI
4. Store token securely

### 2.3 Configure `.pypirc` (Optional but Recommended)

Create `~/.pypirc` (Linux/Mac) or `%USERPROFILE%\.pypirc` (Windows):

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...  # Your PyPI API token

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgEIcHlwaS5vcmc...  # Your TestPyPI API token
```

**Security Note**: Set file permissions to read-only for owner:
```bash
# Linux/Mac
chmod 600 ~/.pypirc

# Windows
icacls %USERPROFILE%\.pypirc /inheritance:r /grant:r "%USERNAME%:R"
```

---

## Package Preparation

### 3.1 Verify Version Numbers

Ensure version 1.0.0 is set in all locations:

**File**: `setup.py`
```python
setup(
    name="mdsa-framework",
    version="1.0.0",  # ← Check this
    # ...
)
```

**File**: `pyproject.toml`
```toml
[project]
name = "mdsa-framework"
version = "1.0.0"  # ← Check this
```

**File**: `mdsa/__init__.py`
```python
__version__ = "1.0.0"  # ← Check this
```

### 3.2 Update README.md

Add PyPI installation instructions to README.md:

```markdown
## Installation

### From PyPI (Recommended)

```bash
pip install mdsa-framework
```

### From Source

```bash
git clone https://github.com/VickyVignesh2002/MDSA-Orchestration-Framework.git
cd MDSA-Orchestration-Framework
pip install -e .
```
```

### 3.3 Verify MANIFEST.in

Ensure all necessary files are included:

```python
# MANIFEST.in
include README.md
include LICENSE
include CHANGELOG.md
include CONTRIBUTING.md
include RELEASE_NOTES.md
include requirements.txt
include configs/framework_config.yaml
recursive-include mdsa *.py
recursive-include mdsa/ui/dashboard/static *.html *.css *.js
recursive-include mdsa/ui/dashboard/templates *.html
recursive-include tests *.py
recursive-exclude * __pycache__
recursive-exclude * *.pyc
recursive-exclude * *.pyo
recursive-exclude * .DS_Store
prune .claude
prune chatbot_app
prune archive
```

### 3.4 Check Dependencies

Verify `requirements.txt` has version constraints:

```txt
# requirements.txt
torch>=2.0.0,<3.0.0
transformers>=4.30.0
sentence-transformers>=2.2.0
chromadb>=0.4.0
flask>=2.3.0
gradio>=3.35.0
ollama>=0.1.0
pyyaml>=6.0
requests>=2.28.0
numpy>=1.24.0
```

**Tip**: Use version ranges (>=x.y.z,<x+1.0.0) for flexibility while ensuring compatibility.

---

## Build Package

### 4.1 Clean Previous Builds

```bash
cd "j:\ME CSE\Sem III\Research Paper\MDSA Orcherstartion Framework\MDSA\version_1"

# Remove old build artifacts
rm -rf build/ dist/ *.egg-info/
rm -rf mdsa.egg-info/ mdsa_framework.egg-info/

# Verify clean state
ls build dist *.egg-info 2>/dev/null || echo "Clean state confirmed"
```

### 4.2 Build Package

```bash
# Build both wheel (.whl) and source distribution (.tar.gz)
python -m build

# Expected output:
# Successfully built mdsa_framework-1.0.0.tar.gz and mdsa_framework-1.0.0-py3-none-any.whl
```

**Output files** in `dist/`:
```
dist/
├── mdsa_framework-1.0.0-py3-none-any.whl       # Wheel distribution (preferred)
└── mdsa_framework-1.0.0.tar.gz                 # Source distribution (fallback)
```

### 4.3 Inspect Package Contents

```bash
# List contents of wheel
python -m zipfile -l dist/mdsa_framework-1.0.0-py3-none-any.whl | head -50

# List contents of source distribution
tar -tzf dist/mdsa_framework-1.0.0.tar.gz | head -50
```

**Verify**:
- ✅ All `mdsa/` Python modules included
- ✅ Dashboard static files (HTML, CSS, JS) included
- ✅ Configuration files included
- ✅ README, LICENSE, CHANGELOG included
- ❌ No `.claude/` files
- ❌ No `chatbot_app/` files
- ❌ No `archive/` files
- ❌ No `.env` or secrets

### 4.4 Check Package Metadata

```bash
# Validate package with twine
twine check dist/*

# Expected output:
# Checking dist/mdsa_framework-1.0.0-py3-none-any.whl: PASSED
# Checking dist/mdsa_framework-1.0.0.tar.gz: PASSED
```

**If FAILED**: Review error messages and fix issues in `setup.py` or `pyproject.toml`.

---

## Test on TestPyPI

### 5.1 Upload to TestPyPI

```bash
# Upload to TestPyPI first (safer)
twine upload --repository testpypi dist/*

# You'll be prompted:
# Enter your username: __token__
# Enter your password: <paste-testpypi-api-token>

# Or if .pypirc is configured:
twine upload -r testpypi dist/*
```

**Expected output**:
```
Uploading distributions to https://test.pypi.org/legacy/
Uploading mdsa_framework-1.0.0-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB • 00:03
Uploading mdsa_framework-1.0.0.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 800/800 KB • 00:02

View at:
https://test.pypi.org/project/mdsa-framework/1.0.0/
```

### 5.2 Verify TestPyPI Listing

1. Visit: https://test.pypi.org/project/mdsa-framework/
2. Check:
   - ✅ Version shows 1.0.0
   - ✅ README renders correctly
   - ✅ Dependencies listed accurately
   - ✅ Project links (GitHub, docs) work
   - ✅ License shows Apache 2.0
   - ✅ No sensitive information visible

### 5.3 Test Installation from TestPyPI

```bash
# Create fresh virtual environment
python -m venv test_pypi_env

# Activate environment
# Windows:
test_pypi_env\Scripts\activate
# Linux/Mac:
source test_pypi_env/bin/activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ mdsa-framework

# Note: --extra-index-url allows dependencies from main PyPI
```

**Expected output**:
```
Collecting mdsa-framework
  Downloading https://test-files.pythonhosted.org/packages/.../mdsa_framework-1.0.0-py3-none-any.whl (1.2 MB)
Collecting torch>=2.0.0 (from mdsa-framework)
  Downloading https://files.pythonhosted.org/packages/.../torch-2.1.0-cp310-cp310-win_amd64.whl
...
Successfully installed mdsa-framework-1.0.0 torch-2.1.0 transformers-4.35.0 ...
```

### 5.4 Verify Installation

```bash
# Check installed version
pip show mdsa-framework

# Expected output:
# Name: mdsa-framework
# Version: 1.0.0
# Summary: Multi-Domain Specialized Agent Orchestration Framework
# Home-page: https://github.com/VickyVignesh2002/MDSA-Orchestration-Framework
# Author: [Your Name]
# License: Apache 2.0
# Location: .../test_pypi_env/lib/python3.10/site-packages
# Requires: torch, transformers, ...

# Test import
python -c "import mdsa; print(f'MDSA version: {mdsa.__version__}')"

# Expected: MDSA version: 1.0.0

# Test basic functionality
python -c "from mdsa import MDSA; print('MDSA imported successfully')"
```

### 5.5 Run Basic Tests

```bash
# Navigate to package installation
cd test_pypi_env/lib/python3.10/site-packages/

# Run quick smoke tests
python -c "
from mdsa.core.router import DomainRouter
from mdsa.rag.dual_rag import DualRAG
from mdsa.models.ollama_integration import OllamaModel
print('All core modules import successfully')
"
```

**If any imports fail**: Fix issues in source code, rebuild package, and re-upload to TestPyPI with incremented version (1.0.0.post1).

### 5.6 Cleanup Test Environment

```bash
# Deactivate and remove test environment
deactivate
rm -rf test_pypi_env/
```

---

## Publish to Production PyPI

### 6.1 Final Pre-Publication Checklist

Before uploading to production PyPI (IRREVERSIBLE for this version):

- [ ] Package tested successfully on TestPyPI
- [ ] All imports work correctly
- [ ] No sensitive information in package
- [ ] README renders correctly
- [ ] Version number is correct (1.0.0)
- [ ] CHANGELOG.md updated with release notes
- [ ] GitHub repository is public and accessible
- [ ] LICENSE file is present
- [ ] All tests pass (`pytest tests/`)
- [ ] Documentation is complete

**IMPORTANT**: Once uploaded to PyPI, **you cannot delete or replace version 1.0.0**. You can only upload new versions (1.0.1, 1.1.0, etc.).

### 6.2 Upload to Production PyPI

```bash
cd "j:\ME CSE\Sem III\Research Paper\MDSA Orcherstartion Framework\MDSA\version_1"

# Upload to PyPI
twine upload dist/*

# You'll be prompted:
# Enter your username: __token__
# Enter your password: <paste-pypi-api-token>

# Or if .pypirc is configured:
twine upload dist/*
```

**Expected output**:
```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading mdsa_framework-1.0.0-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB • 00:05
Uploading mdsa_framework-1.0.0.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 800/800 KB • 00:03

View at:
https://pypi.org/project/mdsa-framework/1.0.0/
```

### 6.3 Verify Production PyPI Listing

1. Visit: https://pypi.org/project/mdsa-framework/
2. Check all metadata is correct
3. Verify README renders properly
4. Test download link

**Congratulations!** Your package is now live on PyPI! 🎉

### 6.4 Test Production Installation

```bash
# Create fresh environment
python -m venv prod_test_env
source prod_test_env/bin/activate  # or prod_test_env\Scripts\activate on Windows

# Install from PyPI
pip install mdsa-framework

# Verify installation
python -c "import mdsa; print(f'Installed MDSA {mdsa.__version__} from PyPI')"

# Expected: Installed MDSA 1.0.0 from PyPI

# Cleanup
deactivate
rm -rf prod_test_env/
```

---

## Post-Publication

### 7.1 Update README Badges

Add PyPI badges to README.md:

```markdown
# MDSA Framework

[![PyPI version](https://badge.fury.io/py/mdsa-framework.svg)](https://pypi.org/project/mdsa-framework/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/mdsa-framework)](https://pypi.org/project/mdsa-framework/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mdsa-framework)](https://pypi.org/project/mdsa-framework/)
[![License](https://img.shields.io/pypi/l/mdsa-framework)](https://github.com/VickyVignesh2002/MDSA-Orchestration-Framework/blob/main/LICENSE)

Multi-Domain Specialized Agent Orchestration Framework for Enterprise AI Applications

## Installation

```bash
pip install mdsa-framework
```
```

### 7.2 Create GitHub Release

1. Go to: https://github.com/VickyVignesh2002/MDSA-Orchestration-Framework/releases
2. Click "Draft a new release"
3. Tag version: `v1.0.0`
4. Release title: `MDSA Framework v1.0.0 - Initial Release`
5. Description: Copy from RELEASE_NOTES.md
6. Attach files:
   - `dist/mdsa_framework-1.0.0-py3-none-any.whl`
   - `dist/mdsa_framework-1.0.0.tar.gz`
7. Click "Publish release"

### 7.3 Update Documentation

**RELEASE_NOTES.md**:
```markdown
## PyPI Availability

MDSA Framework is now available on PyPI:

```bash
pip install mdsa-framework
```

PyPI page: https://pypi.org/project/mdsa-framework/
```

**SETUP_GUIDE.md**:
Update installation section to prioritize PyPI:
```markdown
## Installation

### Option 1: pip install (Recommended)
```bash
pip install mdsa-framework
```

### Option 2: From Source
```bash
git clone https://github.com/VickyVignesh2002/MDSA-Orchestration-Framework.git
cd MDSA-Orchestration-Framework
pip install -e .
```
```

### 7.4 Announce Release

**GitHub Discussions**:
- Create announcement post in Discussions
- Highlight key features and PyPI availability

**Social Media** (if applicable):
- Twitter: "Excited to announce MDSA Framework v1.0.0 is now on PyPI! Install with `pip install mdsa-framework`. #AI #MachineLearning #OpenSource"
- LinkedIn: Post about the release with link to GitHub

**Community**:
- Reddit (r/MachineLearning, r/Python): Share release announcement
- Hacker News: Submit link to GitHub repository
- Dev.to: Write blog post about the framework

### 7.5 Monitor Initial Feedback

**First 48 Hours**:
- Monitor PyPI download stats: https://pypistats.org/packages/mdsa-framework
- Watch GitHub Issues for bug reports
- Respond to questions promptly
- Track installation errors in user reports

**First Week**:
- Gather feedback on installation process
- Document common issues in FAQ
- Prepare v1.0.1 if critical bugs are found

---

## Troubleshooting

### 8.1 Common Upload Errors

#### Error: "File already exists"
```
HTTPError: 400 Bad Request from https://upload.pypi.org/legacy/
The name 'mdsa-framework' is already in use.
```

**Solution**:
- Package name is taken. Choose a different name (e.g., `mdsa-orchestration`, `mdsa-ai`)
- Update `setup.py` and `pyproject.toml` with new name
- Rebuild and retry

#### Error: "Invalid version"
```
HTTPError: 400 Bad Request
Version '1.0.0' is already published for this project.
```

**Solution**:
- You cannot re-upload the same version
- Increment version to 1.0.1 or 1.0.0.post1
- Rebuild and upload new version

#### Error: "Authentication failed"
```
HTTPError: 403 Forbidden
Invalid or expired API token.
```

**Solution**:
- Verify API token is correct and not expired
- Regenerate token at https://pypi.org/manage/account/token/
- Update `.pypirc` or re-enter when prompted

### 8.2 Installation Issues

#### Error: "Could not find a version"
```
ERROR: Could not find a version that satisfies the requirement mdsa-framework
```

**Solution**:
- Wait 1-2 minutes after upload (PyPI indexing delay)
- Check package name spelling: `mdsa-framework` (not `mdsa_framework`)
- Verify package is visible at https://pypi.org/project/mdsa-framework/

#### Error: "Dependency conflicts"
```
ERROR: Cannot install mdsa-framework due to conflicting dependencies.
```

**Solution**:
- Check Python version (requires 3.10+)
- Create fresh virtual environment
- Update pip: `pip install --upgrade pip`
- Install with verbose logging: `pip install mdsa-framework -v`

### 8.3 Metadata Issues

#### Problem: README not rendering on PyPI

**Solution**:
- Ensure README.md is included in MANIFEST.in
- Set `long_description_content_type="text/markdown"` in setup.py
- Validate README with: `twine check dist/*`

#### Problem: Dependencies not installing

**Solution**:
- Verify `install_requires` in setup.py lists all dependencies
- Check version constraints are valid
- Test in clean environment

---

## Version Updates

### 9.1 Publishing New Versions

When releasing v1.0.1, v1.1.0, etc.:

1. **Update version in all files**:
   - `setup.py`
   - `pyproject.toml`
   - `mdsa/__init__.py`
   - `CHANGELOG.md`

2. **Build new package**:
   ```bash
   rm -rf dist/ build/ *.egg-info/
   python -m build
   ```

3. **Test on TestPyPI** (optional but recommended)

4. **Upload to PyPI**:
   ```bash
   twine upload dist/*
   ```

5. **Create GitHub release** with tag `v1.0.1`

### 9.2 Yanking Bad Releases

If you discover a critical bug AFTER publishing:

```bash
# Yank version (marks as unavailable but doesn't delete)
pip install yank
yank mdsa-framework --version 1.0.0 --reason "Critical bug in router module"
```

Then publish fixed version 1.0.1 immediately.

---

## Appendix

### A.1 Full Example Workflow

```bash
# 1. Prepare environment
cd "j:\ME CSE\Sem III\Research Paper\MDSA Orcherstartion Framework\MDSA\version_1"
pip install --upgrade build twine

# 2. Clean and build
rm -rf dist/ build/ *.egg-info/
python -m build

# 3. Check package
twine check dist/*

# 4. Test on TestPyPI
twine upload -r testpypi dist/*
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ mdsa-framework

# 5. Upload to PyPI
twine upload dist/*

# 6. Verify installation
pip install mdsa-framework
python -c "import mdsa; print(mdsa.__version__)"
```

### A.2 Useful Commands

```bash
# Check PyPI download stats
pip install pypistats
pypistats recent mdsa-framework

# View package info
pip show mdsa-framework

# List all versions
pip index versions mdsa-framework

# Install specific version
pip install mdsa-framework==1.0.0

# Upgrade to latest
pip install --upgrade mdsa-framework
```

---

**Publication Status**: Ready to publish MDSA Framework v1.0.0 to PyPI
**Estimated Time**: 1-2 hours (setup + build + upload + verification)
**Package Name**: `mdsa-framework`
**Installation Command**: `pip install mdsa-framework`

**Questions?** Open an issue at https://github.com/VickyVignesh2002/MDSA-Orchestration-Framework/issues

---

*Last updated: December 2025*
