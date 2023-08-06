from queenbee.schema.function import Function
import yaml
import pytest
import warnings
from pydantic.error_wrappers import ValidationError


def test_load_function():
    fp = './tests/assets/function.yaml'
    Function.from_file(fp)


def test_load_function_with_int_input():
    fp = './tests/assets/function_int_input.yaml'
    fn = Function.from_file(fp)
    assert fn.inputs.parameters[1].value == 250


def test_load_illegal_input():
    fp = './tests/assets/function_illegal_input.yaml'

    with pytest.raises(AssertionError):
        f = Function.from_file(fp)
        f.validate_all()


def test_load_workflow_input():
    fp = './tests/assets/function_workflow_reference.yaml'

    with warnings.catch_warnings(record=True) as catcher:
        warnings.simplefilter('always')
        f = Function.from_file(fp)
        f.validate_all()
        assert len(catcher) == 1  # there was a warning
        assert 'workflow.parameters.sky-file' in str(catcher[0].message)
