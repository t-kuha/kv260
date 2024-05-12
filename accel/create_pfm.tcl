#
# Create acceleration platform
#

set OUT_DIR     _pfm

# Remove existing directory
file delete -force ${OUT_DIR}

platform create -name {kv260_accel} -hw {hw.xsa} -hw_emu {hw_emu.xsa} -no-boot-bsp -out ${OUT_DIR}
platform write
platform active {kv260_accel}

domain create -name xrt -os linux -proc psu_cortexa53
domain active xrt
domain config -generate-bif
domain config -qemu-data {petalinux/images/linux}
platform write

platform generate
