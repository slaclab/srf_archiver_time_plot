from typing import Dict

from PyQt5.QtWidgets import QCheckBox
from lcls_tools.superconducting.scLinac import CRYOMODULE_OBJECTS
from lcls_tools.superconducting.sc_linac_utils import ALL_CRYOMODULES
from pydm import Display


class Plot(Display):
    def ui_filename(self):
        return "timeplot.ui"
    
    def __init__(self, parent=None, args=None):
        super().__init__(parent=parent, args=args, ui_filename="timeplot.ui")
        
        self.ui.cm_combobox.addItems(ALL_CRYOMODULES)
        self.ui.suffix_line_edit.returnPressed.connect(self.update)
        self.ui.cm_combobox.currentIndexChanged.connect(self.update)
        self.ui.second_spinbox.valueChanged.connect(self.update_time)
        self.ui.plot.setShowLegend(True)
        self.ui.autoscale_checkbox.stateChanged.connect(self.update)
        self.ui.ymin_spinbox.valueChanged.connect(self.update)
        self.ui.ymax_spinbox.valueChanged.connect(self.update)
        
        self.cavity_checkbox_map: Dict[QCheckBox, int] = {self.ui.c1_checkbox: 1,
                                                          self.ui.c2_checkbox: 2,
                                                          self.ui.c3_checkbox: 3,
                                                          self.ui.c4_checkbox: 4,
                                                          self.ui.c5_checkbox: 5,
                                                          self.ui.c6_checkbox: 6,
                                                          self.ui.c7_checkbox: 7,
                                                          self.ui.c8_checkbox: 8}
    
    @property
    def selected_cavities(self):
        selected_cavities = []
        
        for checkbox, cav_num in self.cavity_checkbox_map.items():
            if checkbox.isChecked():
                selected_cavities.append(cav_num)
        
        return selected_cavities
    
    def update_time(self):
        self.ui.plot.setTimeSpan(self.ui.second_spinbox.value())
    
    def update(self):
        self.ui.plot.clearCurves()
        
        cm_obj = CRYOMODULE_OBJECTS[self.ui.cm_combobox.currentText()]
        
        for cav_num in self.selected_cavities:
            cavity = cm_obj.cavities[cav_num]
            self.ui.plot.addYChannel(y_channel=cavity.pv_addr(self.ui.suffix_line_edit.text()),
                                     useArchiveData=True)
        
        self.ui.plot.setAutoRangeY(self.ui.autoscale_checkbox.isChecked())
        self.ui.plot.setMinYRange(self.ui.ymin_spinbox.value())
        self.ui.plot.setMaxYRange(self.ui.ymax_spinbox.value())
