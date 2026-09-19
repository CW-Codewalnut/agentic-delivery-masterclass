# Authority and tools

This repository defines behaviour, not runtime permissions. A host must separately provide tools and least-privilege authority.

| Role | Default posture | Mutation requires | Never implied by output |
|---|---|---|---|
| Capture & Refine | read requirements and relevant repository evidence | none in this role | Product approval |
| Design | read; specification-only by default | exact editable target, integration, and human authority | Design approval |
| Planner | read repository and operational context | none in this role | implementation authority |
| Builder | local scoped mutation | exact repo/base/surfaces and human authority | merge or release |
| Tester | independent read/execute in isolated target | separate Builder authority for repairs | approval |
| Reviewer | independent read/execute | none in this role | merge or release |
| Curator | read and propose | governed contribution approval for accepted update | adoption or publication |

Credentials, network access, external messages, merges, deployments, and releases remain host-controlled.
