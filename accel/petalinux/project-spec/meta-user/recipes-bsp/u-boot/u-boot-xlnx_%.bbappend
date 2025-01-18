FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI:append = " file://platform-top.h file://bsp.cfg"
SRC_URI += "file://user_2024-06-29-08-16-00.cfg"
