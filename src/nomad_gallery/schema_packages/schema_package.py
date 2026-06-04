from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

from nomad.datamodel.data import Schema
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.metainfo import MEnum, Quantity, SchemaPackage

# configuration = config.get_plugin_entry_point(
#    'nomad_gallery.schema_packages:schema_package_entry_point'
# )

m_package = SchemaPackage()


class GalleryEntry(Schema):
    """
    A schema for describing an entry in the NOMAD Gallery, showcasing features,
    examples, and use cases.
    """

    # 1. Basic Info & Research Field
    name = Quantity(
        type=str,
        description='Title of the Gallery Entry',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
    )

    research_field = Quantity(
        type=str,
        description=' The specific scientific domain\
              (e.g., Battery Science, Catalysis).',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
    )

    description = Quantity(
        type=str,
        description='Project description, research question,\
              and how NOMAD was integrated.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.RichTextEditQuantity),
    )

    # 2. Affiliation / Institution
    institution = Quantity(
        type=str,
        description='Name of the institution or research center.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
    )

    country = Quantity(
        type=str,
        description='Country of the institution.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
    )

    # 3. Authors (Coauthors)
    # Note: The main creator is automatically tracked by NOMAD metadata.
    coauthors = Quantity(
        type=str,
        shape=['*'],
        description='List of coauthors involved in the project.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
    )

    # 4. Methodology
    methodology_type = Quantity(
        type=MEnum('Computational', 'Experimental', 'Mixed/Hybrid'),
        description='Whether the work is primarily\
              computational, experimental, or both.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.EnumEditQuantity),
    )

    technique = Quantity(
        type=str,
        description='Specific experimental or computational techniques used.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
    )

    # 5. Data Metadata
    data_size = Quantity(
        type=str,
        description='Approximate size of the dataset (e.g., "50 GB").',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
    )

    keywords = Quantity(
        type=str,
        shape=['*'],
        description='Keywords or tags (e.g., AI, NeXus, Perovskite).',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
    )

    # 6. Publications, Repositories & Funding
    publication_references = Quantity(
        type=str,
        shape=['*'],
        description='DOIs or links to related publications.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
    )

    repository_references = Quantity(
        type=str,
        shape=['*'],
        description='Links to related source repositories.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
    )

    funding_references = Quantity(
        type=str,
        shape=['*'],
        description='Grant numbers or funding agency references.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
    )

    # 7. Metrics (Optional)
    estimated_active_users = Quantity(
        type=int,
        description='Estimated number of current active users (if applicable).',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )

    downloads = Quantity(
        type=int,
        description='Number of downloads (if applicable).',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )

    # 8. Media
    media_urls = Quantity(
        type=str,
        shape=['*'],
        description='Links to short videos, GIFs, or other media showcasing the tool.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)

        # Log the normalization for debugging
        logger.info('GalleryEntry.normalize', name=self.name)


m_package.__init_metainfo__()
