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

# OSC fields

These accessors belong to `OscExtension`. Catalogs and Collections store fields at the top level; Items store them in `properties`.

| JSON field | Python property | Applies to | Contract |
| --- | --- | --- | --- |
| `osc:type` | `osc_type` | Both | Required: `OscType.PROJECT` or `OscType.PRODUCT`. |
| `osc:status` | `status` | Both | Required: `OscStatus.PLANNED`, `ONGOING`, or `COMPLETED`. |
| `osc:workflows` | `workflows` | Project | Optional list of workflow names. |
| `osc:project` | `project` | Product | Required project name. |
| `osc:region` | `region` | Product | Optional geographic region name. |
| `osc:variables` | `variables` | Product | Optional list of observed variable names. |
| `osc:missions` | `missions` | Product | Optional list of input mission names. |
| `osc:experiment` | `experiment` | Product | Optional generating experiment name. |

The [v1.0.0 schema](https://stac-extensions.github.io/osc/v1.0.0/schema.json) requires nonempty strings for names and list entries, permits empty lists, and rejects unknown `osc:` fields. Project and product fields cannot be mixed. Non-OSC fields remain permitted by the extension schema.

All getters allow missing values; all setters accept `None` to remove a field. Enum getters raise `ValueError` for unrecognized stored enum strings. The wrapper does not enforce every schema constraint: string/list setters do not validate nonempty values, and individual setters can create an invalid combination. Call STAC validation separately.

## Related metadata

`themes` and project `contacts` belong to separate extensions. `related` links connect referenced entities. Variables themselves use themes and related links without OSC fields. Workflows and experiments use [OGC Records](ogc-records.md), with `osc:project` or `osc:workflow` in their properties; they are not additional `OscType` values.
