# Guide Validation Scripts

**Purpose:** Automated validation tools for guide consistency

---

## validate_references.py

**Purpose:** Check all file references in guides are valid

**Usage:**
```bash
python feature-updates/guides_v2/scripts/validate_references.py
```

**What it checks:**
- File references in CLAUDE.md
- Cross-references between guides
- Template references
- Prompt file references

**Exit codes:**
- 0: All references valid
- 1: Broken references found

**When to run:**
- After renaming/moving any guide files
- Before committing guide changes
- During guide review process

---

## Future Scripts

**Planned:**
- validate_terminology.py - Check consistent terminology usage
- validate_gates.py - Verify all gates are documented
- validate_examples.py - Check example code is valid
