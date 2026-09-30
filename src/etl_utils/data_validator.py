import pandas as pd


from etl_utils.exceptions import (SchemaValidationError)

class DataQualityValidator:
    """Reusable DataFrame validation framework."""
    def __init__(self, df):
        self.df = df.copy()

        self.valid_mask = pd.Series(
            True, index=self.df.index
        )

        self.errors = {}

        self.df["rejection_reasons"] = ""

    def _add_rejection_reason(self, mask, reason):
        self.df.loc[mask, "rejection_reasons"] = (
            self.df.loc[mask, "rejection_reasons"]
            .apply(
                lambda existing: (
                    f"{existing},{reason}"
                    if existing else reason
                )
            )
        )

    def validate_columns(self, required_columns: list[str]) :
        """Validate that the DataFrame contains the required columns."""
        missing = [
            col for col in required_columns
            if col not in self.df.columns
        ]
        if missing:
            raise SchemaValidationError(
                f"Missing required columns: {missing}"
            )
        return True

    def validate_required_columns(self,columns: list[str]) -> list[str]:
        """
        Return columns that are missing from the DataFrame.

        Returns:
            list[str]: Missing column names.
        """
        return [
            column
            for column in columns
            if column not in self.df.columns
        ]



    def validate_not_null(self, columns):
        for column in columns:
            if column not in self.df.columns:
                raise ValueError(f"Column not found: {column}")

            invalid = self.df[column].isna()

            self.valid_mask &= ~invalid

            self._add_rejection_reason(
                invalid, "NULL_VALUE"
            )

            self.errors[f"not_null_{column}"] = int(
                invalid.sum()
            )
        return self


    def validate_duplicates(self, columns):
        if isinstance(columns, str):
            columns = [columns]

        invalid = self.df.duplicated(
            subset=columns,
            keep="first"
        )
        self.valid_mask &= ~invalid

        self.errors["duplicates"] = int(invalid.sum())

        return self

    def validate_email(self, column):
        if column not in self.df.columns:
            raise ValueError(f"Column not found: {column}")

        email_pattern = (
            r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        )

        invalid = (
                self.df[column].isna()
                | ~self.df[column].astype("string").str.match(
            email_pattern, na=False
        )
        )

        self.valid_mask &= ~invalid
        self.errors[f"email_{column}"] = int(invalid.sum())

        return self

    def validate_numeric_range(
            self, column, minimum=None, maximum=None
    ):
        if column not in self.df.columns:
            raise ValueError(f"Column not found: {column}")

        values = pd.to_numeric(
            self.df[column], errors="coerce"
        )

        invalid = values.isna()

        if minimum is not None:
            invalid |= values < minimum

        if maximum is not None:
            invalid |= values > maximum

        self.valid_mask &= ~invalid

        self._add_rejection_reason(
            invalid, "NUMERIC_RANGE"
        )

        self.errors[f"numeric_range_{column}"] = int(
            invalid.sum()
        )

        return self

    def validate_unique(self, columns):
        """Reject rows containing duplicate values in the specified columns."""
        if isinstance(columns, str):
            columns = [columns]

        missing = [
            col for col in columns
            if col not in self.df.columns
        ]

        if missing:
            raise ValueError(
                f"Columns not found: {missing}"
            )

        # Identify duplicate rows, keeping the first occurrence.
        duplicate_mask = self.df.duplicated(
            subset=columns,
            keep="first"
        )

        # Reject duplicate rows.
        self.valid_mask &= ~duplicate_mask

        # Record the rejection reason.
        self._add_rejection_reason(
            duplicate_mask,
            "DUPLICATE_VALUE"
        )

        self.errors["unique"] = int(
            duplicate_mask.sum()
        )

        return self

    def valdate_data_types(self,expected_types: dict):
        for column, expected_type in expected_types.items():
            if column not in self.df.columns:
                raise SchemaValidationError(
                    f"Column '{column}' does not exist in the DataFrame."
                )
            converted = self.df[column].map(
                lambda value: isinstance(value, expected_type)
                if pd.notna(value) else True
            )

            self._add_error(
                column,
                ~converted,
                "INVALID_DATA_TYPE"
            )

        return self

    def _add_error(self, column, mask, reason):
        mask = mask.fillna(False).astype(bool)

        for index in self.df.index[mask]:
            self.errors.setdefault(index, []).append(
                f"{column}:{reason}"
            )

    def get_results(self):
        valid = self.df.loc[self.valid_mask].copy()
        rejected = self.df.loc[~self.valid_mask].copy()

        summary = {
            "total_records": len(self.df),
            "valid_records": len(valid),
            "rejected_records": len(rejected),
            "validation_errors": self.errors.copy(),
        }

        return valid, rejected, summary