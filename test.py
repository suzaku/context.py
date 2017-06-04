import pytest

from context import new_context, cur_context


def test_can_access_vars_in_context(mocker):
    func_called_by_inner = mocker.Mock()

    def outter():
        with new_context() as ctx:
            ctx.value = 42
            inner()

    def inner():
        func_called_by_inner(cur_context.value)

    outter()
    func_called_by_inner.assert_called_with(42)


def test_should_raise_AttributeError_if_accessed_outside_context(mocker):
    func_called_outside_context = mocker.Mock()
    with pytest.raises(AttributeError):
        func_called_outside_context(cur_context.value)


def test_can_check_if_attr_exists():
    assert not hasattr(cur_context, 'value')
    with new_context(value=1984):
        assert hasattr(cur_context, 'value')
        assert not hasattr(cur_context, 'other')


def test_contexts_can_be_nested():
    with new_context(a='whatever'):
        assert cur_context.a == 'whatever'
        assert not hasattr(cur_context, 'b')
        with new_context(a='otherwise', b=1984):
            assert cur_context.a == 'otherwise'
            assert cur_context.b == 1984
