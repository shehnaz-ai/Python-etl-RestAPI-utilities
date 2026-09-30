class DataQualityError(Exception):
    """Base exception for data quality failures."""


class SchemaValidationError(DataQualityError):
    """Raised when the input schema is invalid."""


class ETLError(Exception):
    """Base exception for the ETL utilities library."""
    
class DataValidationError(DataQualityError):
    """Raised when data validation fails."""

class ConfigurationError(ETLError):
    """Raised when ETL configuration is invalid."""


class DataValidationError(ETLError):
    """Raised when data fails validation."""


class DataTransformationError(ETLError):
    """Raised when a transformation fails."""


class DataIngestionError(ETLError):
    """Raised when source data cannot be ingested."""


class DataLoadingError(ETLError):
    """Raised when data cannot be written to the target."""


class PipelineExecutionError(ETLError):
    """Raised when a pipeline execution fails."""