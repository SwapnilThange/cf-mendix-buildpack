import subprocess
import basetest
import time


class TestCaseJavaCrashRestartsProcess(basetest.BaseTest):

    def setUp(self):
        self.setUpCF('sample-6.2.0.mda', env_vars={
            'DEPLOY_PASSWORD': self.mx_password,
            'METRICS_INTERVAL': '10',
        })
        self.startApp()

    def test_check_java_crash_restarts_process(self):
        self.assert_app_running(self.app_name)
        print('killing java to see if app will actually restart')
        subprocess.check_call((
            'cf', 'ssh', self.app_name, '-c', 'killall java'
        ), stdout=subprocess.PIPE)
        time.sleep(10)
        cf_events = subprocess.check_output(
            ('cf', 'events', self.app_name)
        )
        print('checking if process has crashed in cf events')
        print(cf_events)
        assert 'app.crash' in cf_events
