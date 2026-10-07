"""Airlytics Services Layer.

Modular services for data loading, model inference, and SHAP explainability.
"""

from app.services.data_service import (
    AIRLINES,
    SOURCES,
    DESTINATIONS,
    ADDITIONAL_INFO_OPTIONS,
    STOP_OPTIONS,
    SOURCE_TO_CODE,
    DESTINATION_TO_CODE,
    CLEANED_DATA_PATH,
    ENGINEERED_DATA_PATH,
    load_reference_routes,
    load_reference_categories,
)
from app.services.model_service import (
    DEFAULT_MODEL_PATH,
    load_artifact,
    suggest_route,
    route_matches_cities,
    routes_for_city_pair,
    build_user_row,
    validate_stops_match_route,
    predict_fare,
)
from app.services.shap_service import (
    _group_transformed_columns,
    local_shap_contributions,
    plot_contributions,
)

__all__ = [
    "AIRLINES",
    "SOURCES",
    "DESTINATIONS",
    "ADDITIONAL_INFO_OPTIONS",
    "STOP_OPTIONS",
    "SOURCE_TO_CODE",
    "DESTINATION_TO_CODE",
    "CLEANED_DATA_PATH",
    "ENGINEERED_DATA_PATH",
    "load_reference_routes",
    "load_reference_categories",
    "DEFAULT_MODEL_PATH",
    "load_artifact",
    "suggest_route",
    "route_matches_cities",
    "routes_for_city_pair",
    "build_user_row",
    "validate_stops_match_route",
    "predict_fare",
    "_group_transformed_columns",
    "local_shap_contributions",
    "plot_contributions",
]
