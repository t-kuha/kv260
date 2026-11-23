"""Generate the KV260 PL device tree overlay with Vitis 2026.1."""

from pathlib import Path
import shutil
import tempfile

import vitis


TOP_DIR = Path(__file__).resolve().parent
XSA = TOP_DIR / "hw.xsa"
OUTPUT = TOP_DIR / "pl.dtbo"
PLATFORM_NAME = "kv260_dtbo"


def main():
    if not XSA.is_file():
        raise FileNotFoundError(f"Hardware handoff not found: {XSA}")

    with tempfile.TemporaryDirectory(prefix="_dtbo_", dir=TOP_DIR) as workspace:
        client = vitis.create_client()
        try:
            client.set_workspace(path=workspace)
            options = client.create_advanced_options_dict(
                dt_overlay="1", dt_zocl="1"
            )
            platform = client.create_platform_component(
                name=PLATFORM_NAME,
                hw_design=str(XSA),
                os="linux",
                cpu="psu_cortexa53",
                domain_name="linux_psu_cortexa53",
                no_boot_bsp=True,
                generate_dtb=True,
                advanced_options=options,
            )
            platform.build()

            overlay = (
                Path(workspace) / PLATFORM_NAME / "export" / PLATFORM_NAME
                / "sw" / "boot" / "pl.dtbo"
            )
            if not overlay.is_file():
                raise FileNotFoundError(f"Vitis did not generate {overlay}")
            shutil.copyfile(overlay, OUTPUT)
            print(f"Generated {OUTPUT}")
        finally:
            vitis.dispose()


if __name__ == "__main__":
    main()
