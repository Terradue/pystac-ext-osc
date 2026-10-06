<!--
Copyright 2026 Terradue

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# Open Science Catalog PySTAC extension

`pystac-ext-osc` provides `OscExtension` for project and product metadata on PySTAC Catalogs, Collections, and Items, and `OGCRecord` for OGC API Records documents.

The OSC wrapper targets [OSC v1.0.0](https://github.com/stac-extensions/osc) and declares `https://stac-extensions.github.io/osc/v1.0.0/schema.json`. The package version is independent of the specification version.

```bash
python -m pip install pystac-ext-osc
```

- [Create a project and product](tutorials/first-steps.md).
- [Update OSC metadata and links](how-to/use-extension.md).
- [Create workflow and experiment records](how-to/ogc-records.md).
- [Look up OSC fields](reference/fields.md) and [OGC Record behavior](reference/ogc-records.md).
- [Browse the Python API](reference/api.md).
- [Understand architecture and validation](explanation/architecture.md).
