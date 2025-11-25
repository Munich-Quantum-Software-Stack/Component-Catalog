<!----------------------------------------------------------------------------
Copyright 2024 Munich Quantum Software Stack Project

Licensed under the Apache License, Version 2.0 with LLVM Exceptions (the
"License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at

https://github.com/Munich-Quantum-Software-Stack/Component-Catalog/blob/develop/LICENSE

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations under
the License.

SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
-------------------------------------------------------------------------- -->

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Munich-Quantum-Software-Stack/QDMI/develop/docs/_static/mqss_logo_dark.svg" width="20%">
    <img src="https://raw.githubusercontent.com/Munich-Quantum-Software-Stack/QDMI/develop/docs/_static/mqss_logo.svg" width="20%">
  </picture>
</p>

# MQSS Component Catalog

<p align="center"><a href="https://munich-quantum-software-stack.github.io/Component-Catalog/"><strong>View the Component Catalog</strong></a></p>

This repository provides the source code of the Component Catalog webpage, a collection of all
software components that are part of the Munich Quantum Software Stack (MQSS). Each component is
designed to work together seamlessly, offering comprehensive tools for quantum computing
development, simulation, and optimization.

As software tools are developed and maintained by different teams within the Munich Quantum Valles
(MQV), this catalog serves as a centralized resource for users to explore, understand, and utilize
the various components of the MQSS. At the same time, it provides maintainers with a platform to
showcase their work and facilitate collaboration across teams.

New components can be added easily through the GitHub interface without requiring a single line of
code. This allows for rapid expansion of the catalog as new tools and libraries are developed within
the MQV.

## Adding Components

To add a new component to the catalog, please follow these steps:

1. Open the "Issues" tab in this repository and click on "New Issue".
2. Select the "New Component Request" issue template.
3. Fill out the form with the necessary details about the component.
   - Some fields are mandatory (name, maintainers, etc.)
   - Other fields are optional but recommended (GitHub link, documentation link, etc.)
   - The field "Programming Languages" should include all programming languages the component is
     implemented in or supports.
   - The field "Built On" should include all frameworks (such as Qiskit) the component is built on
     or compatible with.
   - Make sure the details are correct, as further changes can only be made through pull requests.
4. Submit the issue. After review by the maintainers, the component will be added to the catalog.

## Updating Components

To update an existing component in the catalog, a pull request is required to edit the component's
details. Please follow these steps:

1. Fork the repository to your GitHub account.
2. Navigate to the `_components` directory and locate the Markdown file corresponding to the
   component you wish to update.
3. Make the necessary changes to the component's details in the Markdown file.
4. Commit your changes and push them to your forked repository.
5. Open a pull request from your forked repository to the main repository, describing the changes
   you made.
6. After review by the maintainers, your changes will be merged into the catalog.

## Feature Requests and Bug Reports

If you have any feature requests or encounter any bugs, please open an issue in the "Issues" tab.
Use the appropriate issue template to provide detailed information about your request or the bug you
encountered. This will help us address your concerns more effectively.

## Local build and preview

You can build and preview the site locally in a way that mirrors the CI workflow.

Prerequisites:

- uv installed and available in PATH
- Python 3.10 or newer
- Either Docker (recommended) or a local Jekyll installation

Steps:

- Optionally set a GitHub token to avoid rate limits when fetching star counts:
  - Linux/macOS: `export GITHUB_TOKEN=ghp_your_token`
- Run the local deploy helper:
  - `bash scripts/deploy_local.sh` # builds into ./\_site and serves on http://localhost:4000
  - Options:
    - `--port <PORT>` change the local server port (default 4000)
    - `--skip-fetch` skip the GitHub stars fetch step

Notes:

- The fetch script is executed via uv and targets Python >= 3.10.
- Building prefers Docker image `jekyll/jekyll:4` and falls back to `jekyll build` if Docker is not
  available.
