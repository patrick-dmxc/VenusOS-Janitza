# VenusOS module for support of Janitza Gridmeter/Analyzer - and maybe others
# 
# Community contribution by Patrick Grote
#
# Version 0.8 - 2026-04-23
# - Add Support for UMG 801
#
# Version 0.7 - 2026-02-02
# - Add Support for UMG 96-S2
#
# Version 0.6 - 2026-01-28
# - Add Support for UMG 103-CBM
#
# Version 0.5 - 2025-11-23
# - Add PowerFactor for Sum of L1, L2 and L3
#
# Version 0.4 - 2025-11-22
# - Add PowerFactor for L1, L2 and L3
# - Add Line to Line Voltage
#
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
from register import Reg_s16, Reg_u16, Reg_s32b, Reg_u32b, Reg_s64b, Reg_u64b, Reg_num, Reg_text

log = logging.getLogger()

class Reg_f32b(Reg_num):
    coding = ('>f', '>2H')
    count = 2
    rtype = float

class JANITZA_UMG_96RM(device.EnergyMeter):
    vendor_id = 'ja'
    vendor_name = 'Janitza'
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
        return f"{self.vendor_id}_{self.info['/Serial']}"

class JANITZA_UMG_96S2(device.EnergyMeter):
    vendor_id = 'ja'
    vendor_name = 'Janitza'
    productid = 0xFFFF
    productname = 'Janitza UMG 96 S2'
    min_timeout = 0.5
    age_limit_fast = 0
    refresh_time = 200
    nr_phases = 3


    def __init__(self, *args):
        super(JANITZA_UMG_96S2, self).__init__(*args)
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
                Reg_f32b(1012  + s, '/Ac/L%d/PowerFactor' % n,       1, '%.3f'),
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
                Reg_f32b(1018 , '/Ac/PowerFactor',       1, '%.3f'),
            ]
        except:
            log.info('Janitza device exception while Register f32')


        for n in range(1, phases + 1):
            gRegs += self.phase_regs(n)

        log.info('Janitza set Registers')
        self.data_regs = gRegs
        log.info('Janitza device init done')

    def get_ident(self):
        return f"{self.vendor_id}_{self.info['/Serial']}"

class JANITZA_UMG_96PQ(device.EnergyMeter):
    vendor_id = 'ja'
    vendor_name = 'Janitza'
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
        return f"{self.vendor_id}_{self.info['/Serial']}"

class JANITZA_UMG_103CBM(device.EnergyMeter):
    vendor_id = 'ja'
    vendor_name = 'Janitza'
    productid = 0xFFFF
    productname = 'Janitza UMG 103-CBM'
    min_timeout = 0.5
    age_limit_fast = 0
    refresh_time = 200
    nr_phases = 3


    def __init__(self, *args):
        super(JANITZA_UMG_103CBM, self).__init__(*args)
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
        return f"{self.vendor_id}_{self.info['/Serial']}"

class JANITZA_UMG_801_BASIC_GROUP(device.CustomName, device.SubDevice):
    vendor_id = 'ja'
    vendor_name = 'Janitza'
    productid = 0xFFFF
    productname = 'Janitza UMG 801 Basic Group'
    min_timeout = 0.5
    age_limit_fast = 0
    refresh_time = 200
    nr_phases = 3
    role_names = ['grid', 'pvinverter', 'genset', 'acload', 'evcharger',
                  'heatpump']
    allowed_roles = role_names
    default_role = 'grid'
    default_instance = 41
    position = None


    def __init__(self, parent, basic_group_num):
        super(JANITZA_UMG_801_BASIC_GROUP, self).__init__(parent, f'Basic Group{basic_group_num:02d}')
        self.basic_group_num = basic_group_num
        log.info(f'Janitza UMG 801 Basic Group {basic_group_num} __init__')
        self.productname = f'Janitza UMG 801 Basic Group {basic_group_num}'
        # store a default name separately to avoid inserting a plain string
        # into `self.info` (info entries must be Reg objects)
        self._default_name = f'Basic Group {basic_group_num}'
                
        try:
            self.info_regs = [
                Reg_u64b(4164, '/HardwareVersion'),
                Reg_text(4132, 32, '/FirmwareVersion'),
                Reg_u64b(4174, '/Serial'),
            ]
        except Exception as e:
            log.info(f'Exception while Janitza Probing Basic Group {self.basic_group_num}: {e}')
        log.info(f'Janitza UMG 801 Basic Group {self.basic_group_num} Probing done')


    def phase_regs(self, n):
        basic_group_num = self.basic_group_num
        log.info(f'Janitza UMG 801 Basic Group {basic_group_num} register Phase {n}')
        s = 0x0002 * (n - 1)

        pRegs = None
        voltageAddress=19000 + s
        voltageLineToLineAddress=19006 + s
        currentAddress=19012 + s
        powerAddress=19020 + s
        energyFwdAddress=19054 + s
        energyRevAddress=19070 + s
        powerFactorAddress=19044 + s
        if(basic_group_num > 1):
            baseOffset=(basic_group_num*100) + s
            log.info(f'Janitza UMG 801 Basic Group {basic_group_num} register Phase {n} with offset {baseOffset}')
            currentAddress=19000 + baseOffset
            powerAddress=19000 + baseOffset + 8
            energyFwdAddress=19000 + baseOffset + 38
            energyRevAddress=19000 + baseOffset + 54
            powerFactorAddress=19000 + baseOffset + 32
        else:
            log.info(f'Janitza UMG 801 Basic Group {basic_group_num} register Phase {n} with no offset')
            
        
        
        log.info(f'Janitza UMG 801 Basic Group {basic_group_num} Phase {n} Addresses:\nVoltage {voltageAddress}\nVoltageLineToLine {voltageLineToLineAddress}\nCurrent {currentAddress}\nPower {powerAddress}\nEnergyFwd {energyFwdAddress}\nEnergyRev {energyRevAddress}\nPowerFactor {powerFactorAddress}')
        try:
            pRegs = [
                Reg_f32b(voltageAddress,           '/Ac/L%d/Voltage' % n,           1, '%.3f V'),
                Reg_f32b(voltageLineToLineAddress, '/Ac/L%d/VoltageLineToLine' % n, 1, '%.3f V'),
                Reg_f32b(currentAddress,           '/Ac/L%d/Current' % n,           1, '%.3f A'),
                Reg_f32b(powerAddress,             '/Ac/L%d/Power' % n,             1, '%.3f W'),
                Reg_f32b(energyFwdAddress,         '/Ac/L%d/Energy/Forward' % n, 1000, '%.3f kWh'),
                Reg_f32b(energyRevAddress,         '/Ac/L%d/Energy/Reverse' % n, 1000, '%.3f kWh'),
                Reg_f32b(powerFactorAddress,       '/Ac/L%d/PowerFactor' % n,       1, '%.3f'),
            ]
        except:
            log.info(f'Janitza UMG 801 Basic Group {basic_group_num} register Phase {n} exception while Register f32')
        log.info(f'Janitza UMG 801 Basic Group {basic_group_num} register Phase {n} done')
        return pRegs


    def device_init(self):
        log.info(f'Janitza UMG 801 Basic Group {self.basic_group_num} device init')
        
        basic_group_num = self.basic_group_num
        phases = 3
        gRegs = None

        powerAddress=19026
        currentAddress=19018
        frequencyAddress=19050
        energyFwdAddress=19060        
        powerFactorAddress=19076
        if(basic_group_num > 1):
            log.info(f'Janitza UMG 801 Basic Group {basic_group_num} with offset')
            baseOffset=(basic_group_num*100)
            powerAddress=19000 + baseOffset + 14
            currentAddress=19000 + baseOffset + 6
            energyFwdAddress=19000 + baseOffset + 44
            powerFactorAddress=19000 + baseOffset + 60
        else:
            log.info(f'Janitza UMG 801 Basic Group {basic_group_num} with no offset')
            
        log.info(f'Janitza UMG 801 Basic Group {basic_group_num} Addresses:\nPower {powerAddress}\nCurrent {currentAddress}\nEnergyFwd {energyFwdAddress}\nPowerFactor {powerFactorAddress}')
        try:
            gRegs = [
                Reg_f32b(powerAddress,       '/Ac/Power',             1, '%.3f W'),
                Reg_f32b(currentAddress,     '/Ac/Current',           1, '%.3f A'),
                Reg_f32b(frequencyAddress,   '/Ac/Frequency',         1, '%.3f Hz'),
                Reg_f32b(energyFwdAddress,   '/Ac/Energy/Forward', 1000, '%.3f kWh'),
                Reg_f32b(powerFactorAddress, '/Ac/Energy/Reverse', 1000, '%.3f kWh'),
            ]
        except:
            log.info(f'Janitza UMG 801 Basic Group {basic_group_num} device exception while Register f32')
        
        for n in range(1, phases + 1):
            gRegs += self.phase_regs(n)

        self.data_regs = gRegs
        log.info(f'Janitza UMG 801 Basic Group {basic_group_num} device init done')

    def get_ident(self):
        return f"{self.parent.get_ident()}_BG{self.basic_group_num:02d}"

    def device_init_late(self):
        super().device_init_late()
        log.info(f'Janitza UMG 801 Basic Group {self.basic_group_num} device init late')
        self.settings['customname'] = f'Janitza UMG 801 Basic Group {self.basic_group_num}'

class JANITZA_UMG_801(device.CustomName, device.EnergyMeter):
    vendor_id = 'ja'
    vendor_name = 'Janitza'
    productid = 0xFFFF
    productname = 'Janitza UMG 801'
    min_timeout = 0.5
    age_limit_fast = 0
    refresh_time = 200
    nr_phases = 3


    def __init__(self, *args):
        super(JANITZA_UMG_801, self).__init__(*args)
        log.info('Janitza Probing')
        try:
            self.info_regs = [
                Reg_u64b(4164,     '/HardwareVersion'),
                Reg_text(4132, 32, '/FirmwareVersion'),
                Reg_u64b(4174,     '/Serial'),
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
            ]
        except:
            log.info('Janitza register Phase %d exception while Register f32'% n)
        log.info('Janitza register Phase %d done'% n)
        return pRegs


    def device_init(self):
        log.info('Janitza UMG 801 device init')
        self.read_info()

        phases = 3
        gRegs = None
        try:
            gRegs = [
                Reg_f32b(19050, '/Ac/Frequency',         1, '%.3f Hz'),
            ]
        except:
            log.info('Janitza device exception while Register f32')


        for n in range(1, phases + 1):
            gRegs += self.phase_regs(n)

        log.info('Janitza set Registers')
        self.data_regs = gRegs
        
        # Create SubDevices for each Basic Groub
        log.info('Janitza add Basic Groubs')
        try:
            for basic_group_num in range(1, 4):  # Basic Groubs 1-3                
                try:
                    subdevice = JANITZA_UMG_801_BASIC_GROUP(self, basic_group_num)
                    self.subdevices.append(subdevice)
                    log.info(f'Janitza added Basic Groubs {basic_group_num} as subdevice')
                except Exception as e:
                    log.info(f'Janitza exception adding Basic Groubs {basic_group_num}: {e}')
        except Exception as e:
            log.info(f'Janitza exception scanning Basic Groubs: {e}')
        
        log.info('Janitza UMG 801 device init done')

    def get_ident(self):
        return f"{self.vendor_id}_{self.info['/Serial']}"
    
    def device_init_late(self):
        super().device_init_late()
        log.info(f'Janitza UMG 801 device init late')
        self.settings['customname'] = 'Janitza UMG 801'

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

modelsRegister_20016 = {    
    5228001: {
        'model':    'UMG 103-CBM',
        'handler':  JANITZA_UMG_103CBM,
    },
    5234002: {
        'model':    'UMG 96 S2',
        'handler':  JANITZA_UMG_96S2,
    },
}

modelsRegister_4170 = {    
    2001299945: {
        'model':    'UMG 801',
        'handler':  JANITZA_UMG_801,
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

probe.add_handler(probe.ModelRegister(Reg_s32b(20016), modelsRegister_20016,
                                      methods=['rtu','tcp'],
                                      rates=[115200],
                                      units=[1]))

probe.add_handler(probe.ModelRegister(Reg_u64b(4170), modelsRegister_4170,
                                      methods=['rtu','tcp'],
                                      rates=[115200],
                                      units=[1]))
