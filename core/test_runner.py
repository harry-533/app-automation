from datetime import datetime
import time
from core.task_decomposer import TaskDecomposer
from core.step_executor import StepExecutor
from core.path_manager import PathManager
from reporting.report_generator import ReportGenerator
from reporting.logger import ExecutionLogger

class TestRunner:
    def __init__(self, config, verbose=False):
        self.config = config
        self.verbose = verbose

        self.decomposer = TaskDecomposer(config)
        self.executor = StepExecutor(config)
        self.path_manager = PathManager(config)
        self.logger = ExecutionLogger(config)

        self.execution_log = []
    
    def run_test(self, test_input):
        start_time = time.time()

        test_description = self._load_test(test_input)
        self.logger.log_test_start(test_description)

        saved_path = self.path_manager.find_matching_path(test_description)

        if saved_path:
            self._log(f"Found existing path with {saved_path['success_rate']*100:.0f}% success rate")
            steps = saved_path['steps']
        else:
            self._log("Decomposing test into steps")
            steps = self.decomposer.decompose(test_description)

        self._log(f"Test plan: {len(steps)} steps")
        for i, step in enumerate(steps, 1):
            self._log(f"    {i}. {step}")
        
        all_passed = True
        for step_num, step in enumerate(steps, 1):
            self._log(f"\n{'-'*60}")
            self._log(f"[Step {step_num}/{len(steps)}] {step}")
            self._log(f"{'─'*60}")

            result = self.executor.execute_step(step)
            self.execution_log.append(result)

            if not result.success:
                self._log(f"❌ Step failed: {step}")
                all_passed = False
                break
        
            self._log(f"✅ Step completed using: {result.method}")
            time.sleep(self.config.STEP_DELAY)
        
        if all_passed and self.config.ENABLE_PATH_LEARNING:
            self.path_manager.save_path(test_description, steps, success=True)
        
        duration = time.time() - start_time
        report_path = ReportGenerator(self.config).generate(
            test_description=test_description,
            steps=steps,
            execution_log=self.execution_log,
            passed=all_passed,
            duration=duration
        )

        return TestResult(
            passed=all_passed,
            duration=duration,
            report_path=report_path
        )

    def _load_test(self, test_input):
        if test_input.endswith('.yaml'):
            with open(test_input) as f:
                import yaml
                data = yaml.safe_load(f)
                return data['description']
        else:
            return test_input
        
    def _log(self, message):
        if self.verbose:
            print(message)
        self.logger.log(message)

class TestResult:
    def __init__(self, passed, duration, report_path):
        self.passed = passed
        self.duration = duration
        self.report_path = report_path