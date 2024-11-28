import json
import pathlib
from typing import Any, Protocol, runtime_checkable

import pandas as pd
from attrs import field, frozen

from ref_core.constraints import GroupConstraint
from ref_core.datasets import FacetFilter, SourceDatasetType


@frozen
class Configuration:
    """
    Configuration that describes the input data sources
    """

    output_directory: pathlib.Path
    """
    Directory to write output files to
    """

    # TODO: Add more configuration options here


@frozen
class MetricResult:
    """
    The result of running a metric.

    The content of the result follows the Earth System Metrics and Diagnostics Standards
    ([EMDS](https://github.com/Earth-System-Diagnostics-Standards/EMDS/blob/main/standards.md)).
    """

    # Do we want to load a serialised version of the output bundle here or just a file path?

    output_bundle: pathlib.Path | None
    """
    Path to the output bundle file.

    The contents of this file are defined by
    [EMDS standard](https://github.com/Earth-System-Diagnostics-Standards/EMDS/blob/main/standards.md#common-output-bundle-format-)
    """
    successful: bool
    """
    Whether the metric ran successfully.
    """
    # Log info is in the output bundle file already, but is definitely useful

    @staticmethod
    def build(configuration: Configuration, cmec_output_bundle: dict[str, Any]) -> "MetricResult":
        """
        Build a MetricResult from a CMEC output bundle.

        Parameters
        ----------
        configuration
            The configuration used to run the metric.
        cmec_output_bundle
            An output bundle in the CMEC format.

            TODO: This needs a better type hint

        Returns
        -------
        :
            A prepared MetricResult object.
            The output bundle will be written to the output directory.
        """
        with open(configuration.output_directory / "output.json", "w") as file_handle:
            json.dump(cmec_output_bundle, file_handle)
        return MetricResult(
            output_bundle=configuration.output_directory / "output.json",
            successful=True,
        )


@frozen
class TriggerInfo:
    """
    The reason why the metric was run.
    """

    dataset: pathlib.Path
    """
    Path to the dataset that triggered the metric run.
    """

    # TODO:
    # Add/remove/modified?
    # dataset metadata


@frozen(hash=True)
class DataRequirement:
    """
    Definition of the input datasets that a metric requires to run.

    This is used to create a groups of datasets.
    Each group will be result in an execution of a metric
    and defines the input data for that execution.

    The data catalog is filtered according to the `filters` field,
    then grouped according to the `group_by` field,
    and then each group is checked that it satisfies the `constraints`.
    Each such group will be processed as a separate execution of the metric.
    """

    source_type: SourceDatasetType
    """
    Type of the source dataset (CMIP6, CMIP7 etc)
    """

    filters: tuple[FacetFilter, ...]
    """
    Filters to apply to the data catalog of datasets.

    This is used to reduce the set of datasets to only those that are required by the metric.
    Each filter is applied iterative to a set of datasets to reduce the set of datasets.
    """

    group_by: tuple[str, ...] | None
    """
    The fields to group the datasets by.

    This groupby operation is performed after the data catalog is filtered according to `filters`.
    Each group will contain a unique combination of values from the metadata fields,
    and will result in a separate execution of the metric.
    If `group_by=None`, all datasets will be processed together as a single execution.
    """

    constraints: tuple[GroupConstraint, ...] = field(factory=tuple)
    """
    Constraints that must be satisfied when executing a given metric run

    All of the constraints must be satisfied for a given group to be run.
    Each filter is applied iterative to a set of datasets to reduce the set of datasets.
    This is effectively an AND operation.
    """

    def apply_filters(self, data_catalog: pd.DataFrame) -> pd.DataFrame:
        """
        Apply filters to a DataFrame-based data catalog.

        Parameters
        ----------
        data_catalog
            DataFrame to filter.
            Each column contains a facet

        Returns
        -------
        :
            Filtered data catalog
        """
        for facet_filter in self.filters:
            for facet, value in facet_filter.facets.items():
                clean_value = value if isinstance(value, tuple) else (value,)

                mask = data_catalog[facet].isin(clean_value)
                if not facet_filter.keep:
                    mask = ~mask

                data_catalog = data_catalog[mask]
        return data_catalog


@runtime_checkable
class Metric(Protocol):
    """
    Interface for the calculation of a metric.

    This is a very high-level interface to provide maximum scope for the metrics packages
    to have differing assumptions.
    The configuration and output of the metric should follow the
    Earth System Metrics and Diagnostics Standards formats as much as possible.

    A metric can be executed multiple times,
    each time targeting a different group of input data.
    The groups are determined using the grouping the data catalog according to the `group_by` field
    in the `DataRequirement` object using one or more metadata fields.
    Each group must conform with a set of constraints,
    to ensure that the correct data is available to run the metric.
    Each group will then be processed as a separate execution of the metric.

    See (ref_example.example.ExampleMetric)[] for an example implementation.
    """

    name: str
    """
    Name of the metric being run

    This should be unique for a given provider,
    but multiple providers can implement the same metric.
    """

    data_requirements: tuple[DataRequirement, ...]
    """
    Description of the required datasets for the current metric

    This information is used to filter the a data catalog of both CMIP and/or observation datasets
    that are required by the metric.

    Any modifications to the input data will new metric calculation.
    """

    def run(self, configuration: Configuration, trigger: TriggerInfo | None) -> MetricResult:
        """
        Run the metric on the given configuration.

        The implementation of this method method is left to the metrics providers.

        A CMEC-compatible package can use: TODO: Add link to CMEC metric wrapper

        Parameters
        ----------
        configuration : Configuration
            The configuration to run the metric on.
        trigger : TriggerInfo | None
            Optional information about the dataset that triggered the metric run.

        Returns
        -------
        MetricResult
            The result of running the metric.
        """
