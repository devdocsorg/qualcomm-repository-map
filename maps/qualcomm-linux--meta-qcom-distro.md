# [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro)

OpenEmbedded/Yocto Project Reference Distribution layer for Qualcomm based platforms

## Uses

### Uses automation from

- [github-action-matrix-outputs-read](https://github.com/qualcomm-linux/github-action-matrix-outputs-read) · [Explore](qualcomm-linux--github-action-matrix-outputs-read.md)
- [github-action-matrix-outputs-write](https://github.com/qualcomm-linux/github-action-matrix-outputs-write) · [Explore](qualcomm-linux--github-action-matrix-outputs-write.md)
- [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) · [Explore](qualcomm-linux--meta-qcom.md)
- [upload-private-artifact-action](https://github.com/qualcomm-linux/upload-private-artifact-action) · [Explore](qualcomm-linux--upload-private-artifact-action.md)
- [qcom-reusable-workflows](https://github.com/qualcomm/qcom-reusable-workflows) · [Explore](qualcomm--qcom-reusable-workflows.md)

## Used by

### Integrates with

- [meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) · [Explore](qualcomm-linux--meta-qcom-3rdparty.md)

### Selects for distro

- [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) · [Explore](qualcomm-linux--meta-qcom.md)

<details>
<summary>Applicability and sources</summary>

- Uses: [github-action-matrix-outputs-read](https://github.com/qualcomm-linux/github-action-matrix-outputs-read) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom-distro/blob/805634470ec74ae15ca04b4f164a608f06b362fa/.github/workflows/test-distro.yml)
- Uses: [github-action-matrix-outputs-write](https://github.com/qualcomm-linux/github-action-matrix-outputs-write) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom-distro/blob/805634470ec74ae15ca04b4f164a608f06b362fa/.github/workflows/test-distro.yml)
- Uses: [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom-distro/blob/805634470ec74ae15ca04b4f164a608f06b362fa/.github/workflows/build-yocto.yml) · [source 2](https://github.com/qualcomm-linux/meta-qcom-distro/blob/805634470ec74ae15ca04b4f164a608f06b362fa/.github/workflows/test-distro.yml)
- Uses: [upload-private-artifact-action](https://github.com/qualcomm-linux/upload-private-artifact-action) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom-distro/blob/805634470ec74ae15ca04b4f164a608f06b362fa/.github/actions/compile/action.yml)
- Uses: [qcom-reusable-workflows](https://github.com/qualcomm/qcom-reusable-workflows) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom-distro/blob/805634470ec74ae15ca04b4f164a608f06b362fa/.github/workflows/pr.yml)
- Used by: [meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) — **integrates with**
  - Optional: the dynamic layer applies only when qcom-distro is present.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/conf/layer.conf)
- Used by: [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) — **selects for distro**
  - Optional qcom-distro kas composition; not required by every BSP-only build.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/ci/qcom-distro.yml)

</details>

[Back to the ecosystem map](../README.md).

<!-- Dataset SHA-256: bd976587e3980bd55d7438b70404ec9c904e9867ffff16f5f02793244f602c8a; revision: this checkout. -->
