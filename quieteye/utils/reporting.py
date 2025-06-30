from datetime import datetime
from quieteye.core.metrics import analyze_attention


def format_duration(seconds):
    if seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def format_timestamp(ts):
    return datetime.fromtimestamp(ts).strftime("%H:%M:%S") if ts else "N/A"


def generate_terminal_report(start_time, end_time, attention_log):
    duration = end_time - start_time
    summary = analyze_attention(attention_log)

    print("\n\n--- QuietEye Session Report ---")
    print(f"Session Duration: {format_duration(duration)}")
    print(f"Final Attention Score (avg): {summary['avg']:.2f}")
    print(
        f"Max Attention Score: {summary['max'][0]:.2f} at {format_timestamp(summary['max'][1])}"
    )
    print(
        f"Min Attention Score: {summary['min'][0]:.2f} at {format_timestamp(summary['min'][1])}"
    )
    print(f"Standard Deviation: {summary['std']:.2f}")
    print(f"Total Scores Tracked: {summary['count']}")
    print("--------------------------------")
