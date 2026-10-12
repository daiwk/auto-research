"""L0 cache identity/content checks, not checkpoint capability evidence."""
import hashlib
import pytest
from auto_research.agent_research.oct12_provenance import verify_local_checkpoint


def test_local_revision_is_verified_against_original_download_etags(tmp_path):
    revision = "a"*40
    metadata = tmp_path/".cache/huggingface/download"
    metadata.mkdir(parents=True)
    for name,content in (("config.json",b"{}"),("tokenizer_config.json",b"{}"),
                         ("model.safetensors",b"L0 bytes, not a real model")):
        (tmp_path/name).write_bytes(content)
        digest = hashlib.sha256(content).hexdigest()
        (metadata/(name+".metadata")).write_text(revision+"\n"+digest+"\n0\n")
    result = verify_local_checkpoint(tmp_path,"L0/fixture",revision)
    assert result["immutable_revision_verified"] and result["trust_remote_code"] is False
    assert result["revision"] == revision
    (tmp_path/"model.safetensors").write_bytes(b"tampered")
    with pytest.raises(ValueError,match="mismatch"):
        verify_local_checkpoint(tmp_path,"L0/fixture",revision)
    with pytest.raises(ValueError,match="immutable"):
        verify_local_checkpoint(tmp_path,"L0/fixture","main")
