# [qcom-rpm-utils](https://github.com/qualcomm-linux/qcom-rpm-utils)

This repo will hold build scripts and reusable workflows for pkg rpm builds.

## Uses

### Uses automation from

- [upload-private-artifact-action](https://github.com/qualcomm-linux/upload-private-artifact-action) · [Explore](qualcomm-linux--upload-private-artifact-action.md)
- [qcom-reusable-workflows](https://github.com/qualcomm/qcom-reusable-workflows) · [Explore](qualcomm--qcom-reusable-workflows.md)

## Used by

### Uses automation from

- [pkg-rpm-qcom-fastcv-binaries](https://github.com/qualcomm-linux/pkg-rpm-qcom-fastcv-binaries) · [Explore](qualcomm-linux--pkg-rpm-qcom-fastcv-binaries.md)
- [pkg-rpm-video-driver](https://github.com/qualcomm-linux/pkg-rpm-video-driver) · [Explore](qualcomm-linux--pkg-rpm-video-driver.md)

<details>
<summary>Applicability and sources</summary>

- Uses: [upload-private-artifact-action](https://github.com/qualcomm-linux/upload-private-artifact-action) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/qcom-rpm-utils/blob/2ce52035e30d194fc7402fe49fed45582236604d/.github/workflows/pkg-build-reusable-workflow.yml)
- Uses: [qcom-reusable-workflows](https://github.com/qualcomm/qcom-reusable-workflows) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/qcom-rpm-utils/blob/2ce52035e30d194fc7402fe49fed45582236604d/.github/workflows/qcom-preflight-checks.yml)
- Used by: [pkg-rpm-qcom-fastcv-binaries](https://github.com/qualcomm-linux/pkg-rpm-qcom-fastcv-binaries) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/pkg-rpm-qcom-fastcv-binaries/blob/d13ab7f38f921e2c2efd092cba22dce952ef8e02/.github/workflows/build-on-pr.yml) · [source 2](https://github.com/qualcomm-linux/pkg-rpm-qcom-fastcv-binaries/blob/d13ab7f38f921e2c2efd092cba22dce952ef8e02/.github/workflows/pkg-release.yml)
- Used by: [pkg-rpm-video-driver](https://github.com/qualcomm-linux/pkg-rpm-video-driver) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/pkg-rpm-video-driver/blob/4d308c055e09b144800a773a60cfd02da57110be/.github/workflows/build-on-pr.yml) · [source 2](https://github.com/qualcomm-linux/pkg-rpm-video-driver/blob/4d308c055e09b144800a773a60cfd02da57110be/.github/workflows/pkg-release.yml)

</details>

[Back to the ecosystem map](../README.md).

<!-- Dataset SHA-256: bd976587e3980bd55d7438b70404ec9c904e9867ffff16f5f02793244f602c8a; revision: this checkout. -->
