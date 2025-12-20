# Baseline: error reporting (out-of-bounds, Python)
nums = [1,2,3]
try:
    result = nums[10]
    print(f"result={result}")
except Exception as e:
    print(f"error: {e}")
