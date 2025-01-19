#
#
#
LICENSE = "CLOSED"
LIC_FILES_CHKSUM = ""

FILESEXTRAPATHS:prepend := "${THISDIR}/files:"
SRC_URI = " \
    file://binary_container_1.xclbin \
    file://pl.dtbo \
    file://shell.json \
    file://vadd \
    file://vadd_host \
"

RDEPENDS:{PN} = " xrt zocl"

do_install () {
    # add vadd
    install -d ${D}${sysconfdir}/dfx-mgrd
    install -m 0644 ${WORKDIR}/vadd ${D}${sysconfdir}/dfx-mgrd/${PN}
    install -d ${D}${libdir}/firmware/xilinx/${PN}
    install -d ${D}${bindir}
    install -m 0755 ${WORKDIR}/vadd_host ${D}${bindir}/${PN}
    install -m 0644 ${WORKDIR}/binary_container_1.xclbin ${D}${libdir}/firmware/xilinx/${PN}/${PN}.bin
    install -m 0644 ${WORKDIR}/shell.json ${D}${libdir}/firmware/xilinx/${PN}/shell.json
    install -m 0644 ${WORKDIR}/pl.dtbo ${D}${libdir}/firmware/xilinx/${PN}/${PN}.dtbo
}

FILES:${PN} = " \
    ${sysconfdir}/dfx-mgrd/${PN} \
    ${bindir}/${PN} \
    ${libdir}/firmware/xilinx/${PN}/${PN}.dtbo \
    ${libdir}/firmware/xilinx/${PN}/shell.json \
    ${libdir}/firmware/xilinx/${PN}/${PN}.bin \
"

INSANE_SKIP:${PN} = "file-rdeps ldflags"
