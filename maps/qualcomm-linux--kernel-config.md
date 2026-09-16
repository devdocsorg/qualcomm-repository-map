# Repository map: qualcomm-linux/kernel-config

**You are here: [qualcomm-linux/kernel-config](https://github.com/qualcomm-linux/kernel-config)**

Configuration data to create qcom-next from the tech topic branches

## Outgoing connections

### Configures

- [qualcomm-linux/kernel-config](https://github.com/qualcomm-linux/kernel-config) → **configures** → [qualcomm-linux/automerge](https://github.com/qualcomm-linux/automerge)
  - qcom-next integration configuration.
  - [Explore qualcomm-linux/automerge](qualcomm-linux--automerge.md) · [evidence 1](https://github.com/qualcomm-linux/kernel-config/blob/ca3a00b71520dd58ede87f9c2921b48f95ac0b32/README)

### Selects branches from

- [qualcomm-linux/kernel-config](https://github.com/qualcomm-linux/kernel-config) → **selects branches from** → [qualcomm-linux/kernel](https://github.com/qualcomm-linux/kernel)
  - qcom-next.conf names baseline and topic branches.
  - [Explore qualcomm-linux/kernel](qualcomm-linux--kernel.md) · [evidence 1](https://github.com/qualcomm-linux/kernel-config/blob/ca3a00b71520dd58ede87f9c2921b48f95ac0b32/qcom-next.conf)
- [qualcomm-linux/kernel-config](https://github.com/qualcomm-linux/kernel-config) → **selects branches from** → [qualcomm-linux/kernel-topics](https://github.com/qualcomm-linux/kernel-topics)
  - qcom-next.conf names baseline and topic branches.
  - [Explore qualcomm-linux/kernel-topics](qualcomm-linux--kernel-topics.md) · [evidence 1](https://github.com/qualcomm-linux/kernel-config/blob/ca3a00b71520dd58ede87f9c2921b48f95ac0b32/qcom-next.conf)

### Uses automation from

- [qualcomm-linux/kernel-config](https://github.com/qualcomm-linux/kernel-config) → **uses automation from** → [qualcomm-linux/kernel-checkers](https://github.com/qualcomm-linux/kernel-checkers)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm-linux/kernel-checkers](qualcomm-linux--kernel-checkers.md) · [evidence 1](https://github.com/qualcomm-linux/kernel-config/blob/ca3a00b71520dd58ede87f9c2921b48f95ac0b32/.github/workflows/kernel_checker.yml)
- [qualcomm-linux/kernel-config](https://github.com/qualcomm-linux/kernel-config) → **uses automation from** → [qualcomm/commit-emails-check-action](https://github.com/qualcomm/commit-emails-check-action)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm/commit-emails-check-action](qualcomm--commit-emails-check-action.md) · [evidence 1](https://github.com/qualcomm-linux/kernel-config/blob/ca3a00b71520dd58ede87f9c2921b48f95ac0b32/.github/workflows/email_checker.yml)

## Incoming connections

### Uses automation from (repositories using this one)

- [qualcomm-linux/kernel-checkers](https://github.com/qualcomm-linux/kernel-checkers) → **uses automation from** → [qualcomm-linux/kernel-config](https://github.com/qualcomm-linux/kernel-config)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm-linux/kernel-checkers](qualcomm-linux--kernel-checkers.md) · [evidence 1](https://github.com/qualcomm-linux/kernel-checkers/blob/23c35b0e159903b2f69ec5d11f5b6e5dcd493319/.github/workflows/checker.yml)
- [qualcomm-linux/video-driver](https://github.com/qualcomm-linux/video-driver) → **uses automation from** → [qualcomm-linux/kernel-config](https://github.com/qualcomm-linux/kernel-config)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm-linux/video-driver](qualcomm-linux--video-driver.md) · [evidence 1](https://github.com/qualcomm-linux/video-driver/blob/269addefac0f3378a152cd2cfca18b83103e9300/.github/workflows/owl_build.yml) · [evidence 2](https://github.com/qualcomm-linux/video-driver/blob/269addefac0f3378a152cd2cfca18b83103e9300/.github/workflows/sync-and-build.yml) · [evidence 3](https://github.com/qualcomm-linux/video-driver/blob/269addefac0f3378a152cd2cfca18b83103e9300/.github/workflows/test.yml)

## Full ecosystem map

[Explore the Qualcomm repository map](../README.md).

Connections apply to the linked evidence revisions; use release-compatible revisions for a build.

Dataset SHA-256: `bd976587e3980bd55d7438b70404ec9c904e9867ffff16f5f02793244f602c8a`.
