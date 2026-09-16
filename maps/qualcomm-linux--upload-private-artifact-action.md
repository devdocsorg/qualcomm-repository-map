# [upload-private-artifact-action](https://github.com/qualcomm-linux/upload-private-artifact-action)

An action for use in qualcomm-linux projects that need to publish CI artifacts that aren't cleared for public distribution.

## Uses

### Uses automation from

- [qcom-reusable-workflows](https://github.com/qualcomm/qcom-reusable-workflows) · [Explore](qualcomm--qcom-reusable-workflows.md)

## Used by

### Uses automation from

- [aiml-container-test](https://github.com/qualcomm-linux/aiml-container-test) · [Explore](qualcomm-linux--aiml-container-test.md)
- [awstest-meta-qcom](https://github.com/qualcomm-linux/awstest-meta-qcom) · [Explore](qualcomm-linux--awstest-meta-qcom.md)
- [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) · [Explore](qualcomm-linux--meta-qcom.md)
- [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro) · [Explore](qualcomm-linux--meta-qcom-distro.md)
- [meta-qcom-robotics-sdk](https://github.com/qualcomm-linux/meta-qcom-robotics-sdk) · [Explore](qualcomm-linux--meta-qcom-robotics-sdk.md)
- [pkg-linux-qcom](https://github.com/qualcomm-linux/pkg-linux-qcom) · [Explore](qualcomm-linux--pkg-linux-qcom.md)
- [qcom-deb-images](https://github.com/qualcomm-linux/qcom-deb-images) · [Explore](qualcomm-linux--qcom-deb-images.md)
- [qcom-rpm-utils](https://github.com/qualcomm-linux/qcom-rpm-utils) · [Explore](qualcomm-linux--qcom-rpm-utils.md)
- [qli-ci](https://github.com/qualcomm-linux/qli-ci) · [Explore](qualcomm-linux--qli-ci.md)
- [rpm-images](https://github.com/qualcomm-linux/rpm-images) · [Explore](qualcomm-linux--rpm-images.md)
- [ubuntu-qcom-kernel](https://github.com/qualcomm-linux/ubuntu-qcom-kernel) · [Explore](qualcomm-linux--ubuntu-qcom-kernel.md)

<details>
<summary>Applicability and sources</summary>

- Uses: [qcom-reusable-workflows](https://github.com/qualcomm/qcom-reusable-workflows) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/upload-private-artifact-action/blob/35784966733744f890eca16b3670da4f22df1e76/.github/workflows/qcom-preflight-checks.yml)
- Used by: [aiml-container-test](https://github.com/qualcomm-linux/aiml-container-test) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/aiml-container-test/blob/2dfbb557da0a296ed3d4546c13bbfb5caa6c5490/.github/workflows/docker_build.yml)
- Used by: [awstest-meta-qcom](https://github.com/qualcomm-linux/awstest-meta-qcom) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/awstest-meta-qcom/blob/5135d214d1712ee4b857120fe3bebb0d62a58c45/.github/workflows/build-yocto.yml)
- Used by: [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/.github/workflows/compile.yml)
- Used by: [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom-distro/blob/805634470ec74ae15ca04b4f164a608f06b362fa/.github/actions/compile/action.yml)
- Used by: [meta-qcom-robotics-sdk](https://github.com/qualcomm-linux/meta-qcom-robotics-sdk) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/meta-qcom-robotics-sdk/blob/7b47d3855b440d28626128c0f207d8561d64f718/.github/actions/compile/action.yml)
- Used by: [pkg-linux-qcom](https://github.com/qualcomm-linux/pkg-linux-qcom) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/pkg-linux-qcom/blob/28c5a3a221a74c2023672c0f425b6ba28cad95b7/.github/workflows/build-kernel-debusine.yml) · [source 2](https://github.com/qualcomm-linux/pkg-linux-qcom/blob/28c5a3a221a74c2023672c0f425b6ba28cad95b7/.github/workflows/build-kernel-ubuntu.yml)
- Used by: [qcom-deb-images](https://github.com/qualcomm-linux/qcom-deb-images) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/qcom-deb-images/blob/04ee6f3866e029a811577dd4a8a2a8c09487485e/.github/workflows/build-overlay-deb.yml) · [source 2](https://github.com/qualcomm-linux/qcom-deb-images/blob/04ee6f3866e029a811577dd4a8a2a8c09487485e/.github/workflows/debos.yml) · [source 3](https://github.com/qualcomm-linux/qcom-deb-images/blob/04ee6f3866e029a811577dd4a8a2a8c09487485e/.github/workflows/linux.yml) · [source 4](https://github.com/qualcomm-linux/qcom-deb-images/blob/04ee6f3866e029a811577dd4a8a2a8c09487485e/.github/workflows/u-boot.yml)
- Used by: [qcom-rpm-utils](https://github.com/qualcomm-linux/qcom-rpm-utils) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/qcom-rpm-utils/blob/2ce52035e30d194fc7402fe49fed45582236604d/.github/workflows/pkg-build-reusable-workflow.yml)
- Used by: [qli-ci](https://github.com/qualcomm-linux/qli-ci) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/qli-ci/blob/a9eb55efa7405bea5b8b9a251f87bfcce570be80/.github/workflows/pkg-build-reusable-workflow.yml) · [source 2](https://github.com/qualcomm-linux/qli-ci/blob/a9eb55efa7405bea5b8b9a251f87bfcce570be80/.github/workflows/pkg-release-reusable-workflow.yml)
- Used by: [rpm-images](https://github.com/qualcomm-linux/rpm-images) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/rpm-images/blob/466cb78e65f99e4bd75382fd7ed74093088cd70e/.github/workflows/build-rpm.yml)
- Used by: [ubuntu-qcom-kernel](https://github.com/qualcomm-linux/ubuntu-qcom-kernel) — **uses automation from**
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [source 1](https://github.com/qualcomm-linux/ubuntu-qcom-kernel/blob/a26c66f4e02e0009a19c49368d5557de21c26747/.github/workflows/build-kernel.yml)

</details>

[Back to the ecosystem map](../README.md).

<!-- Dataset SHA-256: bd976587e3980bd55d7438b70404ec9c904e9867ffff16f5f02793244f602c8a; revision: this checkout. -->
