# Repository map: qualcomm-linux/meta-qcom

**You are here: [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom)**

OpenEmbedded/Yocto Project BSP layer for Qualcomm based platforms

## Outgoing connections

### Builds with

- [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom) → **builds with** → [openembedded/bitbake](https://github.com/openembedded/bitbake)
  - Development kas configuration on master; release locks can select other revisions.
  - [Explore openembedded/bitbake](openembedded--bitbake.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/ci/base.yml)
- [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom) → **builds with** → [openembedded/openembedded-core](https://github.com/openembedded/openembedded-core)
  - Development kas configuration on master; release locks can select other revisions.
  - [Explore openembedded/openembedded-core](openembedded--openembedded-core.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/ci/base.yml)

### Fetches source from

- [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom) → **fetches source from** → [qualcomm-linux/kernel](https://github.com/qualcomm-linux/kernel)
  - linux-qcom-next recipe; kernel provider and source revision are configuration-dependent.
  - [Explore qualcomm-linux/kernel](qualcomm-linux--kernel.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/recipes-kernel/linux/linux-qcom-next_git.bb)
- [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom) → **fetches source from** → [qualcomm-linux/qcom-ptool](https://github.com/qualcomm-linux/qcom-ptool)
  - Partition recipe source; pinned by qcom-ptool.inc.
  - [Explore qualcomm-linux/qcom-ptool](qualcomm-linux--qcom-ptool.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/recipes-bsp/partition/qcom-ptool.inc)

### Selects for distro

- [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom) → **selects for distro** → [AudioReach/meta-audioreach](https://github.com/AudioReach/meta-audioreach)
  - Optional qcom-distro kas composition; not required by every BSP-only build.
  - [Explore AudioReach/meta-audioreach](AudioReach--meta-audioreach.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/ci/qcom-distro.yml)
- [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom) → **selects for distro** → [openembedded/meta-openembedded](https://github.com/openembedded/meta-openembedded)
  - Optional qcom-distro kas composition; not required by every BSP-only build.
  - [Explore openembedded/meta-openembedded](openembedded--meta-openembedded.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/ci/qcom-distro.yml)
- [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom) → **selects for distro** → [qualcomm-linux/meta-ai](https://github.com/qualcomm-linux/meta-ai)
  - Optional qcom-distro kas composition; not required by every BSP-only build.
  - [Explore qualcomm-linux/meta-ai](qualcomm-linux--meta-ai.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/ci/qcom-distro.yml)
- [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom) → **selects for distro** → [qualcomm-linux/meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro)
  - Optional qcom-distro kas composition; not required by every BSP-only build.
  - [Explore qualcomm-linux/meta-qcom-distro](qualcomm-linux--meta-qcom-distro.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/ci/qcom-distro.yml)

### Uses automation from

- [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom) → **uses automation from** → [qualcomm-linux/github-action-matrix-outputs-read](https://github.com/qualcomm-linux/github-action-matrix-outputs-read)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm-linux/github-action-matrix-outputs-read](qualcomm-linux--github-action-matrix-outputs-read.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/.github/workflows/test-distro.yml)
- [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom) → **uses automation from** → [qualcomm-linux/github-action-matrix-outputs-write](https://github.com/qualcomm-linux/github-action-matrix-outputs-write)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm-linux/github-action-matrix-outputs-write](qualcomm-linux--github-action-matrix-outputs-write.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/.github/workflows/test-distro.yml)
- [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom) → **uses automation from** → [qualcomm-linux/upload-private-artifact-action](https://github.com/qualcomm-linux/upload-private-artifact-action)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm-linux/upload-private-artifact-action](qualcomm-linux--upload-private-artifact-action.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/.github/workflows/compile.yml)
- [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom) → **uses automation from** → [qualcomm/qcom-reusable-workflows](https://github.com/qualcomm/qcom-reusable-workflows)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm/qcom-reusable-workflows](qualcomm--qcom-reusable-workflows.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/.github/workflows/pr.yml)

## Incoming connections

### Depends on (repositories using this one)

- [qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) → **depends on** → [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom)
  - wrynose-compatible main snapshot 8927b428bcae; required layer collection.
  - [Explore qualcomm-linux/meta-qcom-3rdparty](qualcomm-linux--meta-qcom-3rdparty.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/conf/layer.conf)

### Pins release of (repositories using this one)

- [qualcomm-linux/meta-qcom-releases](https://github.com/qualcomm-linux/meta-qcom-releases) → **pins release of** → [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom)
  - Milestone tags and kas lock files; select the desired release tag.
  - [Explore qualcomm-linux/meta-qcom-releases](qualcomm-linux--meta-qcom-releases.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom-releases/blob/4129a6850c070bb57da122b2ebceff3de9951a1a/README.md)

### Uses automation from (repositories using this one)

- [qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) → **uses automation from** → [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm-linux/meta-qcom-3rdparty](qualcomm-linux--meta-qcom-3rdparty.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/build-yocto.yml) · [evidence 2](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/build-yocto.yml) · [evidence 3](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/test-distro.yml) · [evidence 4](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/test-distro.yml) · [evidence 5](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/test-distro.yml)
- [qualcomm-linux/meta-qcom-arduino](https://github.com/qualcomm-linux/meta-qcom-arduino) → **uses automation from** → [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm-linux/meta-qcom-arduino](qualcomm-linux--meta-qcom-arduino.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom-arduino/blob/35f3dfdd4dca56d0df60b621ff8fd70a8043bcfd/.github/workflows/build-yocto.yml) · [evidence 2](https://github.com/qualcomm-linux/meta-qcom-arduino/blob/35f3dfdd4dca56d0df60b621ff8fd70a8043bcfd/.github/workflows/build-yocto.yml) · [evidence 3](https://github.com/qualcomm-linux/meta-qcom-arduino/blob/35f3dfdd4dca56d0df60b621ff8fd70a8043bcfd/.github/workflows/test-distro.yml) · [evidence 4](https://github.com/qualcomm-linux/meta-qcom-arduino/blob/35f3dfdd4dca56d0df60b621ff8fd70a8043bcfd/.github/workflows/test-distro.yml) · [evidence 5](https://github.com/qualcomm-linux/meta-qcom-arduino/blob/35f3dfdd4dca56d0df60b621ff8fd70a8043bcfd/.github/workflows/test-distro.yml)
- [qualcomm-linux/meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro) → **uses automation from** → [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm-linux/meta-qcom-distro](qualcomm-linux--meta-qcom-distro.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom-distro/blob/805634470ec74ae15ca04b4f164a608f06b362fa/.github/workflows/build-yocto.yml) · [evidence 2](https://github.com/qualcomm-linux/meta-qcom-distro/blob/805634470ec74ae15ca04b4f164a608f06b362fa/.github/workflows/test-distro.yml) · [evidence 3](https://github.com/qualcomm-linux/meta-qcom-distro/blob/805634470ec74ae15ca04b4f164a608f06b362fa/.github/workflows/test-distro.yml) · [evidence 4](https://github.com/qualcomm-linux/meta-qcom-distro/blob/805634470ec74ae15ca04b4f164a608f06b362fa/.github/workflows/test-distro.yml)

## Full ecosystem map

[Explore the Qualcomm repository map](../README.md).

Connections apply to the linked evidence revisions; use release-compatible revisions for a build.

Dataset SHA-256: `bd976587e3980bd55d7438b70404ec9c904e9867ffff16f5f02793244f602c8a`.
