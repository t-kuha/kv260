# The Linux-only custom machine builds BOOT.BIN separately. The full Kria
# QSPI bundle supports only AMD's multidomain machines (image selector/recovery).
EXTRA_IMAGEDEPENDS:remove:kv260-accel-sdt = "kria-qspi"

# EDF selects XRT only for its predefined common machine names.
IMAGE_INSTALL:append:kv260-accel-sdt = " xrt"
