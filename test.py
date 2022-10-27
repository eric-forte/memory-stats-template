# Global imports
from pympler import asizeof, classtracker, muppy, summary, tracker
# Local imports
import support_fxns


# Check memory usage summary (by object type)
mem_summary_init = summary.summarize(muppy.get_objects())
rows = summary.format_(mem_summary_init)
summary.print_(mem_summary_init)

# Check memory usage diff
x = [2] * 10
mem_summary_new = summary.summarize(muppy.get_objects())
diff = summary.get_diff(mem_summary_init, mem_summary_new)
summary.print_(diff)

# Check memory size of a specific object
print(asizeof.asizeof(x)) 
print(asizeof.asized(x, detail = 1).format()) 
# Looking at optimization of literals (private heap optimization)
y = [2] * 10
print(asizeof.asizeof(y)) 
print(asizeof.asized(y, detail = 1).format()) 
print(asizeof.asizeof(x)) 
print(asizeof.asized(x, detail = 1).format()) 

# Check for memory leaks
tr = tracker.SummaryTracker()
tr.print_diff()
support_fxns.test_fxn()
tr.print_diff()

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

# Checking size
print(asizeof.asized(my_class, detail = 1).format()) 
print(asizeof.asized(my_class.__dict__, detail = 1).format()) 