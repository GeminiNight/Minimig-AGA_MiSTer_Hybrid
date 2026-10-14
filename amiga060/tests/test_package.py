"""Functional host checks. Never access a real /media/fat or run ARM binaries."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

PACKAGE = Path(os.environ.get('AMIGA060_PACKAGE', '/tmp/amiga060-package'))

class PackageTest(unittest.TestCase):
    def run_script(self, script, root, ok=True, *args):
        result = subprocess.run(['sh', str(script), *args], env={**os.environ, 'AMIGA060_FAT_ROOT': str(root)}, capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, ok, result.stdout + result.stderr)
        return result

    def test_install_select_backup_restore(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'MiSTer').write_bytes(b'original-main-test')
            (root / '_Computer').mkdir()
            (root / '_Computer/Minimig.rbf').write_bytes(b'normal-core')
            self.run_script(PACKAGE / 'install.sh', root)
            self.assertEqual((root / 'MiSTer').read_bytes(), b'original-main-test')
            self.assertEqual((root / '_Computer/Minimig.rbf').read_bytes(), b'normal-core')
            self.run_script(PACKAGE / 'install.sh', root, False)
            control = root / 'Amiga060_Testing'
            for cpu in ['020', '030', '040', '060']:
                self.run_script(control / 'set_cpu.sh', root, True, cpu)
                self.assertEqual((root / 'Minimig_Hybrid/cpu_model').read_text(), 'm68' + cpu + '\n')
            self.run_script(control / 'set_cpu.sh', root, False, '999')
            self.run_script(control / 'activate.sh', root)
            self.assertEqual((root / 'MiSTer').read_bytes(), (control / 'Hybrid_Main').read_bytes())
            backup = control / 'original-main/MiSTer'
            self.assertEqual(backup.read_bytes(), b'original-main-test')
            self.run_script(control / 'activate.sh', root, False)
            self.run_script(control / 'restore.sh', root)
            self.run_script(control / 'restore.sh', root)
            self.assertEqual((root / 'MiSTer').read_bytes(), b'original-main-test')
            backup.write_bytes(b'corrupt')
            self.run_script(control / 'restore.sh', root, False)
            self.assertEqual((root / 'MiSTer').read_bytes(), b'original-main-test')

    def test_launcher_arguments_and_invalid_cpu(self):
        # Mock hardware/loader only: verifies argv, not emulation or kernel access.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            hybrid = root / 'Minimig_Hybrid'
            (hybrid / 'kernel_patch').mkdir(parents=True)
            (hybrid / 'qemu/libs/lib').mkdir(parents=True)
            stubs = root / 'stubs'
            stubs.mkdir()
            files = {
                stubs / 'taskset': '#!/bin/sh\nexit 0\n',
                stubs / 'cat': '#!/bin/sh\ncase "$1" in /sys/*) echo applied;; *) exec /bin/cat "$@";; esac\n',
                hybrid / 'kernel_patch/setup': '#!/bin/sh\nexit 0\n',
                hybrid / 'qemu/libs/lib/ld-linux-armhf.so.3': '#!/bin/sh\nprintf "%s\\n" "$@" > "$AMIGA060_FAT_ROOT/argv"\n',
            }
            for path, content in files.items():
                path.write_text(content)
                path.chmod(0o755)
            # Host cannot supply /sys/module/minimig_irq: replace only the
            # hardware existence check in a temporary test copy, never production.
            launcher = root / 'start'
            source = PACKAGE / 'payload/Minimig_Hybrid/start'
            launcher.write_text(source.read_text().replace('test -d /sys/module/minimig_irq', 'true'))
            env = {**os.environ, 'AMIGA060_FAT_ROOT': str(root), 'PATH': str(stubs) + ':' + os.environ['PATH']}
            for cpu in ['m68020', 'm68030', 'm68040', 'm68060']:
                (hybrid / 'cpu_model').write_text(cpu + '\n')
                subprocess.run(['sh', str(launcher)], env=env, check=True, capture_output=True)
                argv = (root / 'argv').read_text().splitlines()
                self.assertEqual(argv, ['./qemu/qemu-system-m68k', '--machine', 'mister_minimig', '-cpu', cpu, '--nographic', '-D', '/tmp/qemu.log', '-m', '10M', '-d', 'int'])
            (root / 'argv').unlink()
            (hybrid / 'cpu_model').write_text('bad-model\n')
            self.assertNotEqual(subprocess.run(['sh', str(launcher)], env=env, capture_output=True).returncode, 0)
            self.assertFalse((root / 'argv').exists())

    def test_integrity(self):
        subprocess.run(['sha256sum', '--quiet', '-c', 'SHA256SUMS'], cwd=PACKAGE, check=True)

if __name__ == '__main__':
    unittest.main()
