"""Utility for test_report_diff."""
import importlib
import pkgutil
import os


def get_processors() -> list:
    """Get all processors in processors directory"""
    lib_path: str = os.path.abspath(__file__)[: -len(os.path.basename(__file__))]
    return [name for _, name, _ in pkgutil.iter_modules([lib_path + 'processors'])]


def get_processor_class_by_report_type(report_type, processors: list) -> object:
    """Try to get processor class by the given report_type"""
    for processor in processors:
        mod = importlib.import_module(
            f".processors.{processor}", package="test_report_diff"
        )
        processor_class = getattr(mod, f'{report_type}', None)
        if processor_class is not None:
            return processor_class
