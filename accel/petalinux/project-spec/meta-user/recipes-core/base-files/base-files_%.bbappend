#base-files_%.bbappend content

# dirs755 += "/media/card"

FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI += "file://rtl8188eufw.bin"

do_install:append() {
	# Install wl1831's firmware
	install -d 0644 ${D}${base_libdir}/firmware/rtlwifi
	install -m 0644 rtl8188eufw.bin ${D}${base_libdir}/firmware/rtlwifi
	
	# Auto-mount boot directory of SD card 
	# sed -i '/mmcblk0p1/s/^#//g' ${D}${sysconfdir}/fstab
}
