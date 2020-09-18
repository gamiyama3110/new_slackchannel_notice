from handler import Channels


def test_channels_exists():
    assert Channels([0]).has_channels()


def test_channels_not_exists():
    assert not Channels([]).has_channels()


def test_channels_no_line():
    assert Channels([]).length() == 0


def test_channels_one_line():
    assert Channels([0]).length() == 1


def test_channels_two_lines():
    assert Channels([0, 1]).length() == 2
