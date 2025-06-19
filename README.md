⚠️ *Archived Repository*


This repository has been archived and is no longer actively maintained. No further updates will be made. To learn more about Riverlane's products for Quantum Error Correction, visit [riverlane.com](riverlane.com).

Feel free to fork Aqueduct if you find it useful!


# PyAqueduct: Aqueduct Python Client Library

[![Automated release](https://github.com/AqueductHub/pyaqueduct/actions/workflows/automated_release.yaml/badge.svg)](https://github.com/AqueductHub/pyaqueduct/actions/workflows/automated_release.yaml)
[![Tests](https://github.com/AqueductHub/pyaqueduct/actions/workflows/static_analysis_and_tests.yaml/badge.svg)](https://github.com/AqueductHub/pyaqueduct/actions/workflows/static_analysis_and_tests.yaml)
[![pages-build-deployment](https://github.com/AqueductHub/pyaqueduct/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/AqueductHub/pyaqueduct/actions/workflows/pages/pages-build-deployment)

Aqueduct is a versatile experiment management system designed to streamline and simplify quantum system administration. Automation, data management and a multi-user platform come together to facilitate demanding experimental activities, through an intuitive, consistent, open interface. With robust security features including role-based access control and authentication, Aqueduct ensures data integrity and accessibility throughout the experiment pipeline.

Aqueduct is an extensible platform, with a full API allowing connectivity with external systems, and an extensions SDK allowing extensions to expand core Aqueduct functionality in a flexible and secure way. This first version of Aqueduct contains data management tools that augment a lab’s existing data storage systems by tracking critical settings, raw data and processed data from experiments, keeping them organised and readily accessible. Through convenient features such as tagging, favouriting, archiving, and annotation of experimental data, we facilitate a smoother data workflow for all labs. Aqueduct’s software APIs make it possible to retrofit existing experiment scripts so that all the lab’s data, not just the data produced by Deltaflow.Control, can be saved and accessed in a single, centralized location.

This functionality is faciliated through 2 components: `aqueductcore` is  the server software that hosts the main application, web interface, and handles data storage. `pyaqueduct` is our python client which allows easy creation of experiments and upload of data and metadata for them.

## Installation

You can install PyAqueduct releases from PyPi:

```bash
pip install pyaqueduct
```

## Contributing

Aqueduct is an open-source project, and we greatly value all contributions. Contributions are not limited to coding; you can also help by filing issues to report bugs, enhancing our documentation, or requesting new features. We strongly recommend using the templates provided for each of these tasks. If you’re interested in contributing, please refer to our [contribution guide](/CONTRIBUTING.md) for more information. We really appreciate your consideration for contributing to Aqueduct.

## License

This project is licensed under the MIT License - see the [MIT](/LICENSE) file for details
