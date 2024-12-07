**Overview**  
 We use `unittest` to write test methods in `test_webgraph.py` and measure how much of our code is covered by these tests using the `coverage` tool.

---

**1. Writing and Organizing Tests (test_webgraph.py)**  
We create a test class that inherits from `unittest.TestCase`, and each test method name starts with `test_`. This naming convention allows the `unittest` discovery mechanism to automatically find and run these tests. Our tests typically target the public functions of `webgraph.py`:

- **Core Methods:**  
  - `test_add_node()`: Ensures adding a node with metadata stores it correctly.  
  - `test_add_edge()`: Checks if adding edges between existing nodes works properly.  
  - `test_remove_node()` and `test_remove_edge()`: Verifies removal of nodes and edges, ensuring no orphan references remain.  
  - `test_update_node_metadata()`: Confirms that updating a node’s metadata works as expected.  
  - `test_calculate_pagerank()` and related tests: Ensures that PageRank calculations run correctly and results can be retrieved.  
  - `test_get_subgraph()`: Checks that we can retrieve a neighborhood subgraph for a given node.

- **Edge Cases and Exceptions:**  
  We also test how the code handles unusual or erroneous conditions:  
  - Trying to get metadata for a non-existent node should raise `KeyError`.  
  - Calling `get_pagerank()` before running the calculation should produce a meaningful error or exception.  
  - Removing non-existent nodes or edges should be handled gracefully without causing crashes.

This broad approach ensures we test the main functionality as well as how the code responds to invalid input or unexpected states.

---

**2. Improving Coverage by Adjusting the Code (webgraph.py)**  
After running our tests, we use coverage reports to find lines of code not executed by any test (labeled “missing”). These missing lines often correspond to rarely triggered conditions or error-handling paths. For instance:

- **Initializing Attributes:**  
  If tests show that calling `get_pagerank()` before `calculate_pagerank()` causes an unhandled error, we might initialize `self.pagerank = None` in the constructor. This way, the code can detect the uninitialized state and raise a `KeyError` or return a helpful message.

- **Handling Exceptions and Uncovered Branches:**  
  If an `if` condition or exception branch never gets triggered, we can add a test specifically designed to hit that scenario—for example, a test that requests a non-existent node to ensure that the proper exception is raised. If the code itself needs refinement to handle such cases consistently, we modify `webgraph.py` accordingly.

By iterating this process—adding tests, refining code to handle edge cases, and checking coverage again—we gradually ensure that all meaningful code paths are tested.

---

**3. Running Tests with Coverage**  
To run our tests and collect coverage data, we navigate to the directory containing our tests and run:

```bash
coverage run -m unittest discover
```

- `coverage run`: Activates the coverage tool to track which lines of code are executed.  
- `-m unittest discover`: Automatically finds and runs all tests in files named `test_*.py`.

This step executes our entire test suite and records coverage data.

---

**4. Viewing Coverage Reports**  
To see a summary of coverage results in the terminal, we run:

```bash
coverage report -m
```

This shows:

- **Stmts (Statements)**: Total lines of code that can execute.  
- **Miss (Missing)**: Lines never executed by any test.  
- **Cover (Coverage Percentage)**: The percentage of executed lines.  
- **Missing**: The exact line numbers untested.

By analyzing these numbers, we know where to improve our tests. If certain lines remain untested, we create additional tests or adjust existing ones until those scenarios are covered.

---

**6. Iterative Improvement**  
After examining the coverage report, we may still find some lines uncovered. We then write or modify tests to cover those lines, run `coverage` again, and repeat until we’re satisfied with the testing completeness. The goal is not just hitting 90%-100% coverage, but ensuring our tests are meaningful, accurately reflecting the behavior of our code under both normal and exceptional conditions.

---

**In Summary**:  
1. We write comprehensive tests in `test_webgraph.py` to cover normal operations and edge cases of `webgraph.py`.  
2. We use `coverage` to identify missing lines.  
3. We refine `webgraph.py` and add new tests to handle those missing scenarios.  
4. We run `coverage report` to guide further test improvements.  
5. Through iteration, we improve both coverage and code quality, ensuring the `WebGraph` functionality is robust, reliable, and well-tested.