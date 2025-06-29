def compute_attention_score(gaze_direction, pitch, yaw):
    gaze_weight = 0.4
    yaw_weight = 0.3
    pitch_weight = 0.3

    gaze_score = {
        "center": 1.0,
        "left": 0.6,
        "right": 0.6
    }.get(gaze_direction.lower(), 0.6)

    pitch_score = max(0.0, 1.0 - min(abs(pitch) / 30.0, 1.0))
    yaw_score = max(0.0, 1.0 - min(abs(yaw) / 30.0, 1.0))

    attention_score = (
        gaze_weight * gaze_score +
        yaw_weight * yaw_score +
        pitch_weight * pitch_score
    )

    return int(round(attention_score * 100))
