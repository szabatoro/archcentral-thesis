from PySide6.QtCore import QByteArray, QProcess, QObject,  Signal

# Wrapper around QProcess to make getting cli output easier
class QProcessHandler(QObject):
    finished: Signal = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.process: QProcess = None

    # Start the given process with the given arguments
    def start_process(self, program, arguments) -> None:
        if self.process is None:
            self.process = QProcess()
            self.process.finished.connect(self._handle_finished)
            self.process.start(program, arguments)

    # Emit finish signal with decoded process stdout
    def _handle_finished(self) -> None:
        if self.process:
            data: QByteArray = self.process.readAllStandardOutput()
            if data:
                output: str = bytes(data).decode("utf8").strip()
                self.finished.emit(output)
            else:
                self.finished.emit("")
        self.process = None
