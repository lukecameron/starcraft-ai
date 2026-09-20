# Third-party inputs

Downloaded source and game data live in ignored local directories. Reproducible source pins are in the port documents and opponent manifest; generated module provenance is retained beside each binary.

- McRave: MIT, Christian McCrave. Its license is preserved in [ports/mcrave/LICENSE](ports/mcrave/LICENSE). The native patch contains portability fixes, undefined-behavior repairs and passive evaluation telemetry. Competition permission is a separate venue requirement; this project has not submitted a derivative.
- ZZZKBot: LGPL-3.0, Chris Coxe and upstream contributors. Preserve [LICENSE.txt](ports/zzzkbot/LICENSE.txt), [LGPL text](ports/zzzkbot/COPYING.LESSER.txt), and [GPL text](ports/zzzkbot/COPYING.txt) with the patch and any distribution. Source/build instructions remain available here; no tournament package is distributed yet.
- UAlbertaBot, BOSS and SparCraft: MIT, David Churchill and upstream contributors. Notice preserved at [ports/ualbertabot/LICENSE.md](ports/ualbertabot/LICENSE.md); original configuration is included with the native module adapter.
- OpenBW's BWAPI fork and official BWAPI: LGPL-3.0, fetched separately at documented revisions. The official headers are used for source compatibility checks, never linked into the OpenBW runtime.
- OpenBW: the inspected revision has no explicit repository license file. It is a local development dependency; resolve redistribution terms before distributing engine-derived binaries. The intended tournament package uses official BWAPI instead.
- screp: Apache-2.0, built separately from the pinned source release for replay validation.
- Blizzard StarEdit MPQs and SSCAIT maps: sourced from their documented public downloads, retained locally with hashes. They are not included in this source repository or a bot package.

Upstream licenses apply to their respective code and modifications. Public source access and a software license do not establish competition eligibility or equivalence to a live ladder binary.
