# generate device tree
set XSA_NAME kv260.xsa
set DT_SRC ../_device-tree-xlnx/

hsi open_hw_design ${XSA_NAME}
hsi set_repo_path ${DT_SRC}
hsi create_sw_design device-tree -os device_tree -proc psu_cortexa53_0
hsi set_property CONFIG.dt_overlay true [hsi::get_os]
hsi set_property CONFIG.dt_zocl true [hsi::get_os]
hsi generate_target -dir _devicetree
hsi close_hw_design [hsi current_hw_design]
