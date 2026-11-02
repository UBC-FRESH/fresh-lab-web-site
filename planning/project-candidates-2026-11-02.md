# GitHub Project Candidate Audit

Date: 2026-11-02

## Question

Which public repositories in the `UBC-FRESH` GitHub organization are candidates for new public project pages, which should be folded into existing project pages as supporting links, and which should stay out of the projects section?

## Method

- Listed all repositories through the GitHub REST API endpoint `GET /orgs/UBC-FRESH/repos` (two pages, 127 repositories) on 2026-11-02.
- Captured repository name, description, topics, primary language, fork/archive status, stars, open issues, homepage, GitHub Pages status, license, creation date, and last push date.
- Read README content for the strongest candidates to distinguish public-ready project evidence from early scaffolding, data repositories, and one-off artifacts.
- Compared the repository list against the 26 maintained records in `content/projects.json` and the repository links already present in those records.
- Verified the two CWL-gated web applications: `https://ws4.01101.dev` and `https://fhops.01101.dev` both redirect to the UBC FRESH Cloudflare Access login.

Counts from the snapshot: 127 repositories, 6 forks, 0 archived repositories. Thirty-nine repositories have no description, and 11 carry the placeholder description `some default`, which is a useful signal that a repository is data-only, experimental, or not yet ready for public promotion.

## Current Public Coverage

The projects index currently has 42 records:

- Ongoing Research: 16.
- Open Software: 19.
- Past And Recent Projects: 7.

Direct repository links in public project records now include `ws3`, `ws4`, `fhops`, `femic`, `nemora`, `modelwright`, `fable-pyculator`, `figrecover`, `fresh-hectaresbc`, `badc`, `ML4seeding`, `fresh-fvsbc`, `wbi-birds`, `paws3`, `fresh-solutions`, `fieldatlas`, `bc-npp-database`, `freshforge`, `ecotrust-dss`, `nbds_dss`, `nbds_mining`, `kamloops-fbp-priority`, `fresh-fuchs`, `fresh-daugherty`, `fresh-yan`, `fresh-salvage`, `fresh-cbm`, `dbhdistfit-papers`, and `fresh-hectaresbc-data`. WS4, FHOPS, and the Tier 1 and Tier 2 pages added in this pass are reflected in the current count.

## Added New Pages: Tier 1

These have public documentation, a README that explains the project, and enough evidence to support a conservative public record. All records in this table were added to the public projects index on 2026-11-02.

| Page | Category | Repository evidence | Why it was added |
|---|---|---|---|
| WS4 | Open Software | `ws4`; docs at `ubc-fresh.github.io/ws4`; CWL app | Flagship spatially explicit wood supply model, active development, public docs. Added in this pass. |
| FRESH-FVSbc | Open Software | `fresh-fvsbc`; docs; pinned `PyFVS` fork | BC variant of FVS builds and runs; public release v0.20.0; serves FEMIC, WS3, WS4, FRESHForge, and Nemora. |
| WBI harvesting and birds | Ongoing Research | `wbi-birds`; `wbi-harvesting-birds-ems`; legacy `wbi_harvesting-birds`, `wbi_fullwbmodel` | v1.0.0 simulation engine for even-flow harvest versus multi-species bird abundance, with a companion manuscript in preparation. |
| PAWS3 | Open Software | `paws3` | Principal-agent wood supply simulation framework with rolling-horizon and bilevel variants, aligned with FHOPS conventions. |
| FRESH Solutions | Open Software | `fresh-solutions` | Hybrid metaheuristic solver at v0.8.0 with public benchmark evidence; artifact for a second paper. |
| FieldAtlas | Open Software | `fieldatlas` | Offline georeferenced field map iPhone app; Phase 1 app-shell work complete. Distinct from existing modelling projects. |
| BC Native Plant & Pollinator Database | Open Software | `bc-npp-database`; docs site | Evidence-based native plant and pollinator decision-support database for coastal BC; public schema, CLI, and documentation scaffold. |
| FRESHForge | Open Software | `freshforge`; docs; PyPI alpha | Workflow-as-code layer for composing FRESH modelling tools; public alpha release. |
| EcoTrust DSS | Past And Recent Projects | `ecotrust-dss`; `ecotrust-dss-data` | Web decision-support system for GHG and biodiversity outcomes, with a Zenodo DOI and documented deployment. |
| NbDS DSS | Past And Recent Projects | `nbds_dss`, `nbds_mining`, `nbds_dss-data`, `nbds_dss-outputs`, `nbds_dss_manuscript` | Nature-based decarbonization decision-support notebooks with a Zenodo DOI and mining-sector case studies. |

## Added Pages And Deferred Candidates: Tier 2

These are credible projects that needed PI, student, collaborator, or publication-status review before public copy was curated. All except the TASS II wrapper were added on 2026-11-02 with conservative public copy; the TASS II wrapper remains deferred pending licensing and partner review.

| Proposed page | Category | Repository evidence | Review needed |
|---|---|---|---|
| Kamloops FBP priority mapping | Ongoing Research | `kamloops-fbp-priority` | Leah Nash MGEM project; Phase 0 feasibility prototype is complete, but the LiDAR fuel-type experiment is the thesis contribution and is not finished. |
| FRESH-Fuchs risk-aware planning | Ongoing Research | `fresh-fuchs` | Stochastic, risk-aware TSA29 landscape planning with nested policy and enterprise decisions; confirm public scope and student/collaborator attribution. |
| Daugherty (1991) reproduction | Ongoing Research | `fresh-daugherty`, `fresh_daugherty_manuscript` | Reproducible reproduction of Daugherty's LP forest-planning credibility case study; confirm whether this is a public methods project or a manuscript-support artifact. |
| HWP half-life and displacement uncertainty | Ongoing Research | `fresh-yan`, `yan-yancun-masc-thesis-paper` | CJFR manuscript in preparation; confirm author list, status, and whether the repository should be public before acceptance. |
| TSA29 salvage subsidy model | Ongoing Research | `fresh-salvage` | Extends the Davis Xu MASc principal-agent salvage work; confirm relationship to the existing thesis page and whether it should be a separate project or a major update. |
| TASS II wrapper | Open Software | `tassii-wrapper` | Wine wrapper for the proprietary TASS II executable; useful public tooling, but confirm licensing and partner constraints before promotion. |
| FRESH-CBM | Open Software | `fresh-cbm`; docs | Cached libcbm stand-state tables for WS4/FEMIC carbon work; P0 complete, P1 planned. Better as a supporting link until a release exists. |

## Fold Into Existing Pages

Do not create separate pages for these repository families. Add them as links, outputs, or deployment examples on the parent project record.

| Existing page | Repositories and links to fold in |
|---|---|
| FEMIC | `femic-tsa08-instance`, `femic-tsa16-instance`, `femic-tsa23-instance`, `femic-tsa24-instance`, `femic-tsa27-instance`, `femic-tsa29-instance`, `femic-tsa29mini-instance`, `femic-tsa40-instance`, `femic-tsa41-instance`, `femic-tsa46-instance`, `femic-tsa47-instance`, `femic-tsa48-instance`, `femic-tfl6-instance`, `femic-afrf-gavinlake-instance`, `femic-afrf-knifecreek-instance`, `femic-gnn-instance`, `femic-northisland-instance`, `femic-k3z-instance`, `femic-mkrf-instance`, `femic-public-data` |
| WS3 | `spades_ws3`, `spades_ws3_dataInit`, `ws3_carbon_dss_demo`, `ws3_spatialoptimize`, `fresh-interop` (also WS4), related model instances |
| WS4 | `fresh-cbm`, `fresh-road`, `fresh-beast`, `fresh-interop`, FEMIC model instances used as WS4 cases |
| FHOPS | `fhops-manuscript`, `fhops-manuscript-extras`, `fhops-cjfr-rolling-horizon`, `jaffray-masc-fhops-model`, `https://fhops.01101.dev` (CWL) |
| FlashForest drone seeding microsite ML | `ML4seeding`, `fresh-ml4seeding`, `microsite-annotation-flywheel`, `a58-microsite-sandbox`, `drone-tree-planting` |
| CLEWs-C2070 NRCan grant | `clews-c2070-fresh`, `clews-c2070-fresh-data` |
| FRESH-hectaresbc | `fresh-hectaresbc-data` |
| badc | `badc-bogus-data` only if the bogus-data example is intentionally public; otherwise leave out |
| CCCANDiES | `cccandies_demo`, `cccandies_demo_input`, `bogus_fire` |
| Stem diameter distribution fitting | `hpsdistfit`, `dbhdistfit-papers`, `dbhdistfit-data`, `nemora` |
| Rosalia Jaffray MASc thesis | `jaffray-masc-review-paper`, `jaffray-masc-fhops-model`, `fhops-cjfr-rolling-horizon` |
| Jinming (Jimmy) Ke MSc thesis | `msc_jimmy_ke`, `model_prototype_0`; evaluate `nbds_mining` as related work |
| Yancun (Walter) Yan MSc thesis | `msc_walter_yan`, `yan-yancun-masc-thesis-paper`, `fresh-yan` |
| Yunhao (Davis) Xu MASc thesis | `xu_yunhao_masc_thesis`, `fresh-salvage`; `masc-yunhao-xu` is referenced in the salvage README but is not publicly resolvable |
| EcoTrust DSS | `ecotrust-dss-data` |
| NbDS DSS | `nbds_dss-data`, `nbds_dss-outputs`, `nbds_dss_manuscript` |
| WBI harvesting and birds | `wbi-harvesting-birds-ems` (manuscript), `wbi_harvesting-birds` and `wbi_fullwbmodel` (legacy prototypes) |
| FRESH-Daugherty | `fresh_daugherty_manuscript` |

Status: the Phase D links in this table were added to the existing project records on 2026-11-02.

## Do Not Add As Project Pages

| Group | Repositories | Reason |
|---|---|---|
| Forks of external projects | `PyFVS`, `HawkEars`, `rglobus`, `staged-recipes`, `conda-forge-staged-recipes-libcbm`, `ArcRasterRescue` | Not lab-originated projects. `PyFVS` can be mentioned as the upstream build dependency of FRESH-FVSbc. |
| Website, deployment, and knowledge infrastructure | `fresh-lab-web-site`, `jupyterhub-container-deploy`, `lab-knowledge`, `ubc-fresh-dev-workflow` | Infrastructure for running the lab, not research projects. |
| Agent and developer tooling | `fresh-agent-core`, `agent-workbench`, `agent-delegation-lab`, `codex-local-file-link-patch`, `bibtex-utils`, `Article-overleaf-template` | Useful utilities but not public research projects; keep out unless the lab wants a dedicated tools section. |
| Teaching and workshops | `frst521`, `ubc-frst318`, `fope512_module2.1`, `lab-data-workflow-workshop` | Course and training material, not project records. |
| Data-only repositories | `deg`, `deg-vri-fullbc`, `mea`, `mea-sem`, `nbds_dss-data`, `nbds_dss-outputs`, `badc-bogus-data`, `cccandies_demo_input`, `dbhdistfit-data`, `ecotrust-dss-data`, `femic-public-data`, `clews-c2070-fresh-data`, `fresh-hectaresbc-data`, and the `femic-*-instance` family | Link from a parent project instead of creating a page. |
| Placeholder, junk, or unexplained repos | `bogus`, `foo`, `bogus_fire`, and the 11 repositories described as `some default` | No public project narrative or evidence. |
| Administrative automation | `ubc-workday-fgst-canvas-bridge` | Useful internal automation, but not a research project. |
| Draft or pre-tender material | `urban-woodland-growing-medium` | Explicitly pre-tender and not professionally certified; not ready for public project promotion. |
| Workshop handout draft | `forest-carbon-offset-protocol-summaries`, `forest-carbon-offset-protocol-summaries-publish` | Workshop materials circulated as a working draft; better treated as an outreach output if used at all. |
| Alpha or deferred operational tools | `fresh-beast`, `fresh-road`, `fresh-interop` | Promising, but alpha, benchmark-only, or explicitly deferred for operational use. Fold into WS3/WS4 first and revisit at release. |
| Legacy or one-off research code | `fmg-original-python2`, `ria_yield`, `fci_hg_invyld`, `ws3_spatialoptimize`, `ws3_carbon_dss_demo`, `Resultant_Builder_BC`, `model_prototype_0`, `biomass_project`, `drone-tree-planting`, `wbi_harvesting-carbon`, `wbi-ria-ws3` | Older code without maintained public documentation. Mention only where a thesis or paper page needs provenance. |
| Private or unpublished references | `fresh-solutions-papers`, `wbi-birds-manuscript`, `masc-yunhao-xu` | Referenced in public READMEs but return 404 through the public API; do not link until they are published. |

## Suggested Sequencing

1. Phase A (done in this pass): add WS4 and the CWL-gated WS4 and FHOPS web application links.
2. Phase B (done in this pass): add the Tier 1 pages with conservative summaries and verified links: FRESH-FVSbc, WBI harvesting and birds, PAWS3, FRESH Solutions, FieldAtlas, BC-NPPD, FRESHForge, EcoTrust DSS, and NbDS DSS.
3. Phase C (done in this pass): add the Tier 2 pages for Kamloops FBP priority, FRESH-Fuchs, FRESH-Daugherty, FRESH-Yan, FRESH-Salvage, and FRESH-CBM. TASS II wrapper stays deferred pending licensing and partner review.
4. Phase D (done in this pass): enriched existing pages with the folded repository families, including FEMIC deployment-instance guides and examples, WS3 SpaDES and interoperability links, WS4 carbon/road/disturbance links, FHOPS thesis and rolling-horizon repositories, FlashForest microsite tooling, CLEWs model and data repositories, CCCANDiES demonstration data, stem-diameter fitting repositories, thesis repositories, EcoTrust and NbDS archives, WBI legacy models, and the pinned PyFVS fork.
5. Phase E: revisit FRESH-ROAD, FRESH-BEAST, FRESH-Interop, and TASS II wrapper when they have a release or a stable public workflow.

## Source Notes

- Repository metadata came from the public GitHub API on 2026-11-02. Counts and status values will drift as repositories are created, renamed, or released.
- README-derived statements were paraphrased for candidate triage only; public project copy still needs normal editorial review and, where relevant, PI/student approval.
- The `01101.dev` applications are behind UBC FRESH Cloudflare Access and redirect to a UBC CWL login. Public links should carry the login note.
- No private repository content or credentials were used in this audit.

## Open Questions

- Should EcoTrust DSS and NbDS DSS be treated as current/open software or as past/recent projects? Both have a DOI and a documented workflow but no recent push activity.
- Should FRESH-Interop become a public project page or remain a supporting link under WS3/WS4?
- Should the agent-assisted workflow repositories become one public "research software tooling" page, or remain internal infrastructure?
- Which Tier 2 projects have approval to name students, collaborators, and manuscript status publicly?
