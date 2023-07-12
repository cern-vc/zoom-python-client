from typing_extensions import NotRequired, TypedDict

from zoom_python_client.utils.typed_dict_parameters import generate_parameters_dict


class _TestListDict(TypedDict):
    type: NotRequired[str]
    page_size: NotRequired[int]
    next_page_token: NotRequired[str]
    page_number: NotRequired[int]
    from_date: NotRequired[str]
    to_date: NotRequired[str]


def test_generate_params_dict():
    data = _TestListDict(type="test", page_number=1, page_size=10)
    parameters = generate_parameters_dict(data)
    assert parameters == {"type": "test", "page_size": 10, "page_number": 1}


def test_generate_params_dict_with_to_date():
    data = _TestListDict(to_date="2021-01-01T00:00:00Z")
    parameters = generate_parameters_dict(data)
    assert parameters == {"to": "2021-01-01T00:00:00Z"}


def test_generate_params_dict_with_from_date():
    data = _TestListDict(from_date="2021-01-01T00:00:00Z")
    parameters = generate_parameters_dict(data)
    assert parameters == {"from": "2021-01-01T00:00:00Z"}
