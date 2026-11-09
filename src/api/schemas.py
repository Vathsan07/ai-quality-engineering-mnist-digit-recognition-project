from pydantic import BaseModel, Field, field_validator
import math


class PredictionRequest(BaseModel):

    image: list[list[float]] = Field(
        ...,
        description="28x28 grayscale image with pixel values between 0 and 1"
    )

    @field_validator("image")
    @classmethod
    def validate_image(cls, image):

        if len(image) != 28:
            raise ValueError("Image must contain exactly 28 rows")

        for row_index, row in enumerate(image):

            if len(row) != 28:
                raise ValueError(
                    f"Row {row_index} must contain exactly 28 pixels"
                )

            for value in row:

                if not math.isfinite(value):
                    raise ValueError("Pixel values must be finite numbers")

                if value < 0 or value > 1:
                    raise ValueError(
                        "Pixel values must be between 0 and 1"
                    )

        return image


class PredictionResponse(BaseModel):

    predicted_digit: int = Field(ge=0, le=9)
    confidence: float = Field(ge=0, le=1)
    processing_time_ms: float = Field(ge=0)