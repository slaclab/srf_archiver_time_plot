from PyQt5.QtCore import pyqtSlot
from pydm import Display
from lcls_tools.superconducting.sc_linac_utils import ALL_CRYOMODULES
from lcls_tools.superconducting.scLinac import CRYOMODULE_OBJECTS


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
        
    def update_time(self):
        self.ui.plot.setTimeSpan(self.ui.second_spinbox.value())
    
    def update(self):
        self.ui.plot.clearCurves()
        
        cm_obj = CRYOMODULE_OBJECTS[self.ui.cm_combobox.currentText()]
        
        for cavity in cm_obj.cavities.values():
            self.ui.plot.addYChannel(y_channel=cavity.pv_addr(self.ui.suffix_line_edit.text()),
                                     useArchiveData=True)
            
        self.ui.plot.setAutoRangeY(self.ui.autoscale_checkbox.isChecked())
        self.ui.plot.setMinYRange(self.ui.ymin_spinbox.value())
        self.ui.plot.setMaxYRange(self.ui.ymax_spinbox.value())