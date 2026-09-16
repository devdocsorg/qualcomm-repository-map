# [meta-qcom-releases](https://github.com/qualcomm-linux/meta-qcom-releases)

This repo will be used to store kas-lock files for milestone releases of meta-qcom

## Uses

### Pins release of

- [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) · [Explore](qualcomm-linux--meta-qcom.md)

### Uses automation from

- [qcom-reusable-workflows](https://github.com/qualcomm/qcom-reusable-workflows) · [Explore](qualcomm--qcom-reusable-workflows.md)

<details>
<summary>Applicability and sources</summary>

- Uses: [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) — **pins release of**
  - Milestone tags and kas lock files; select the desired release tag.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom-releases/blob/4129a6850c070bb57da122b2ebceff3de9951a1a/README.md)
- Uses: [qcom-reusable-workflows](https://github.com/qualcomm/qcom-reusable-workflows) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom-releases/blob/4129a6850c070bb57da122b2ebceff3de9951a1a/.github/workflows/qcom-preflight-checks.yml)

</details>

[Back to the ecosystem map](../README.md).

<!-- Dataset SHA-256: bd976587e3980bd55d7438b70404ec9c904e9867ffff16f5f02793244f602c8a; revision: this checkout. -->
