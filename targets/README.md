# Target Projects

## Purpose

This folder holds **Target Projects** — repositories used to test the Trust-Judge,
Debugging, and Code Review workflows of the byte-squad-trustlayer system. Target
Projects are **not** part of the system's own source code; they exist solely as
realistic subjects against which the system's capabilities are evaluated. Each
target is placed in a size-appropriate sub-folder (`small/`, `medium/`, or
`large/`) according to the criteria below.

---

## Sizing Criteria

| Criteria      | Small            | Medium                  | Large                   |
|---------------|------------------|-------------------------|-------------------------|
| Lines of Code | < 3,000          | 3,000 – 30,000          | > 30,000                |
| File Count    | < 15             | 15 – 100                | > 100                   |
| Dependencies  | 0–3              | 4–15                    | 15+                     |
| License       | N/A (self-built) | MIT/Apache/BSD only     | MIT/Apache/BSD only     |
| Last Commit   | N/A              | < 12 months             | < 24 months             |
| Language      | Python only      | Python ≥95% of codebase | Python ≥95% of codebase |

