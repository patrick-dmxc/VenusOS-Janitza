# VenusOS module for support of Janitza UMG 96 Analyzer - and maybe others
# 
# Community contribution by Patrick Grote
# Version 0.5 - 2025-11-23
# - Add PowerFactor for Sum of L1, L2 and L3
# Version 0.4 - 2025-11-22
# - Add PowerFactor for L1, L2 and L3
# - Add Line to Line Voltage
# Version 0.2 - 2024-01-18
# - Switched Identifyer to ProductNumber
# - Added other Models
# - Fix Hardware-Version
# - Increase resolution
#
# Version 0.1 - 2023-05-22

import logging
import device
import probe
from register import Reg_s16, Reg_u16, Reg_s32b, Reg_u32b, Reg_num

log = logging.getLogger()
        
#class Reg_f32b(Reg_num): # Works in 3.10
#    def __init__(self, base, *args, **kwargs):
#        super(Reg_f32b, self).__init__(base, 2, *args, **kwargs)
#        self.coding = ('>f', '>2H')
#        self.scale = float(self.scale)

### Untested 3.11 & 3.12

class Reg_f32b(Reg_num): # Works in 3.13
    coding = ('>f', '>2H')
    count = 2
    rtype = float

class JANITZA_UMG_96RM(device.EnergyMeter):
    productid = 0xFFFF
    productname = 'Janitza UMG 96 RM'
    min_timeout = 0.5
    age_limit_fast = 0
    refresh_time = 200
    nr_phases = 3


    def __init__(self, *args):
        super(JANITZA_UMG_96RM, self).__init__(*args)
        log.info('Janitza Probing')
        try:
            self.info_regs = [
                Reg_u16(751, '/HardwareVersion'),
                Reg_u16(750, '/FirmwareVersion'),
                Reg_u32b(754, '/Serial'),
            ]
        except:
            log.info('Exception while Janitza Probing')
        log.info('Janitza Probing done')

    def phase_regs(self, n):
        log.info('Janitza register Phase %d' % n)
        s = 0x0002 * (n - 1)

        pRegs = None
        try:
            pRegs = [
                Reg_f32b(19000 + s, '/Ac/L%d/Voltage' % n,           1, '%.3f V'),
                Reg_f32b(19006 + s, '/Ac/L%d/VoltageLineToLine' % n, 1, '%.3f V'),
                Reg_f32b(19012 + s, '/Ac/L%d/Current' % n,           1, '%.3f A'),
                Reg_f32b(19020 + s, '/Ac/L%d/Power' % n,             1, '%.3f W'),
                Reg_f32b(19062 + s, '/Ac/L%d/Energy/Forward' % n, 1000, '%.3f kWh'),
                Reg_f32b(19068 + s, '/Ac/L%d/Energy/Reverse' % n, 1000, '%.3f kWh'),
                Reg_f32b(828   + s, '/Ac/L%d/PowerFactor' % n,       1, '%.3f'),
            ]
        except:
            log.info('Janitza register Phase %d exception while Register f32'% n)
        log.info('Janitza register Phase %d done'% n)
        return pRegs


    def device_init(self):
        log.info('Janitza device init')
        self.read_info()

        phases = 3
        gRegs = None
        try:
            gRegs = [
                Reg_f32b(19026, '/Ac/Power',             1, '%.3f W'),
                Reg_f32b(19018, '/Ac/Current',           1, '%.3f A'),
                Reg_f32b(19050, '/Ac/Frequency',         1, '%.3f Hz'),
                Reg_f32b(19068, '/Ac/Energy/Forward', 1000, '%.3f kWh'),
                Reg_f32b(19076, '/Ac/Energy/Reverse', 1000, '%.3f kWh'),
                Reg_f32b(834  , '/Ac/PowerFactor',       1, '%.3f'),
            ]
        except:
            log.info('Janitza device exception while Register f32')


        for n in range(1, phases + 1):
            gRegs += self.phase_regs(n)

        log.info('Janitza set Registers')
        self.data_regs = gRegs
        log.info('Janitza device init done')

    def get_ident(self):
        return 'cg_%s' % self.info['/Serial']

class JANITZA_UMG_96PQ(device.EnergyMeter):
    productid = 0xFFFF
    productname = 'Janitza UMG 96 PQ'
    min_timeout = 0.5
    age_limit_fast = 0
    refresh_time = 200
    nr_phases = 3


    def __init__(self, *args):
        super(JANITZA_UMG_96PQ, self).__init__(*args)
        log.info('Janitza Probing')
        try:
            self.info_regs = [
                Reg_u16(20037, '/HardwareVersion'),
                Reg_u16(20009, '/FirmwareVersion'),
                Reg_u32b(911, '/Serial'),
            ]
        except:
            log.info('Exception while Janitza Probing')
        log.info('Janitza Probing done')

    def phase_regs(self, n):
        log.info('Janitza register Phase %d' % n)
        s = 0x0002 * (n - 1)

        pRegs = None
        try:
            pRegs = [
                Reg_f32b(19000 + s, '/Ac/L%d/Voltage' % n,           1, '%.3f V'),
                Reg_f32b(19006 + s, '/Ac/L%d/VoltageLineToLine' % n, 1, '%.3f V'),
                Reg_f32b(19012 + s, '/Ac/L%d/Current' % n,           1, '%.3f A'),
                Reg_f32b(19020 + s, '/Ac/L%d/Power' % n,             1, '%.3f W'),
                Reg_f32b(19062 + s, '/Ac/L%d/Energy/Forward' % n, 1000, '%.3f kWh'),
                Reg_f32b(19068 + s, '/Ac/L%d/Energy/Reverse' % n, 1000, '%.3f kWh'),
                Reg_f32b(1294   + s, '/Ac/L%d/PowerFactor' % n,      1, '%.3f'),
            ]
        except:
            log.info('Janitza register Phase %d exception while Register f32'% n)
        log.info('Janitza register Phase %d done'% n)
        return pRegs


    def device_init(self):
        log.info('Janitza device init')
        self.read_info()

        phases = 3
        gRegs = None
        try:
            gRegs = [
                Reg_f32b(19026, '/Ac/Power',             1, '%.3f W'),
                Reg_f32b(19018, '/Ac/Current',           1, '%.3f A'),
                Reg_f32b(19050, '/Ac/Frequency',         1, '%.3f Hz'),
                Reg_f32b(19068, '/Ac/Energy/Forward', 1000, '%.3f kWh'),
                Reg_f32b(19076, '/Ac/Energy/Reverse', 1000, '%.3f kWh'),
                Reg_f32b(1300 , '/Ac/PowerFactor',       1, '%.3f'),
            ]
        except:
            log.info('Janitza device exception while Register f32')


        for n in range(1, phases + 1):
            gRegs += self.phase_regs(n)

        log.info('Janitza set Registers')
        self.data_regs = gRegs
        log.info('Janitza device init done')

    def get_ident(self):
        return 'cg_%s' % self.info['/Serial']

class JANITZA_UMG_103CBM(device.EnergyMeter):
    productid = 0xFFFF
    productname = 'Janitza UMG 103-CBM'
    min_timeout = 0.5
    age_limit_fast = 0
    refresh_time = 200
    nr_phases = 3


    def __init__(self, *args):
        super(JANITZA_UMG_96PQ, self).__init__(*args)
        log.info('Janitza Probing')
        try:
            self.info_regs = [
                Reg_u16(914, '/HardwareVersion'),
                Reg_u16(913, '/FirmwareVersion'),
                Reg_u32b(911, '/Serial'),
            ]
        except:
            log.info('Exception while Janitza Probing')
        log.info('Janitza Probing done')

    def phase_regs(self, n):
        log.info('Janitza register Phase %d' % n)
        s = 0x0002 * (n - 1)

        pRegs = None
        try:
            pRegs = [
                Reg_f32b(19000 + s, '/Ac/L%d/Voltage' % n,           1, '%.3f V'),
                Reg_f32b(19006 + s, '/Ac/L%d/VoltageLineToLine' % n, 1, '%.3f V'),
                Reg_f32b(19012 + s, '/Ac/L%d/Current' % n,           1, '%.3f A'),
                Reg_f32b(19020 + s, '/Ac/L%d/Power' % n,             1, '%.3f W'),
                Reg_f32b(19062 + s, '/Ac/L%d/Energy/Forward' % n, 1000, '%.3f kWh'),
                Reg_f32b(19068 + s, '/Ac/L%d/Energy/Reverse' % n, 1000, '%.3f kWh'),
                Reg_f32b(1294   + s, '/Ac/L%d/PowerFactor' % n,      1, '%.3f'),
            ]
        except:
            log.info('Janitza register Phase %d exception while Register f32'% n)
        log.info('Janitza register Phase %d done'% n)
        return pRegs


    def device_init(self):
        log.info('Janitza device init')
        self.read_info()

        phases = 3
        gRegs = None
        try:
            gRegs = [
                Reg_f32b(19026, '/Ac/Power',             1, '%.3f W'),
                Reg_f32b(19018, '/Ac/Current',           1, '%.3f A'),
                Reg_f32b(19050, '/Ac/Frequency',         1, '%.3f Hz'),
                Reg_f32b(19068, '/Ac/Energy/Forward', 1000, '%.3f kWh'),
                Reg_f32b(19076, '/Ac/Energy/Reverse', 1000, '%.3f kWh'),
                Reg_f32b(1300 , '/Ac/PowerFactor',       1, '%.3f'),
            ]
        except:
            log.info('Janitza device exception while Register f32')


        for n in range(1, phases + 1):
            gRegs += self.phase_regs(n)

        log.info('Janitza set Registers')
        self.data_regs = gRegs
        log.info('Janitza device init done')

    def get_ident(self):
        return 'cg_%s' % self.info['/Serial']

models96RM = {
    5222036: {
        'model':    'UMG 96 RM-E-RCM',
        'handler':  JANITZA_UMG_96RM,
    },
    5222061: {
        'model':    'UMG 96 RM',
        'handler':  JANITZA_UMG_96RM,
    },
    5222062: {
        'model':    'UMG 96 RM-E',
        'handler':  JANITZA_UMG_96RM,
    },
    5222063: {
        'model':    'UMG 96 RM-E',
        'handler':  JANITZA_UMG_96RM,
    },
    5222064: {
        'model':    'UMG 96 RM-P',
        'handler':  JANITZA_UMG_96RM,
    },
    5222065: {
        'model':    'UMG 96 RM-P',
        'handler':  JANITZA_UMG_96RM,
    },
    5222066: {
        'model':    'UMG 96 RM-CBM',
        'handler':  JANITZA_UMG_96RM,
    },
    5222067: {
        'model':    'UMG 96 RM-CBM',
        'handler':  JANITZA_UMG_96RM,
    },
    5222068: {
        'model':    '???',
        'handler':  JANITZA_UMG_96RM,
    },
    5222069: {
        'model':    'UMG 96 RM-M',
        'handler':  JANITZA_UMG_96RM,
    },
    5222070: {
        'model':    'UMG 96 RM',
        'handler':  JANITZA_UMG_96RM,
    },
    5222071: {
        'model':    '???',
        'handler':  JANITZA_UMG_96RM,
    },
    5222072: {
        'model':    '???',
        'handler':  JANITZA_UMG_96RM,
    },
    5222073: {
        'model':    'UMG 96 RM-M',
        'handler':  JANITZA_UMG_96RM,
    },
    5222090: {
        'model':    'UMG 96 RM-PN',
        'handler':  JANITZA_UMG_96RM,
    },
    5222091: {
        'model':    'UMG 96 RM-PN',
        'handler':  JANITZA_UMG_96RM,
    },
}

models96PQ = {    
    45030080: {
        'model':    'UMG 96 PQ-L',
        'handler':  JANITZA_UMG_96PQ,
    },
}

models103CBM = {    
    5228001: {
        'model':    'UMG 103-CBM',
        'handler':  JANITZA_UMG_103CBM,
    },
}

probe.add_handler(probe.ModelRegister(Reg_s32b(769), models96RM,
                                      methods=['rtu','tcp'],
                                      rates=[115200],
                                      units=[1]))

probe.add_handler(probe.ModelRegister(Reg_s32b(194), models96PQ,
                                      methods=['rtu','tcp'],
                                      rates=[115200],
                                      units=[1]))


probe.add_handler(probe.ModelRegister(Reg_s32b(20016), models103CBM,
                                      methods=['rtu','tcp'],
                                      rates=[115200],
                                      units=[1]))
