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

# Scope, architecture, and validation

## Package structure

The distribution is `pystac-ext-osc`. Import OSC wrappers from `pystac.extensions.osc` and the record adapter from `pystac.extensions.ogc_record`. The wheel excludes the shared namespace initializer owned by PySTAC.

`OscExtension.ext()` chooses a Catalog, Collection, or Item wrapper. It writes directly into the object's existing metadata dictionary. It does not register an `.ext.osc` accessor. `OSC_EXTENSION_HOOKS` declares the v1.0.0 schema, no previous extension identifiers, and Catalog/Collection/Item types; registration with a migration system is left to callers.

The published OSC v1.0.0 schema and upstream main schema were compared on 2026-10-06 and were identical. The implemented project/product field set matches them. Source: [OSC specification](https://github.com/stac-extensions/osc).

## OGC Records and STAC

`OGCRecord` subclasses `pystac.Item` to reuse links, assets, and compatible extension wrappers. It initializes `STACObject` directly to allow records without a STAC datetime. This dependency on PySTAC's object internals warrants testing when upgrading PySTAC.

Default serialization produces a Record GeoJSON Feature. STAC declarations and assets are preserved as foreign members when supplied. Use `OGCRecord.from_dict()` explicitly: ordinary PySTAC dispatch does not distinguish arbitrary records from STAC Items. `to_stac_item()` is an explicit conversion requiring a STAC instant or both interval endpoints. OGC `time` is independent and is never converted automatically.

## Validation boundaries

Neither OSC apply methods nor serialization runs JSON Schema validation. Apply methods mutate fields sequentially and clear omitted optional values. They do not provide transactional updates or create related links.

For STAC validation, install `pystac[validation]` and call the STAC object's `validate()`. Schema retrieval may require network access or an application-configured schema cache.

`OGCRecord.from_dict()` checks basic Feature structure, not full OGC conformance. The metadata accessors expose dictionaries and do not validate nested schemas. `record.validate(validator)` requires an explicit object exposing `validate(document)`, configured for the OGC schema and references. Calling it without a validator raises `ValueError`. For STAC validation use `record.to_stac_item().validate()`.

The adapter is an in-memory document interface, not an OGC API server, search client, or conformance certification. See [OGC Record reference](../reference/ogc-records.md).
