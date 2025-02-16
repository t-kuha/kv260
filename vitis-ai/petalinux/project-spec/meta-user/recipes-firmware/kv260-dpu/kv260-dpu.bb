#
# DPU
#
LICENSE = "CLOSED"
LIC_FILES_CHKSUM = ""

FILESEXTRAPATHS:prepend := "${THISDIR}/files:"
SRC_URI = " \
    file://dpu \
    file://dpu.bin \
    file://dpu.xclbin \
    file://dpu.dtbo \
    file://shell.json \
"

RDEPENDS:{PN} = " xrt zocl"

do_install () {
    # add bitstream etc.
    install -d ${D}${sysconfdir}/dfx-mgrd
    install -m 0644 ${WORKDIR}/dpu ${D}${sysconfdir}/dfx-mgrd/dpu
    install -d ${D}${base_libdir}/firmware/xilinx/dpu
    install -m 0644 ${WORKDIR}/dpu.bin    ${D}${base_libdir}/firmware/xilinx/dpu/dpu.bin
    install -m 0644 ${WORKDIR}/dpu.xclbin ${D}${base_libdir}/firmware/xilinx/dpu/dpu.xclbin
    install -m 0644 ${WORKDIR}/dpu.dtbo   ${D}${base_libdir}/firmware/xilinx/dpu/dpu.dtbo
    install -m 0644 ${WORKDIR}/shell.json ${D}${base_libdir}/firmware/xilinx/dpu/shell.json
}

FILES:${PN} = " \
    ${sysconfdir}/dfx-mgrd/dpu \
    ${base_libdir}/firmware/xilinx/dpu/dpu.bin \
    ${base_libdir}/firmware/xilinx/dpu/dpu.xclbin \
    ${base_libdir}/firmware/xilinx/dpu/dpu.dtbo \
    ${base_libdir}/firmware/xilinx/dpu/shell.json \
"

INSANE_SKIP:${PN} = "file-rdeps ldflags"
