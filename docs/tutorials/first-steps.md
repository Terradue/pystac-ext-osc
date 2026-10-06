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

# Create a project and product

[Install the package](../how-to/install.md) before running this complete example. OSC represents projects and products as STAC Collections; product Items can carry the same OSC fields for discovery.

```python
import pystac
from pystac.extensions.osc import OscExtension, OscStatus

project = pystac.Collection(
    id="ocean-science",
    description="Ocean science research project",
    extent=pystac.Extent(
        pystac.SpatialExtent([[-180, -90, 180, 90]]),
        pystac.TemporalExtent([[None, None]]),
    ),
    license="proprietary",
)
OscExtension.ext(project, add_if_missing=True).apply_project(
    status=OscStatus.ONGOING,
    workflows=["ocean-workflow"],
)

product = pystac.Collection(
    id="ocean-temperature",
    description="Sea surface temperature product",
    extent=project.extent.clone(),
    license="CC-BY-4.0",
)
osc = OscExtension.ext(product, add_if_missing=True)
osc.apply_product(
    status=OscStatus.COMPLETED,
    project=project.id,
    region="Arctic",
    variables=["Sea surface temperature"],
    missions=["Sentinel-3"],
    experiment="experiment-42",
)
product.add_link(pystac.Link(
    rel="related",
    target="https://example.org/projects/ocean-science.json",
    media_type="application/json",
))

serialized = product.to_dict()
assert serialized["osc:project"] == project.id
assert OscExtension.get_schema_uri() in serialized["stac_extensions"]
restored = pystac.Collection.from_dict(serialized)
assert OscExtension.ext(restored).variables == ["Sea surface temperature"]
```

Collection OSC fields are top-level members; Item OSC fields live in `properties`. Use `OscExtension.ext(object)` explicitly: the package does not install an `object.ext.osc` shortcut.

Serialization does not validate a document. See [validation boundaries](../explanation/architecture.md#validation-boundaries).
