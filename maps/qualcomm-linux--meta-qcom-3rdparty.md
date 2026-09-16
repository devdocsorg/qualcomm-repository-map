# [meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty)

OpenEmbedded/Yocto Project BSP layer for Third-Party Maintained Qualcomm based platforms

## Uses

### Depends on

- [openembedded-core](https://github.com/openembedded/openembedded-core) · [Explore](openembedded--openembedded-core.md)
- [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) · [Explore](qualcomm-linux--meta-qcom.md)

### Fetches source from

- [boot-assets](https://github.com/rubikpi-ai/boot-assets) · [Explore](rubikpi-ai--boot-assets.md)

### Integrates with

- [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro) · [Explore](qualcomm-linux--meta-qcom-distro.md)

### Uses automation from

- [bitbake-lint-action](https://github.com/qualcomm-linux/bitbake-lint-action) · [Explore](qualcomm-linux--bitbake-lint-action.md)
- [github-action-matrix-outputs-read](https://github.com/qualcomm-linux/github-action-matrix-outputs-read) · [Explore](qualcomm-linux--github-action-matrix-outputs-read.md)
- [github-action-matrix-outputs-write](https://github.com/qualcomm-linux/github-action-matrix-outputs-write) · [Explore](qualcomm-linux--github-action-matrix-outputs-write.md)
- [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) · [Explore](qualcomm-linux--meta-qcom.md)
- [qcom-reusable-workflows](https://github.com/qualcomm/qcom-reusable-workflows) · [Explore](qualcomm--qcom-reusable-workflows.md)

### Uses indirectly

- [qcom-ptool](https://github.com/qualcomm-linux/qcom-ptool) · [Explore](qualcomm-linux--qcom-ptool.md)

<details>
<summary>Applicability and sources</summary>

- Uses: [openembedded-core](https://github.com/openembedded/openembedded-core) — **depends on**
  - wrynose-compatible main snapshot 8927b428bcae; required layer collection.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/conf/layer.conf)
- Uses: [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) — **depends on**
  - wrynose-compatible main snapshot 8927b428bcae; required layer collection.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/conf/layer.conf)
- Uses: [boot-assets](https://github.com/rubikpi-ai/boot-assets) — **fetches source from**
  - RUBIK Pi 3 boot firmware only; pinned by the recipe SRCREV.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/recipes-bsp/firmware-boot/firmware-qcom-boot-rubikpi3_20260621.bb)
- Uses: [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro) — **integrates with**
  - Optional: the dynamic layer applies only when qcom-distro is present.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/conf/layer.conf)
- Uses: [bitbake-lint-action](https://github.com/qualcomm-linux/bitbake-lint-action) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/bitbake-lint.yml)
- Uses: [github-action-matrix-outputs-read](https://github.com/qualcomm-linux/github-action-matrix-outputs-read) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/test-distro.yml)
- Uses: [github-action-matrix-outputs-write](https://github.com/qualcomm-linux/github-action-matrix-outputs-write) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/test-distro.yml)
- Uses: [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/build-yocto.yml) · [source 2](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/test-distro.yml)
- Uses: [qcom-reusable-workflows](https://github.com/qualcomm/qcom-reusable-workflows) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/qcom-preflight-checks.yml)
- Uses: [qcom-ptool](https://github.com/qualcomm-linux/qcom-ptool) — **uses indirectly**
  - Partition tooling is supplied through meta-qcom; this is an indirect relationship, not an extra layer dependency.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/recipes-bsp/partition/qcom-ptool.inc) · [source 2](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/conf/machine/rubikpi3.conf)

</details>

[Back to the ecosystem map](../README.md).

<!-- Dataset SHA-256: bd976587e3980bd55d7438b70404ec9c904e9867ffff16f5f02793244f602c8a; revision: this checkout. -->
