#!/usr/bin/env bash
# Build AMD EDF 26.06.1 for the accel/hw.xsa acceleration platform.
set -eo pipefail
edf_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
work_dir="$edf_dir/_work"
amd_tools_dir=${AMD_TOOLS_DIR:-/home/imagingtechnerd/amd/2026.1}
machine=kv260-accel-sdt
image=edf-linux-disk-image-kria
stage=${1:-all}

setup() {
    mkdir -p "$work_dir/bin"
    if [[ ! -x "$work_dir/bin/repo" ]]; then
        curl --fail --location --silent --show-error \
            https://storage.googleapis.com/git-repo-downloads/repo \
            -o "$work_dir/bin/repo"
        chmod +x "$work_dir/bin/repo"
    fi
    cd "$work_dir"
    if [[ ! -d .repo ]]; then
        ./bin/repo init -u https://github.com/Xilinx/yocto-manifests.git \
            -b refs/tags/amd-edf-rel-v26.06.1 -m default-edf.xml --depth=1
    fi
    ./bin/repo sync -j4 --fail-fast
    ./bin/repo manifest -r -o manifest.lock.xml
    cat > "$edf_dir/bitbake.apparmor" <<EOF
abi <abi/4.0>,
include <tunables/global>
profile kv260-edf-bitbake $work_dir/sources/poky/bitbake/bin/bitbake flags=(unconfined) {
    userns,
}
EOF
}

sdt() {
    "$amd_tools_dir/Vivado/bin/sdtgen" \
        -xsa "$edf_dir/../hw.xsa" -dir "$work_dir/sdt" \
        -user_dts zynqmp-smk-k26-reva.dtsi zynqmp-sck-kv-g-revb.dtsi \
        -zocl enable
    # An archive avoids embedding the host's absolute directory tree in the SDT.
    tar -czf "$work_dir/kv260-sdt.tar.gz" -C "$work_dir/sdt" .
    sha256sum "$edf_dir/../hw.xsa" > "$work_dir/hardware.sha256"
}

init_env() {
    if [[ -n ${XILINX_VIVADO:-} || -n ${XILINX_VITIS:-} || -n ${PETALINUX:-} ]]; then
        echo "Run EDF from a fresh shell without Vivado/Vitis/PetaLinux settings." >&2
        exit 1
    fi
    cd "$work_dir"
    source ./edf-init-build-env > /dev/null
}

configure() {
    init_env
    if ! bitbake-layers show-layers | grep -q '^meta-kv260 '; then
        bitbake-layers add-layer "$edf_dir/meta-kv260"
    fi
    if ! grep -Fq "$edf_dir/local.conf.inc" conf/local.conf; then
        printf '\nrequire %s/local.conf.inc\n' "$edf_dir" >> conf/local.conf
    fi
    gen_cmd=(gen-machine-conf
        --template ../sources/meta-kria/conf/machineyaml/k26-smk-kv-sdt.yaml
        --machine-name "$machine" -c "$edf_dir/meta-kv260/conf"
        parse-sdt --hw-description "$work_dir/kv260-sdt.tar.gz" -g full)
    # The generator starts BitBake via Python, so inherit its namespace profile.
    if command -v aa-exec > /dev/null && \
       [[ $(cat /proc/sys/kernel/apparmor_restrict_unprivileged_userns 2>/dev/null) == 1 ]]; then
        if ! aa-exec -p kv260-edf-bitbake -- true 2>/dev/null; then
            echo "Ubuntu requires the workspace's BitBake namespace profile." >&2
            echo "Load it with: sudo apparmor_parser -r $edf_dir/bitbake.apparmor" >&2
            exit 1
        fi
        aa-exec -p kv260-edf-bitbake -- "${gen_cmd[@]}"
    else
        "${gen_cmd[@]}"
    fi
}

build() {
    init_env
    MACHINE="$machine" bitbake xilinx-bootbin "$image"
    ln -sfn "$work_dir/build/tmp/deploy/images/$machine" "$edf_dir/images"
    echo "EDF artifacts: $edf_dir/images"
}

case "$stage" in
    setup) setup ;;
    sdt) sdt ;;
    configure) configure ;;
    build) build ;;
    all) setup; sdt; configure; build ;;
    *) echo "Usage: $0 [all|setup|sdt|configure|build]" >&2; exit 2 ;;
esac
