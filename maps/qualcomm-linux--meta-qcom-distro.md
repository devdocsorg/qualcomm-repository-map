# Repository map: qualcomm-linux/meta-qcom-distro

**You are here: [qualcomm-linux/meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro)**

OpenEmbedded/Yocto Project Reference Distribution layer for Qualcomm based platforms

## Outgoing connections

**Uses automation from**

- [qualcomm-linux/meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro) → **uses automation from** → [qualcomm-linux/github-action-matrix-outputs-read](https://github.com/qualcomm-linux/github-action-matrix-outputs-read)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm-linux/github-action-matrix-outputs-read](qualcomm-linux--github-action-matrix-outputs-read.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom-distro/blob/805634470ec74ae15ca04b4f164a608f06b362fa/.github/workflows/test-distro.yml)
- [qualcomm-linux/meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro) → **uses automation from** → [qualcomm-linux/github-action-matrix-outputs-write](https://github.com/qualcomm-linux/github-action-matrix-outputs-write)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm-linux/github-action-matrix-outputs-write](qualcomm-linux--github-action-matrix-outputs-write.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom-distro/blob/805634470ec74ae15ca04b4f164a608f06b362fa/.github/workflows/test-distro.yml)
- [qualcomm-linux/meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro) → **uses automation from** → [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm-linux/meta-qcom](qualcomm-linux--meta-qcom.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom-distro/blob/805634470ec74ae15ca04b4f164a608f06b362fa/.github/workflows/build-yocto.yml) · [evidence 2](https://github.com/qualcomm-linux/meta-qcom-distro/blob/805634470ec74ae15ca04b4f164a608f06b362fa/.github/workflows/test-distro.yml) · [evidence 3](https://github.com/qualcomm-linux/meta-qcom-distro/blob/805634470ec74ae15ca04b4f164a608f06b362fa/.github/workflows/test-distro.yml) · [evidence 4](https://github.com/qualcomm-linux/meta-qcom-distro/blob/805634470ec74ae15ca04b4f164a608f06b362fa/.github/workflows/test-distro.yml)
- [qualcomm-linux/meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro) → **uses automation from** → [qualcomm-linux/upload-private-artifact-action](https://github.com/qualcomm-linux/upload-private-artifact-action)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm-linux/upload-private-artifact-action](qualcomm-linux--upload-private-artifact-action.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom-distro/blob/805634470ec74ae15ca04b4f164a608f06b362fa/.github/actions/compile/action.yml)
- [qualcomm-linux/meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro) → **uses automation from** → [qualcomm/qcom-reusable-workflows](https://github.com/qualcomm/qcom-reusable-workflows)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm/qcom-reusable-workflows](qualcomm--qcom-reusable-workflows.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom-distro/blob/805634470ec74ae15ca04b4f164a608f06b362fa/.github/workflows/pr.yml)

## Incoming connections

**Integrates with** (repositories using this one)

- [qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) → **integrates with** → [qualcomm-linux/meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro)
  - Optional: the dynamic layer applies only when qcom-distro is present.
  - [Explore qualcomm-linux/meta-qcom-3rdparty](qualcomm-linux--meta-qcom-3rdparty.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/conf/layer.conf)

**Selects for distro** (repositories using this one)

- [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom) → **selects for distro** → [qualcomm-linux/meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro)
  - Optional qcom-distro kas composition; not required by every BSP-only build.
  - [Explore qualcomm-linux/meta-qcom](qualcomm-linux--meta-qcom.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/ci/qcom-distro.yml)

## Full ecosystem map

[Explore the Qualcomm repository map](../README.md).

Connections apply to the linked evidence revisions; use release-compatible revisions for a build.

Dataset SHA-256: `602a68056238817dccee9f98db5c06ea20d0bb165a53a0c23ff2d0423240dfca`.
