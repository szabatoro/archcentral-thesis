from PySide6.QtCore import QByteArray, QProcess, QObject, Signal

class QProcessHandler(QObject):
    finished: Signal = Signal(str)
    stream: Signal = Signal(str)  # new streaming signal

    def __init__(self) -> None:
        super().__init__()
        self.process: QProcess = None
        self._buffer = ""  # optional, in case you want to collect full output

    def start_process(self, program, arguments) -> None:
        if self.process is None:
            self.process = QProcess()
            self.process.readyReadStandardOutput.connect(self._read_stdout)  # stream output
            self.process.finished.connect(self._handle_finished)
            self.process.start(program, arguments)

    def _read_stdout(self) -> None:
        if self.process:
            data: QByteArray = self.process.readAllStandardOutput()
            if data:
                output: str = bytes(data).decode("utf8")
                self._buffer += output  # keep a running buffer
                self.stream.emit(output)  # stream immediately

    def _handle_finished(self) -> None:
        if self.process:
            # emit any remaining output
            remaining_data: QByteArray = self.process.readAllStandardOutput()
            if remaining_data:
                self._buffer += bytes(remaining_data).decode("utf8")
            # emit final combined output
            self.finished.emit(self._buffer.strip())
        self.process = None
        self._buffer = ""
