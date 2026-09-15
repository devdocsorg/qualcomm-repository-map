# Repository map: qualcomm-linux/pkg-urm

**You are here: [qualcomm-linux/pkg-urm](https://github.com/qualcomm-linux/pkg-urm)**

This project handles Debian packaging for the URM project (https://github.com/qualcomm/userspace-resource-manager)

## Outgoing connections

**Packages**

- [qualcomm-linux/pkg-urm](https://github.com/qualcomm-linux/pkg-urm) → **packages** → [qualcomm/userspace-resource-manager](https://github.com/qualcomm/userspace-resource-manager)
  - Package metadata and source ownership are separate; choose the package branch before editing packaging.
  - [Explore qualcomm/userspace-resource-manager](qualcomm--userspace-resource-manager.md) · [evidence 1](https://github.com/qualcomm-linux/pkg-urm/blob/f3dd7df55fe9522d5dabd9b00729c54d7076a111/README.md)

**Uses automation from**

- [qualcomm-linux/pkg-urm](https://github.com/qualcomm-linux/pkg-urm) → **uses automation from** → [qualcomm-linux/debusine-action](https://github.com/qualcomm-linux/debusine-action)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm-linux/debusine-action](qualcomm-linux--debusine-action.md) · [evidence 1](https://github.com/qualcomm-linux/pkg-urm/blob/f3dd7df55fe9522d5dabd9b00729c54d7076a111/.github/workflows/debusine-daily.yml) · [evidence 2](https://github.com/qualcomm-linux/pkg-urm/blob/f3dd7df55fe9522d5dabd9b00729c54d7076a111/.github/workflows/debusine-pr-check.yml) · [evidence 3](https://github.com/qualcomm-linux/pkg-urm/blob/f3dd7df55fe9522d5dabd9b00729c54d7076a111/.github/workflows/debusine-release.yml)
- [qualcomm-linux/pkg-urm](https://github.com/qualcomm-linux/pkg-urm) → **uses automation from** → [qualcomm-linux/qli-ci](https://github.com/qualcomm-linux/qli-ci)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm-linux/qli-ci](qualcomm-linux--qli-ci.md) · [evidence 1](https://github.com/qualcomm-linux/pkg-urm/blob/f3dd7df55fe9522d5dabd9b00729c54d7076a111/.github/workflows/pkg-build.yml) · [evidence 2](https://github.com/qualcomm-linux/pkg-urm/blob/f3dd7df55fe9522d5dabd9b00729c54d7076a111/.github/workflows/pkg-pr-hook.yml) · [evidence 3](https://github.com/qualcomm-linux/pkg-urm/blob/f3dd7df55fe9522d5dabd9b00729c54d7076a111/.github/workflows/pkg-promote-prebuilt.yml) · [evidence 4](https://github.com/qualcomm-linux/pkg-urm/blob/f3dd7df55fe9522d5dabd9b00729c54d7076a111/.github/workflows/pkg-promote.yml) · [evidence 5](https://github.com/qualcomm-linux/pkg-urm/blob/f3dd7df55fe9522d5dabd9b00729c54d7076a111/.github/workflows/pkg-release.yml)

## Full ecosystem map

[Explore the Qualcomm repository map](../README.md).

Connections apply to the linked evidence revisions; use release-compatible revisions for a build.

Dataset SHA-256: `602a68056238817dccee9f98db5c06ea20d0bb165a53a0c23ff2d0423240dfca`.
