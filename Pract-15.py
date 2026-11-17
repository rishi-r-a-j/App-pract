
import gc
import sys
import time
import weakref
import tracemalloc


def section(title):
    print(f"\n{'=' * 8} {title} {'=' * 8}")


# Node Class
class Node:
    def __init__(self, name):
        self.name = name
        self.other = None

    def __del__(self):
        print(f"[__del__] {self.name} destroyed")


# 1. Reference Counting
def exp1_reference_counting():
    section("1. Reference Counting")

    a = Node("A")
    print("Reference count:", sys.getrefcount(a))

    b = a
    print("After b = a:", sys.getrefcount(a))

    del a
    print("After deleting a:", sys.getrefcount(b))

    print("Deleting the last reference...")
    del b


# 2. Reference Cycle and Manual Collection
def exp2_cycle_and_manual_collect():
    section("2. Reference Cycle and Manual Collection")

    gc.collect()
    gc.disable()

    print("GC enabled?", gc.isenabled())

    x = Node("X")
    y = Node("Y")

    x.other = y
    y.other = x

    del x, y

    print("Objects are still in memory due to reference cycle")

    found = gc.collect()
    print("Objects collected:", found)

    gc.enable()


# 3. Thresholds, Counts and Statistics
def exp3_thresholds_counts_stats():
    section("3. Thresholds, Counts and Statistics")

    print("Threshold:", gc.get_threshold())
    print("Count:", gc.get_count())
    print("Statistics:", gc.get_stats())


# 4. Automatic Garbage Collection
def exp4_automatic_trigger():
    section("4. Automatic Garbage Collection")

    events = []

    def watcher(phase, info):
        if phase == "stop":
            events.append((info["generation"], info["collected"]))

    gc.callbacks.append(watcher)

    old = gc.get_threshold()
    gc.collect()

    gc.set_threshold(50, 5, 5)
    events.clear()

    for _ in range(300):
        a, b = [], []
        a.append(b)
        b.append(a)

    gc.set_threshold(*old)
    gc.callbacks.remove(watcher)

    print("Automatic collections:", len(events))
    print("First few events:", events[:5])


# 5. Generational Garbage Collection
def exp5_generations():
    section("5. Generational Garbage Collection")

    gc.collect()

    keeper = [Node("K")]
    keeper[0].other = keeper

    print("Before collection:",
          [len(gc.get_objects(g)) for g in range(3)])

    gc.collect(0)
    print("After generation 0:",
          [len(gc.get_objects(g)) for g in range(3)])

    gc.collect(1)
    print("After generation 1:",
          [len(gc.get_objects(g)) for g in range(3)])

    keeper[0].other = None
    del keeper


# 6. Memory Effect of Garbage Collection
def exp6_memory_effect():
    section("6. Memory Effect of Garbage Collection")

    gc.collect()
    gc.disable()

    tracemalloc.start()
    base = tracemalloc.get_traced_memory()[0]

    for _ in range(20000):
        a, b = {}, {}
        a["b"] = b
        b["a"] = a

    del a, b

    leaked = tracemalloc.get_traced_memory()[0] - base

    n = gc.collect()
    after = tracemalloc.get_traced_memory()[0] - base

    tracemalloc.stop()
    gc.enable()

    print("Memory before collection:",
          round(leaked / 1024, 1), "KiB")

    print("Objects collected:", n)

    print("Memory after collection:",
          round(after / 1024, 1), "KiB")


# 7. DEBUG_SAVEALL
def exp7_debug_saveall():
    section("7. DEBUG_SAVEALL")

    gc.collect()
    gc.set_debug(gc.DEBUG_SAVEALL)

    p, q = [1], [2]

    p.append(q)
    q.append(p)

    del p, q

    gc.collect()

    print("Garbage objects:", gc.garbage)

    gc.set_debug(0)
    gc.garbage.clear()

    gc.collect()


# 8. Object Tracking and Weak References
def exp8_tracking_and_weakref():
    section("8. Object Tracking and Weak References")

    samples = [
        ("Integer", 5),
        ("String", "hi"),
        ("List", [1]),
        ("Empty Dictionary", {}),
        ("Dictionary with List", {"k": [1]}),
        ("Tuple", (1, 2)),
        ("Node", Node("T"))
    ]

    for label, obj in samples:
        print(label, "tracked?", gc.is_tracked(obj))

    n = Node("W")

    ref = weakref.ref(n)

    print("Weak reference alive?", ref() is not None)

    del n

    print("After deletion:", ref() is not None)


# 9. Freeze and Unfreeze
def exp9_freeze():
    section("9. Freeze and Unfreeze")

    gc.collect()

    print("Frozen before:", gc.get_freeze_count())

    gc.freeze()

    print("Frozen after:", gc.get_freeze_count())

    gc.unfreeze()

    print("After unfreeze:", gc.get_freeze_count())


# 10. Garbage Collection Performance
def exp10_timing():
    section("10. Garbage Collection Performance")

    def work():
        data = []

        for i in range(400000):
            data.append([i])

        return len(data)

    results = {}

    for label, enabled in [
        ("GC Enabled", True),
        ("GC Disabled", False)
    ]:
        gc.collect()

        if enabled:
            gc.enable()
        else:
            gc.disable()

        start = time.perf_counter()

        work()

        results[label] = time.perf_counter() - start

        gc.enable()

        print(label, ":", round(results[label] * 1000, 2), "ms")

    print("Execution time depends on the system and Python version.")


# Main Program
if __name__ == "__main__":

    print("Python Version:", sys.version.split()[0])

    exp1_reference_counting()
    exp2_cycle_and_manual_collect()
    exp3_thresholds_counts_stats()
    exp4_automatic_trigger()
    exp5_generations()
    exp6_memory_effect()
    exp7_debug_saveall()
    exp8_tracking_and_weakref()
    exp9_freeze()
    exp10_timing()
