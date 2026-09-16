# [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)

OpenEmbedded/Yocto Project BSP layer for Qualcomm based platforms

## Uses

### Builds with

- [bitbake](https://github.com/openembedded/bitbake) · [Explore](openembedded--bitbake.md)
- [openembedded-core](https://github.com/openembedded/openembedded-core) · [Explore](openembedded--openembedded-core.md)

### Fetches source from

- [kernel](https://github.com/qualcomm-linux/kernel) · [Explore](qualcomm-linux--kernel.md)
- [qcom-ptool](https://github.com/qualcomm-linux/qcom-ptool) · [Explore](qualcomm-linux--qcom-ptool.md)

### Selects for distro

- [meta-audioreach](https://github.com/AudioReach/meta-audioreach) · [Explore](AudioReach--meta-audioreach.md)
- [meta-openembedded](https://github.com/openembedded/meta-openembedded) · [Explore](openembedded--meta-openembedded.md)
- [meta-ai](https://github.com/qualcomm-linux/meta-ai) · [Explore](qualcomm-linux--meta-ai.md)
- [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro) · [Explore](qualcomm-linux--meta-qcom-distro.md)

### Uses automation from

- [github-action-matrix-outputs-read](https://github.com/qualcomm-linux/github-action-matrix-outputs-read) · [Explore](qualcomm-linux--github-action-matrix-outputs-read.md)
- [github-action-matrix-outputs-write](https://github.com/qualcomm-linux/github-action-matrix-outputs-write) · [Explore](qualcomm-linux--github-action-matrix-outputs-write.md)
- [upload-private-artifact-action](https://github.com/qualcomm-linux/upload-private-artifact-action) · [Explore](qualcomm-linux--upload-private-artifact-action.md)
- [qcom-reusable-workflows](https://github.com/qualcomm/qcom-reusable-workflows) · [Explore](qualcomm--qcom-reusable-workflows.md)

## Used by

### Depends on

- [meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) · [Explore](qualcomm-linux--meta-qcom-3rdparty.md)

### Pins release of

- [meta-qcom-releases](https://github.com/qualcomm-linux/meta-qcom-releases) · [Explore](qualcomm-linux--meta-qcom-releases.md)

### Uses automation from

- [meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) · [Explore](qualcomm-linux--meta-qcom-3rdparty.md)
- [meta-qcom-arduino](https://github.com/qualcomm-linux/meta-qcom-arduino) · [Explore](qualcomm-linux--meta-qcom-arduino.md)
- [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro) · [Explore](qualcomm-linux--meta-qcom-distro.md)

<details>
<summary>Applicability and sources</summary>

- Uses: [bitbake](https://github.com/openembedded/bitbake) — **builds with**
  - Development kas configuration on master; release locks can select other revisions.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/ci/base.yml)
- Uses: [openembedded-core](https://github.com/openembedded/openembedded-core) — **builds with**
  - Development kas configuration on master; release locks can select other revisions.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/ci/base.yml)
- Uses: [kernel](https://github.com/qualcomm-linux/kernel) — **fetches source from**
  - linux-qcom-next recipe; kernel provider and source revision are configuration-dependent.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/recipes-kernel/linux/linux-qcom-next_git.bb)
- Uses: [qcom-ptool](https://github.com/qualcomm-linux/qcom-ptool) — **fetches source from**
  - Partition recipe source; pinned by qcom-ptool.inc.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/recipes-bsp/partition/qcom-ptool.inc)
- Uses: [meta-audioreach](https://github.com/AudioReach/meta-audioreach) — **selects for distro**
  - Optional qcom-distro kas composition; not required by every BSP-only build.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/ci/qcom-distro.yml)
- Uses: [meta-openembedded](https://github.com/openembedded/meta-openembedded) — **selects for distro**
  - Optional qcom-distro kas composition; not required by every BSP-only build.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/ci/qcom-distro.yml)
- Uses: [meta-ai](https://github.com/qualcomm-linux/meta-ai) — **selects for distro**
  - Optional qcom-distro kas composition; not required by every BSP-only build.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/ci/qcom-distro.yml)
- Uses: [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro) — **selects for distro**
  - Optional qcom-distro kas composition; not required by every BSP-only build.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/ci/qcom-distro.yml)
- Uses: [github-action-matrix-outputs-read](https://github.com/qualcomm-linux/github-action-matrix-outputs-read) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/.github/workflows/test-distro.yml)
- Uses: [github-action-matrix-outputs-write](https://github.com/qualcomm-linux/github-action-matrix-outputs-write) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/.github/workflows/test-distro.yml)
- Uses: [upload-private-artifact-action](https://github.com/qualcomm-linux/upload-private-artifact-action) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/.github/workflows/compile.yml)
- Uses: [qcom-reusable-workflows](https://github.com/qualcomm/qcom-reusable-workflows) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/.github/workflows/pr.yml)
- Used by: [meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) — **depends on**
  - wrynose-compatible main snapshot 8927b428bcae; required layer collection.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/conf/layer.conf)
- Used by: [meta-qcom-releases](https://github.com/qualcomm-linux/meta-qcom-releases) — **pins release of**
  - Milestone tags and kas lock files; select the desired release tag.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom-releases/blob/4129a6850c070bb57da122b2ebceff3de9951a1a/README.md)
- Used by: [meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/build-yocto.yml) · [source 2](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/test-distro.yml)
- Used by: [meta-qcom-arduino](https://github.com/qualcomm-linux/meta-qcom-arduino) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom-arduino/blob/35f3dfdd4dca56d0df60b621ff8fd70a8043bcfd/.github/workflows/build-yocto.yml) · [source 2](https://github.com/qualcomm-linux/meta-qcom-arduino/blob/35f3dfdd4dca56d0df60b621ff8fd70a8043bcfd/.github/workflows/test-distro.yml)
- Used by: [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom-distro/blob/805634470ec74ae15ca04b4f164a608f06b362fa/.github/workflows/build-yocto.yml) · [source 2](https://github.com/qualcomm-linux/meta-qcom-distro/blob/805634470ec74ae15ca04b4f164a608f06b362fa/.github/workflows/test-distro.yml)

</details>

[Back to the ecosystem map](../README.md).

<!-- Dataset SHA-256: bd976587e3980bd55d7438b70404ec9c904e9867ffff16f5f02793244f602c8a; revision: this checkout. -->
