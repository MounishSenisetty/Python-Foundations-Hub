# DSA Interview Patterns — Reference Guide

A pattern-oriented tour of the data-structure and algorithm techniques that
recur across coding interviews and, more importantly, in day-to-day systems
work. Rather than cataloguing problems, this guide groups them by the *shape* of
the underlying idea, so that recognising the pattern points straight at the
tool.

Each pattern below links its implementations under
[`patterns/`](../../patterns) and their tests under
[`tests/patterns/`](../../tests/patterns). Every module is runnable
(`python patterns/<pattern>/<module>.py`) and documents its own time and space
complexity.

## Pattern index

| Pattern | Core idea | Typical time | Modules |
| --- | --- | --- | --- |
| [Two Pointers](#two-pointers) | Converge or chase two indices across a sequence | O(n) | 4 |
| [Hash Maps & Sets](#hash-maps--sets) | Trade memory for O(1) lookup | O(n) | 3 |
| [Linked Lists](#linked-lists) | Pointer rewiring with dummy nodes | O(n) | 4 |
| [Fast & Slow Pointers](#fast--slow-pointers) | Two pointers at different speeds | O(n) | 3 |
| [Sliding Window](#sliding-window) | A moving sub-range with incremental state | O(n) | 3 |
| [Binary Search](#binary-search) | Halve a sorted or monotonic search space | O(log n) | 4 |

---

## Two Pointers

**When to use it.** A sequence (usually sorted) where a brute-force pair or
triplet scan is O(n²) or worse, and the structure lets you rule out whole
regions by moving one of two indices.

**Complexity.** O(n) time, O(1) space — the pointers replace a nested loop.

**Modules**
- [`pair_sum_sorted.py`](../../patterns/two_pointers/pair_sum_sorted.py) — two-sum on a sorted array by converging from both ends.
- [`triplet_sum.py`](../../patterns/two_pointers/triplet_sum.py) — 3-Sum in O(n²) with duplicate triplets skipped.
- [`is_palindrome_valid.py`](../../patterns/two_pointers/is_palindrome_valid.py) — in-place palindrome check ignoring non-alphanumerics.
- [`largest_container.py`](../../patterns/two_pointers/largest_container.py) — maximum-area container by shrinking from the widest pair.

**In the real world.** Merging two sorted streams (log-structured merge trees),
the merge step of merge sort, and reconciling two sorted change lists in a diff
algorithm.

---

## Hash Maps & Sets

**When to use it.** You need membership, counting, or complement lookups and can
afford O(n) extra memory to turn a repeated search into an O(1) one.

**Complexity.** O(n) time; O(n) space, except `zero_striping` which reuses the
input for O(1) auxiliary space.

**Modules**
- [`pair_sum_unsorted.py`](../../patterns/hash_maps_sets/pair_sum_unsorted.py) — single-pass two-sum via a complement map.
- [`verify_sudoku_board.py`](../../patterns/hash_maps_sets/verify_sudoku_board.py) — row/column/box validation with sets.
- [`zero_striping.py`](../../patterns/hash_maps_sets/zero_striping.py) — in-place matrix zeroing using the first row and column as markers.

**In the real world.** De-duplicating records, request rate-limiting by key,
join operations in query engines, and detecting duplicate transactions.

---

## Linked Lists

**When to use it.** Sequential data with frequent insertions/removals at
arbitrary positions, or when constant-time splice matters more than random
access. A *dummy head* removes special cases when the first node may change.

**Complexity.** O(n) traversal; O(1) splices. `LRUCache` combines a hash map
with a doubly linked list for O(1) `get`/`put`.

**Modules**
- [`linked_list_reversal.py`](../../patterns/linked_lists/linked_list_reversal.py) — iterative (O(1) space) and recursive reversal.
- [`remove_kth_last_node.py`](../../patterns/linked_lists/remove_kth_last_node.py) — leader/trailer removal in one pass with a dummy node.
- [`linked_list_intersection.py`](../../patterns/linked_lists/linked_list_intersection.py) — two-pointer shared-tail detection.
- [`lru_cache.py`](../../patterns/linked_lists/lru_cache.py) — O(1) LRU cache (hash map + doubly linked list).

**In the real world.** LRU caches back CPU caches, database buffer pools, and
CDN edge eviction; adjacency lists represent graphs; free-lists manage memory
allocators.

---

## Fast & Slow Pointers

**When to use it.** Cycle detection, or finding a positional landmark (like the
middle) in a single pass over a structure with no random access.

**Complexity.** O(n) time, O(1) space — strictly better than a visited-set
approach on memory.

**Modules**
- [`linked_list_loop.py`](../../patterns/fast_slow_pointers/linked_list_loop.py) — Floyd's tortoise-and-hare cycle detection.
- [`linked_list_midpoint.py`](../../patterns/fast_slow_pointers/linked_list_midpoint.py) — one-pass midpoint via a doubled-speed pointer.
- [`happy_number.py`](../../patterns/fast_slow_pointers/happy_number.py) — cycle detection over a numeric sequence.

**In the real world.** Detecting loops in dependency graphs and deadlock
waits-for graphs, and finding cycles in linked data structures during garbage
collection.

---

## Sliding Window

**When to use it.** The answer concerns a contiguous sub-array or substring, and
adjacent windows share almost all of their elements, so state can be updated
incrementally instead of recomputed.

**Complexity.** O(n) time; O(1) space for the fixed-alphabet variants here.

**Modules**
- [`substring_anagrams.py`](../../patterns/sliding_window/substring_anagrams.py) — fixed-size window with frequency arrays.
- [`longest_substring_unique.py`](../../patterns/sliding_window/longest_substring_unique.py) — dynamic window with last-seen-index jumps.
- [`longest_uniform_substring.py`](../../patterns/sliding_window/longest_uniform_substring.py) — dynamic window allowing up to `k` replacements.

**In the real world.** Moving averages and rolling aggregates in stream
processing, per-window rate limiting, and network throughput sampled over a
time window.

---

## Binary Search

**When to use it.** A sorted array, or — more generally — a *monotonic*
predicate over a range of candidate answers, where each probe lets you discard
half the remaining space.

**Complexity.** O(log n) probes; each probe is O(1), or O(n) when the predicate
itself scans the input (as in `cutting_wood`).

**Modules**
- [`find_insertion_index.py`](../../patterns/binary_search/find_insertion_index.py) — lower-bound search for a target or its insertion point.
- [`first_last_occurrences.py`](../../patterns/binary_search/first_last_occurrences.py) — lower- and upper-bound searches over duplicates.
- [`cutting_wood.py`](../../patterns/binary_search/cutting_wood.py) — binary search on the answer range of a monotonic function.
- [`target_in_rotated_array.py`](../../patterns/binary_search/target_in_rotated_array.py) — modified search that identifies the sorted half.

**In the real world.** Index lookups in databases and sorted files, version
bisection (`git bisect`), autoscaling to the smallest capacity that meets an SLA,
and any "find the threshold" tuning of a monotonic system.

---

## Running the tests

```bash
pytest tests/patterns -q          # all patterns
pytest tests/patterns/test_binary_search.py -q   # one pattern
```
