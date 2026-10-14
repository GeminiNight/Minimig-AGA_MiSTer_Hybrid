# Amiga 060 Testing v0.1

The smallest probe: use historical Hybrid QEMU with an explicit m68020,
m68030, m68040 or m68060 CPU. FPGA 68000/68020 logic is unchanged.
The DE10-Nano's onboard Cortex-A9 runs QEMU; no extra computer is needed.
A registered QEMU CPU is not proof of Amiga 060 compatibility.

## Build the test package on your development computer

Use Python 3 and Git. No Quartus or Main compilation is needed for this probe.

```
git clone https://github.com/scrameta/MiSTer_Hybrid_Support.git /tmp/hybrid-support
git -C /tmp/hybrid-support checkout 61e059cccf8f719a7624266220604c1e5bcaca41
python3 amiga060/build_package.py /tmp/hybrid-support /tmp/amiga060-package
```

The builder verifies all reused binary files against UPSTREAM_SHA256SUMS.
The output records the exact source and hashes. No mystery binaries are
committed here. The packaged RBF is an unchanged copy of historical
MinimigHybrid.rbf, renamed Amiga_060_Testing.rbf. Its embedded OSD still
uses historical labels; choose 68Arm for every ARM CPU model.

## Install and activate on MiSTer

Copy the package directory to your SD card. Back up the card first. In its
Linux terminal, run `sh /media/fat/amiga060-package/install.sh` (adjust the
package directory). Installation refuses existing Minimig_Hybrid or test
files, rather than overwriting a previous installation. Normal Minimig.rbf
and Main stay untouched during installation.

To enable the historical Hybrid-aware Main:

```
sh /media/fat/Amiga060_Testing/activate.sh
reboot
```

This changes Main for the whole MiSTer session, not only this core. It is
required because historical Hybrid relies on modified Main. A verified
backup is retained at Amiga060_Testing/original-main/MiSTer. Activation
refuses to overwrite that backup; even after restore it cannot be repeated
without separately preserving and managing that directory.

One-command restoration (then reboot):

```
sh /media/fat/Amiga060_Testing/restore.sh
```

Restore verifies and keeps the backup and is repeatable. Do not run
install/activate/restore concurrently or interrupt a card write. Scripts
cannot guarantee recovery from SD-card failure; keep an external backup.

## Boot sequence

Use your legally obtained Kickstart ROM and copied test disks, not your
only writable Workbench disk. On DE10-Nano with 128 MB SDRAM:

1. Load the separate Amiga_060_Testing core. Test 68020 FPGA first.
2. Default ARM model is m68020. Select historical `68Arm` in OSD. Test boot.
3. If ARM 020 fails, stop and diagnose; do not proceed to higher models.
4. Return to the MiSTer menu to stop the emulator. Run
   `sh /media/fat/Amiga060_Testing/set_cpu.sh 030`, then reload the test core.
5. Repeat with `040`, then `060`. Never switch a running CPU live.

FPGA 68000 and 68020 remain available; helper selection only affects ARM.
Historical kernel modules must match your installed MiSTer kernel. The
launcher keeps CPU affinity, overlay setup, library loader, 10M memory
argument and interrupt logging from upstream. It checks overlay/module
readiness and stops if unavailable. It does not update your kernel.

Logs: /tmp/qemu.log (exceptions/interrupts, replaced each launch),
/tmp/amiga060_cpu.log (selected CPU, time, PID and startup errors).
Copy logs before another test/reboot; /tmp is temporary. Additional trace
categories can be added for a diagnosed failure, but may generate huge logs.

Record each CPU separately: Level 0 actual QEMU start; 1 Kickstart executes;
2 early boot; 3 desktop; 4 correct CPU detection; 5 normal software;
6 FPU/060.library and accelerator-sensitive software. No hardware levels
have been demonstrated by the cloud tests. Check reset, exception frames,
interrupts, bus access, FPU/MMU/CACR/VBR, removed instructions, ROM remapping,
JIT invalidation and self-modifying/DMA-visible code before compatibility claims.

Historical AllocP/StackAttack advice is retained upstream, not installed
into your Amiga startup files. Those workarounds are not the final solution.
No bridge widening, optimisation, backend switch or V80 work is part of v0.1.
After this probe, port minimal Hybrid functionality into current MiSTer
Minimig and Main without regressing their newer features.

Cloud validation covers package integrity, selection and safe backup/restore.
Main/QEMU software builds and FPGA builds were not performed. Reusing the
historical RBF avoids a rebuild; hardware/kernel compatibility still requires
the physical DE10-Nano. See CREDITS.md before redistributing the package.

Host checks: `AMIGA060_PACKAGE=/tmp/amiga060-package python3 amiga060/tests/test_package.py`. Launcher tests mock hardware and the ARM loader; they do not demonstrate Level 0.
