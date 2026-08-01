"""
Hivax — Cronômetro & Alarme Profissional
Requer: pip install PyQt6
"""

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTabWidget, QSpinBox, QFileDialog,
    QFrame, QSizePolicy, QGridLayout, QTimeEdit, QCheckBox,
    QSlider, QGroupBox, QLineEdit
)
from PyQt6.QtCore import (
    Qt, QTimer, QTime, QDateTime, pyqtSignal, QPropertyAnimation,
    QEasingCurve
)
from PyQt6.QtGui import QFont, QFontDatabase, QPalette, QColor, QIcon
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl
import datetime

# ── Palette ──────────────────────────────────────────────────────────────────
BG       = "#0F1117"   # near-black background
SURFACE  = "#1A1D27"   # card / panel surface
BORDER   = "#2A2D3E"   # subtle borders
TEXT     = "#E8EAF0"   # primary text
MUTED    = "#6B7194"   # secondary / muted text
ACCENT   = "#4F8EF7"   # electric blue — clock world accent
ACCENT2  = "#C0C8E8"   # light complement
DANGER   = "#F7604F"   # stop / alarm alert
SUCCESS  = "#4FD18B"   # running / active state

STYLE = f"""
QMainWindow, QWidget {{
    background-color: {BG};
    color: {TEXT};
    font-family: 'Segoe UI', 'Inter', sans-serif;
}}

QTabWidget::pane {{
    border: 1px solid {BORDER};
    background-color: {SURFACE};
    border-radius: 8px;
}}

QTabBar::tab {{
    background: {BG};
    color: {MUTED};
    padding: 10px 28px;
    font-size: 13px;
    font-weight: 500;
    border: none;
    border-bottom: 2px solid transparent;
    margin-right: 2px;
}}

QTabBar::tab:selected {{
    color: {TEXT};
    border-bottom: 2px solid {ACCENT};
    background: {BG};
}}

QTabBar::tab:hover:!selected {{
    color: {ACCENT2};
}}

QPushButton {{
    border-radius: 6px;
    font-size: 13px;
    font-weight: 600;
    padding: 9px 22px;
    border: none;
    outline: none;
}}

QPushButton#btn_primary {{
    background-color: {ACCENT};
    color: #fff;
}}
QPushButton#btn_primary:hover {{
    background-color: #6AA3FF;
}}
QPushButton#btn_primary:pressed {{
    background-color: #3A7AE0;
}}

QPushButton#btn_danger {{
    background-color: {DANGER};
    color: #fff;
}}
QPushButton#btn_danger:hover {{
    background-color: #FF7B6D;
}}

QPushButton#btn_neutral {{
    background-color: {BORDER};
    color: {TEXT};
}}
QPushButton#btn_neutral:hover {{
    background-color: #363A54;
}}

QPushButton#btn_icon {{
    background: transparent;
    color: {MUTED};
    font-size: 16px;
    padding: 6px 10px;
    border: 1px solid {BORDER};
    border-radius: 6px;
}}
QPushButton#btn_icon:hover {{
    color: {TEXT};
    border-color: {ACCENT};
}}

QSpinBox, QTimeEdit, QLineEdit {{
    background-color: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 6px;
    color: {TEXT};
    padding: 6px 10px;
    font-size: 13px;
    selection-background-color: {ACCENT};
}}
QSpinBox:focus, QTimeEdit:focus, QLineEdit:focus {{
    border-color: {ACCENT};
}}
QSpinBox::up-button, QSpinBox::down-button {{
    background: {BORDER};
    border: none;
    width: 18px;
}}

QLabel#lbl_big {{
    color: {TEXT};
    font-size: 58px;
    font-weight: 300;
    letter-spacing: 4px;
}}
QLabel#lbl_days {{
    color: {MUTED};
    font-size: 14px;
    font-weight: 500;
    letter-spacing: 2px;
}}
QLabel#lbl_status {{
    color: {MUTED};
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 1px;
    text-transform: uppercase;
}}
QLabel#lbl_section {{
    color: {MUTED};
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
}}
QLabel#lbl_clock {{
    color: {TEXT};
    font-size: 48px;
    font-weight: 200;
    letter-spacing: 6px;
}}
QLabel#lbl_date {{
    color: {MUTED};
    font-size: 14px;
    letter-spacing: 1px;
}}

QFrame#separator {{
    background: {BORDER};
    max-height: 1px;
}}

QGroupBox {{
    border: 1px solid {BORDER};
    border-radius: 8px;
    margin-top: 14px;
    padding: 12px;
    color: {MUTED};
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 6px;
    background: {SURFACE};
    color: {MUTED};
    font-size: 11px;
    letter-spacing: 2px;
}}

QCheckBox {{
    color: {TEXT};
    font-size: 13px;
    spacing: 8px;
}}
QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border: 1px solid {BORDER};
    border-radius: 4px;
    background: {SURFACE};
}}
QCheckBox::indicator:checked {{
    background: {ACCENT};
    border-color: {ACCENT};
}}

QSlider::groove:horizontal {{
    height: 4px;
    background: {BORDER};
    border-radius: 2px;
}}
QSlider::handle:horizontal {{
    background: {ACCENT};
    width: 14px;
    height: 14px;
    margin: -5px 0;
    border-radius: 7px;
}}
QSlider::sub-page:horizontal {{
    background: {ACCENT};
    border-radius: 2px;
}}

QScrollBar:vertical {{
    background: {BG};
    width: 8px;
}}
QScrollBar::handle:vertical {{
    background: {BORDER};
    border-radius: 4px;
    min-height: 20px;
}}
"""


def sep():
    f = QFrame()
    f.setObjectName("separator")
    f.setFrameShape(QFrame.Shape.HLine)
    return f


def label(text, obj="", parent=None):
    lbl = QLabel(text, parent)
    if obj:
        lbl.setObjectName(obj)
    return lbl


# ── Stopwatch Tab ─────────────────────────────────────────────────────────────
class StopwatchTab(QWidget):
    def __init__(self):
        super().__init__()
        self.elapsed_ms = 0
        self.running = False
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self._tick)
        self.laps = []
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(40, 36, 40, 36)
        root.setSpacing(0)

        # Display
        self.lbl_days = label("DIA 0", "lbl_days")
        self.lbl_days.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self.lbl_days)
        root.addSpacing(4)

        self.lbl_time = label("00:00:00", "lbl_big")
        self.lbl_time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self.lbl_time)

        self.lbl_ms = label(".000", "lbl_days")
        self.lbl_ms.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self.lbl_ms)

        self.lbl_status = label("PARADO", "lbl_status")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addSpacing(8)
        root.addWidget(self.lbl_status)

        root.addSpacing(28)
        root.addWidget(sep())
        root.addSpacing(24)

        # Controls
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.btn_start = QPushButton("▶  Iniciar")
        self.btn_start.setObjectName("btn_primary")
        self.btn_start.setFixedHeight(42)
        self.btn_start.clicked.connect(self._toggle)

        self.btn_reset = QPushButton("↺  Resetar")
        self.btn_reset.setObjectName("btn_neutral")
        self.btn_reset.setFixedHeight(42)
        self.btn_reset.clicked.connect(self._reset)

        self.btn_lap = QPushButton("⊕  Volta")
        self.btn_lap.setObjectName("btn_neutral")
        self.btn_lap.setFixedHeight(42)
        self.btn_lap.clicked.connect(self._lap)

        btn_row.addWidget(self.btn_start)
        btn_row.addWidget(self.btn_reset)
        btn_row.addWidget(self.btn_lap)
        root.addLayout(btn_row)
        root.addSpacing(20)

        # Optional countdown setup
        grp = QGroupBox("CONTAR A PARTIR DE")
        g_lay = QGridLayout(grp)
        g_lay.setSpacing(10)

        for i, (lbl_txt, max_v) in enumerate(
            [("Dias", 999), ("Horas", 23), ("Minutos", 59), ("Segundos", 59)]
        ):
            g_lay.addWidget(QLabel(lbl_txt), 0, i, alignment=Qt.AlignmentFlag.AlignCenter)
            spin = QSpinBox()
            spin.setRange(0, max_v)
            spin.setFixedWidth(72)
            spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            g_lay.addWidget(spin, 1, i, alignment=Qt.AlignmentFlag.AlignCenter)
            setattr(self, f"spin_{lbl_txt.lower()}", spin)

        btn_set = QPushButton("Definir tempo inicial")
        btn_set.setObjectName("btn_neutral")
        btn_set.clicked.connect(self._set_initial)
        g_lay.addWidget(btn_set, 2, 0, 1, 4)

        root.addWidget(grp)
        root.addSpacing(16)

        # Lap list
        self.lbl_lap_title = label("VOLTAS", "lbl_section")
        root.addWidget(self.lbl_lap_title)
        root.addSpacing(6)

        self.laps_layout = QVBoxLayout()
        self.laps_layout.setSpacing(4)
        root.addLayout(self.laps_layout)

        root.addStretch()

    def _ms_to_str(self, ms):
        total_s = ms // 1000
        days = total_s // 86400
        hours = (total_s % 86400) // 3600
        mins = (total_s % 3600) // 60
        secs = total_s % 60
        millis = ms % 1000
        return days, f"{hours:02d}:{mins:02d}:{secs:02d}", f".{millis:03d}"

    def _update_display(self):
        days, t, ms = self._ms_to_str(self.elapsed_ms)
        self.lbl_days.setText(f"DIA {days}" if days > 0 else "")
        self.lbl_time.setText(t)
        self.lbl_ms.setText(ms)

    def _tick(self):
        self.elapsed_ms += 10
        self._update_display()

    def _toggle(self):
        if self.running:
            self.timer.stop()
            self.running = False
            self.btn_start.setText("▶  Continuar")
            self.btn_start.setObjectName("btn_primary")
            self.lbl_status.setText("PAUSADO")
            self.lbl_status.setStyleSheet(f"color: {ACCENT};")
        else:
            self.timer.start()
            self.running = True
            self.btn_start.setText("⏸  Pausar")
            self.btn_start.setObjectName("btn_danger")
            self.lbl_status.setText("RODANDO")
            self.lbl_status.setStyleSheet(f"color: {SUCCESS};")
        self.btn_start.setStyle(self.btn_start.style())

    def _reset(self):
        self.timer.stop()
        self.running = False
        self.elapsed_ms = 0
        self._update_display()
        self.btn_start.setText("▶  Iniciar")
        self.btn_start.setObjectName("btn_primary")
        self.btn_start.setStyle(self.btn_start.style())
        self.lbl_status.setText("PARADO")
        self.lbl_status.setStyleSheet(f"color: {MUTED};")
        for i in reversed(range(self.laps_layout.count())):
            w = self.laps_layout.itemAt(i).widget()
            if w:
                w.deleteLater()
        self.laps.clear()

    def _lap(self):
        if not self.running:
            return
        idx = len(self.laps) + 1
        _, t, ms = self._ms_to_str(self.elapsed_ms)
        self.laps.append(self.elapsed_ms)

        row = QFrame()
        row.setStyleSheet(f"background:{SURFACE}; border-radius:6px; padding:2px;")
        rl = QHBoxLayout(row)
        rl.setContentsMargins(12, 6, 12, 6)
        n = QLabel(f"#{idx:02d}")
        n.setStyleSheet(f"color:{MUTED}; font-size:12px;")
        v = QLabel(f"{t}{ms}")
        v.setStyleSheet(f"color:{TEXT}; font-size:13px; font-family:monospace;")
        rl.addWidget(n)
        rl.addStretch()
        rl.addWidget(v)
        self.laps_layout.addWidget(row)

    def _set_initial(self):
        d = self.spin_dias.value()
        h = self.spin_horas.value()
        m = self.spin_minutos.value()
        s = self.spin_segundos.value()
        self.elapsed_ms = ((d * 86400 + h * 3600 + m * 60 + s) * 1000)
        self._update_display()


# ── Countdown Timer Tab ───────────────────────────────────────────────────────
class CountdownTab(QWidget):
    def __init__(self):
        super().__init__()
        self.remaining_ms = 0
        self.running = False
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self._tick)
        self.audio_path = None
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(40, 36, 40, 36)
        root.setSpacing(0)

        # Big countdown display
        self.lbl_time = label("00:00:00", "lbl_big")
        self.lbl_time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self.lbl_time)

        self.lbl_status = label("AGUARDANDO", "lbl_status")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addSpacing(8)
        root.addWidget(self.lbl_status)

        root.addSpacing(24)
        root.addWidget(sep())
        root.addSpacing(20)

        # Time selector
        grp = QGroupBox("DEFINIR DURAÇÃO")
        g_lay = QGridLayout(grp)
        g_lay.setSpacing(10)

        for i, (lbl_txt, max_v) in enumerate(
            [("Dias", 999), ("Horas", 23), ("Minutos", 59), ("Segundos", 59)]
        ):
            g_lay.addWidget(QLabel(lbl_txt), 0, i, alignment=Qt.AlignmentFlag.AlignCenter)
            spin = QSpinBox()
            spin.setRange(0, max_v)
            spin.setFixedWidth(72)
            spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            g_lay.addWidget(spin, 1, i, alignment=Qt.AlignmentFlag.AlignCenter)
            setattr(self, f"spin_{lbl_txt.lower()}", spin)

        root.addWidget(grp)
        root.addSpacing(12)

        # Audio
        grp2 = QGroupBox("ALARME / MÚSICA")
        a_lay = QHBoxLayout(grp2)
        a_lay.setSpacing(8)
        self.lbl_audio = QLabel("Nenhum arquivo")
        self.lbl_audio.setStyleSheet(f"color:{MUTED}; font-size:12px;")
        self.lbl_audio.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        btn_browse = QPushButton("📂  Escolher")
        btn_browse.setObjectName("btn_neutral")
        btn_browse.setFixedHeight(36)
        btn_browse.clicked.connect(self._browse_audio)
        self.btn_preview = QPushButton("▶")
        self.btn_preview.setObjectName("btn_icon")
        self.btn_preview.setFixedSize(36, 36)
        self.btn_preview.clicked.connect(self._preview_audio)
        a_lay.addWidget(self.lbl_audio)
        a_lay.addWidget(btn_browse)
        a_lay.addWidget(self.btn_preview)
        root.addWidget(grp2)
        root.addSpacing(20)

        # Controls
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.btn_start = QPushButton("▶  Iniciar")
        self.btn_start.setObjectName("btn_primary")
        self.btn_start.setFixedHeight(42)
        self.btn_start.clicked.connect(self._toggle)

        self.btn_reset = QPushButton("↺  Resetar")
        self.btn_reset.setObjectName("btn_neutral")
        self.btn_reset.setFixedHeight(42)
        self.btn_reset.clicked.connect(self._reset)

        btn_row.addWidget(self.btn_start)
        btn_row.addWidget(self.btn_reset)
        root.addLayout(btn_row)
        root.addStretch()

        # Media player
        self.player = QMediaPlayer()
        self.audio_out = QAudioOutput()
        self.player.setAudioOutput(self.audio_out)
        self.audio_out.setVolume(0.9)

    def _ms_to_str(self, ms):
        total_s = ms // 1000
        days = total_s // 86400
        hours = (total_s % 86400) // 3600
        mins = (total_s % 3600) // 60
        secs = total_s % 60
        return days, f"{hours:02d}:{mins:02d}:{secs:02d}"

    def _update_display(self):
        days, t = self._ms_to_str(self.remaining_ms)
        day_str = f"DIA {days}  " if days > 0 else ""
        self.lbl_time.setText(f"{day_str}{t}")

    def _tick(self):
        self.remaining_ms -= 100
        if self.remaining_ms <= 0:
            self.remaining_ms = 0
            self._update_display()
            self._alarm()
            return
        self._update_display()

    def _toggle(self):
        if not self.running:
            if self.remaining_ms == 0:
                d = self.spin_dias.value()
                h = self.spin_horas.value()
                m = self.spin_minutos.value()
                s = self.spin_segundos.value()
                self.remaining_ms = (d * 86400 + h * 3600 + m * 60 + s) * 1000
                if self.remaining_ms == 0:
                    return
            self.timer.start()
            self.running = True
            self.btn_start.setText("⏸  Pausar")
            self.btn_start.setObjectName("btn_danger")
            self.btn_start.setStyle(self.btn_start.style())
            self.lbl_status.setText("CONTANDO")
            self.lbl_status.setStyleSheet(f"color:{SUCCESS};")
        else:
            self.timer.stop()
            self.running = False
            self.btn_start.setText("▶  Continuar")
            self.btn_start.setObjectName("btn_primary")
            self.btn_start.setStyle(self.btn_start.style())
            self.lbl_status.setText("PAUSADO")
            self.lbl_status.setStyleSheet(f"color:{ACCENT};")

    def _reset(self):
        self.timer.stop()
        self.running = False
        self.remaining_ms = 0
        self.lbl_time.setText("00:00:00")
        self.lbl_time.setStyleSheet("")
        self.btn_start.setText("▶  Iniciar")
        self.btn_start.setObjectName("btn_primary")
        self.btn_start.setStyle(self.btn_start.style())
        self.lbl_status.setText("AGUARDANDO")
        self.lbl_status.setStyleSheet(f"color:{MUTED};")
        self.player.stop()

    def _alarm(self):
        self.timer.stop()
        self.running = False
        self.lbl_status.setText("⏰  TEMPO ESGOTADO!")
        self.lbl_status.setStyleSheet(f"color:{DANGER}; font-size:14px;")
        self.lbl_time.setStyleSheet(f"color:{DANGER};")
        self.btn_start.setText("▶  Iniciar")
        self.btn_start.setObjectName("btn_primary")
        self.btn_start.setStyle(self.btn_start.style())
        if self.audio_path:
            self.player.setSource(QUrl.fromLocalFile(self.audio_path))
            self.player.play()

    def _browse_audio(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Escolher áudio", "",
            "Áudio (*.mp3 *.wav *.ogg *.flac *.aac);;Todos (*)"
        )
        if path:
            self.audio_path = path
            self.lbl_audio.setText(os.path.basename(path))
            self.lbl_audio.setStyleSheet(f"color:{TEXT}; font-size:12px;")

    def _preview_audio(self):
        if not self.audio_path:
            return
        if self.player.isPlaying():
            self.player.stop()
            self.btn_preview.setText("▶")
        else:
            self.player.setSource(QUrl.fromLocalFile(self.audio_path))
            self.player.play()
            self.btn_preview.setText("⏹")


# ── Clock Tab ─────────────────────────────────────────────────────────────────
class ClockTab(QWidget):
    def __init__(self):
        super().__init__()
        self.alarm_time = None
        self.alarm_enabled = False
        self.alarm_triggered = False
        self.audio_path = None
        self._build()
        self.tick_timer = QTimer()
        self.tick_timer.setInterval(500)
        self.tick_timer.timeout.connect(self._tick)
        self.tick_timer.start()
        self._tick()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(40, 36, 40, 36)
        root.setSpacing(0)

        self.lbl_clock = label("00:00:00", "lbl_clock")
        self.lbl_clock.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self.lbl_clock)

        self.lbl_date = label("", "lbl_date")
        self.lbl_date.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addSpacing(4)
        root.addWidget(self.lbl_date)

        root.addSpacing(28)
        root.addWidget(sep())
        root.addSpacing(24)

        # Alarm
        grp = QGroupBox("DESPERTADOR")
        a_lay = QVBoxLayout(grp)
        a_lay.setSpacing(10)

        time_row = QHBoxLayout()
        time_row.setSpacing(10)
        lbl_t = QLabel("Hora do alarme:")
        lbl_t.setStyleSheet(f"color:{MUTED}; font-size:13px;")
        self.alarm_edit = QTimeEdit()
        self.alarm_edit.setDisplayFormat("HH:mm:ss")
        self.alarm_edit.setFixedWidth(120)
        self.alarm_edit.setTime(QTime.currentTime())
        time_row.addWidget(lbl_t)
        time_row.addWidget(self.alarm_edit)
        time_row.addStretch()
        a_lay.addLayout(time_row)

        # Audio for alarm
        audio_row = QHBoxLayout()
        audio_row.setSpacing(8)
        lbl_a = QLabel("Música:")
        lbl_a.setStyleSheet(f"color:{MUTED}; font-size:13px;")
        self.lbl_alarm_audio = QLabel("Nenhum arquivo")
        self.lbl_alarm_audio.setStyleSheet(f"color:{MUTED}; font-size:12px;")
        self.lbl_alarm_audio.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        btn_browse = QPushButton("📂  Escolher")
        btn_browse.setObjectName("btn_neutral")
        btn_browse.setFixedHeight(34)
        btn_browse.clicked.connect(self._browse_alarm_audio)
        audio_row.addWidget(lbl_a)
        audio_row.addWidget(self.lbl_alarm_audio)
        audio_row.addWidget(btn_browse)
        a_lay.addLayout(audio_row)

        # Toggle
        toggle_row = QHBoxLayout()
        self.chk_alarm = QCheckBox("Ativar alarme")
        self.chk_alarm.stateChanged.connect(self._toggle_alarm)
        self.lbl_alarm_status = QLabel("Desligado")
        self.lbl_alarm_status.setStyleSheet(f"color:{MUTED}; font-size:12px;")
        toggle_row.addWidget(self.chk_alarm)
        toggle_row.addStretch()
        toggle_row.addWidget(self.lbl_alarm_status)
        a_lay.addLayout(toggle_row)

        root.addWidget(grp)
        root.addSpacing(16)

        # Dismiss button (hidden by default)
        self.btn_dismiss = QPushButton("⏹  Desligar alarme")
        self.btn_dismiss.setObjectName("btn_danger")
        self.btn_dismiss.setFixedHeight(42)
        self.btn_dismiss.clicked.connect(self._dismiss)
        self.btn_dismiss.hide()
        root.addWidget(self.btn_dismiss)

        root.addStretch()

        self.player = QMediaPlayer()
        self.audio_out = QAudioOutput()
        self.player.setAudioOutput(self.audio_out)
        self.audio_out.setVolume(1.0)

    def _tick(self):
        now = datetime.datetime.now()
        self.lbl_clock.setText(now.strftime("%H:%M:%S"))
        days_pt = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        months_pt = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
        d = days_pt[now.weekday()]
        m = months_pt[now.month - 1]
        self.lbl_date.setText(f"{d}, {now.day} de {m} de {now.year}")

        if self.alarm_enabled and not self.alarm_triggered:
            at = self.alarm_edit.time()
            if (at.hour() == now.hour and
                    at.minute() == now.minute and
                    at.second() == now.second):
                self._trigger_alarm()

    def _toggle_alarm(self, state):
        self.alarm_enabled = bool(state)
        self.alarm_triggered = False
        if self.alarm_enabled:
            at = self.alarm_edit.time()
            self.lbl_alarm_status.setText(f"Ativo — {at.toString('HH:mm:ss')}")
            self.lbl_alarm_status.setStyleSheet(f"color:{SUCCESS}; font-size:12px;")
        else:
            self.lbl_alarm_status.setText("Desligado")
            self.lbl_alarm_status.setStyleSheet(f"color:{MUTED}; font-size:12px;")
            self.player.stop()
            self.btn_dismiss.hide()
            self.lbl_clock.setStyleSheet("")

    def _trigger_alarm(self):
        self.alarm_triggered = True
        self.lbl_clock.setStyleSheet(f"color:{DANGER};")
        self.btn_dismiss.show()
        if self.audio_path:
            self.player.setSource(QUrl.fromLocalFile(self.audio_path))
            self.player.play()

    def _dismiss(self):
        self.player.stop()
        self.btn_dismiss.hide()
        self.lbl_clock.setStyleSheet("")
        self.chk_alarm.setChecked(False)

    def _browse_alarm_audio(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Escolher áudio", "",
            "Áudio (*.mp3 *.wav *.ogg *.flac *.aac);;Todos (*)"
        )
        if path:
            self.audio_path = path
            self.lbl_alarm_audio.setText(os.path.basename(path))
            self.lbl_alarm_audio.setStyleSheet(f"color:{TEXT}; font-size:12px;")


# ── Main Window ───────────────────────────────────────────────────────────────
class HivaxWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hivax")
        self.setMinimumSize(600, 600)
        self.resize(600, 600)
        self.setStyleSheet(STYLE)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Header
        header = QWidget()
        header.setFixedHeight(54)
        header.setStyleSheet(f"background:{SURFACE}; border-bottom:1px solid {BORDER};")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(24, 0, 24, 0)

        logo = QLabel("HIVAX")
        logo.setStyleSheet(
            f"color:{TEXT}; font-size:15px; font-weight:700; letter-spacing:3px;"
        )
        tagline = QLabel("Cronômetro & Alarme")
        tagline.setStyleSheet(f"color:{MUTED}; font-size:11px;")
        hl.addWidget(logo)
        hl.addStretch()
        hl.addWidget(tagline)
        root.addWidget(header)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        self.sw = StopwatchTab()
        self.cd = CountdownTab()
        self.clk = ClockTab()

        self.tabs.addTab(self.sw, "Cronômetro")
        self.tabs.addTab(self.cd, "Temporizador")
        self.tabs.addTab(self.clk, "Relógio")

        root.addWidget(self.tabs)

        # Footer
        footer = QWidget()
        footer.setFixedHeight(28)
        footer.setStyleSheet(f"background:{SURFACE}; border-top:1px solid {BORDER};")
        fl = QHBoxLayout(footer)
        fl.setContentsMargins(24, 0, 24, 0)
        ver = QLabel("v1.0.0")
        ver.setStyleSheet(f"color:{MUTED}; font-size:11px;")
        fl.addStretch()
        fl.addWidget(ver)
        root.addWidget(footer)


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Hivax")
    window = HivaxWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()