![Pytest](https://github.com/XDevos/registest/actions/workflows/test.yml/badge.svg?branch=main)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

# RegisTest

*Registration Testing Tool*

## 1. Installation

|OS|Linux|Windows|Mac|
|:-:|:-:|:-:|:-:|
|**compatibility**|Yes|?|?|

### [Optional] Install conda

*We use conda environment to avoid version problem between RegisTest dependencies and other applications.*

We recommend to download the lighter version via [Miniconda](https://docs.anaconda.com/miniconda/install/#quick-command-line-install) (if you only intend to use RegisTest without developing new feature).

### [Optional] Create the environment
```bash
conda create -n registest python=3.11
conda activate registest
```

---

### Install from PyPi
   ```bash
   pip install registest
   ```

To check if RegisTest is well installed, run:
```bash
registest --help
```

---

### [Optional] Install with dev mod

```bash
git clone git@github.com:XDevos/registest.git
cd registest
pip install -e .
```

## **2. Usage**

---

## 3. **Support**

If you encounter any issues or have questions, [open an issue in the GitHub repository](https://github.com/XDevos/registest/issues).
