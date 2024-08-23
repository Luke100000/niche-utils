from niche_utils import FilesQueue


def test_file_list():
    file_list = FilesQueue()
    assert file_list.pop() is None
    file_list.push("test")
    file_list.set(["a", "b"])
    assert file_list.pop() == "b"
