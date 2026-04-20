import time
import sys

def print_progress(index, total, fetched_count, total_uncached, start_time):
    elapsed = time.time() - start_time

    rate = fetched_count / elapsed if elapsed > 0 else 0
    remaining_uncached = total_uncached - fetched_count
    eta = remaining_uncached / rate if rate > 0 else 0

    # Progress bar based on total loop
    progress = index / total
    bar_length = 20
    filled = int(bar_length * progress)
    bar = "█" * filled + "░" * (bar_length - filled)

    sys.stdout.write(
        f"\rDetails: [{bar}] {index}/{total} | "
        f"API: {fetched_count}/{total_uncached} | "
        f"{rate:.2f}/s | ETA: {eta:.1f}s"
    )
    sys.stdout.flush()
