---
id: 202508220429
title: "Daily Knowledge Maintenance"
date: 2025-08-22
type: atomic
source: knowledge-management-workflows.md
extraction_method: header_split
created: 2025-08-22T04:29:54.171924
---

# Daily Knowledge Maintenance

1. **Morning Audit** (Automated)
   ```bash
   /kc-audit
   /kb-organize
   ```

2. **Validation Queue** (Semi-automated)
   ```bash
   /kc-validate [pending entries]
   /kc-enrich [low-quality entries]
   ```

3. **Graph Update** (On-demand)
   ```bash
   /kg-build [updated domains]
   /kg-cluster
   ```

## Connections
- Related concepts: [[to-be-linked]]
