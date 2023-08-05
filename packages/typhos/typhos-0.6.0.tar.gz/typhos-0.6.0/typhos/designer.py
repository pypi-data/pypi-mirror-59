import logging

from pydm.widgets.qtplugin_base import qtplugin_factory

from .signal import TyphosSignalPanel
from .display import TyphosDeviceDisplay
from .func import TyphosMethodButton
from .positioner import TyphosPositionerWidget

logger = logging.getLogger(__name__)
logger.info("Loading Typhos QtDesigner plugins ...")

group_name = 'Typhos Widgets'
TyphosSignalPanelPlugin = qtplugin_factory(TyphosSignalPanel,
                                           group=group_name)
TyphosDeviceDisplayPlugin = qtplugin_factory(TyphosDeviceDisplay,
                                             group=group_name)
TyphosMethodButtonPlugin = qtplugin_factory(TyphosMethodButton,
                                            group=group_name)
TyphosPositionerWidgetPlugin = qtplugin_factory(TyphosPositionerWidget,
                                                group=group_name)
