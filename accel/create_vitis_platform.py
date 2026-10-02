'''Create acceleration platform using the local AMD EDF build.
'''
import os
import shutil

import vitis


PFM_NAME = 'kv260'
top_dir = os.path.dirname(os.path.abspath(__file__))
pfm_dir = os.path.join(top_dir, '_pfm')
boot_dir = os.path.join(top_dir, '_boot')
sd_dir = os.path.join(top_dir, '_sd_dir')
hw_xsa_path = os.path.join(top_dir, 'hw.xsa')
# hw_emu_xsa_path = os.path.join(top_dir, 'hw_emu.xsa')


# path to source files
images_dir_path = os.path.join(top_dir, 'edf', 'images')
machine = 'kv260-accel-sdt'

# Map EDF deploy names to the filenames expected by Vitis's generated BIF.
boot_files = {
    'arm-trusted-firmware.elf': 'bl31.elf',
    f'pmu-firmware-{machine}.elf': 'pmufw.elf',
    f'fsbl-{machine}.elf': 'fsbl.elf',
    'u-boot.elf': 'u-boot.elf',
}
# EDF boots its root filesystem from the SD disk image, without a ramdisk.
sd_files = ['boot.scr', 'Image', 'system.dtb']

# Validate inputs before replacing an existing platform workspace.
for path in [hw_xsa_path] + [
    os.path.join(images_dir_path, fn) for fn in list(boot_files) + sd_files
]:
    if not os.path.isfile(path):
        raise FileNotFoundError(
            f'Missing platform input: {path}. '
            'Generate hw.xsa and run accel/edf/build.sh first.'
        )

# prepare required files
for d in [pfm_dir, boot_dir, sd_dir]:
    if os.path.exists(d):
        shutil.rmtree(d)
    os.mkdir(d)

for source, destination in boot_files.items():
    shutil.copy(
        os.path.join(images_dir_path, source),
        os.path.join(boot_dir, destination)
    )

for fn in sd_files:
    shutil.copy(os.path.join(images_dir_path, fn), sd_dir)

# generate platform
client = vitis.create_client()
client.set_workspace(path=pfm_dir)

platform = client.create_platform_component(
    name=PFM_NAME, hw_design=hw_xsa_path, desc='KV260 Vitis acceleration platform',
    os='linux', cpu='psu_cortexa53', no_boot_bsp=True,
    # emu_design=hw_emu_xsa_path
)

domain = platform.get_domain(name='linux_psu_cortexa53')
assert domain.update_name(new_name='xrt')
assert domain.generate_bif()
assert domain.set_boot_dir(boot_dir)
assert domain.set_sd_dir(sd_dir)

platform.remove_boot_bsp()
status = platform.build()

print('----- domain.report')
domain.report()
print('----- platform.report')
platform.report()

vitis.dispose()
