# generate device tree
set XSA_NAME hw.xsa
set DT_SRC device-tree-xlnx/

if {[file exists ${DT_SRC}] == 0} {
    # clone device tree repo if necessary
    exec -ignorestderr git clone https://github.com/Xilinx/device-tree-xlnx.git -b xilinx_v2023.2
}

hsi open_hw_design ${XSA_NAME}
hsi set_repo_path ${DT_SRC}
hsi create_sw_design device-tree -os device_tree -proc psu_cortexa53_0
hsi set_property CONFIG.dt_overlay true [hsi::get_os]
hsi set_property CONFIG.dt_zocl true [hsi::get_os]
hsi generate_target -dir _devicetree
hsi close_hw_design [hsi current_hw_design]

exec -ignorestderr dtc -o pl.dtbo _devicetree/pl.dtsi
