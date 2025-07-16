# qtmlib

This is a Python 3.11 & 3.12 app called qtmlib. It is an internal Quantinuum library which builds on pytket to make building quantum algorithms with pytket easy, leveraging the `Registerbox` abstraction.

## Git Branching Strategy

All feature branching should be done off the `main` branch.

Pull requests can go into the `main` branch. There is also a `research` branch which can be used for research features and contains more experimental code and a sub folder `research` it is syncs with `main`. Working in the research folder ensure no merge conflicts when merging `main` into `research`, research PR can go into here if you want to share you work with the team.

Because this is a young research-focused repo, we will use the GitHub flow branching strategy. All features go into `main` It will move forward by `feature/xxx` branches merging into it. The branching strategy is as follows:

- `feature/xxx` - Features to get into `main`
- `research-xxx` - Research features which will be PRed to `research`. Can be thought of as a staging area for a feature.
- `bugfix/xxx` - Bug fixes

Please use rebase over merge where possible, apart from on pull requests. This will ensure the git history is tidy. Please ask for a GitLens+ license from IT so you can use their amazing git commit graph feature.

## Project Structure

The project is structured as follows:

- **Circuits**: Circuit primitives which can be combined to build a set of quantum algorithms.
- **Measurement**: Interchangeable routines which measure the quantum circuit.
- **Algorithms**: Quantum algorithms which combine circuit and measurement.
- **Operators**: Operators which can be used in the circuits.

## Installation

To install the project, clone the repository and run:

```sh
python -m pip install --upgrade pip
python -m pip install uv
uv venv .venv -p 3.12
source .venv/bin/activate
uv pip install -r requirements.txt
uv pip install -e .
uv pip install pre-commit
pre-commit run --all-files
```

## Developers

It is strongly recommended developers use VSCode, using the configuration provided in `.vscode`.

Useful extensions:

- [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- [Typos](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker)
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) (includes Pyright and Jupyter)
- [GitHub Pull Requests and Issues](https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-pull-request-github)
- [SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh)
- [GitLens](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens) (Optional, but very useful for visualizing git history)

qtmlib uses pre-commit via a `.pre-commit-config.yaml`. This runs a series of checks on each local commit to make sure your code is up to the correct standard of the library. It will be annoying at first, but lead to very high code quality. These are:

- **Ruff-format**: This is a reformatter. If your code is not formatted correctly, it will be reformatted on the commit. If this happens, just commit again and it should pass the reformatting.
- **Ruff**: Ruff is the fastest, most modern Python linter written in Rust. Think of it as a code spell checker [Ruff Documentation](https://beta.ruff.rs/docs/). It will keep your code to a good standard and give you lots of warnings and errors as you develop the code. These will also show up in the problems bar (VSCode). If you commit without fixing these, your commit will fail. Ruff also ensures docstrings are formatted correctly, where we use the Google style for readability. If your docstrings are not good enough, you will not be able to commit your code.
- **Pyright**: Pyright is a C++ Python type checker [Pyright Documentation](https://microsoft.github.io/pyright/#/). It comes with Pylance (Python language server) in VSCode. It enforces you to have all the object input and output types correctly defined. If this is not the case, your commit will fail. Type checking errors will appear in the problems bar (VSCode).
- **typos**: This is a spell checker for your code. It will check all the strings in your code to make sure they are spelled correctly. If they are not, you will not be able to commit your code. It will autofix your code on commit and give you a diff. False positives can be added to the `._typos.toml` file.

Because we are using Pyright and Ruff, pre-commit should be very quick and barely noticeable, hence leading to a much better developer experience and higher code quality.

## Testing

We use pytest with `.conftest.py` and `lazy_fixture` to ensure test parameterization is easy [pytest parameterization](https://docs.pytest.org/en/7.3.x/how-to/parametrize.html). When developing a feature, please always have a test in mind. Feature branches will not be accepted without extensive testing.

Pytest can be run in parallel locally with the following command:

```sh
pytest --workers auto --tests-per-worker auto
```

These run on PR and pushes to `main` and `research` via a GitHub action `.github/workflows/python_app.yml`. This will run the tests in parallel on the GitHub runners.

## CI

The same pre-commit hooks are run in the CI via GitHub actions. These ensure local commits should pass the linting and type checking CI. All tests are run in CI. The CO workflows are in `.github/workflows/python_app.yml`.

