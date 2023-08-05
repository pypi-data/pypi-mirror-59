#!/usr/bin/env python
# -*- coding: utf-8 -*-
############
# Standard #
############
import logging
import time
from collections import OrderedDict
import pytest

###############
# Third Party #
###############
import numpy as np
from ophyd.device import Device

########
# SLAC #
########

##########
# Module #
##########
from .conftest import get_classes_in_module, fake_device
from hxrsnd import rtd

logger = logging.getLogger(__name__)

@pytest.mark.parametrize("dev", get_classes_in_module(rtd, Device))
def test_rtd_devices_instantiate_and_run_ophyd_functions(dev):
    device = fake_device(dev)
    assert(isinstance(device.read(), OrderedDict))
    assert(isinstance(device.read_configuration(), OrderedDict))
