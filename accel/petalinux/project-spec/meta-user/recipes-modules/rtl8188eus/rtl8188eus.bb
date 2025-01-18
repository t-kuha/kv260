# Kernel module for RealTek RTL8188EUS chip
# 
# Source of firmware: https://github.com/lwfinger/rtl8188eu
# 
SUMMARY = "Recipe for building an external Linux kernel module for REL8188EUS chip"
SECTION = "PETALINUX/modules"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/GPL-2.0-only;md5=801f80980d171dd6425610833a22dbe6"

FILESEXTRAPATHS:append := "${THISDIR}/files:"
SRCREV = "3fae7237ba121f1169e9a2ea55040dc123697d3b"
SRC_URI = " \
    git://github.com/aircrack-ng/rtl8188eus.git;protocol=https;branch=v5.3.9 \
    file://rtl8188eufw.bin \
    file://8188eu.conf \
"

inherit module
S = "${WORKDIR}/git"
DEPENDS += "virtual/kernel"

EXTRA_OEMAKE = "\
    CONFIG_WILC=y \
    KSRC=${STAGING_KERNEL_DIR} \
"

do_install() {
    # .ko
    install -d ${D}${base_libdir}/modules/${KERNEL_VERSION}/kernel/drivers/net/wireless/
    cp ${S}/8188eu.ko ${D}${base_libdir}/modules/${KERNEL_VERSION}/kernel/drivers/net/wireless/

    # firmware
    install -d ${D}${base_libdir}/firmware/rtlwifi
    install -m 0755 ${WORKDIR}/rtl8188eufw.bin ${D}${base_libdir}/firmware/rtlwifi
    # module list
    install -d ${D}${sysconfdir}/modules-load.d
    cp ${WORKDIR}/8188eu.conf ${D}${sysconfdir}/modules-load.d/
}

FILES:${PN} = " \
    ${base_libdir}/firmware/rtlwifi/rtl8188eufw.bin \
    ${sysconfdir}/modules-load.d/8188eu.conf \
"
