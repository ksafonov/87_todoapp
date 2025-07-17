from django.test.runner import DiscoverRunner
import unittest

class QuietTestRunner(DiscoverRunner):
    def run_suite(self, suite, **kwargs):
        kwargs = self.get_test_runner_kwargs()
        runner = unittest.TextTestRunner(**kwargs)
        
        result = runner._makeResult()
        result.failfast = runner.failfast
        result.buffer = runner.buffer
        startTestRun = getattr(result, 'startTestRun', None)
        if startTestRun is not None:
            startTestRun()
        try:
            suite(result)
        finally:
            stopTestRun = getattr(result, 'stopTestRun', None)
            if stopTestRun is not None:
                stopTestRun()
        
        # Print separator and result with test count but no timing
        runner.stream.writeln()
        runner.stream.writeln("----------------------------------------------------------------------")
        runner.stream.writeln(f"Ran {result.testsRun} tests")
        
        if result.wasSuccessful():
            runner.stream.writeln("OK")
        else:
            runner.stream.writeln("FAILED")
            
        return result
