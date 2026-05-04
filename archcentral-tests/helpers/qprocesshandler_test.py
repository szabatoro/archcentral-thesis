import unittest
from unittest.mock import MagicMock, patch
from archcentral.helpers.qprocesshelper import QProcessHandler

class TestQProcessHandler(unittest.TestCase):

    @patch("archcentral.helpers.qprocesshelper.QProcess")
    def test_start_process_initializes_and_starts(self, mock_qprocess):
        handler = QProcessHandler()

        mock_process = MagicMock()
        mock_qprocess.return_value = mock_process

        handler.start_process("echo", ["hello"])

        self.assertIs(handler.process, mock_process)
        mock_process.start.assert_called_once_with("echo", ["hello"])

    def test_read_stdout_updates_buffer_and_emits_signal(self):
        handler = QProcessHandler()

        mock_process = MagicMock()
        handler.process = mock_process

        mock_process.readAllStandardOutput.return_value = b"hello"

        emitted = []
        handler.stream.connect(lambda x: emitted.append(x))

        handler._read_stdout()

        self.assertEqual(emitted, ["hello"])
        self.assertIn("hello", handler._buffer)

    def test_read_stderr_updates_buffer_and_emits_signal(self):
        handler = QProcessHandler()

        mock_process = MagicMock()
        handler.process = mock_process

        mock_process.readAllStandardError.return_value = b"error"

        emitted = []
        handler.stream.connect(lambda x: emitted.append(x))

        handler._read_stderr()

        self.assertEqual(emitted, ["error"])
        self.assertIn("error", handler._buffer)

    def test_handle_finished_emits_final_output_and_exit_code(self):
        handler = QProcessHandler()

        mock_process = MagicMock()
        handler.process = mock_process

        handler._buffer = "hello "

        mock_process.readAllStandardOutput.return_value = b"world"
        mock_process.exitCode.return_value = 0

        finished_output = []
        exit_code_data = []

        handler.finished.connect(lambda x: finished_output.append(x))
        handler.finished_with_exit_code.connect(lambda text, code: exit_code_data.append((text, code)))

        handler._handle_finished()

        self.assertEqual(finished_output[0], "hello world")
        self.assertEqual(exit_code_data[0], ("hello world", 0))
        self.assertIsNone(handler.process)
        self.assertEqual(handler._buffer, "")

    def test_write_to_stdin_sends_encoded_data(self):
        handler = QProcessHandler()

        mock_process = MagicMock()
        handler.process = mock_process

        handler.write_to_stdin("test input")

        mock_process.write.assert_called_once_with(b"test input")

    @patch("archcentral.helpers.qprocesshelper.subprocess.run")
    def test_send_sigint_calls_subprocess(self, mock_run):
        handler = QProcessHandler()

        mock_process = MagicMock()
        mock_process.processId.return_value = 1234
        handler.process = mock_process

        handler.send_sigint()

        mock_run.assert_called_once_with(["pkexec", "kill", "-INT", "1234"])
