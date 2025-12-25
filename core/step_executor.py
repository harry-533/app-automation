from functions.function_registry import FunctionRegistry
from ai.ai_engine import AIEngine
from automation.screen_analyser import ScreenAnalyser
from automation.action_executor import ActionExecutor
from verification.ai_verifier import AIVerifier
import time

class StepExecutor:
    def __init__(self, config):
        self.config = config
        self.function_registry = FunctionRegistry(config)
        self.ai = AIEngine(config)
        self.screen = ScreenAnalyser(config)
        self.actions = ActionExecutor(config)
        self.verifier = AIVerifier(config)
    
    def execute_steps(self, step_name):
        func = self.function_registry.get_function(step_name)

        if func:
            print(f"Function found: {func.__name__}")
            result = self._try_function(func, step_name)

            if result.success:
                return result
            
            print("Function failed, AI used as backup")

        return self._execute_with_ai(step_name)
    
    def _try_function(self, func, step_name):
        try:
            func()

            time.sleep(2)
            screenshot = self.screen.take_screenshot()

            verified = self.verifier.verify_step_complete(
                step_name=step_name,
                screenshot=screenshot
            )
            
            if verified:
                return StepResult(
                    success=True,
                    method=f"function: {func.__name__}",
                    screenshot=screenshot
                )
            else:
                return StepResult(
                    success=False,
                    method=f"function: {func.__name__}",
                    error="Function executed but verification failed"
                )
        
        except Exception as e:
            return StepResult(
                success=False,
                method=f"Function: {func.__name__}",
                error=str(e)
            )
    
    def _execute_with_ai(self, step_name):
        max_actions = 10
        actions_taken = []

        for attempt in range(max_actions):
            screenshot = self.screen.take_screenshot()
            ui_hierarchy = self.screen.get_ui_heirarchy()

            decision = self.ai.decide_next_action(
                goal=step_name,
                current_screen=screenshot,
                ui_hierarchy=ui_hierarchy,
                actions_so_far=actions_taken
            )

            if decision['status'] == 'complete':
                return StepResult(
                    success=True,
                    method="autonomous",
                    screenshot=screenshot,
                    actions_taken=actions_taken
                )
            
            actions_success = self.actions.execute(decision['action'])
            actions_taken.append(decision['action'])

            if not actions_success:
                return StepResult(
                    success=False,
                    method="autonomous",
                    error=f"Failed to execute action: {decision['aciton']}"
                )
            
            time.sleep(1)

        return StepResult(
            success=False,
            method="autonomous",
            error=f"Max actions ({max_actions}) reached without completing step"
        )

class StepResult:
    def __init__(self, success, method, screenshot=None, error=None, actions_taken=None):
        self.success = success
        self.method = method
        self.screenshot = screenshot
        self.error = error
        self.actions_taken = actions_taken or []