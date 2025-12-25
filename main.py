import argparse
from datetime import datetime
from core.test_runner import TestRunner
from config import Config

def main():
    parser = argparse.ArgumentParser(
        description='Bentley AI test automation'
    )
    parser.add_argument(
        '--test',
        type=str,
        required=True,
        help='Test description or path to test file'
    )
    parser.add_argument(
        '--mode',
        type=str,
        default='free',
        choices=['free', 'paid'],
        help='AI used: free (local) or paid (API)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show execution logs'
    )

    args = parser.parse_args()

    config = Config(ai_mode=args.mode)
    runner = TestRunner(config, verbose = args.verbose)

    print(f"\n{'='*60}")
    print(f"Mode: {args.mode.upper()}")
    print(f"Test: {args.test}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    result = runner.run_test(args.test)

    print(f"\n{'='*60}")
    print(f"{'✅ TEST PASSED' if result.passed else '❌ TEST FAILED'}")
    print(f"Duration: {result.duration:.2f}s")
    print(f"Report: {result.report_path}")
    print(f"{'='*60}\n")

    return 0 if result.passed else 1

if __name__ == "__main__":
    exit(main())