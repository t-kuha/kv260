"""Building simple vector addition app."""
import os
import shutil

import vitis

# settings
top_dir = os.path.dirname(os.path.abspath(__file__))
ws_dir = os.path.join(top_dir, '_vitis-ws')

if os.path.exists(ws_dir):
    print('[INFO] removing existing workspace...')
    shutil.rmtree(ws_dir) 

# start building
client = vitis.create_client()
status = client.set_workspace(path=ws_dir)
assert (status)

proj = client.create_sys_project(
    name="vadd",
    platform=f"{os.path.join(os.environ['XILINX_VITIS'], 'base_platforms', 'kv260_base', 'kv260_base.xpfm')}",
    template="installed_examples/vadd",
    packaging_mode="petalinux"
)
proj = client.get_sys_project(name="vadd")
proj.build(target="hw")

vitis.dispose()
