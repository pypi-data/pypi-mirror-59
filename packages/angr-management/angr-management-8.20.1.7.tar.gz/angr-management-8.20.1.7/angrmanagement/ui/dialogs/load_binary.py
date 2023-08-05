import os
import logging

from PySide2.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QPushButton, QCheckBox, QFrame, \
    QGroupBox, QListWidgetItem, QListWidget, QMessageBox
from PySide2.QtCore import Qt

import cle


l = logging.getLogger('dialogs.load_binary')


class LoadBinaryError(Exception):
    pass


class LoadBinary(QDialog):
    def __init__(self, partial_ld, parent=None):
        super(LoadBinary, self).__init__(parent)

        # initialization
        self.file_path = partial_ld.main_object.binary
        self.option_widgets = { }

        # return values
        self.cfg_args = None
        self.load_options = None

        self.setWindowTitle('Load a new binary')

        self.main_layout = QVBoxLayout()

        self._init_widgets()

        self._try_loading(partial_ld)

        self.setLayout(self.main_layout)

    @property
    def filename(self):
        return os.path.basename(self.file_path)

    #
    # Private methods
    #

    def _try_loading(self, partial_ld):
        deps = [ ]
        processed_objects = set()
        for ident, obj in partial_ld._satisfied_deps.items():
            if obj is partial_ld._kernel_object or \
                    obj is partial_ld._tls_object or \
                    obj is partial_ld._extern_object or \
                    obj is partial_ld.main_object:
                continue
            if obj in processed_objects:
                continue
            deps.append(ident)
            processed_objects.add(obj)

        dep_list = self.option_widgets['dep_list']  # type: QListWidget
        for dep in deps:
            dep_item = QListWidgetItem(dep)
            dep_item.setData(Qt.CheckStateRole, Qt.Unchecked)
            dep_list.addItem(dep_item)

    def _init_widgets(self):

        # filename

        filename_caption = QLabel(self)
        filename_caption.setText('File name:')

        filename = QLabel(self)
        filename.setText(self.filename)

        filename_layout = QHBoxLayout()
        filename_layout.addWidget(filename_caption)
        filename_layout.addWidget(filename)
        self.main_layout.addLayout(filename_layout)

        # central tab

        tab = QTabWidget()
        self._init_central_tab(tab)

        self.main_layout.addWidget(tab)

        # buttons

        ok_button = QPushButton(self)
        ok_button.setText('OK')
        ok_button.clicked.connect(self._on_ok_clicked)

        cancel_button = QPushButton(self)
        cancel_button.setText('Cancel')
        cancel_button.clicked.connect(self._on_cancel_clicked)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)

        self.main_layout.addLayout(buttons_layout)

    def _init_central_tab(self, tab):
        self._init_load_options_tab(tab)
        self._init_cfg_options_tab(tab)

    def _init_load_options_tab(self, tab):

        # auto load libs

        auto_load_libs = QCheckBox(self)
        auto_load_libs.setText("Automatically load all libraries")
        auto_load_libs.setChecked(False)
        self.option_widgets['auto_load_libs'] = auto_load_libs

        # dependencies list

        dep_group = QGroupBox("Dependencies")
        dep_list = QListWidget(self)
        self.option_widgets['dep_list'] = dep_list

        sublayout = QVBoxLayout()
        sublayout.addWidget(dep_list)
        dep_group.setLayout(sublayout)

        layout = QVBoxLayout()
        layout.addWidget(auto_load_libs)
        layout.addWidget(dep_group)
        layout.addStretch(0)

        frame = QFrame(self)
        frame.setLayout(layout)
        tab.addTab(frame, "Loading Options")

    def _init_cfg_options_tab(self, tab):
        resolve_indirect_jumps = QCheckBox(self)
        resolve_indirect_jumps.setText('Resolve indirect jumps')
        resolve_indirect_jumps.setChecked(True)
        self.option_widgets['resolve_indirect_jumps'] = resolve_indirect_jumps

        collect_data_refs = QCheckBox(self)
        collect_data_refs.setText('Collect cross-references and infer data types')
        collect_data_refs.setChecked(True)
        self.option_widgets['collect_data_refs'] = collect_data_refs

        layout = QVBoxLayout()
        layout.addWidget(resolve_indirect_jumps)
        layout.addWidget(collect_data_refs)
        layout.addStretch(0)
        frame = QFrame(self)
        frame.setLayout(layout)
        tab.addTab(frame, 'CFG Options')

    #
    # Event handlers
    #

    def _on_ok_clicked(self):

        force_load_libs = [ ]
        skip_libs = set()

        dep_list = self.option_widgets['dep_list']  # type: QListWidget
        for i in range(dep_list.count()):
            item = dep_list.item(i)  # type: QListWidgetItem
            if item.checkState() == Qt.Checked:
                force_load_libs.append(item.text())
            else:
                skip_libs.add(item.text())

        self.load_options = { }
        self.load_options['auto_load_libs'] = self.option_widgets['auto_load_libs'].isChecked()
        if force_load_libs:
            self.load_options['force_load_libs'] = force_load_libs
        if skip_libs:
            self.load_options['skip_libs'] = skip_libs

        self.cfg_args = {
            'resolve_indirect_jumps': self.option_widgets['resolve_indirect_jumps'].isChecked(),
            'collect_data_references': self.option_widgets['collect_data_refs'].isChecked(),
        }

        self.close()

    def _on_cancel_clicked(self):
        self.cfg_args = None
        self.close()

    @staticmethod
    def run(partial_ld):
        try:
            dialog = LoadBinary(partial_ld)
            dialog.setModal(True)
            dialog.exec_()

            if dialog.cfg_args is not None:
                # load the binary
                return dialog.load_options, dialog.cfg_args
        except LoadBinaryError:
            pass
        return None, None
