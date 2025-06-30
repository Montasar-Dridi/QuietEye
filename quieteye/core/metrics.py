import statistics

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

def analyze_attention(attention_log):
    if not attention_log:
        return {
            "avg": 0.0, "min": (0.0, None), "max": (0.0, None),
            "std": 0.0, "count": 0
        }

    scores = [s for _, s in attention_log]
    timestamps = [t for t, _ in attention_log]

    avg = sum(scores) / len(scores)
    std = statistics.stdev(scores) if len(scores) > 1 else 0.0
    min_score = min(scores)
    max_score = max(scores)

    min_time = timestamps[scores.index(min_score)]
    max_time = timestamps[scores.index(max_score)]

    return {
        "avg": avg,
        "std": std,
        "min": (min_score, min_time),
        "max": (max_score, max_time),
        "count": len(scores)
    }
