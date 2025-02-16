'''Create acceleration platform for Vitis-AI.
'''
import os
import shutil
import vitis


PFM_NAME = 'kv260_vai'
top_dir = os.path.dirname(__file__)
pfm_dir = os.path.join(top_dir, '_pfm')
hw_xsa_path = os.path.join(top_dir, 'hw.xsa')

# prepare required files
for d in [pfm_dir]:
    if os.path.exists(d):
        shutil.rmtree(d)
    os.mkdir(d)

# generate platform
client = vitis.create_client()
client.set_workspace(path=pfm_dir)

platform = client.create_platform_component(
    name=PFM_NAME, hw=hw_xsa_path, desc='KV260 Vitis acceleration platform',
    os='linux', cpu='psu_cortexa53', no_boot_bsp=True
)

domain = platform.get_domain(name='linux_psu_cortexa53')
assert domain.update_name(new_name='xrt')
platform = client.get_platform_component(name=PFM_NAME)

platform.remove_boot_bsp()
status = platform.build()

print('----- domain.report')
domain.report()
print('----- platform.report')
platform.report()
