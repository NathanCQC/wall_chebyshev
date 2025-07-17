# wall-chebyshev: A Computational Study for Ground State Projections

This repository accompanies our research paper on implementing the wall Chebyshev projector, featuring its application in the [guppy](https://github.com/CQCL/guppylang) framework. The paper discusses a novel computational technique to attain the ground state via the following projection scheme:

$$
\lvert\Psi^{(n,\mu)}\rangle = \left[\prod_{\nu=0}^{\mu}\frac{\hat{H}-a_{\nu}}{S-a_{\nu}}\right] \left[g^{\text{wall-Ch}}(\hat{H})\right]^n \lvert\Phi\rangle.
$$

## Repository Overview

The codebase provided within this repository serves as the practical implementation that complements the theoretical exposition of the paper. It supports reproducibility and further exploratory research in quantum state projection methods.

## Installation

To replicate our experimental results, follow these steps to set up your project environment:

1. Open your terminal and navigate to the project directory.
2. Execute the following commands to create and synchronize the virtual environment:

```bash
uv venv .venv
uv sync
```

These commands will install the necessary dependencies, including the wallcheb package, ensuring that all computational experiments run seamlessly.

## Examples

For a detailed demonstration of the projector in action—specifically within the Hubbard model framework—please refer to the accompanying Jupyter notebook:

[wall_chebyshev_projector.ipynb](https://github.com/NathanCQC/wall_chebyshev/blob/main/examples/wall_chebyshev_projector.ipynb)

This example can be generalized to other lattice models and quantum systems, showcasing the versatility of the wall Chebyshev projector.

## Citation

If you find this work helpful in your research, please consider citing our paper:

    @article{wallcheb2023,
      title={Efficient Ground State Projection using the Wall Chebyshev Method},
      author={Your Name and Collaborators},
      journal={Journal of Computational Methods},
      year={2023},
    }

