from auto_research.runtime import runtime_summary


class _Device:
    type = "cpu"

    def __str__(self):
        return "cpu"


class _Cuda:
    @staticmethod
    def is_available():
        return False


class _MPS:
    @staticmethod
    def is_available():
        return False


class _Backends:
    mps = _MPS()


class _Torch:
    __version__ = "2.7.0+internal.build"
    cuda = _Cuda()
    backends = _Backends()

    @staticmethod
    def device(value):
        return _Device()

    @staticmethod
    def set_num_threads(value):
        return None


def test_runtime_summary_omits_internal_build_and_os_release(monkeypatch):
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr("platform.machine", lambda: "x86_64")
    result = runtime_summary(_Torch())
    assert result["platform"] == "Linux x86_64"
    assert result["torch_version"] == "2.7.0"
    assert "internal" not in str(result)
