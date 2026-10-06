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

# Work with OSC metadata

These examples continue from the product Collection in the [tutorial](../tutorials/first-steps.md).

## Update and clear fields

```python
osc = OscExtension.ext(product)
osc.region = "Agulhas"
osc.experiment = None
assert "osc:experiment" not in product.extra_fields
```

`ext()` requires the OSC schema declaration. Pass `add_if_missing=True` to add it. Getters return `None` for absent fields, and assigning `None` removes a field. Removing required fields leaves an incomplete document.

## Change resource type

```python
osc.apply_project(status=OscStatus.PLANNED, workflows=["new-workflow"])
assert "osc:project" not in product.extra_fields
osc.apply_product(status=OscStatus.ONGOING, project="ocean-science")
assert "osc:workflows" not in product.extra_fields
```

Both apply methods replace their supported fields: omitted optional arguments clear existing values. `apply_project()` removes product-only fields; `apply_product()` removes project workflows. Individual setters do not enforce these relationships.

## Attach themes, contacts, and links

Themes and contacts use their own STAC extensions, not `osc:` fields. Use the respective PySTAC extension APIs and declare their schemas when adding them. OSC uses theme concepts under `https://github.com/stac-extensions/osc#theme` by default. Project contacts use roles `technical_officer` and `consortium_member` where applicable.

Use `pystac.Link(rel="related", target=...)` for resources named in OSC metadata and themes. The wrapper does not create these links automatically. Projects can contain products as child Collections; products can contain other catalogs or data Items.

## Apply fields to Items and Catalogs

`OscExtension.ext()` also accepts Items and Catalogs. The same apply methods work on each; Item fields are written into `properties`, while Catalog and Collection fields are written into `extra_fields`. Mirror a product's metadata onto its Items explicitly when needed for search.

Assets, item asset definitions, and links are not OSC field targets. There is no OSC summaries helper. Upstream does not validate Collection summaries and recommends using the existing top-level Collection fields instead.

See the [upstream specification](https://github.com/stac-extensions/osc) and [field reference](../reference/fields.md).
