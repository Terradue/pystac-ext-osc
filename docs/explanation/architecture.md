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

The distribution is `pystac-ext-osc`. Import OSC wrappers from `pystac.extensions.osc`. The wheel excludes the shared namespace initializer owned by PySTAC.

`OscExtension.ext()` chooses a Catalog, Collection, or Item wrapper. It writes directly into the object's existing metadata dictionary. It does not register an `.ext.osc` accessor. `OSC_EXTENSION_HOOKS` declares the v1.0.0 schema, no previous extension identifiers, and Catalog/Collection/Item types; registration with a migration system is left to callers.

The published OSC v1.0.0 schema and upstream main schema were compared on 2026-10-06 and were identical. The implemented project/product field set matches them. Source: [OSC specification](https://github.com/stac-extensions/osc).

## Validation boundaries

Neither OSC apply methods nor serialization runs JSON Schema validation. Apply methods mutate fields sequentially and clear omitted optional values. They do not provide transactional updates or create related links.

For STAC validation, install `pystac[validation]` and call the STAC object's `validate()`. Schema retrieval may require network access or an application-configured schema cache.
