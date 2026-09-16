# [meta-ai](https://github.com/qualcomm-linux/meta-ai)

OpenEmbedded layer for AI/ML related recipes

## Uses

### Uses automation from

- [qcom-reusable-workflows](https://github.com/qualcomm/qcom-reusable-workflows) · [Explore](qualcomm--qcom-reusable-workflows.md)

## Used by

### Selects for distro

- [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) · [Explore](qualcomm-linux--meta-qcom.md)

<details>
<summary>Applicability and sources</summary>

- Uses: [qcom-reusable-workflows](https://github.com/qualcomm/qcom-reusable-workflows) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/meta-ai/blob/21e7b36b0d259a9cf5d2226160b227962f762585/.github/workflows/pr.yml) · [source 2](https://github.com/qualcomm-linux/meta-ai/blob/21e7b36b0d259a9cf5d2226160b227962f762585/.github/workflows/qcom-preflight-checks.yml)
- Used by: [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) — **selects for distro**
  - Optional qcom-distro kas composition; not required by every BSP-only build.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/ci/qcom-distro.yml)

</details>

[Back to the ecosystem map](../README.md).

<!-- Dataset SHA-256: bd976587e3980bd55d7438b70404ec9c904e9867ffff16f5f02793244f602c8a; revision: this checkout. -->
