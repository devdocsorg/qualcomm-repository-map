# [kernel-config](https://github.com/qualcomm-linux/kernel-config)

Configuration data to create qcom-next from the tech topic branches

## Uses

### Configures

- [automerge](https://github.com/qualcomm-linux/automerge) · [Explore](qualcomm-linux--automerge.md)

### Selects branches from

- [kernel](https://github.com/qualcomm-linux/kernel) · [Explore](qualcomm-linux--kernel.md)
- [kernel-topics](https://github.com/qualcomm-linux/kernel-topics) · [Explore](qualcomm-linux--kernel-topics.md)

### Uses automation from

- [kernel-checkers](https://github.com/qualcomm-linux/kernel-checkers) · [Explore](qualcomm-linux--kernel-checkers.md)
- [commit-emails-check-action](https://github.com/qualcomm/commit-emails-check-action) · [Explore](qualcomm--commit-emails-check-action.md)

## Used by

### Uses automation from

- [kernel-checkers](https://github.com/qualcomm-linux/kernel-checkers) · [Explore](qualcomm-linux--kernel-checkers.md)
- [video-driver](https://github.com/qualcomm-linux/video-driver) · [Explore](qualcomm-linux--video-driver.md)

<details>
<summary>Applicability and sources</summary>

- Uses: [automerge](https://github.com/qualcomm-linux/automerge) — **configures**
  - qcom-next integration configuration.
  - [source 1](https://github.com/qualcomm-linux/kernel-config/blob/ca3a00b71520dd58ede87f9c2921b48f95ac0b32/README)
- Uses: [kernel](https://github.com/qualcomm-linux/kernel) — **selects branches from**
  - qcom-next.conf names baseline and topic branches.
  - [source 1](https://github.com/qualcomm-linux/kernel-config/blob/ca3a00b71520dd58ede87f9c2921b48f95ac0b32/qcom-next.conf)
- Uses: [kernel-topics](https://github.com/qualcomm-linux/kernel-topics) — **selects branches from**
  - qcom-next.conf names baseline and topic branches.
  - [source 1](https://github.com/qualcomm-linux/kernel-config/blob/ca3a00b71520dd58ede87f9c2921b48f95ac0b32/qcom-next.conf)
- Uses: [kernel-checkers](https://github.com/qualcomm-linux/kernel-checkers) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/kernel-config/blob/ca3a00b71520dd58ede87f9c2921b48f95ac0b32/.github/workflows/kernel_checker.yml)
- Uses: [commit-emails-check-action](https://github.com/qualcomm/commit-emails-check-action) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/kernel-config/blob/ca3a00b71520dd58ede87f9c2921b48f95ac0b32/.github/workflows/email_checker.yml)
- Used by: [kernel-checkers](https://github.com/qualcomm-linux/kernel-checkers) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/kernel-checkers/blob/23c35b0e159903b2f69ec5d11f5b6e5dcd493319/.github/workflows/checker.yml)
- Used by: [video-driver](https://github.com/qualcomm-linux/video-driver) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/video-driver/blob/269addefac0f3378a152cd2cfca18b83103e9300/.github/workflows/owl_build.yml) · [source 2](https://github.com/qualcomm-linux/video-driver/blob/269addefac0f3378a152cd2cfca18b83103e9300/.github/workflows/sync-and-build.yml) · [source 3](https://github.com/qualcomm-linux/video-driver/blob/269addefac0f3378a152cd2cfca18b83103e9300/.github/workflows/test.yml)

</details>

[Back to the ecosystem map](../README.md).

<!-- Dataset SHA-256: bd976587e3980bd55d7438b70404ec9c904e9867ffff16f5f02793244f602c8a; revision: this checkout. -->
