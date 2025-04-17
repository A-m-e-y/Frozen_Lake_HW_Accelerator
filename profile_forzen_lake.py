import cProfile
import pstats
from io import StringIO
from Frozen_Lake_Q_Learning import train_q_learning

def profile_training(runs=5):
    total_stats = None
    for i in range(runs):
        print(f"🔄 Run {i + 1}/{runs}")
        profiler = cProfile.Profile()
        profiler.enable()
        train_q_learning()
        profiler.disable()

        # Collect stats
        s = StringIO()
        ps = pstats.Stats(profiler, stream=s).sort_stats(pstats.SortKey.CUMULATIVE)
        ps.print_stats()

        # Aggregate stats
        if total_stats is None:
            total_stats = ps
        else:
            total_stats.add(ps)

    # Print average stats
    print("\n=== Average Profiling Results ===")
    total_stats.print_stats()

if __name__ == '__main__':
    profile_training(runs=5)
