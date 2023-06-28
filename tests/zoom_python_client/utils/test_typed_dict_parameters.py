from typing_extensions import NotRequired, TypedDict

from zoom_python_client.utils.typed_dict_parameters import generate_parms_dict


class TestListDict(TypedDict):
    type: NotRequired[str]
    page_size: NotRequired[int]
    next_page_token: NotRequired[str]
    page_number: NotRequired[int]
    from_date: NotRequired[str]
    to_date: NotRequired[str]


def test_generate_params_dict():
    data = TestListDict(type="test", page_number=1, page_size=10)
    parameters = generate_parms_dict(data)
    assert parameters == {"type": "test", "page_size": 10, "page_number": 1}
