# output_formatter.py

def print_results(start, max_distance, forbidden, reachable, distance):
    """Prints final results in a readable form."""
    print("=" * 60)
    print("RAILWAY REACHABILITY ANALYSIS")
    print("=" * 60)

    print(f"Start station: {start}")
    print(f"Maximum distance B: {max_distance}")

    if forbidden:
        print(f"Forbidden stations: {', '.join(sorted(forbidden))}")
    else:
        print("Forbidden stations: none")

    print("-" * 60)

    if not reachable:
        print("No reachable stations.")
        print("Reachable station count: 0")
        return

    print("Reachable stations:")
    for station in sorted(reachable, key=lambda s: (distance[s], s)):
        print(f"  {station:15s} distance = {distance[station]}")

    print("-" * 60)
    print(f"Reachable station count including start station: {len(reachable)}")
    print(f"Reachable station count excluding start station: {max(0, len(reachable) - 1)}")