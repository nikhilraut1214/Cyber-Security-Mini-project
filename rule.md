# Operational Rules for AI Agents: Mobile DLP Console

**Repository:** https://github.com/nikhilraut1214/Cyber-Security-Mini-project  
**Role:** Mandatory Operating Constraints and Quality Governance for AI Coding Agents  
**Last Updated:** 2026-10-23  

---

## 1. Operating Principles

1. **Read `memory.md` First:** Before planning or implementing any task, read `memory.md` to understand persistent architectural context, decisions, and system constraints.
2. **Inspect Code Before Assuming:** The actual Python implementation in `core/`, `pages/`, `app.py`, and `tests/` takes strict precedence over outdated documentation or assumptions.
3. **No Unauthorized Rebuilds:** Never redesign, refactor, or rebuild working components without explicit, prior user approval.
4. **No Framework Migrations:** The application is built with Python and Streamlit. Never attempt or propose migrating to React, Vue, FastAPI, or another frontend framework.
5. **Preserve Business Logic:** Do not modify `core/analyzer.py`, `core/dlp.py`, `core/rules.py`, or `core/store.py` unless a critical technical bug is verified.
6. **No Fictitious Functionality or Metrics:** Never invent metrics (e.g., "100% Policy Adherence"), fake threat feeds, fictitious enrollment tokens, or decorative charts with fake data.
7. **No Unsupported Security Claims:** Always accurately represent the project as an **educational simulation**. Never claim it is an actual Android MDM, production DLP, or network security appliance.
8. **Follow SOC Technical Minimal Design:** Maintain the approved minimal, information-dense visual identity. Avoid purple gradients, glassmorphism, huge rounded cards, and casual emojis.
9. **Maintain Dual-Theme Support:** Every new or updated UI view must function cleanly in both **Dark (SOC)** and **Light** modes via `core/ui.py`.
10. **Zero Unnecessary Dependencies:** Keep the stack minimal (`streamlit`, `pytest`). Do not add third-party component libraries or heavy dependencies.
11. **Minimal & Maintainable Code:** Write readable, standard Python code. Avoid brittle CSS hacks, unsafe HTML, or complex JavaScript injections.
12. **Documentation-Code Alignment:** Technical documentation must strictly match the source code. Never describe an algorithm, rule, or parameter that does not exist in the code.
13. **Empirical Test Verification:** Never claim tests pass or that regressions were avoided without executing `pytest` and reviewing actual test runner output.
14. **Git Safety:** Never commit, push, merge, or alter Git history unless explicitly authorized.
15. **Protect User Work:** Never delete user code, uncommitted work, environment configurations, or existing test fixtures.
16. **Explicit Approval for Destructive Actions:** Always halt and seek approval before deleting, moving, or restructuring files.
17. **Comprehensive Implementation Reporting:** Conclude every session with an accurate, verifiable technical report documenting all files touched, tests run, and operational status.
