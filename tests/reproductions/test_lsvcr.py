from auto_research.reproductions.lsvcr.data import JointData, JointRow, instruction


def test_joint_instruction_contains_both_histories():
    data = JointData((), (), ("item a", "item b"), ("comment a", "comment b"))
    row = JointRow((0, 1), (0, 1), 1, 1)
    prompt = instruction(data, row, "comment")
    assert "item a" in prompt and "comment a" in prompt
    assert prompt.endswith("next comment:")
