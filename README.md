# memory-stats-template
Notes on Python memory management

## Installation

```
python3 -m venv venv
```

Activate using your preferred shell (e.g. fish)
```
source venv/bin/activate.fish
```
Install required package 
```
pip install -r requirements.txt 
```

## Usage
This repo is designed to be use as notes for keeping track of memory statistics when writing code. Additionally, the provided files can be used to test different allocation strategies and experiment with optimizations. 

Note: As noted in the `support_fxns.py` module, you can simulate a memory leak/garbage collection failure, using `time.sleep()`. This works if you make the function `async` as `time.sleep()` freezes the resources/memory and prevents them from being modified by calling path. If one desires to correctly test an async function with `sleep()`, remember to use `asyncio`'s sleep function for handling memory properly. 

To run 
```
python3 test.py
```

## Tutotial

This repo uses the `pympler` library for memory statistics.


### Get a memory usage using `summary`
```py
# Check memory usage summary (by object type)
mem_summary_init = summary.summarize(muppy.get_objects())
rows = summary.format_(mem_summary_init)
summary.print_(mem_summary_init)
```
Note that this gets you a summary of the object types. This is useful in high level debugging of determining what data types are taking the most resources, especially if one can replace/fix inefficient objects.

The summary library also supports using diffs to see a quick comparison of techniques. 
```py
# Check memory usage diff
x = [2] * 10
mem_summary_new = summary.summarize(muppy.get_objects())
diff = summary.get_diff(mem_summary_init, mem_summary_new)
summary.print_(diff)
```
Note: even with diff, one should use this as a high level description of memory differences focusing on the `types` and `total size` output columns, unless one is very familiar with Python's object allocation. 

### Check the memory size of an object using `asizeof`
```py
x = [2] * 10
# Check memory size of a specific object
print(asizeof.asizeof(x)) 
print(asizeof.asized(x, detail = 1).format()) 
```
Note: the above example uses a list of int literals. As each `2` object is identical to the following object in the list, only the first reference of `2` uses its full memory requirements. Python's private heap optimization iterates the reference count to the `2` object as opposed to allocating an identical object. This can have interesting behavior especially with regard to mutable objects. 

### Block Summation using `SummaryTracker()`
```py
async def test_fxn():
    import time
    my_dict = {"x":0}
    # in async sleep freezes resources 
    time.sleep(5)
    return 0

# Find the memory leak simulation
tr = tracker.SummaryTracker()
tr.print_diff()
test_fxn()
tr.print_diff()
```
This can be used to place checkpoints of memory usage in the code and automatically diff them. This can be useful to check for memory leaks among other purposes. The above example simulates a memory leak by exploiting the behavior of async functions when calling `sleep()`. 

### Checking the memory size of objects using `ClassTracker()`
```py
# Check memory usage of an object over time
class test_class:
    x = 4
    y = 5
    z = 6
    def multiply(self, n: int):
        self.x = [self.x] * n
        self.y = [self.y] * n
        self.z = [self.z] * n
my_class = test_class() 
# Initialize tracker 
c_tr = classtracker.ClassTracker()
c_tr.track_object(my_class)
c_tr.create_snapshot()
# Allocate some memory
my_class.multiply(1000)
# Check difference
c_tr.create_snapshot()
c_tr.stats.print_summary()
```

One can use `ClassTracker()` snapshots to track memory usage of an object over time. The above example tracks the allocation of three lists of size `n`, in this case 1000. One can also use asizeof.asized to get the direct size of an object at any given point in time via the following:
```py
asizeof.asized(my_class, detail = 1).format()
```
