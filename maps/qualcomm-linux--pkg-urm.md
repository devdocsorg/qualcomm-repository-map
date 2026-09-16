# [pkg-urm](https://github.com/qualcomm-linux/pkg-urm)

This project handles Debian packaging for the URM project (https://github.com/qualcomm/userspace-resource-manager)

## Uses

### Packages

- [userspace-resource-manager](https://github.com/qualcomm/userspace-resource-manager) · [Explore](qualcomm--userspace-resource-manager.md)

### Uses automation from

- [debusine-action](https://github.com/qualcomm-linux/debusine-action) · [Explore](qualcomm-linux--debusine-action.md)
- [qli-ci](https://github.com/qualcomm-linux/qli-ci) · [Explore](qualcomm-linux--qli-ci.md)

<details>
<summary>Applicability and sources</summary>

- Uses: [userspace-resource-manager](https://github.com/qualcomm/userspace-resource-manager) — **packages**
  - Package metadata and source ownership are separate; choose the package branch before editing packaging.
  - [source 1](https://github.com/qualcomm-linux/pkg-urm/blob/f3dd7df55fe9522d5dabd9b00729c54d7076a111/README.md)
- Uses: [debusine-action](https://github.com/qualcomm-linux/debusine-action) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/pkg-urm/blob/f3dd7df55fe9522d5dabd9b00729c54d7076a111/.github/workflows/debusine-daily.yml) · [source 2](https://github.com/qualcomm-linux/pkg-urm/blob/f3dd7df55fe9522d5dabd9b00729c54d7076a111/.github/workflows/debusine-pr-check.yml) · [source 3](https://github.com/qualcomm-linux/pkg-urm/blob/f3dd7df55fe9522d5dabd9b00729c54d7076a111/.github/workflows/debusine-release.yml)
- Uses: [qli-ci](https://github.com/qualcomm-linux/qli-ci) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/pkg-urm/blob/f3dd7df55fe9522d5dabd9b00729c54d7076a111/.github/workflows/pkg-build.yml) · [source 2](https://github.com/qualcomm-linux/pkg-urm/blob/f3dd7df55fe9522d5dabd9b00729c54d7076a111/.github/workflows/pkg-pr-hook.yml) · [source 3](https://github.com/qualcomm-linux/pkg-urm/blob/f3dd7df55fe9522d5dabd9b00729c54d7076a111/.github/workflows/pkg-promote-prebuilt.yml) · [source 4](https://github.com/qualcomm-linux/pkg-urm/blob/f3dd7df55fe9522d5dabd9b00729c54d7076a111/.github/workflows/pkg-promote.yml) · [source 5](https://github.com/qualcomm-linux/pkg-urm/blob/f3dd7df55fe9522d5dabd9b00729c54d7076a111/.github/workflows/pkg-release.yml)

</details>

[Back to the ecosystem map](../README.md).

<!-- Dataset SHA-256: bd976587e3980bd55d7438b70404ec9c904e9867ffff16f5f02793244f602c8a; revision: this checkout. -->
