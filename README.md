# Qualcomm repository map

Qualcomm repositories: public repositories in Qualcomm's GitHub organisations (qualcomm-linux and qualcomm). Upstream projects, board vendors, and tools are not recorded. The map is not limited to a release or engagement.

**Coverage:** 126 repositories; 19 recorded build/component relationships.

Repository inventory is broader than reviewed relationships. An absent edge means no relationship has been recorded, not proof of independence.

Click a repository node to open it. Indirect connections follow the actual path through their provider.

- [Yocto builds and releases](#yocto-builds-and-releases)
- [Kernel integration](#kernel-integration)
- [Source packaging](#source-packaging)

## Yocto builds and releases

```mermaid
flowchart LR
    r0["kernel"]
    click r0 href "https://github.com/qualcomm-linux/kernel" _blank
    r1["meta-ai"]
    click r1 href "https://github.com/qualcomm-linux/meta-ai" _blank
    r2["meta-qcom"]
    click r2 href "https://github.com/qualcomm-linux/meta-qcom" _blank
    r3["meta-qcom-3rdparty"]
    click r3 href "https://github.com/qualcomm-linux/meta-qcom-3rdparty" _blank
    r4["meta-qcom-distro"]
    click r4 href "https://github.com/qualcomm-linux/meta-qcom-distro" _blank
    r5["meta-qcom-hwe"]
    click r5 href "https://github.com/qualcomm-linux/meta-qcom-hwe" _blank
    r6["meta-qcom-releases"]
    click r6 href "https://github.com/qualcomm-linux/meta-qcom-releases" _blank
    r7["qcom-ptool"]
    click r7 href "https://github.com/qualcomm-linux/qcom-ptool" _blank
    r8["fastrpc"]
    click r8 href "https://github.com/qualcomm/fastrpc" _blank
    r2 -->|"fetches Linux kernel sources from"| r0
    r2 -->|"includes for Qualcomm Linux images"| r1
    r2 -->|"includes for Qualcomm Linux images"| r4
    r2 -->|"gets partition tools from"| r7
    r2 -->|"fetches sources from"| r8
    r3 -->|"adds third-party board support to"| r2
    r3 -->|"can use Qualcomm Linux settings from"| r4
    r3 -->|"builds on (scarthgap, kirkstone)"| r5
    r6 -->|"pins a release of"| r2
```

## Kernel integration

```mermaid
flowchart LR
    r0["automerge"]
    click r0 href "https://github.com/qualcomm-linux/automerge" _blank
    r1["kernel"]
    click r1 href "https://github.com/qualcomm-linux/kernel" _blank
    r2["kernel-checkers"]
    click r2 href "https://github.com/qualcomm-linux/kernel-checkers" _blank
    r3["kernel-config"]
    click r3 href "https://github.com/qualcomm-linux/kernel-config" _blank
    r4["kernel-topics"]
    click r4 href "https://github.com/qualcomm-linux/kernel-topics" _blank
    r5["ubuntu-qcom-kernel"]
    click r5 href "https://github.com/qualcomm-linux/ubuntu-qcom-kernel" _blank
    r6["upload-private-artifact-action"]
    click r6 href "https://github.com/qualcomm-linux/upload-private-artifact-action" _blank
    r7["commit-emails-check-action"]
    click r7 href "https://github.com/qualcomm/commit-emails-check-action" _blank
    r2 -->|"runs automation from"| r3
    r3 -->|"configures"| r0
    r3 -->|"selects branches from"| r1
    r3 -->|"runs automation from"| r2
    r3 -->|"selects branches from"| r4
    r3 -->|"runs automation from"| r7
    r5 -->|"runs automation from"| r6
```

## Source packaging

```mermaid
flowchart LR
    r0["gbm-msm-backend"]
    click r0 href "https://github.com/qualcomm-linux/gbm-msm-backend" _blank
    r1["kgsl"]
    click r1 href "https://github.com/qualcomm-linux/kgsl" _blank
    r2["pkg-gbm-msm-backend"]
    click r2 href "https://github.com/qualcomm-linux/pkg-gbm-msm-backend" _blank
    r3["pkg-kgsl"]
    click r3 href "https://github.com/qualcomm-linux/pkg-kgsl" _blank
    r4["pkg-urm"]
    click r4 href "https://github.com/qualcomm-linux/pkg-urm" _blank
    r5["userspace-resource-manager"]
    click r5 href "https://github.com/qualcomm/userspace-resource-manager" _blank
    r2 -->|"packages sources from"| r0
    r3 -->|"packages sources from"| r1
    r4 -->|"packages sources from"| r5
```

## Reference details

<details>
<summary>Repository inventory</summary>

### Boot and firmware

- [qualcomm-linux/boot-firmware-ci](https://github.com/qualcomm-linux/boot-firmware-ci) — Boot Firmware CI/CD repo providing build artifacts for reuse across distros (default branch: `main`).
- [qualcomm-linux/edk2](https://github.com/qualcomm-linux/edk2) — Qualcomm upstream staging repo for edk2 (default branch: `qcom-next`).
- [qualcomm-linux/edk2-platforms](https://github.com/qualcomm-linux/edk2-platforms) — Qualcomm upstream staging repo for edk2-platforms (default branch: `qcom-next`).
- [qualcomm-linux/optee_os](https://github.com/qualcomm-linux/optee_os) — Qualcomm upstream staging repo for OP-TEE OS (default branch: `qcom-next`).
- [qualcomm-linux/qcom-ptool](https://github.com/qualcomm-linux/qcom-ptool) — qcom-ptool contains various device partitioning utilities like ptool.py, gen_partitions.py and various sample partition configuration files needed for Qualcomm SoCs. (default branch: `main`).
- [qualcomm-linux/qcom-sec-tools-wrapper](https://github.com/qualcomm-linux/qcom-sec-tools-wrapper) — Shell tooling around Qualcomm's secure boot flow - generate OEM keys, sign images, provision fuses, and build UEFI update capsules. (default branch: `main`).
- [qualcomm-linux/snagboot](https://github.com/qualcomm-linux/snagboot) — Generic recovery and reflashing tool for embedded platforms (default branch: `main`).
- [qualcomm-linux/trusted-firmware-a](https://github.com/qualcomm-linux/trusted-firmware-a) — Qualcomm upstream staging repo for Trusted Firmware-A (default branch: `qcom-next`).
- [qualcomm-linux/u-boot](https://github.com/qualcomm-linux/u-boot) — "Das U-Boot" Source Tree (default branch: `master`).

### Images and build tooling

- [qualcomm-linux/docker-pkg-build](https://github.com/qualcomm-linux/docker-pkg-build) — Debian packages build tool for native (arm64-arm64) or cross (amd64-arm64) build (default branch: `main`).
- [qualcomm-linux/qcom-build-utils](https://github.com/qualcomm-linux/qcom-build-utils) — Qualcomm utilities for Linux builds (default branch: `main`).
- [qualcomm-linux/qcom-deb-images](https://github.com/qualcomm-linux/qcom-deb-images) — Qualcomm Linux Debian build scripts (default branch: `main`).
- [qualcomm-linux/qcom-rpm-utils](https://github.com/qualcomm-linux/qcom-rpm-utils) — This repo will hold build scripts and reusable workflows for pkg rpm builds. (default branch: `main`).
- [qualcomm-linux/qli-ci](https://github.com/qualcomm-linux/qli-ci) — Central location for pkg reusable workflows (default branch: `main`).
- [qualcomm-linux/rpm-images](https://github.com/qualcomm-linux/rpm-images) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `main`).
- [qualcomm/commit-emails-check-action](https://github.com/qualcomm/commit-emails-check-action) — GitHub action for checking email addresses in PR/Push commits (default branch: `main`).
- [qualcomm/qcom-reusable-workflows](https://github.com/qualcomm/qcom-reusable-workflows) — Qualcomm reusable workflows (default branch: `main`).

### Kernel integration

- [qualcomm-linux/automerge](https://github.com/qualcomm-linux/automerge) — Tools to manage creation of qcom-next from the topic branches (default branch: `main`).
- [qualcomm-linux/kernel](https://github.com/qualcomm-linux/kernel) — Linux Kernel for QLI mainline (default branch: `main`).
- [qualcomm-linux/kernel-checkers](https://github.com/qualcomm-linux/kernel-checkers) — Checker tests kernel patches for correctness by running a suite of tests. (default branch: `main`).
- [qualcomm-linux/kernel-config](https://github.com/qualcomm-linux/kernel-config) — Configuration data to create qcom-next from the tech topic branches (default branch: `main`).
- [qualcomm-linux/kernel-topics](https://github.com/qualcomm-linux/kernel-topics) — Tech Topic Branches for QLI mainline (default branch: `main`).
- [qualcomm-linux/kmake-image](https://github.com/qualcomm-linux/kmake-image) — Docker setup for building the Linux kernel (default branch: `main`).
- [qualcomm-linux/ubuntu-qcom-kernel](https://github.com/qualcomm-linux/ubuntu-qcom-kernel) — Mirror and CI build pipeline for Canonical kernel  (default branch: `main`).

### Layers and releases

- [qualcomm-linux/meta-ai](https://github.com/qualcomm-linux/meta-ai) — OpenEmbedded layer for AI/ML related recipes (default branch: `main`).
- [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom) — OpenEmbedded/Yocto Project BSP layer for Qualcomm based platforms (default branch: `master`).
- [qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) — OpenEmbedded/Yocto Project BSP layer for Third-Party Maintained Qualcomm based platforms (default branch: `main`).
- [qualcomm-linux/meta-qcom-arduino](https://github.com/qualcomm-linux/meta-qcom-arduino) — OpenEmbedded/Yocto Project BSP layer for Qualcomm based Arduino platforms (default branch: `main`).
- [qualcomm-linux/meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro) — OpenEmbedded/Yocto Project Reference Distribution layer for Qualcomm based platforms (default branch: `main`).
- [qualcomm-linux/meta-qcom-extras-releases](https://github.com/qualcomm-linux/meta-qcom-extras-releases) — This repo will be used to store kas-lock files for milestone releases of meta-qcom-extras (default branch: `main`).
- [qualcomm-linux/meta-qcom-hwe](https://github.com/qualcomm-linux/meta-qcom-hwe) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `main`).
- [qualcomm-linux/meta-qcom-qim-product-sdk](https://github.com/qualcomm-linux/meta-qcom-qim-product-sdk) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `scarthgap`).
- [qualcomm-linux/meta-qcom-realtime](https://github.com/qualcomm-linux/meta-qcom-realtime) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `scarthgap`).
- [qualcomm-linux/meta-qcom-releases](https://github.com/qualcomm-linux/meta-qcom-releases) — This repo will be used to store kas-lock files for milestone releases of meta-qcom (default branch: `main`).
- [qualcomm-linux/meta-qcom-robotics](https://github.com/qualcomm-linux/meta-qcom-robotics) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `scarthgap`).
- [qualcomm-linux/meta-qcom-robotics-distro](https://github.com/qualcomm-linux/meta-qcom-robotics-distro) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `scarthgap`).
- [qualcomm-linux/meta-qcom-robotics-releases](https://github.com/qualcomm-linux/meta-qcom-robotics-releases) — This repo will be used to store kas-lock files for milestone releases of meta-qcom-robotics-sdk (default branch: `main`).
- [qualcomm-linux/meta-qcom-robotics-sdk](https://github.com/qualcomm-linux/meta-qcom-robotics-sdk) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `main`).
- [qualcomm-linux/qcom-manifest](https://github.com/qualcomm-linux/qcom-manifest) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qcom-linux-scarthgap`).

### Other repositories

- [qualcomm-linux/.github](https://github.com/qualcomm-linux/.github) — Qualcomm Linux GitHub organization action templates and configs (default branch: `main`).
- [qualcomm-linux/Robotics-SDK-Ubuntu](https://github.com/qualcomm-linux/Robotics-SDK-Ubuntu) —  Qualcomm Intelligent Robotics SDK (QIR SDK) for ubuntu (default branch: `main`).
- [qualcomm-linux/TC9564_Host_Driver](https://github.com/qualcomm-linux/TC9564_Host_Driver) — TC9564 PCIe-Ethernet Bridge Linux Host Driver (default branch: `qcom`).
- [qualcomm-linux/abctl](https://github.com/qualcomm-linux/abctl) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `main`).
- [qualcomm-linux/apt-artifactory-action](https://github.com/qualcomm-linux/apt-artifactory-action) — A GitHub Action for managing Debian packages in JFrog Artifactory. This action streamlines workflows for uploading artifacts, validating metadata, cleaning up stale packages, and performing custom operations on APT repositories hosted in Artifactory. (default branch: `main`).
- [qualcomm-linux/bitbake-lint-action](https://github.com/qualcomm-linux/bitbake-lint-action) — GitHub Action for linting bitbake recipes using oelint-adv linter  (default branch: `main`).
- [qualcomm-linux/camera-driver](https://github.com/qualcomm-linux/camera-driver) — This repository contains the source code of camera-kernel driver for the downstream camera-kernel (default branch: `camera-kernel.qclinux.0.0`).
- [qualcomm-linux/clk-debug-tools-for-qualcomm-linux](https://github.com/qualcomm-linux/clk-debug-tools-for-qualcomm-linux) — Out-of-tree clk debug patches for linux-next and scripts for clock-measurement based debugging on Qualcomm SoCs. (default branch: `main`).
- [qualcomm-linux/debusine-action](https://github.com/qualcomm-linux/debusine-action) — A GitHub Actions composite action that automates uploading Debian source packages and triggering Debusine workflows. (default branch: `main`).
- [qualcomm-linux/display-driver](https://github.com/qualcomm-linux/display-driver) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `main`).
- [qualcomm-linux/eva-driver](https://github.com/qualcomm-linux/eva-driver) — This repository contains the source code of eva-kernel driver for the downstream eva-kernel (default branch: `eva-kernel.qclinux.0.0`).
- [qualcomm-linux/gbm-msm-backend](https://github.com/qualcomm-linux/gbm-msm-backend) — MSM Backend repository to overlay on top of upstream MESA GBM. (default branch: `main`).
- [qualcomm-linux/github-action-matrix-outputs-read](https://github.com/qualcomm-linux/github-action-matrix-outputs-read) — Workaround implementation - Read matrix jobs outputs (default branch: `main`).
- [qualcomm-linux/github-action-matrix-outputs-write](https://github.com/qualcomm-linux/github-action-matrix-outputs-write) — Workaround implementation - Write matrix jobs outputs (default branch: `main`).
- [qualcomm-linux/kgsl](https://github.com/qualcomm-linux/kgsl) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `gfx-kernel.le.0.0`).
- [qualcomm-linux/location-apis-qcom](https://github.com/qualcomm-linux/location-apis-qcom) — Location Client API layer for Qualcomm based platforms (default branch: `location.lnx.0.0`).
- [qualcomm-linux/location-hal-qcom](https://github.com/qualcomm-linux/location-hal-qcom) — Location hal layer for Qualcomm based platforms (default branch: `location.lnx.0.0`).
- [qualcomm-linux/qcom-dtb-metadata](https://github.com/qualcomm-linux/qcom-dtb-metadata) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `main`).
- [qualcomm-linux/qcom-linux-skills](https://github.com/qualcomm-linux/qcom-linux-skills) — Agent Skills for Qualcomm Linux (default branch: `main`).
- [qualcomm-linux/qualcomm-CDI-generator](https://github.com/qualcomm-linux/qualcomm-CDI-generator) — Tooling to generate CDI config files to pass devices through to containers (default branch: `main`).
- [qualcomm-linux/rtss-mailbox-kmd](https://github.com/qualcomm-linux/rtss-mailbox-kmd) — RTSS Mailbox Kernel Mode Driver (KMD) for IPC-based inter-processor communication on Qualcomm Automotive, IE-IoT, Robotics SoCs. (default branch: `main`).
- [qualcomm-linux/rtss-mailbox-umd](https://github.com/qualcomm-linux/rtss-mailbox-umd) — RTSS Mailbox User Space package of libraries, demo applications, utils for Qualcomm Automotive, IE-IoT, Robotics SoCs. (default branch: `main`).
- [qualcomm-linux/upload-private-artifact-action](https://github.com/qualcomm-linux/upload-private-artifact-action) — An action for use in qualcomm-linux projects that need to publish CI artifacts that aren't cleared for public distribution. (default branch: `aws`).
- [qualcomm-linux/video-driver](https://github.com/qualcomm-linux/video-driver) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `video.qclinux.main`).
- [qualcomm-linux/weston-sdm-backend](https://github.com/qualcomm-linux/weston-sdm-backend) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `main`).
- [qualcomm/fastrpc](https://github.com/qualcomm/fastrpc) — FastRPC library and daemons for offloading work to Hexagon DSPs. (default branch: `not inventoried`).
- [qualcomm/userspace-resource-manager](https://github.com/qualcomm/userspace-resource-manager) — Upstream userspace resource manager source packaged by pkg-urm. (default branch: `not inventoried`).

### Packaging

- [qualcomm-linux/pkg-adreno](https://github.com/qualcomm-linux/pkg-adreno) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-alsa-ucm-conf](https://github.com/qualcomm-linux/pkg-alsa-ucm-conf) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-android-platform-tools](https://github.com/qualcomm-linux/pkg-android-platform-tools) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-audioreach-audio-utils](https://github.com/qualcomm-linux/pkg-audioreach-audio-utils) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-audioreach-conf](https://github.com/qualcomm-linux/pkg-audioreach-conf) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-audioreach-dkms](https://github.com/qualcomm-linux/pkg-audioreach-dkms) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-audioreach-graphmgr](https://github.com/qualcomm-linux/pkg-audioreach-graphmgr) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-audioreach-graphservices](https://github.com/qualcomm-linux/pkg-audioreach-graphservices) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-audioreach-pal](https://github.com/qualcomm-linux/pkg-audioreach-pal) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-audioreach-pipewire-plugin](https://github.com/qualcomm-linux/pkg-audioreach-pipewire-plugin) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-btftm](https://github.com/qualcomm-linux/pkg-btftm) — this is for bt-performant.qclinux.0.0  Btdiag debian generate and upload to apt (default branch: `qli-ci`).
- [qualcomm-linux/pkg-camx-dev](https://github.com/qualcomm-linux/pkg-camx-dev) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-camx-dkms](https://github.com/qualcomm-linux/pkg-camx-dkms) — repo to created camx-dlkm debian (default branch: `qli-ci`).
- [qualcomm-linux/pkg-camx-firmware-glymur](https://github.com/qualcomm-linux/pkg-camx-firmware-glymur) — add repo for glymur target firmware (default branch: `qli-ci`).
- [qualcomm-linux/pkg-camx-firmware-hamoa](https://github.com/qualcomm-linux/pkg-camx-firmware-hamoa) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-camx-firmware-kodiak](https://github.com/qualcomm-linux/pkg-camx-firmware-kodiak) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-camx-firmware-lemans](https://github.com/qualcomm-linux/pkg-camx-firmware-lemans) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-camx-firmware-talos](https://github.com/qualcomm-linux/pkg-camx-firmware-talos) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-camx-glymur](https://github.com/qualcomm-linux/pkg-camx-glymur) — repo for glymur target (default branch: `qli-ci`).
- [qualcomm-linux/pkg-camx-hamoa](https://github.com/qualcomm-linux/pkg-camx-hamoa) — Camera hamoa (default branch: `qli-ci`).
- [qualcomm-linux/pkg-camx-kodiak](https://github.com/qualcomm-linux/pkg-camx-kodiak) — camx kodiak UMD Debian creation (default branch: `qli-ci`).
- [qualcomm-linux/pkg-camx-lemans](https://github.com/qualcomm-linux/pkg-camx-lemans) — camx lemans UMD Debian creation (default branch: `qli-ci`).
- [qualcomm-linux/pkg-camx-nhx](https://github.com/qualcomm-linux/pkg-camx-nhx) — camx test Debian creation (default branch: `qli-ci`).
- [qualcomm-linux/pkg-camx-talos](https://github.com/qualcomm-linux/pkg-camx-talos) — camx talos UMD Debian. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-diag-router](https://github.com/qualcomm-linux/pkg-diag-router) — Debain package repo for qcom-diag-router (default branch: `qli-ci`).
- [qualcomm-linux/pkg-eva-dkms](https://github.com/qualcomm-linux/pkg-eva-dkms) — Qcom Linux repo to generate the EVA dlkm debian packages (default branch: `qli-ci`).
- [qualcomm-linux/pkg-fastrpc](https://github.com/qualcomm-linux/pkg-fastrpc) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-gbm-msm-backend](https://github.com/qualcomm-linux/pkg-gbm-msm-backend) — Packaging repo for gbm-msm-backend (default branch: `qli-ci`).
- [qualcomm-linux/pkg-gst-plugins-imsdk](https://github.com/qualcomm-linux/pkg-gst-plugins-imsdk) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-kgsl](https://github.com/qualcomm-linux/pkg-kgsl) — Packaging repo for kgsl (default branch: `qli-ci`).
- [qualcomm-linux/pkg-libdiag](https://github.com/qualcomm-linux/pkg-libdiag) — Deb file distribution repo for libdiag and diagnostics utils  (default branch: `qli-ci`).
- [qualcomm-linux/pkg-linux-qcom](https://github.com/qualcomm-linux/pkg-linux-qcom) — QCOM Linux Kernel Debian Package repository (default branch: `main`).
- [qualcomm-linux/pkg-mink-idl-compiler](https://github.com/qualcomm-linux/pkg-mink-idl-compiler) — Debian packaging meta-data for mink-idl-compiler project. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-minkipc](https://github.com/qualcomm-linux/pkg-minkipc) — Debian packaging meta-data for minkipc project. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-optee-client](https://github.com/qualcomm-linux/pkg-optee-client) — Debian package meta-data to package Qualcomm vendored mink optee-client library (default branch: `qli-ci`).
- [qualcomm-linux/pkg-optee-test](https://github.com/qualcomm-linux/pkg-optee-test) — Debian package meta-data to package Qualcomm vendored mink xtest for QTEE (default branch: `qli-ci`).
- [qualcomm-linux/pkg-qcom-fastcv-binaries](https://github.com/qualcomm-linux/pkg-qcom-fastcv-binaries) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-qcom-sensors](https://github.com/qualcomm-linux/pkg-qcom-sensors) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-qcom-sv-binaries](https://github.com/qualcomm-linux/pkg-qcom-sv-binaries) — Qcom Linux SV Debian packaging repository (default branch: `qli-ci`).
- [qualcomm-linux/pkg-qimsdk-smartvenc](https://github.com/qualcomm-linux/pkg-qimsdk-smartvenc) — pkg-bin-smart-venc-ctrl (default branch: `qli-ci`).
- [qualcomm-linux/pkg-qmi-framework](https://github.com/qualcomm-linux/pkg-qmi-framework) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-qti-camera-service](https://github.com/qualcomm-linux/pkg-qti-camera-service) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-quic-teec](https://github.com/qualcomm-linux/pkg-quic-teec) — Debian packaging meta-data for quic-teec project. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-ros-jazzy-xsens-mti-ros2-driver](https://github.com/qualcomm-linux/pkg-ros-jazzy-xsens-mti-ros2-driver) — ROS 2 driver for Xsens MTi IMU sensors (default branch: `qcom/debian/latest`).
- [qualcomm-linux/pkg-rpm-qcom-fastcv-binaries](https://github.com/qualcomm-linux/pkg-rpm-qcom-fastcv-binaries) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `main`).
- [qualcomm-linux/pkg-rpm-video-driver](https://github.com/qualcomm-linux/pkg-rpm-video-driver) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `main`).
- [qualcomm-linux/pkg-sensinghub](https://github.com/qualcomm-linux/pkg-sensinghub) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-thermald](https://github.com/qualcomm-linux/pkg-thermald) — Debian overlay package for thermald: backports upstream patches  (default branch: `qli-ci`).
- [qualcomm-linux/pkg-time-services](https://github.com/qualcomm-linux/pkg-time-services) — Time-services package repo (default branch: `qli-ci`).
- [qualcomm-linux/pkg-tinyalsa](https://github.com/qualcomm-linux/pkg-tinyalsa) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-tinycompress](https://github.com/qualcomm-linux/pkg-tinycompress) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qli-ci`).
- [qualcomm-linux/pkg-urm](https://github.com/qualcomm-linux/pkg-urm) — This project handles Debian packaging for the URM project (<https://github.com/qualcomm/userspace-resource-manager>) (default branch: `qli-ci`).
- [qualcomm-linux/pkg-urm-ext](https://github.com/qualcomm-linux/pkg-urm-ext) — This project handles Debian packaging for the URM extension project i.e <https://github.com/qualcomm/userspace-resource-manager-extensions>  (default branch: `qli-ci`).
- [qualcomm-linux/pkg-video-driver](https://github.com/qualcomm-linux/pkg-video-driver) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `qli-ci`).

### Validation

- [qualcomm-linux/aiml-container-test](https://github.com/qualcomm-linux/aiml-container-test) — Container targeted at testing AI and ML workloads for Qualcomm platforms (default branch: `main`).
- [qualcomm-linux/awstest-meta-qcom](https://github.com/qualcomm-linux/awstest-meta-qcom) — OpenEmbedded/Yocto Project BSP layer for Qualcomm based platforms (default branch: `master`).
- [qualcomm-linux/job_render](https://github.com/qualcomm-linux/job_render) — Lava job render (default branch: `main`).
- [qualcomm-linux/lava-test-plans](https://github.com/qualcomm-linux/lava-test-plans) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `master`).
- [qualcomm-linux/mark-test](https://github.com/qualcomm-linux/mark-test) — Repository purpose needs review; open the repository for its maintained documentation. (default branch: `main`).
- [qualcomm-linux/qcom-linux-testkit](https://github.com/qualcomm-linux/qcom-linux-testkit) — This repository provides standalone validation scripts designed to test and verify various Linux features, particularly for Qualcomm RB3Gen2 and platforms based on meta-qcom and meta-qcom-distros. (default branch: `main`).

</details>

<details>
<summary>Relationship applicability and sources</summary>

### qualcomm-linux/kernel-checkers

- **runs automation from** [kernel-config](https://github.com/qualcomm-linux/kernel-config)
  - GitHub Actions integration
  - [checker.yml](https://github.com/qualcomm-linux/kernel-checkers/blob/23c35b0e159903b2f69ec5d11f5b6e5dcd493319/.github/workflows/checker.yml)

### qualcomm-linux/kernel-config

- **configures** [automerge](https://github.com/qualcomm-linux/automerge)
  - qcom-next integration configuration.
  - [README](https://github.com/qualcomm-linux/kernel-config/blob/ca3a00b71520dd58ede87f9c2921b48f95ac0b32/README)
- **selects branches from** [kernel](https://github.com/qualcomm-linux/kernel)
  - qcom-next.conf names baseline and topic branches.
  - [qcom-next.conf](https://github.com/qualcomm-linux/kernel-config/blob/ca3a00b71520dd58ede87f9c2921b48f95ac0b32/qcom-next.conf)
- **runs automation from** [kernel-checkers](https://github.com/qualcomm-linux/kernel-checkers)
  - GitHub Actions integration
  - [kernel_checker.yml](https://github.com/qualcomm-linux/kernel-config/blob/ca3a00b71520dd58ede87f9c2921b48f95ac0b32/.github/workflows/kernel_checker.yml)
- **selects branches from** [kernel-topics](https://github.com/qualcomm-linux/kernel-topics)
  - qcom-next.conf names baseline and topic branches.
  - [qcom-next.conf](https://github.com/qualcomm-linux/kernel-config/blob/ca3a00b71520dd58ede87f9c2921b48f95ac0b32/qcom-next.conf)
- **runs automation from** [commit-emails-check-action](https://github.com/qualcomm/commit-emails-check-action)
  - GitHub Actions integration
  - [email_checker.yml](https://github.com/qualcomm-linux/kernel-config/blob/ca3a00b71520dd58ede87f9c2921b48f95ac0b32/.github/workflows/email_checker.yml)

### qualcomm-linux/meta-qcom

- **fetches Linux kernel sources from** [kernel](https://github.com/qualcomm-linux/kernel)
  - linux-qcom-next recipe; kernel provider and source revision are configuration-dependent.
  - [linux-qcom-next_git.bb](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/recipes-kernel/linux/linux-qcom-next_git.bb)
- **includes for Qualcomm Linux images** [meta-ai](https://github.com/qualcomm-linux/meta-ai)
  - Optional qcom-distro kas composition; not required by every BSP-only build.
  - [qcom-distro.yml](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/ci/qcom-distro.yml)
- **includes for Qualcomm Linux images** [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro)
  - Optional qcom-distro kas composition; not required by every BSP-only build.
  - [qcom-distro.yml](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/ci/qcom-distro.yml)
- **gets partition tools from** [qcom-ptool](https://github.com/qualcomm-linux/qcom-ptool)
  - Partition recipe source; pinned by qcom-ptool.inc.
  - [qcom-ptool.inc](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/recipes-bsp/partition/qcom-ptool.inc)
- **fetches sources from** [fastrpc](https://github.com/qualcomm/fastrpc)
  - fastrpc recipe; the tagged release is pinned by SRCREV.
  - [fastrpc_1.0.7.bb](https://github.com/qualcomm-linux/meta-qcom/blob/1d8048f3a515eeef3758868566ec847b63065811/recipes-support/fastrpc/fastrpc_1.0.7.bb)

### qualcomm-linux/meta-qcom-3rdparty

- **through [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)** [kernel](https://github.com/qualcomm-linux/kernel)
  - linux-qcom-next recipe; kernel provider and source revision are configuration-dependent.
  - [rubikpi3.conf](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/conf/machine/rubikpi3.conf)
  - [linux-qcom-next_git.bb](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/recipes-kernel/linux/linux-qcom-next_git.bb)
- **through [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)** [meta-ai](https://github.com/qualcomm-linux/meta-ai)
  - Optional qcom-distro kas composition; not required by every BSP-only build.
  - [qcom-distro.yml](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/ci/qcom-distro.yml)
  - [qcom-distro.yml](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/ci/qcom-distro.yml)
- **adds third-party board support to** [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)
  - wrynose-compatible main snapshot 8927b428bcae; required layer collection.
  - [layer.conf](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/conf/layer.conf)
- **can use Qualcomm Linux settings from** [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro)
  - Optional: the dynamic layer applies only when qcom-distro is present.
  - [layer.conf](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/conf/layer.conf)
- **builds on (scarthgap, kirkstone)** [meta-qcom-hwe](https://github.com/qualcomm-linux/meta-qcom-hwe)
  - scarthgap and kirkstone branches only (Qualcomm Linux 1.x); required layer collection. main and wrynose do not depend on it.
  - [layer.conf](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/b411da79d08b3726eeba85df834627008b31fd7c/conf/layer.conf)
  - [layer.conf](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/d2f48af6ee98870294be24c16673dde7fa941543/conf/layer.conf)
- **through [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)** [qcom-ptool](https://github.com/qualcomm-linux/qcom-ptool)
  - Partition tooling is supplied through meta-qcom; this is an indirect relationship, not an extra layer dependency.
  - [qcom-ptool.inc](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/recipes-bsp/partition/qcom-ptool.inc)
  - [rubikpi3.conf](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/conf/machine/rubikpi3.conf)
- **through [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)** [fastrpc](https://github.com/qualcomm/fastrpc)
  - Both machines: the QCS6490 SoC include they require recommends packagegroup-qcom-boot-additional, which adds fastrpc on aarch64.
  - [rubikpi3.conf](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/conf/machine/rubikpi3.conf)
  - [qcom-qcs6490.inc](https://github.com/qualcomm-linux/meta-qcom/blob/1d8048f3a515eeef3758868566ec847b63065811/conf/machine/include/qcom-qcs6490.inc)
  - [packagegroup-qcom.bb](https://github.com/qualcomm-linux/meta-qcom/blob/1d8048f3a515eeef3758868566ec847b63065811/recipes-bsp/packagegroups/packagegroup-qcom.bb)
  - [fastrpc_1.0.7.bb](https://github.com/qualcomm-linux/meta-qcom/blob/1d8048f3a515eeef3758868566ec847b63065811/recipes-support/fastrpc/fastrpc_1.0.7.bb)

### qualcomm-linux/meta-qcom-releases

- **pins a release of** [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)
  - Milestone tags and kas lock files; select the desired release tag.
  - [README.md](https://github.com/qualcomm-linux/meta-qcom-releases/blob/4129a6850c070bb57da122b2ebceff3de9951a1a/README.md)

### qualcomm-linux/pkg-gbm-msm-backend

- **packages sources from** [gbm-msm-backend](https://github.com/qualcomm-linux/gbm-msm-backend)
  - Package metadata and source ownership are separate; choose the package branch before editing packaging.
  - [README.md](https://github.com/qualcomm-linux/pkg-gbm-msm-backend/blob/f6b4fbab5add28563a816f3c49f94c5651c04972/README.md)

### qualcomm-linux/pkg-kgsl

- **packages sources from** [kgsl](https://github.com/qualcomm-linux/kgsl)
  - Package metadata and source ownership are separate; choose the package branch before editing packaging.
  - [README.md](https://github.com/qualcomm-linux/pkg-kgsl/blob/e86b135670ce1464db9035193492ddf08ad7f5ed/README.md)

### qualcomm-linux/pkg-urm

- **packages sources from** [userspace-resource-manager](https://github.com/qualcomm/userspace-resource-manager)
  - Package metadata and source ownership are separate; choose the package branch before editing packaging.
  - [README.md](https://github.com/qualcomm-linux/pkg-urm/blob/f3dd7df55fe9522d5dabd9b00729c54d7076a111/README.md)

### qualcomm-linux/ubuntu-qcom-kernel

- **runs automation from** [upload-private-artifact-action](https://github.com/qualcomm-linux/upload-private-artifact-action)
  - GitHub Actions integration
  - [build-kernel.yml](https://github.com/qualcomm-linux/ubuntu-qcom-kernel/blob/a26c66f4e02e0009a19c49368d5557de21c26747/.github/workflows/build-kernel.yml)

</details>

[Map data and updates](data/README.md).

<!-- Dataset SHA-256: e31bc2e3c37c6daebc112fc3f6c5c0b013d6f10727403fa360cb7b15678ee329. -->
