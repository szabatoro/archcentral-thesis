from PySide6.QtCore import QByteArray, QProcess, QObject, Signal

class QProcessHandler(QObject):
    started: Signal = Signal()
    finished: Signal = Signal(str)
    finished_with_exit_code: Signal = Signal(str, int)
    stream: Signal = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.process: QProcess = None
        self._buffer = ""

    def start_process(self, program, arguments) -> None:
        """
        Uses QProcess() to start a program with its arguments and continously logs stdout.
        """
        if self.process is None:
            self.process = QProcess()
            self.process.readyReadStandardOutput.connect(self._read_stdout)
            self.process.readyReadStandardError.connect(self._read_stderr)
            self.process.started.connect(self.started.emit)
            self.process.finished.connect(self._handle_finished)
            self.process.start(program, arguments)

    def write_to_stdin(self, str: str) -> None:
        """Encodes a given string to bytes and writes it to stdin."""
        writeable_data = str.encode("utf-8")
        self.process.write(writeable_data)

    def _read_stdout(self) -> None:
        if self.process:
            data: QByteArray = self.process.readAllStandardOutput()
            if data:
                output: str = bytes(data).decode("utf8")
                self._buffer += output
                self.stream.emit(output)

    def _read_stderr(self) -> None:
        if self.process:
            data = self.process.readAllStandardError()
            if data:
                output = bytes(data).decode("utf8")
                self._buffer += output
                self.stream.emit(output)

    def _handle_finished(self) -> None:
        if self.process:
            # emit any remaining output
            remaining_data: QByteArray = self.process.readAllStandardOutput()
            if remaining_data:
                self._buffer += bytes(remaining_data).decode("utf8")
            # emit final combined output
            self.finished.emit(self._buffer.strip())
            self.finished_with_exit_code.emit(self._buffer.strip(), self.process.exitCode())
        self.process = None
        self._buffer = ""
