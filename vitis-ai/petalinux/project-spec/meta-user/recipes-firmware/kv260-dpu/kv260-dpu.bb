#
# DPU
#
LICENSE = "CLOSED"
LIC_FILES_CHKSUM = ""

FILESEXTRAPATHS:prepend := "${THISDIR}/files:"
SRC_URI = " \
    file://dpu \
    file://dpu.bin \
    file://dpu.dtbo \
    file://shell.json \
"

RDEPENDS:{PN} = " xrt zocl"

do_install () {
    # add vadd
    install -d ${D}${sysconfdir}/dfx-mgrd
    install -m 0644 ${WORKDIR}/dpu ${D}${sysconfdir}/dfx-mgrd/dpu
    install -d ${D}${libdir}/firmware/xilinx/dpu
    install -m 0644 ${WORKDIR}/dpu.bin    ${D}${libdir}/firmware/xilinx/dpu/dpu.bin
    install -m 0644 ${WORKDIR}/dpu.dtbo   ${D}${libdir}/firmware/xilinx/dpu/dpu.dtbo
    install -m 0644 ${WORKDIR}/shell.json ${D}${libdir}/firmware/xilinx/dpu/shell.json
}

FILES:${PN} = " \
    ${sysconfdir}/dfx-mgrd/dpu \
    ${libdir}/firmware/xilinx/dpu/dpu.bin \
    ${libdir}/firmware/xilinx/dpu/dpu.dtbo \
    ${libdir}/firmware/xilinx/dpu/shell.json \
"

INSANE_SKIP:${PN} = "file-rdeps ldflags"
