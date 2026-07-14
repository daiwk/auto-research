from auto_research.reproductions.sessionrec.model import SessionRecConfig, load_kuairand_sessions


def test_kuairand_sessions_preserve_exposed_negatives(tmp_path):
    directory = tmp_path / "kuairand-pure" / "data"
    directory.mkdir(parents=True)
    path = directory / "log_standard_4_22_to_5_08_pure.csv"
    header = "user_id,video_id,date,hourmin,time_ms,is_click,is_like,is_follow,is_comment,is_forward,is_hate,long_view,play_time_ms,duration_ms,profile_stay_time,comment_stay_time,is_profile_enter,is_rand,tab\n"
    rows = []
    for session in range(4):
        timestamp = session * 3_600_000
        rows.append(f"0,{session * 2},20220422,1600,{timestamp},1,0,0,0,0,0,0,1,1,0,0,0,0,0")
        rows.append(f"0,{session * 2 + 1},20220422,1600,{timestamp + 1},0,0,0,0,0,0,0,0,1,0,0,0,0,0")
    path.write_text(header + "\n".join(rows) + "\n")
    data = load_kuairand_sessions(tmp_path, SessionRecConfig(rows=100, users=1))
    assert data.train and data.validation and data.test
    assert data.test[0].negatives
    assert data.test[0].positives != data.test[0].negatives
