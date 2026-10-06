# Copyright 2026 Terradue
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Implements the :stac-ext:`Open Science Catalog Extension <osc>`."""

from __future__ import annotations

from typing import Any, ClassVar, Generic, Literal, TypeVar, cast

from pystac.extensions.base import ExtensionManagementMixin, PropertiesExtension
from pystac.extensions.hooks import ExtensionHooks
from pystac.utils import StringEnum

import pystac

#: Generalized version of :class:`~pystac.Catalog`, :class:`~pystac.Collection`,
#: or :class:`~pystac.Item`
T = TypeVar("T", pystac.Catalog, pystac.Collection, pystac.Item)

SCHEMA_URI: str = "https://stac-extensions.github.io/osc/v1.0.0/schema.json"
PREFIX: str = "osc:"

TYPE_PROP: str = PREFIX + "type"
STATUS_PROP: str = PREFIX + "status"
WORKFLOWS_PROP: str = PREFIX + "workflows"
PROJECT_PROP: str = PREFIX + "project"
REGION_PROP: str = PREFIX + "region"
VARIABLES_PROP: str = PREFIX + "variables"
MISSIONS_PROP: str = PREFIX + "missions"
EXPERIMENT_PROP: str = PREFIX + "experiment"


class OscType(StringEnum):
    """The supported Open Science Catalog resource types."""

    PROJECT = "project"
    PRODUCT = "product"


class OscStatus(StringEnum):
    """The supported lifecycle states for OSC projects and products."""

    PLANNED = "planned"
    ONGOING = "ongoing"
    COMPLETED = "completed"


class OscExtension(
    Generic[T],
    PropertiesExtension,
    ExtensionManagementMixin[pystac.Catalog | pystac.Collection | pystac.Item],
):
    """The Open Science Catalog Extension for Catalogs, Collections, and Items."""

    name: Literal["osc"] = "osc"

    def apply_project(
        self,
        *,
        status: OscStatus,
        workflows: list[str] | None = None,
    ) -> None:
        """Apply the OSC project fields and remove product-only fields."""
        self.osc_type = OscType.PROJECT
        self.status = status
        self.workflows = workflows

        self.project = None
        self.region = None
        self.variables = None
        self.missions = None
        self.experiment = None

    def apply_product(
        self,
        *,
        status: OscStatus,
        project: str,
        region: str | None = None,
        variables: list[str] | None = None,
        missions: list[str] | None = None,
        experiment: str | None = None,
    ) -> None:
        """Apply the OSC product fields and remove project-only fields."""
        self.osc_type = OscType.PRODUCT
        self.status = status
        self.project = project
        self.region = region
        self.variables = variables
        self.missions = missions
        self.experiment = experiment

        self.workflows = None

    @property
    def osc_type(self) -> OscType | None:
        """The OSC resource type."""
        value = self._get_property(TYPE_PROP, str)
        return OscType(value) if value is not None else None

    @osc_type.setter
    def osc_type(self, value: OscType | None) -> None:
        self._set_property(TYPE_PROP, value.value if value is not None else None)

    @property
    def status(self) -> OscStatus | None:
        """The OSC lifecycle status."""
        value = self._get_property(STATUS_PROP, str)
        return OscStatus(value) if value is not None else None

    @status.setter
    def status(self, value: OscStatus | None) -> None:
        self._set_property(STATUS_PROP, value.value if value is not None else None)

    @property
    def workflows(self) -> list[str] | None:
        """The workflows created by an OSC project."""
        return self._get_property(WORKFLOWS_PROP, list[str])

    @workflows.setter
    def workflows(self, value: list[str] | None) -> None:
        self._set_property(WORKFLOWS_PROP, value)

    @property
    def project(self) -> str | None:
        """The project associated with an OSC product."""
        return self._get_property(PROJECT_PROP, str)

    @project.setter
    def project(self, value: str | None) -> None:
        self._set_property(PROJECT_PROP, value)

    @property
    def region(self) -> str | None:
        """The geographic region associated with an OSC product."""
        return self._get_property(REGION_PROP, str)

    @region.setter
    def region(self, value: str | None) -> None:
        self._set_property(REGION_PROP, value)

    @property
    def variables(self) -> list[str] | None:
        """The variables observed by an OSC product."""
        return self._get_property(VARIABLES_PROP, list[str])

    @variables.setter
    def variables(self, value: list[str] | None) -> None:
        self._set_property(VARIABLES_PROP, value)

    @property
    def missions(self) -> list[str] | None:
        """The missions providing input to an OSC product."""
        return self._get_property(MISSIONS_PROP, list[str])

    @missions.setter
    def missions(self, value: list[str] | None) -> None:
        self._set_property(MISSIONS_PROP, value)

    @property
    def experiment(self) -> str | None:
        """The experiment that created an OSC product."""
        return self._get_property(EXPERIMENT_PROP, str)

    @experiment.setter
    def experiment(self, value: str | None) -> None:
        self._set_property(EXPERIMENT_PROP, value)

    @classmethod
    def get_schema_uri(cls) -> str:
        """Return the supported OSC extension schema identifier."""
        return SCHEMA_URI

    @classmethod
    def ext(cls, obj: T, add_if_missing: bool = False) -> OscExtension[T]:
        """Wrap a Catalog, Collection, or Item with live OSC accessors.

        Args:
            obj: Object whose OSC fields will be read or modified.
            add_if_missing: Add the schema declaration when absent.

        Raises:
            pystac.ExtensionNotImplemented: If the declaration is missing and
                adding it was not requested.
            pystac.ExtensionTypeError: If the object type is unsupported.
        """
        if isinstance(obj, pystac.Collection):
            cls.ensure_has_extension(obj, add_if_missing)
            return cast("OscExtension[T]", CollectionOscExtension(obj))
        if isinstance(obj, pystac.Catalog):
            cls.ensure_has_extension(obj, add_if_missing)
            return cast("OscExtension[T]", CatalogOscExtension(obj))
        if isinstance(obj, pystac.Item):
            cls.ensure_has_extension(obj, add_if_missing)
            return cast("OscExtension[T]", ItemOscExtension(obj))
        raise pystac.ExtensionTypeError(cls._ext_error_message(obj))


class CatalogOscExtension(OscExtension[pystac.Catalog]):
    """Expose OSC fields on a PySTAC catalog."""

    catalog: pystac.Catalog
    properties: dict[str, Any]

    def __init__(self, catalog: pystac.Catalog) -> None:
        self.catalog = catalog
        self.properties = catalog.extra_fields

    def __repr__(self) -> str:
        return f"<CatalogOscExtension Catalog id={self.catalog.id}>"


class CollectionOscExtension(OscExtension[pystac.Collection]):
    """Expose OSC fields on a PySTAC collection."""

    collection: pystac.Collection
    properties: dict[str, Any]

    def __init__(self, collection: pystac.Collection) -> None:
        self.collection = collection
        self.properties = collection.extra_fields

    def __repr__(self) -> str:
        return f"<CollectionOscExtension Collection id={self.collection.id}>"


class ItemOscExtension(OscExtension[pystac.Item]):
    """Expose OSC fields on a PySTAC item."""

    item: pystac.Item
    properties: dict[str, Any]

    def __init__(self, item: pystac.Item) -> None:
        self.item = item
        self.properties = item.properties

    def __repr__(self) -> str:
        return f"<ItemOscExtension Item id={self.item.id}>"


class OscExtensionHooks(ExtensionHooks):
    """Describe OSC schema membership for PySTAC migration hooks."""

    schema_uri: str = SCHEMA_URI
    prev_extension_ids: ClassVar[set[str]] = set()
    stac_object_types: ClassVar[set[pystac.STACObjectType]] = {
        pystac.STACObjectType.CATALOG,
        pystac.STACObjectType.COLLECTION,
        pystac.STACObjectType.ITEM,
    }


OSC_EXTENSION_HOOKS: ExtensionHooks = OscExtensionHooks()
