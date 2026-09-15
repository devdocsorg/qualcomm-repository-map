# Repository map: qualcomm-linux/qcom-rpm-utils

**You are here: [qualcomm-linux/qcom-rpm-utils](https://github.com/qualcomm-linux/qcom-rpm-utils)**

This repo will hold build scripts and reusable workflows for pkg rpm builds.

## Outgoing connections

**Uses automation from**

- [qualcomm-linux/qcom-rpm-utils](https://github.com/qualcomm-linux/qcom-rpm-utils) → **uses automation from** → [qualcomm-linux/upload-private-artifact-action](https://github.com/qualcomm-linux/upload-private-artifact-action)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm-linux/upload-private-artifact-action](qualcomm-linux--upload-private-artifact-action.md) · [evidence 1](https://github.com/qualcomm-linux/qcom-rpm-utils/blob/2ce52035e30d194fc7402fe49fed45582236604d/.github/workflows/pkg-build-reusable-workflow.yml)
- [qualcomm-linux/qcom-rpm-utils](https://github.com/qualcomm-linux/qcom-rpm-utils) → **uses automation from** → [qualcomm/qcom-reusable-workflows](https://github.com/qualcomm/qcom-reusable-workflows)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm/qcom-reusable-workflows](qualcomm--qcom-reusable-workflows.md) · [evidence 1](https://github.com/qualcomm-linux/qcom-rpm-utils/blob/2ce52035e30d194fc7402fe49fed45582236604d/.github/workflows/qcom-preflight-checks.yml)

## Incoming connections

**Uses automation from** (repositories using this one)

- [qualcomm-linux/pkg-rpm-qcom-fastcv-binaries](https://github.com/qualcomm-linux/pkg-rpm-qcom-fastcv-binaries) → **uses automation from** → [qualcomm-linux/qcom-rpm-utils](https://github.com/qualcomm-linux/qcom-rpm-utils)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm-linux/pkg-rpm-qcom-fastcv-binaries](qualcomm-linux--pkg-rpm-qcom-fastcv-binaries.md) · [evidence 1](https://github.com/qualcomm-linux/pkg-rpm-qcom-fastcv-binaries/blob/d13ab7f38f921e2c2efd092cba22dce952ef8e02/.github/workflows/build-on-pr.yml) · [evidence 2](https://github.com/qualcomm-linux/pkg-rpm-qcom-fastcv-binaries/blob/d13ab7f38f921e2c2efd092cba22dce952ef8e02/.github/workflows/pkg-release.yml)
- [qualcomm-linux/pkg-rpm-video-driver](https://github.com/qualcomm-linux/pkg-rpm-video-driver) → **uses automation from** → [qualcomm-linux/qcom-rpm-utils](https://github.com/qualcomm-linux/qcom-rpm-utils)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm-linux/pkg-rpm-video-driver](qualcomm-linux--pkg-rpm-video-driver.md) · [evidence 1](https://github.com/qualcomm-linux/pkg-rpm-video-driver/blob/4d308c055e09b144800a773a60cfd02da57110be/.github/workflows/build-on-pr.yml) · [evidence 2](https://github.com/qualcomm-linux/pkg-rpm-video-driver/blob/4d308c055e09b144800a773a60cfd02da57110be/.github/workflows/pkg-release.yml)

## Full ecosystem map

[Explore the Qualcomm repository map](../README.md).

Connections apply to the linked evidence revisions; use release-compatible revisions for a build.

Dataset SHA-256: `602a68056238817dccee9f98db5c06ea20d0bb165a53a0c23ff2d0423240dfca`.
