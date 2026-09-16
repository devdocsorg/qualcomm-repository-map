# Qualcomm repository map

Qualcomm repository ecosystem. Initial inventory covers public qualcomm-linux repositories and verified neighbouring upstreams; it is not limited to a release or engagement. Other Qualcomm organisations can be added using the same schema.

**Coverage:** 130 repositories, 110 with reviewed connections, 189 evidenced relationships.

Repository inventory is broader than reviewed relationships. An absent edge means no relationship has been recorded, not proof of independence.

Repository names open the repository. **Explore** links move through its neighbourhood. Open `index.html` for local browsing without a server; external repository and evidence links need network access.

## Connected repositories

### [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom)

- **Builds with:** [bitbake](https://github.com/openembedded/bitbake) · [openembedded-core](https://github.com/openembedded/openembedded-core)
- **Fetches source from:** [kernel](https://github.com/qualcomm-linux/kernel) · [qcom-ptool](https://github.com/qualcomm-linux/qcom-ptool)
- **Selects for distro:** [meta-audioreach](https://github.com/AudioReach/meta-audioreach) · [meta-openembedded](https://github.com/openembedded/meta-openembedded) · [meta-ai](https://github.com/qualcomm-linux/meta-ai) · [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro)

[Explore connections](maps/qualcomm-linux--meta-qcom.md).

### [qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty)

- **Depends on:** [openembedded-core](https://github.com/openembedded/openembedded-core) · [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)
- **Fetches source from:** [boot-assets](https://github.com/rubikpi-ai/boot-assets)
- **Integrates with:** [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro)
- **Uses indirectly:** [qcom-ptool](https://github.com/qualcomm-linux/qcom-ptool)

[Explore connections](maps/qualcomm-linux--meta-qcom-3rdparty.md).

### [qualcomm-linux/kernel-config](https://github.com/qualcomm-linux/kernel-config)

- **Configures:** [automerge](https://github.com/qualcomm-linux/automerge)
- **Selects branches from:** [kernel](https://github.com/qualcomm-linux/kernel) · [kernel-topics](https://github.com/qualcomm-linux/kernel-topics)

[Explore connections](maps/qualcomm-linux--kernel-config.md).

### [qualcomm-linux/pkg-kgsl](https://github.com/qualcomm-linux/pkg-kgsl)

- **Packages:** [kgsl](https://github.com/qualcomm-linux/kgsl)

[Explore connections](maps/qualcomm-linux--pkg-kgsl.md).

## All repositories

Groups organise browsing; they do not assert dependencies.

### Boot and firmware

- [qualcomm-linux/boot-firmware-ci](https://github.com/qualcomm-linux/boot-firmware-ci) · [Explore](maps/qualcomm-linux--boot-firmware-ci.md) · connections not yet reviewed
- [qualcomm-linux/edk2](https://github.com/qualcomm-linux/edk2) · [Explore](maps/qualcomm-linux--edk2.md) · connections not yet reviewed
- [qualcomm-linux/edk2-platforms](https://github.com/qualcomm-linux/edk2-platforms) · [Explore](maps/qualcomm-linux--edk2-platforms.md) · connections not yet reviewed
- [qualcomm-linux/optee_os](https://github.com/qualcomm-linux/optee_os) · [Explore](maps/qualcomm-linux--optee_os.md) · connections not yet reviewed
- [qualcomm-linux/qcom-ptool](https://github.com/qualcomm-linux/qcom-ptool) · [Explore](maps/qualcomm-linux--qcom-ptool.md)
- [qualcomm-linux/qcom-sec-tools-wrapper](https://github.com/qualcomm-linux/qcom-sec-tools-wrapper) · [Explore](maps/qualcomm-linux--qcom-sec-tools-wrapper.md)
- [qualcomm-linux/snagboot](https://github.com/qualcomm-linux/snagboot) · [Explore](maps/qualcomm-linux--snagboot.md) · connections not yet reviewed
- [qualcomm-linux/trusted-firmware-a](https://github.com/qualcomm-linux/trusted-firmware-a) · [Explore](maps/qualcomm-linux--trusted-firmware-a.md) · connections not yet reviewed
- [qualcomm-linux/u-boot](https://github.com/qualcomm-linux/u-boot) · [Explore](maps/qualcomm-linux--u-boot.md) · connections not yet reviewed
- [rubikpi-ai/boot-assets](https://github.com/rubikpi-ai/boot-assets) · [Explore](maps/rubikpi-ai--boot-assets.md)

### Images and build tooling

- [openembedded/bitbake](https://github.com/openembedded/bitbake) · [Explore](maps/openembedded--bitbake.md)
- [qualcomm-linux/docker-pkg-build](https://github.com/qualcomm-linux/docker-pkg-build) · [Explore](maps/qualcomm-linux--docker-pkg-build.md) · connections not yet reviewed
- [qualcomm-linux/qcom-build-utils](https://github.com/qualcomm-linux/qcom-build-utils) · [Explore](maps/qualcomm-linux--qcom-build-utils.md)
- [qualcomm-linux/qcom-deb-images](https://github.com/qualcomm-linux/qcom-deb-images) · [Explore](maps/qualcomm-linux--qcom-deb-images.md)
- [qualcomm-linux/qcom-rpm-utils](https://github.com/qualcomm-linux/qcom-rpm-utils) · [Explore](maps/qualcomm-linux--qcom-rpm-utils.md)
- [qualcomm-linux/qli-ci](https://github.com/qualcomm-linux/qli-ci) · [Explore](maps/qualcomm-linux--qli-ci.md)
- [qualcomm-linux/rpm-images](https://github.com/qualcomm-linux/rpm-images) · [Explore](maps/qualcomm-linux--rpm-images.md)
- [qualcomm/commit-emails-check-action](https://github.com/qualcomm/commit-emails-check-action) · [Explore](maps/qualcomm--commit-emails-check-action.md)
- [qualcomm/qcom-reusable-workflows](https://github.com/qualcomm/qcom-reusable-workflows) · [Explore](maps/qualcomm--qcom-reusable-workflows.md)

### Kernel integration

- [qualcomm-linux/automerge](https://github.com/qualcomm-linux/automerge) · [Explore](maps/qualcomm-linux--automerge.md)
- [qualcomm-linux/kernel](https://github.com/qualcomm-linux/kernel) · [Explore](maps/qualcomm-linux--kernel.md)
- [qualcomm-linux/kernel-checkers](https://github.com/qualcomm-linux/kernel-checkers) · [Explore](maps/qualcomm-linux--kernel-checkers.md)
- [qualcomm-linux/kernel-config](https://github.com/qualcomm-linux/kernel-config) · [Explore](maps/qualcomm-linux--kernel-config.md)
- [qualcomm-linux/kernel-topics](https://github.com/qualcomm-linux/kernel-topics) · [Explore](maps/qualcomm-linux--kernel-topics.md)
- [qualcomm-linux/kmake-image](https://github.com/qualcomm-linux/kmake-image) · [Explore](maps/qualcomm-linux--kmake-image.md) · connections not yet reviewed
- [qualcomm-linux/ubuntu-qcom-kernel](https://github.com/qualcomm-linux/ubuntu-qcom-kernel) · [Explore](maps/qualcomm-linux--ubuntu-qcom-kernel.md)

### Layers and releases

- [AudioReach/meta-audioreach](https://github.com/AudioReach/meta-audioreach) · [Explore](maps/AudioReach--meta-audioreach.md)
- [openembedded/meta-openembedded](https://github.com/openembedded/meta-openembedded) · [Explore](maps/openembedded--meta-openembedded.md)
- [openembedded/openembedded-core](https://github.com/openembedded/openembedded-core) · [Explore](maps/openembedded--openembedded-core.md)
- [qualcomm-linux/meta-ai](https://github.com/qualcomm-linux/meta-ai) · [Explore](maps/qualcomm-linux--meta-ai.md)
- [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom) · [Explore](maps/qualcomm-linux--meta-qcom.md)
- [qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) · [Explore](maps/qualcomm-linux--meta-qcom-3rdparty.md)
- [qualcomm-linux/meta-qcom-arduino](https://github.com/qualcomm-linux/meta-qcom-arduino) · [Explore](maps/qualcomm-linux--meta-qcom-arduino.md)
- [qualcomm-linux/meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro) · [Explore](maps/qualcomm-linux--meta-qcom-distro.md)
- [qualcomm-linux/meta-qcom-extras-releases](https://github.com/qualcomm-linux/meta-qcom-extras-releases) · [Explore](maps/qualcomm-linux--meta-qcom-extras-releases.md)
- [qualcomm-linux/meta-qcom-hwe](https://github.com/qualcomm-linux/meta-qcom-hwe) · [Explore](maps/qualcomm-linux--meta-qcom-hwe.md) · connections not yet reviewed
- [qualcomm-linux/meta-qcom-qim-product-sdk](https://github.com/qualcomm-linux/meta-qcom-qim-product-sdk) · [Explore](maps/qualcomm-linux--meta-qcom-qim-product-sdk.md) · connections not yet reviewed
- [qualcomm-linux/meta-qcom-realtime](https://github.com/qualcomm-linux/meta-qcom-realtime) · [Explore](maps/qualcomm-linux--meta-qcom-realtime.md) · connections not yet reviewed
- [qualcomm-linux/meta-qcom-releases](https://github.com/qualcomm-linux/meta-qcom-releases) · [Explore](maps/qualcomm-linux--meta-qcom-releases.md)
- [qualcomm-linux/meta-qcom-robotics](https://github.com/qualcomm-linux/meta-qcom-robotics) · [Explore](maps/qualcomm-linux--meta-qcom-robotics.md) · connections not yet reviewed
- [qualcomm-linux/meta-qcom-robotics-distro](https://github.com/qualcomm-linux/meta-qcom-robotics-distro) · [Explore](maps/qualcomm-linux--meta-qcom-robotics-distro.md) · connections not yet reviewed
- [qualcomm-linux/meta-qcom-robotics-releases](https://github.com/qualcomm-linux/meta-qcom-robotics-releases) · [Explore](maps/qualcomm-linux--meta-qcom-robotics-releases.md)
- [qualcomm-linux/meta-qcom-robotics-sdk](https://github.com/qualcomm-linux/meta-qcom-robotics-sdk) · [Explore](maps/qualcomm-linux--meta-qcom-robotics-sdk.md)
- [qualcomm-linux/qcom-manifest](https://github.com/qualcomm-linux/qcom-manifest) · [Explore](maps/qualcomm-linux--qcom-manifest.md) · connections not yet reviewed

### Other repositories

- [qualcomm-linux/.github](https://github.com/qualcomm-linux/.github) · [Explore](maps/qualcomm-linux--.github.md) · connections not yet reviewed
- [qualcomm-linux/Robotics-SDK-Ubuntu](https://github.com/qualcomm-linux/Robotics-SDK-Ubuntu) · [Explore](maps/qualcomm-linux--Robotics-SDK-Ubuntu.md)
- [qualcomm-linux/TC9564_Host_Driver](https://github.com/qualcomm-linux/TC9564_Host_Driver) · [Explore](maps/qualcomm-linux--TC9564_Host_Driver.md) · connections not yet reviewed
- [qualcomm-linux/abctl](https://github.com/qualcomm-linux/abctl) · [Explore](maps/qualcomm-linux--abctl.md)
- [qualcomm-linux/apt-artifactory-action](https://github.com/qualcomm-linux/apt-artifactory-action) · [Explore](maps/qualcomm-linux--apt-artifactory-action.md)
- [qualcomm-linux/bitbake-lint-action](https://github.com/qualcomm-linux/bitbake-lint-action) · [Explore](maps/qualcomm-linux--bitbake-lint-action.md)
- [qualcomm-linux/camera-driver](https://github.com/qualcomm-linux/camera-driver) · [Explore](maps/qualcomm-linux--camera-driver.md)
- [qualcomm-linux/clk-debug-tools-for-qualcomm-linux](https://github.com/qualcomm-linux/clk-debug-tools-for-qualcomm-linux) · [Explore](maps/qualcomm-linux--clk-debug-tools-for-qualcomm-linux.md)
- [qualcomm-linux/debusine-action](https://github.com/qualcomm-linux/debusine-action) · [Explore](maps/qualcomm-linux--debusine-action.md)
- [qualcomm-linux/display-driver](https://github.com/qualcomm-linux/display-driver) · [Explore](maps/qualcomm-linux--display-driver.md)
- [qualcomm-linux/eva-driver](https://github.com/qualcomm-linux/eva-driver) · [Explore](maps/qualcomm-linux--eva-driver.md)
- [qualcomm-linux/gbm-msm-backend](https://github.com/qualcomm-linux/gbm-msm-backend) · [Explore](maps/qualcomm-linux--gbm-msm-backend.md)
- [qualcomm-linux/github-action-matrix-outputs-read](https://github.com/qualcomm-linux/github-action-matrix-outputs-read) · [Explore](maps/qualcomm-linux--github-action-matrix-outputs-read.md)
- [qualcomm-linux/github-action-matrix-outputs-write](https://github.com/qualcomm-linux/github-action-matrix-outputs-write) · [Explore](maps/qualcomm-linux--github-action-matrix-outputs-write.md)
- [qualcomm-linux/kgsl](https://github.com/qualcomm-linux/kgsl) · [Explore](maps/qualcomm-linux--kgsl.md)
- [qualcomm-linux/location-apis-qcom](https://github.com/qualcomm-linux/location-apis-qcom) · [Explore](maps/qualcomm-linux--location-apis-qcom.md)
- [qualcomm-linux/location-hal-qcom](https://github.com/qualcomm-linux/location-hal-qcom) · [Explore](maps/qualcomm-linux--location-hal-qcom.md)
- [qualcomm-linux/qcom-dtb-metadata](https://github.com/qualcomm-linux/qcom-dtb-metadata) · [Explore](maps/qualcomm-linux--qcom-dtb-metadata.md)
- [qualcomm-linux/qcom-linux-skills](https://github.com/qualcomm-linux/qcom-linux-skills) · [Explore](maps/qualcomm-linux--qcom-linux-skills.md)
- [qualcomm-linux/qualcomm-CDI-generator](https://github.com/qualcomm-linux/qualcomm-CDI-generator) · [Explore](maps/qualcomm-linux--qualcomm-CDI-generator.md)
- [qualcomm-linux/rtss-mailbox-kmd](https://github.com/qualcomm-linux/rtss-mailbox-kmd) · [Explore](maps/qualcomm-linux--rtss-mailbox-kmd.md)
- [qualcomm-linux/rtss-mailbox-umd](https://github.com/qualcomm-linux/rtss-mailbox-umd) · [Explore](maps/qualcomm-linux--rtss-mailbox-umd.md)
- [qualcomm-linux/upload-private-artifact-action](https://github.com/qualcomm-linux/upload-private-artifact-action) · [Explore](maps/qualcomm-linux--upload-private-artifact-action.md)
- [qualcomm-linux/video-driver](https://github.com/qualcomm-linux/video-driver) · [Explore](maps/qualcomm-linux--video-driver.md)
- [qualcomm-linux/weston-sdm-backend](https://github.com/qualcomm-linux/weston-sdm-backend) · [Explore](maps/qualcomm-linux--weston-sdm-backend.md)
- [qualcomm/userspace-resource-manager](https://github.com/qualcomm/userspace-resource-manager) · [Explore](maps/qualcomm--userspace-resource-manager.md)

### Packaging

- [qualcomm-linux/pkg-adreno](https://github.com/qualcomm-linux/pkg-adreno) · [Explore](maps/qualcomm-linux--pkg-adreno.md)
- [qualcomm-linux/pkg-alsa-ucm-conf](https://github.com/qualcomm-linux/pkg-alsa-ucm-conf) · [Explore](maps/qualcomm-linux--pkg-alsa-ucm-conf.md)
- [qualcomm-linux/pkg-android-platform-tools](https://github.com/qualcomm-linux/pkg-android-platform-tools) · [Explore](maps/qualcomm-linux--pkg-android-platform-tools.md)
- [qualcomm-linux/pkg-audioreach-audio-utils](https://github.com/qualcomm-linux/pkg-audioreach-audio-utils) · [Explore](maps/qualcomm-linux--pkg-audioreach-audio-utils.md)
- [qualcomm-linux/pkg-audioreach-conf](https://github.com/qualcomm-linux/pkg-audioreach-conf) · [Explore](maps/qualcomm-linux--pkg-audioreach-conf.md)
- [qualcomm-linux/pkg-audioreach-dkms](https://github.com/qualcomm-linux/pkg-audioreach-dkms) · [Explore](maps/qualcomm-linux--pkg-audioreach-dkms.md)
- [qualcomm-linux/pkg-audioreach-graphmgr](https://github.com/qualcomm-linux/pkg-audioreach-graphmgr) · [Explore](maps/qualcomm-linux--pkg-audioreach-graphmgr.md)
- [qualcomm-linux/pkg-audioreach-graphservices](https://github.com/qualcomm-linux/pkg-audioreach-graphservices) · [Explore](maps/qualcomm-linux--pkg-audioreach-graphservices.md)
- [qualcomm-linux/pkg-audioreach-pal](https://github.com/qualcomm-linux/pkg-audioreach-pal) · [Explore](maps/qualcomm-linux--pkg-audioreach-pal.md)
- [qualcomm-linux/pkg-audioreach-pipewire-plugin](https://github.com/qualcomm-linux/pkg-audioreach-pipewire-plugin) · [Explore](maps/qualcomm-linux--pkg-audioreach-pipewire-plugin.md)
- [qualcomm-linux/pkg-btftm](https://github.com/qualcomm-linux/pkg-btftm) · [Explore](maps/qualcomm-linux--pkg-btftm.md)
- [qualcomm-linux/pkg-camx-dev](https://github.com/qualcomm-linux/pkg-camx-dev) · [Explore](maps/qualcomm-linux--pkg-camx-dev.md)
- [qualcomm-linux/pkg-camx-dkms](https://github.com/qualcomm-linux/pkg-camx-dkms) · [Explore](maps/qualcomm-linux--pkg-camx-dkms.md)
- [qualcomm-linux/pkg-camx-firmware-glymur](https://github.com/qualcomm-linux/pkg-camx-firmware-glymur) · [Explore](maps/qualcomm-linux--pkg-camx-firmware-glymur.md)
- [qualcomm-linux/pkg-camx-firmware-hamoa](https://github.com/qualcomm-linux/pkg-camx-firmware-hamoa) · [Explore](maps/qualcomm-linux--pkg-camx-firmware-hamoa.md)
- [qualcomm-linux/pkg-camx-firmware-kodiak](https://github.com/qualcomm-linux/pkg-camx-firmware-kodiak) · [Explore](maps/qualcomm-linux--pkg-camx-firmware-kodiak.md)
- [qualcomm-linux/pkg-camx-firmware-lemans](https://github.com/qualcomm-linux/pkg-camx-firmware-lemans) · [Explore](maps/qualcomm-linux--pkg-camx-firmware-lemans.md)
- [qualcomm-linux/pkg-camx-firmware-talos](https://github.com/qualcomm-linux/pkg-camx-firmware-talos) · [Explore](maps/qualcomm-linux--pkg-camx-firmware-talos.md)
- [qualcomm-linux/pkg-camx-glymur](https://github.com/qualcomm-linux/pkg-camx-glymur) · [Explore](maps/qualcomm-linux--pkg-camx-glymur.md)
- [qualcomm-linux/pkg-camx-hamoa](https://github.com/qualcomm-linux/pkg-camx-hamoa) · [Explore](maps/qualcomm-linux--pkg-camx-hamoa.md)
- [qualcomm-linux/pkg-camx-kodiak](https://github.com/qualcomm-linux/pkg-camx-kodiak) · [Explore](maps/qualcomm-linux--pkg-camx-kodiak.md)
- [qualcomm-linux/pkg-camx-lemans](https://github.com/qualcomm-linux/pkg-camx-lemans) · [Explore](maps/qualcomm-linux--pkg-camx-lemans.md)
- [qualcomm-linux/pkg-camx-nhx](https://github.com/qualcomm-linux/pkg-camx-nhx) · [Explore](maps/qualcomm-linux--pkg-camx-nhx.md)
- [qualcomm-linux/pkg-camx-talos](https://github.com/qualcomm-linux/pkg-camx-talos) · [Explore](maps/qualcomm-linux--pkg-camx-talos.md)
- [qualcomm-linux/pkg-diag-router](https://github.com/qualcomm-linux/pkg-diag-router) · [Explore](maps/qualcomm-linux--pkg-diag-router.md)
- [qualcomm-linux/pkg-eva-dkms](https://github.com/qualcomm-linux/pkg-eva-dkms) · [Explore](maps/qualcomm-linux--pkg-eva-dkms.md)
- [qualcomm-linux/pkg-fastrpc](https://github.com/qualcomm-linux/pkg-fastrpc) · [Explore](maps/qualcomm-linux--pkg-fastrpc.md)
- [qualcomm-linux/pkg-gbm-msm-backend](https://github.com/qualcomm-linux/pkg-gbm-msm-backend) · [Explore](maps/qualcomm-linux--pkg-gbm-msm-backend.md)
- [qualcomm-linux/pkg-gst-plugins-imsdk](https://github.com/qualcomm-linux/pkg-gst-plugins-imsdk) · [Explore](maps/qualcomm-linux--pkg-gst-plugins-imsdk.md)
- [qualcomm-linux/pkg-kgsl](https://github.com/qualcomm-linux/pkg-kgsl) · [Explore](maps/qualcomm-linux--pkg-kgsl.md)
- [qualcomm-linux/pkg-libdiag](https://github.com/qualcomm-linux/pkg-libdiag) · [Explore](maps/qualcomm-linux--pkg-libdiag.md)
- [qualcomm-linux/pkg-linux-qcom](https://github.com/qualcomm-linux/pkg-linux-qcom) · [Explore](maps/qualcomm-linux--pkg-linux-qcom.md)
- [qualcomm-linux/pkg-mink-idl-compiler](https://github.com/qualcomm-linux/pkg-mink-idl-compiler) · [Explore](maps/qualcomm-linux--pkg-mink-idl-compiler.md)
- [qualcomm-linux/pkg-minkipc](https://github.com/qualcomm-linux/pkg-minkipc) · [Explore](maps/qualcomm-linux--pkg-minkipc.md)
- [qualcomm-linux/pkg-optee-client](https://github.com/qualcomm-linux/pkg-optee-client) · [Explore](maps/qualcomm-linux--pkg-optee-client.md)
- [qualcomm-linux/pkg-optee-test](https://github.com/qualcomm-linux/pkg-optee-test) · [Explore](maps/qualcomm-linux--pkg-optee-test.md)
- [qualcomm-linux/pkg-qcom-fastcv-binaries](https://github.com/qualcomm-linux/pkg-qcom-fastcv-binaries) · [Explore](maps/qualcomm-linux--pkg-qcom-fastcv-binaries.md)
- [qualcomm-linux/pkg-qcom-sensors](https://github.com/qualcomm-linux/pkg-qcom-sensors) · [Explore](maps/qualcomm-linux--pkg-qcom-sensors.md)
- [qualcomm-linux/pkg-qcom-sv-binaries](https://github.com/qualcomm-linux/pkg-qcom-sv-binaries) · [Explore](maps/qualcomm-linux--pkg-qcom-sv-binaries.md)
- [qualcomm-linux/pkg-qimsdk-smartvenc](https://github.com/qualcomm-linux/pkg-qimsdk-smartvenc) · [Explore](maps/qualcomm-linux--pkg-qimsdk-smartvenc.md)
- [qualcomm-linux/pkg-qmi-framework](https://github.com/qualcomm-linux/pkg-qmi-framework) · [Explore](maps/qualcomm-linux--pkg-qmi-framework.md)
- [qualcomm-linux/pkg-qti-camera-service](https://github.com/qualcomm-linux/pkg-qti-camera-service) · [Explore](maps/qualcomm-linux--pkg-qti-camera-service.md)
- [qualcomm-linux/pkg-quic-teec](https://github.com/qualcomm-linux/pkg-quic-teec) · [Explore](maps/qualcomm-linux--pkg-quic-teec.md)
- [qualcomm-linux/pkg-ros-jazzy-xsens-mti-ros2-driver](https://github.com/qualcomm-linux/pkg-ros-jazzy-xsens-mti-ros2-driver) · [Explore](maps/qualcomm-linux--pkg-ros-jazzy-xsens-mti-ros2-driver.md)
- [qualcomm-linux/pkg-rpm-qcom-fastcv-binaries](https://github.com/qualcomm-linux/pkg-rpm-qcom-fastcv-binaries) · [Explore](maps/qualcomm-linux--pkg-rpm-qcom-fastcv-binaries.md)
- [qualcomm-linux/pkg-rpm-video-driver](https://github.com/qualcomm-linux/pkg-rpm-video-driver) · [Explore](maps/qualcomm-linux--pkg-rpm-video-driver.md)
- [qualcomm-linux/pkg-sensinghub](https://github.com/qualcomm-linux/pkg-sensinghub) · [Explore](maps/qualcomm-linux--pkg-sensinghub.md)
- [qualcomm-linux/pkg-thermald](https://github.com/qualcomm-linux/pkg-thermald) · [Explore](maps/qualcomm-linux--pkg-thermald.md)
- [qualcomm-linux/pkg-time-services](https://github.com/qualcomm-linux/pkg-time-services) · [Explore](maps/qualcomm-linux--pkg-time-services.md)
- [qualcomm-linux/pkg-tinyalsa](https://github.com/qualcomm-linux/pkg-tinyalsa) · [Explore](maps/qualcomm-linux--pkg-tinyalsa.md)
- [qualcomm-linux/pkg-tinycompress](https://github.com/qualcomm-linux/pkg-tinycompress) · [Explore](maps/qualcomm-linux--pkg-tinycompress.md)
- [qualcomm-linux/pkg-urm](https://github.com/qualcomm-linux/pkg-urm) · [Explore](maps/qualcomm-linux--pkg-urm.md)
- [qualcomm-linux/pkg-urm-ext](https://github.com/qualcomm-linux/pkg-urm-ext) · [Explore](maps/qualcomm-linux--pkg-urm-ext.md)
- [qualcomm-linux/pkg-video-driver](https://github.com/qualcomm-linux/pkg-video-driver) · [Explore](maps/qualcomm-linux--pkg-video-driver.md)

### Validation

- [qualcomm-linux/aiml-container-test](https://github.com/qualcomm-linux/aiml-container-test) · [Explore](maps/qualcomm-linux--aiml-container-test.md)
- [qualcomm-linux/awstest-meta-qcom](https://github.com/qualcomm-linux/awstest-meta-qcom) · [Explore](maps/qualcomm-linux--awstest-meta-qcom.md)
- [qualcomm-linux/job_render](https://github.com/qualcomm-linux/job_render) · [Explore](maps/qualcomm-linux--job_render.md) · connections not yet reviewed
- [qualcomm-linux/lava-test-plans](https://github.com/qualcomm-linux/lava-test-plans) · [Explore](maps/qualcomm-linux--lava-test-plans.md) · connections not yet reviewed
- [qualcomm-linux/mark-test](https://github.com/qualcomm-linux/mark-test) · [Explore](maps/qualcomm-linux--mark-test.md) · connections not yet reviewed
- [qualcomm-linux/qcom-linux-testkit](https://github.com/qualcomm-linux/qcom-linux-testkit) · [Explore](maps/qualcomm-linux--qcom-linux-testkit.md)

[Map data and updates](data/README.md) · [Licence](LICENSE)
