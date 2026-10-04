import os
import subprocess
import sys
import time


def run_test(script_name):
    print("\n" + "=" * 70)
    print(f"RUNNING: {script_name}")
    print("=" * 70)

    start = time.perf_counter()

    result = subprocess.run(
        [sys.executable, script_name],
        capture_output=True,
        text=True
    )

    elapsed = time.perf_counter() - start

    print(result.stdout)

    if result.stderr:
        print("Warnings/Errors:")
        print(result.stderr)

    if result.returncode == 0:
        print(f"STATUS: PASS ✅")
        print(f"Execution time: {elapsed:.4f} seconds")
        return True
    else:
        print(f"STATUS: FAIL ❌")
        print(f"Execution time: {elapsed:.4f} seconds")
        return False


def main():

    print("=" * 70)
    print("SIH WATERMARKING — COMPLETE TEST SUITE")
    print("=" * 70)

    tests = [
        "test_5_docx.py",
        "test_image_robustness.py",
        "test_pdf_robustness.py",
        "generate_metrics_table.py",
        "test_10page_speed.py"
    ]

    passed = 0
    failed = 0

    for test in tests:

        if not os.path.exists(test):
            print(f"\n{test}: FILE NOT FOUND ❌")
            failed += 1
            continue

        if run_test(test):
            passed += 1
        else:
            failed += 1

    print("\n" + "=" * 70)
    print("COMPLETE TEST SUITE SUMMARY")
    print("=" * 70)

    print(f"Total test modules : {len(tests)}")
    print(f"Passed             : {passed}")
    print(f"Failed             : {failed}")

    if failed == 0:
        print("\nOVERALL RESULT: ALL TEST MODULES PASSED ✅")
    else:
        print("\nOVERALL RESULT: SOME TESTS FAILED ❌")

    print("=" * 70)


if __name__ == "__main__":
    main()