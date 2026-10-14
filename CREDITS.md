# Credits and source provenance

All existing copyright/licence headers remain intact. No FPGA or Main
implementation is replaced. New experiment scripts are GPL-3.0-or-later;
see Main_MiSTer_Hybrid/LICENSE for the full GPLv3 text.

| Source | Authors / contributors | Licence / use in this experiment |
| --- | --- | --- |
| [Minimig](https://github.com/MiSTer-devel/Minimig-AGA_MiSTer) | Dennis van Weeren, Jakub Bednarski, Sascha Boing, Rok Krajnc, A.M. Robinson, Christian Vogelsang, Tobias Gubener, Till Harbaum; upstream contributors | GPL-3.0-or-later per repository README; existing source and unchanged historical RBF |
| [MiSTer Minimig](https://github.com/MiSTer-devel/Minimig-AGA_MiSTer) | Sorgelig and MiSTer contributors; underlying core authors above | Existing FPGA source retains per-file notices (including CPU cores); modern port reference |
| [Hybrid Minimig](https://github.com/scrameta/Minimig-AGA_MiSTer_Hybrid) | Mark Watson (scrameta), prior Minimig/MiSTer contributors | Existing fork, GPL notices retained; FPGA unmodified |
| [MiSTer Main](https://github.com/MiSTer-devel/Main_MiSTer) | Sorgelig and Main contributors | GPLv3 repository licence; existing source unchanged |
| [Hybrid Main](https://github.com/scrameta/Main_MiSTer_Hybrid) | Mark Watson and Main contributors | Existing lifecycle/launcher reference; upstream support Main reused unchanged |
| [QEMU](https://www.qemu.org/) / [Hybrid QEMU](https://github.com/scrameta/qemu_MiSTer_Hybrid) | QEMU authors and contributors, Mark Watson | GPLv2 with component-specific licences; historical executable reused unchanged; no new emulator |
| [Hybrid support](https://github.com/scrameta/MiSTer_Hybrid_Support) | Mark Watson and bundled component authors | Commit 61e059cccf8f719a7624266220604c1e5bcaca41; Main, RBF, qemu runtime and kernel_patch copied only into local output; launcher adapted with CPU selection/readiness checks |
| [Kernel module](https://github.com/scrameta/MiSTer_Hybrid_Kernel_Module) | Mark Watson / Linux contributors | Historical kernel binaries from support; consult source notices and exact kernel compatibility |
| [Musashi](https://github.com/kstenerud/Musashi) / [Hybrid Musashi](https://github.com/scrameta/Musashi_MiSTer_Hybrid) | Karl Stenerud, contributors, Mark Watson | Reference only; not packaged; consult upstream licence |
| [UAE4ARM Hybrid](https://github.com/scrameta/uae4arm_MiSTer_Hybrid) | UAE/UAE4ARM contributors and Mark Watson | Future backend reference only; no code copied; consult per-file licences |
| Historical runtime libraries | glibc, GLib, SDL, pixman and other respective authors | Bundled upstream shared libraries retain original bytes; mixed LGPL/GPL/other terms, not relicensed by this project |

The support repository does not provide a complete component licence/source
bundle. Exact artifact hashes are recorded in amiga060/UPSTREAM_SHA256SUMS;
the local package adds SHA256SUMS and SOURCE.txt. The pinned support commit
identifies binary provenance, not necessarily the exact source revision used
to compile each binary. Before public binary redistribution, obtain matching
source, copyright notices and component licences from their upstreams; do
not infer that every bundled artifact has the same licence. This repository
commits scripts and manifests only, not third-party binaries. Reference-only
projects are not claims of code reuse. Additional sources must be credited
when incorporated; preserve their notices and add licences as appropriate.
