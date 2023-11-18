'''Create acceleration platform using BSP from AMD/Xilinx.
'''
import argparse
import os
import shutil
import vitis


PFM_NAME = 'kv260'
top_dir = os.path.dirname(__file__)
pfm_dir = os.path.join(top_dir, '_pfm')
boot_dir = os.path.join(top_dir, '_boot')
sd_dir = os.path.join(top_dir, '_sd_dir')
hw_xsa_path = os.path.join(top_dir, 'hw.xsa')
hw_emu_xsa_path = os.path.join(top_dir, 'hw_emu.xsa')

parser = argparse.ArgumentParser()
parser.add_argument('bsp_path', type=str, help='path to KV260 Petalinux BSP')
args = parser.parse_args()

if not os.path.exists(args.bsp_path):
    raise FileNotFoundError(f'{args.bsp_path = :}')

# path to source files
images_dir_path = os.path.join(args.bsp_path, 'pre-built', 'linux', 'images')
# dtb_path = os.path.join(images_dir_path, 'system-zynqmp-sck-kv-g-revB.dtb')
# dtb_path = os.path.join(images_dir_path, 'system-zynqmp-sck-kv-g-revB.dtb')

# prepare required files
for d in [pfm_dir, boot_dir, sd_dir]:
    if os.path.exists(d):
        shutil.rmtree(d)
    os.mkdir(d)

for fn in ['bl31.elf', 'pmufw.elf']:
    shutil.copy(os.path.join(images_dir_path, fn), boot_dir)

# need renaming
shutil.copy(
    os.path.join(images_dir_path, 'zynqmp_fsbl.elf'),
    os.path.join(boot_dir, 'fsbl.elf')
)
shutil.copy(
    os.path.join(images_dir_path, 'u-boot-dtb.elf'),
    os.path.join(boot_dir, 'u-boot.elf')
)

# shutil.copy(
#     os.path.join(images_dir_path, 'system-zynqmp-sck-kv-g-revB.dtb'),
#     os.path.join(boot_dir, 'system.dtb')
# )
# shutil.copy(
#     os.path.join(images_dir_path, 'system-zynqmp-sck-kv-g-revB.dtb'),
#     os.path.join(boot_dir, 'system-zynqmp-sck-kv-g-revB.dtb')
# )

for fn in ['boot.scr', 'Image', 'ramdisk.cpio.gz.u-boot', 'system-zynqmp-sck-kv-g-revB.dtb', 'system.dtb']:
    shutil.copy(os.path.join(images_dir_path, fn), sd_dir)

# generate platform
client = vitis.create_client()
client.set_workspace(path=pfm_dir)

platform = client.create_platform_component(
    name=PFM_NAME, hw=hw_xsa_path, desc='KV260 Vitis acceleration platform',
    os='linux', cpu='psu_cortexa53', no_boot_bsp=True,
    emulation_xsa_path=hw_emu_xsa_path
)

domain = platform.get_domain(name='linux_psu_cortexa53')
status = domain.update_name(new_name='xrt')
assert status
status = domain.generate_bif()
assert status
status = domain.add_boot_dir(images_dir_path)
status = domain.add_boot_dir(boot_dir)
assert status
status = domain.set_sd_dir(sd_dir)
assert status
# status = domain.set_dtb(path=dtb_path)
# assert status
platform = client.get_platform_component(name=PFM_NAME)

platform.remove_boot_bsp()
status = platform.build()

print('----- domain.report')
domain.report()
print('----- platform.report')
platform.report()
