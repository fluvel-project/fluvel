# Contributing to Fluvel
Fluvel is a newly launched project. Many parts of the systems that make up the architecture are still being defined.

For Fluvel's core, we opted for a systemic approach. We don't view modules as mere scripts or isolated algorithms, but as integral components of a **coherent**, **efficient**, **linear**, and **deterministic** system.

If you'd like to help, here's how we're handling it:

## Development and Pull Requests
Given the critical nature of the architecture, development is governed by the following principles:

* **Prior Discussion**: Before making structural changes to the core, open an issue to discuss the systemic impact.

* **Atomic Modularity**: Contributions must respect the hierarchy of abstract models. Modules must be independent but integral to the system.

* **Technical Documentation**: Fluvel does not exist without its documentation. Any changes to the logic of **Pyro** or **Fluml** must be reflected in the technical manuals at `docs/md/`.

## Integrity Rules
* **Predictability**: The code must be deterministic. We avoid "magical" behaviors or hidden side effects that break the linearity of the data flow.

* **Style**: We follow PEP 8, but prioritize clarity of intent to improve DX over code brevity, especially in APIs for end users.

* **License**: By contributing, you agree that your code will be distributed under the terms of the **LGPL-3.0** license.
