from nomad.config.models.plugins import SchemaPackageEntryPoint
from pydantic import Field

from nomad_gallery.schema_packages.schema_package import m_package


class NewSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        return m_package


schema_package_entry_point = NewSchemaPackageEntryPoint(
    name='NewSchemaPackage',
    description='New schema package entry point configuration.',
)
