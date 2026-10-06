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

# Simplify the EarthCODE workflow example

The EarthCODE tutorial's [Create new workflow record section](https://esa-earthcode.github.io/tutorials/osc-pr-pystac/) builds a nested dictionary in `create_workflow_collection()`. With this package, you can create an `OGCRecord`, assign common metadata through named accessors, and use ordinary PySTAC links. You no longer need a helper whose responsibility is assembling the record's JSON envelope.

This tutorial uses illustrative workflow metadata and retains the source example's custom workflow properties. It also identifies the differences between preserving that example and claiming OGC conformance.

## 1. Install and create the record

[Install the package](../how-to/install.md), then run the following blocks in order. Creating the record needs no catalog checkout or network access.

```python
from datetime import datetime, timezone

import pystac
from pystac.extensions.ogc_record import OGCRecord
from pystac.utils import datetime_to_str

project_id = "crop-mapping"
workflow = OGCRecord(
    id="crop-mapping-workflow",
    properties={
        "osc:project": project_id,
        "osc:type": "workflow",
        "osc:status": "completed",
        "version": "1",
    },
)
workflow.type = "workflow"
workflow.title = "Crop mapping workflow"
workflow.description = "A reproducible workflow for mapping cropland."
workflow.license = "proprietary"
workflow.keywords = ["cropland", "classification"]
workflow.formats = [{"name": "openEO process graph"}]
workflow.created = workflow.updated = datetime_to_str(datetime.now(timezone.utc))

workflow.add_links([
    pystac.Link(
        rel="root", target="../../catalog.json",
        media_type="application/json", title="Open Science Catalog",
    ),
    pystac.Link(
        rel="parent", target="../catalog.json",
        media_type="application/json", title="Workflows",
    ),
    pystac.Link(
        rel="related", target=f"../../projects/{project_id}/collection.json",
        media_type="application/json", title="Project: Crop mapping",
    ),
])
```

The adapter supplies the Feature envelope and null geometry. Common properties use accessors such as `title`, `formats`, and `license`; custom fields remain explicit in `properties`. `pystac.Link` handles link serialization, including mapping `target` to JSON `href` and `media_type` to JSON `type`.

The timestamp is computed once using timezone-aware UTC. These metadata accessors store strings, so `datetime_to_str()` supplies the serialized timestamp. `created` and `updated` describe metadata timestamps; they do not supply a STAC Item `datetime`.

## 2. See what the API replaces

| Responsibility | Dictionary-based helper | Implemented API |
| --- | --- | --- |
| Feature envelope | Explicit `type`, `geometry`, `properties`, and `links` members | `OGCRecord(id=..., properties=...)` and `to_record_dict()` |
| Common metadata | Nested property-key assignments | `workflow.title`, `workflow.keywords`, `workflow.license`, etc. |
| Resource links | Handwritten link dictionaries | `pystac.Link` and `add_links()` |
| Optional metadata removal | Delete a nested key | Assign `None` to a common metadata accessor |
| Independent copy | Copy the document and manage nested state | `workflow.clone()` |
| Load existing JSON | Work directly with nested dictionaries | `OGCRecord.from_dict(document)` |

The main benefit is less document-assembly code and one consistent object API for creation, editing, copying, and serialization. Domain decisions remain yours: which project the workflow belongs to, which formats it uses, and where its links point.

## 3. Inspect and round-trip the result

```python
document = workflow.to_record_dict(transform_hrefs=False)
assert document["type"] == "Feature"
assert document["geometry"] is None
assert document["properties"]["title"] == workflow.title
assert document["properties"]["osc:project"] == project_id
assert "datetime" not in document["properties"]
assert "stac_version" not in document
assert document["links"][2]["href"] == (
    f"../../projects/{project_id}/collection.json"
)

restored = OGCRecord.from_dict(document)
assert restored.title == workflow.title
assert restored.to_record_dict(transform_hrefs=False) == document

working_copy = restored.clone()
working_copy.keywords = None
assert "keywords" not in working_copy.properties
assert restored.keywords == ["cropland", "classification"]
```

`transform_hrefs=False` preserves the link strings for this standalone example. Relative links are intended for a record at `workflows/<workflow-id>/record.json` inside the catalog checkout. Moving the JSON to another directory changes what those links resolve to.

## 4. Write a staging file

This block writes `workflow_record.json` in the current directory, replacing it if it already exists:

```python
import json
from pathlib import Path

output_path = Path("workflow_record.json")
output_path.write_text(
    json.dumps(workflow.to_record_dict(transform_hrefs=False), indent=2) + "\n",
    encoding="utf-8",
)
loaded = OGCRecord.from_dict(json.loads(output_path.read_text(encoding="utf-8")))
assert loaded.title == workflow.title
```

This is a staging artifact. Place it at the intended catalog location, add the catalog/project return links required by the contribution workflow, and run the catalog's validation before opening a pull request. The adapter does not perform those repository operations.

## Compatibility choices

This example deliberately makes the following choices explicit:

- **Resource type:** `workflow.type = "workflow"` adds `properties.type`; the top-level `type` remains `Feature`. The retained `osc:type`, `osc:status`, and `version` keys preserve the EarthCODE example's custom metadata. They are not evidence that the record satisfies the OSC STAC schema.
- **OSC scope:** upstream OSC describes workflows with `osc:project` and a `related` project link. Add `child` links when experiments exist. `OscType` only contains project and product; do not use `OscExtension.apply_project()` or `apply_product()` to construct a workflow, or declare their STAC schema for this record.
- **Conformance:** the source example includes a record-core `/req/` identifier. This tutorial omits `conformsTo` because constructing an object does not establish conformance. After verification, an applicable record-core conformance identifier is `http://www.opengis.net/spec/ogcapi-records-1/1.0/conf/record-core`, supplied through `conforms_to` or `workflow.conforms_to`. Conformance identifiers and `stac_extensions` serve different purposes.
- **Optional members:** `linkTemplates` is omitted when unused. Assign `workflow.link_templates = []` if a consumer expects an explicit empty list.
- **Extent:** the source helper accepts `workflow_extent` without using it. No equivalent unused argument is needed here. If the resource has spatial or temporal coverage, supply appropriate record `geometry`, `bbox`, or OGC `time` explicitly; a STAC Collection extent is not converted automatically.

These are documented differences, so the example is not a byte-for-byte replacement. See the [OSC specification](https://github.com/stac-extensions/osc#workflows-and-experiments-via-ogc-api---records) and [OGC Record Core requirements](https://docs.ogc.org/is/20-004r1/20-004r1.html#clause-record-core) for the contracts.

Neither setters nor serialization perform schema validation. `workflow.validate()` requires an explicit OGC validator; the catalog's additional contribution checks still apply. Continue with the [OGC Record reference](../reference/ogc-records.md) and [workflow/experiment guide](../how-to/ogc-records.md).
