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
            log.error('Exception while Janitza Probing')
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
            log.error('Janitza register Phase %d exception while Register f32'% n)
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
            log.error('Janitza device exception while Register f32')


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
            log.error('Exception while Janitza Probing')
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
            log.error('Janitza register Phase %d exception while Register f32'% n)
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
            log.error('Janitza device exception while Register f32')


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
            log.error('Exception while Janitza Probing')
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
            log.error('Janitza register Phase %d exception while Register f32'% n)
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
            log.error('Janitza device exception while Register f32')


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
            log.error('Exception while Janitza Probing')
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
            log.error('Janitza register Phase %d exception while Register f32'% n)
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
            log.error('Janitza device exception while Register f32')


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
    role_names = ['grid', 'pvinverter', 'genset', 'acload', 'evcharger',
                  'heatpump']
    allowed_roles = role_names
    default_role = 'grid'
    default_instance = 41
    position = None


    def __init__(self, parent, basic_group_num, isL4MeasureNeutral = False, isL4SinglePhase = False, phaseSetting = None):
        l4NameFlag = ' L4' if isL4SinglePhase is True else ''
        super(JANITZA_UMG_801_BASIC_GROUP, self).__init__(parent, f'Basic Group{basic_group_num:02d}{l4NameFlag}')        
        nr_phases = 3 if isL4SinglePhase is False else 1
        self.basic_group_num = basic_group_num
        self.enabled = True        
        self.isL4MeasureNeutral = isL4MeasureNeutral
        self.isL4SinglePhase = isL4SinglePhase
        self.phaseSetting = phaseSetting if phaseSetting in (1, 2, 3) else min(max(basic_group_num, 1), 3)
        log.info(f'Janitza UMG 801 Basic Group {basic_group_num}{l4NameFlag} __init__')
        self.productname = f'Janitza UMG 801 Basic Group {basic_group_num}{l4NameFlag}'
        # store a default name separately to avoid inserting a plain string
        # into `self.info` (info entries must be Reg objects)
        self._default_name = f'Basic Group {basic_group_num}{l4NameFlag}'
                
        try:
            self.info_regs = [
                Reg_u64b(4164, '/HardwareVersion'),
                Reg_text(4132, 32, '/FirmwareVersion'),
                Reg_u64b(4174, '/Serial'),
            ]
        except Exception as e:
            log.error(f'Exception while Janitza Probing Basic Group {self.basic_group_num}{l4NameFlag}: {e}')
        log.info(f'Janitza UMG 801 Basic Group {self.basic_group_num}{l4NameFlag} Probing done')


    def phase_regs(self, n):
        basic_group_num = self.basic_group_num
        l4NameFlag = ' L4' if self.isL4SinglePhase is True else ''
        if self.isL4SinglePhase is True:
            n = self.phaseSetting
        log.info(f'Janitza UMG 801 Basic Group {basic_group_num}{l4NameFlag} register Phase {n}')
        s = 0x0002 * (n - 1)

        pRegs = None
        baseAddress=19000
        voltageAddress=19000 + s
        voltageLineToLineAddress=19006 + s
        currentAddress=19012 + s
        powerAddress=19020 + s
        energyFwdAddress=19062 + s
        energyRevAddress=19070 + s
        powerFactorAddress=19044 + s
        if(basic_group_num > 1):
            baseOffset=(basic_group_num*100) + s
            log.info(f'Janitza UMG 801 Basic Group {basic_group_num}{l4NameFlag} register Phase {n} with offset {baseOffset}')
            currentAddress=baseAddress + baseOffset
            powerAddress=baseAddress + baseOffset + 8
            energyFwdAddress=baseAddress + baseOffset + 46
            energyRevAddress=baseAddress + baseOffset + 54
            powerFactorAddress=baseAddress + baseOffset + 32
        else:
            log.info(f'Janitza UMG 801 Basic Group {basic_group_num}{l4NameFlag} register Phase {n} with no offset')           

        if self.isL4SinglePhase is True:
            baseAddress=21500
            baseOffset=(basic_group_num - 1) * 24
            log.info(f'Janitza UMG 801 Basic Group {basic_group_num}{l4NameFlag} register on BaseAddress {baseAddress} Phase {n} with offset {baseOffset}')
            powerAddress=baseAddress + baseOffset
            energyFwdAddress=baseAddress + baseOffset + 10
            energyRevAddress=baseAddress + baseOffset + 12
            powerFactorAddress=baseAddress + baseOffset + 6
            
        
        log.info(f'Janitza UMG 801 Basic Group {basic_group_num}{l4NameFlag} Phase {n} Addresses:\nVoltage {voltageAddress}\nVoltageLineToLine {voltageLineToLineAddress}\nCurrent {currentAddress}\nPower {powerAddress}\nEnergyFwd {energyFwdAddress}\nEnergyRev {energyRevAddress}\nPowerFactor {powerFactorAddress}')
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
            log.error(f'Janitza UMG 801 Basic Group {basic_group_num}{l4NameFlag} register Phase {n} exception while Register f32')
        log.info(f'Janitza UMG 801 Basic Group {basic_group_num}{l4NameFlag} register Phase {n} done')
        return pRegs


    def device_init(self):
        l4NameFlag = ' L4' if self.isL4SinglePhase is True else ''
        log.info(f'Janitza UMG 801 Basic Group {self.basic_group_num}{l4NameFlag} device init')
        
        basic_group_num = self.basic_group_num
        gRegs = None

        powerAddress=19026
        currentAddress=19018
        frequencyAddress=19050
        energyFwdAddress=19068        
        energyRevAddress=19076
        if(basic_group_num > 1):
            log.info(f'Janitza UMG 801 Basic Group {basic_group_num}{l4NameFlag} with offset')
            baseOffset=(basic_group_num*100)
            powerAddress=19000 + baseOffset + 14
            currentAddress=19000 + baseOffset + 6
            energyFwdAddress=19000 + baseOffset + 52
            energyRevAddress=19000 + baseOffset + 60
        else:
            log.info(f'Janitza UMG 801 Basic Group {basic_group_num}{l4NameFlag} with no offset')

        if self.isL4SinglePhase is True:
            baseAddress=21500
            baseOffset=(basic_group_num - 1) * 24
            log.info(f'Janitza UMG 801 Basic Group {basic_group_num}{l4NameFlag} register on BaseAddress {baseAddress} with offset {baseOffset}')
            powerAddress=baseAddress + baseOffset
            energyFwdAddress=baseAddress + baseOffset + 10
            energyRevAddress=baseAddress + baseOffset + 12
            
        log.info(f'Janitza UMG 801 Basic Group {basic_group_num}{l4NameFlag} Addresses:\nPower {powerAddress}\nCurrent {currentAddress}\nEnergyFwd {energyFwdAddress}\nEnergyRev {energyRevAddress}')
        try:
            gRegs = [
                Reg_f32b(powerAddress,       '/Ac/Power',             1, '%.3f W'),
                Reg_f32b(currentAddress,     '/Ac/Current',           1, '%.3f A'),
                Reg_f32b(frequencyAddress,   '/Ac/Frequency',         1, '%.3f Hz'),
                Reg_f32b(energyFwdAddress,   '/Ac/Energy/Forward', 1000, '%.3f kWh'),
                Reg_f32b(energyRevAddress,   '/Ac/Energy/Reverse', 1000, '%.3f kWh'),
            ]
        except:
            log.error(f'Janitza UMG 801 Basic Group {basic_group_num}{l4NameFlag} device exception while Register f32')
        
        if self.isL4SinglePhase is False:
            phases = 3 
            for n in range(1, phases + 1):
                gRegs += self.phase_regs(n)
        else:
            selectedPhase = self.phaseSetting
            settings = getattr(self, 'settings', None)
            if settings is not None:
                try:
                    selectedPhase = int(settings['phasesetting'])
                except Exception:
                    selectedPhase = self.phaseSetting

            if selectedPhase not in (1, 2, 3):
                selectedPhase = 1

            self.phaseSetting = selectedPhase
            log.info(f'Janitza UMG 801 Basic Group {basic_group_num}{l4NameFlag} using PhaseSetting {selectedPhase} for single-phase L4 mapping')
            gRegs += self.phase_regs(4)
            
        if self.isL4MeasureNeutral is True and self.isL4SinglePhase is False:
            log.info(f'Janitza UMG 801 Basic Group {basic_group_num}{l4NameFlag} adding L4 Current Register for Neutral Measurement')
            offset=88+(basic_group_num-1)*100
            if(basic_group_num <= 1):
                offset = 0
            nCurrentAddr=19018 + offset
            log.info(f'Janitza UMG 801 Basic Group {basic_group_num}{l4NameFlag} L4 Current Register Address {nCurrentAddr}')
            try:
                gRegs += [
                    Reg_f32b(nCurrentAddr, '/Ac/N/Current', 1, '%.3f A'),
                ]
            except:
                log.error(f'Janitza UMG 801 Basic Group {basic_group_num}{l4NameFlag} exception while Register f32 for L4 Current')

        self.data_regs = gRegs
        log.info(f'Janitza UMG 801 Basic Group {basic_group_num}{l4NameFlag} device init done')

    def get_ident(self):
        if self.isL4SinglePhase is True:
            return f"{self.parent.get_ident()}_BG{self.basic_group_num:02d}_L4SinglePhase"
        return f"{self.parent.get_ident()}_BG{self.basic_group_num:02d}"

    def device_update(self):
        if not self.enabled:
            return
        super().device_update()

    def device_init_late(self):
        l4NameFlag = ' L4' if self.isL4SinglePhase is True else ''
        log.info(f'Janitza UMG 801 Basic Group {self.basic_group_num}{l4NameFlag} device init late')
        super().device_init_late()

        if self.position is None and self.role in ('pvinverter', 'evcharger', 'heatpump', 'acload', 'genset'):
            if 'position' not in self.dbus_settings:
                self.add_settings({'position': ['/Position', 0, 0, 2]})
                self.add_dbus_setting('position', '/Position')
        
        if 'phasesetting' not in self.dbus_settings and self.isL4SinglePhase is True:
            self.add_settings({'phasesetting': ['/PhaseSetting', self.phaseSetting, 1, 3]})
            self.add_dbus_setting('phasesetting', '/PhaseSetting')

    def setting_changed(self, name, old, new):
        if name == 'phasesetting' and self.isL4SinglePhase:
            try:
                phase = int(new)
            except Exception:
                phase = 1
            if phase not in (1, 2, 3):
                phase = 1
            self.phaseSetting = phase
            log.info(f'Janitza UMG 801 Basic Group {self.basic_group_num} L4 PhaseSetting changed from {old} to {phase}')
            # Remove old phase DBus paths before rebuilding with new phase
            try:
                old_phase = int(old)
                if old_phase in (1, 2, 3) and old_phase != phase:
                    log.info(f'Janitza UMG 801 Basic Group {self.basic_group_num} L4 deleting /Ac/Lx from dbus')
                    self.dbus.del_tree(f'/Ac')
                    log.info(f'Janitza UMG 801 Basic Group {self.basic_group_num} L4 deleted /Ac/Lx from dbus')
            except Exception as e:
                log.error(f'Janitza UMG 801 Basic Group {self.basic_group_num} L4 exception deleting old phase paths: {e}')
            self.device_init()
            self.init_data_regs()

        return super().setting_changed(name, old, new)

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
            log.error('Exception while Janitza Probing')
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
            log.error('Janitza register Phase %d exception while Register f32'% n)
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
            log.error('Janitza device exception while Register f32')


        for n in range(1, phases + 1):
            gRegs += self.phase_regs(n)

        log.info('Janitza set Registers')
        self.data_regs = gRegs
                
        # Create SubDevices for each Basic Group (enabled status set in device_init_late)
        self._subdevice_blueprints = {}  # key -> dict of constructor kwargs
        log.info('Janitza add Basic Groups')
        try:
            for basic_group_num in range(1, 4):  # Basic Groups 1-3
                try:
                    probe_result = self.probe_groups(basic_group_num)

                    # Build blueprint list based on probe result
                    blueprints = []
                    if probe_result['l4_state'] == 'neutral':
                        blueprints = [dict(basic_group_num=basic_group_num, isL4MeasureNeutral=True,  isL4SinglePhase=False)]
                    elif probe_result['l4_state'] == 'separate_single_phase':
                        blueprints = [dict(basic_group_num=basic_group_num, isL4MeasureNeutral=False, isL4SinglePhase=False),
                                      dict(basic_group_num=basic_group_num, isL4MeasureNeutral=False, isL4SinglePhase=True)]
                    else:  # no_l4_support or partial_or_unknown
                        blueprints = [dict(basic_group_num=basic_group_num, isL4MeasureNeutral=False, isL4SinglePhase=False)]

                    for bp in blueprints:
                        subdevice = JANITZA_UMG_801_BASIC_GROUP(self, **bp)
                        key = self._subdevice_setting_key(subdevice)
                        self._subdevice_blueprints[key] = bp
                        self.subdevices.append(subdevice)
                        log.info(f'Janitza added Basic Group {basic_group_num} subdevice {key}')

                except Exception as e:
                    log.error(f'Janitza exception adding Basic Groups {basic_group_num}: {e}')
        except Exception as e:
            log.error(f'Janitza exception scanning Basic Groups: {e}')

        log.info('Janitza UMG 801 device init done')

    def probe_groups(self, group_num):
        def _safe_read_f32(addr):
            reg = Reg_f32b(addr)
            rr = self.read_modbus(reg.base, reg.count, reg.access)
            if rr.isError():
                return None
            reg.decode(rr.registers)
            return reg.value
        group_idx = group_num - 1
        phase_offset = 2
        active_power_l1_addr = 19020
        apparent_power_l1_addr = 19022
        reactive_power_l1_addr = 19024
        cos_phi_l1_addr = 19044
        harmonics_l1_addr = 19116

        group_l4_offset = 24
        active_power_l4_addr = 21500
        apparent_power_l4_addr = 21502
        reactive_power_l4_addr = 21504
        cos_phi_l4_addr = 21506
        harmonics_l4_addr = 21522
        
        offset_l1_l2_l3 = 100 * (group_idx)
        if(group_idx == 0):
            offset_l1_l2_l3 = 0
        if(group_idx >= 1):
            offset_l1_l2_l3 = 88 +(100 * (group_idx))

        for phase_idx in range(0, 3):
            offset_phase = phase_offset * phase_idx
            active_power = _safe_read_f32(active_power_l1_addr + offset_l1_l2_l3 + offset_phase)
            apparent_power = _safe_read_f32(apparent_power_l1_addr + offset_l1_l2_l3 + offset_phase)
            reactive_power = _safe_read_f32(reactive_power_l1_addr + offset_l1_l2_l3 + offset_phase)
            cos_phi = _safe_read_f32(cos_phi_l1_addr + offset_l1_l2_l3 + offset_phase)
            harmonics = _safe_read_f32(harmonics_l1_addr + offset_l1_l2_l3 + offset_phase)
            log.info('Janitza UMG 801 L%d probe Basic Group %d offset %d: activePowerL%d=%s, apparentPowerL%d=%s, reactivePowerL%d=%s, cosPhiL%d=%s, harmonicsL%d=%s',
                        phase_idx + 1, group_idx + 1, offset_l1_l2_l3 + offset_phase,
                        phase_idx + 1, active_power, phase_idx + 1, apparent_power, phase_idx + 1, reactive_power, phase_idx + 1, cos_phi, phase_idx + 1, harmonics)

        offset_l4 = group_l4_offset * group_idx
        active_power_l4 = _safe_read_f32(active_power_l4_addr + offset_l4)
        apparent_power_l4 = _safe_read_f32(apparent_power_l4_addr + offset_l4)
        reactive_power_l4 = _safe_read_f32(reactive_power_l4_addr + offset_l4)
        cos_phi_l4 = _safe_read_f32(cos_phi_l4_addr + offset_l4)
        harmonics_l4 = _safe_read_f32(harmonics_l4_addr + offset_l4)
        log.info('Janitza UMG 801 L4 probe Basic Group %d offset %d: activePowerL4=%s, apparentPowerL4=%s, reactivePowerL4=%s, cosPhiL4=%s, harmonicsL4=%s',
                    group_idx + 1, offset_l4, active_power_l4, apparent_power_l4, reactive_power_l4, cos_phi_l4, harmonics_l4)
        if(active_power_l4 is None and apparent_power_l4 is None and reactive_power_l4 is None and cos_phi_l4 is None and harmonics_l4 is None):
            log.info('Janitza UMG 801 Basic Group %d seems to have no L4 support', group_idx + 1)
            l4_state = 'no_l4_support'
        elif(active_power_l4 is None and apparent_power_l4 is None and reactive_power_l4 is None and cos_phi_l4 is None and harmonics_l4 is not None):
            log.info('Janitza UMG 801 Basic Group %d seems to have L4 setup as N', group_idx + 1)
            l4_state = 'neutral'
        elif(active_power_l4 is not  None and apparent_power_l4 is not  None and reactive_power_l4 is not  None and cos_phi_l4 is not None and harmonics_l4 is not None):
            log.info('Janitza UMG 801 Basic Group %d seems to have L4 setup as separate Single-Phase', group_idx + 1)
            l4_state = 'separate_single_phase'
        else:
            l4_state = 'partial_or_unknown'

        log.info('Janitza UMG 801 Basic Group %d probe result: L4 State: %s', group_idx + 1, l4_state)

        return {
            'group_num': group_num,
            'l4_state': l4_state,
        }

    def get_ident(self):
        return f"{self.vendor_id}_{self.info['/Serial']}"

    def _subdevice_setting_key(self, subdevice):
        key = f'bg{subdevice.basic_group_num:02d}'
        if subdevice.isL4SinglePhase:
            key += 'l4'
        return key

    def _subdevice_setting_path(self, subdevice):
        path = f'/EnabledBasicGroup{subdevice.basic_group_num:02d}'
        if subdevice.isL4SinglePhase:
            path += 'L4'
        return path

    def update_basic_group_subdevices(self):
        log.info('Janitza UMG 801 update_basic_group_subdevices')
        blueprints = getattr(self, '_subdevice_blueprints', {})

        for key, bp in blueprints.items():
            try:
                enabled = bool(self.settings[key])
            except Exception:
                enabled = True

            existing = next((s for s in self.subdevices
                             if self._subdevice_setting_key(s) == key), None)

            if enabled and existing is None:
                try:
                    subdevice = JANITZA_UMG_801_BASIC_GROUP(self, **bp)
                    self.subdevices.append(subdevice)
                    subdevice.init()
                    log.info(f'Janitza re-added subdevice {key}')
                except Exception as e:
                    log.error(f'Janitza exception re-adding subdevice {key}: {e}')

            elif not enabled and existing is not None:
                try:
                    existing.destroy()
                except Exception as e:
                    log.error(f'Janitza exception destroying subdevice {key}: {e}')
                self.subdevices.remove(existing)
                log.info(f'Janitza removed subdevice {key}')

    def setting_changed(self, name, old, new):
        result = super().setting_changed(name, old, new)

        if name.startswith('bg'):
            self.update_basic_group_subdevices()
            return True

        return result

    def device_init_late(self):
        super().device_init_late()
        log.info(f'Janitza UMG 801 device init late')

        for subdevice in self.subdevices:
            setting_name = self._subdevice_setting_key(subdevice)
            setting_path = self._subdevice_setting_path(subdevice)
            if setting_name not in self.dbus_settings:
                self.add_settings({setting_name: [setting_path, 1, 0, 1]})
                self.add_dbus_setting(setting_name, setting_path)

        self.update_basic_group_subdevices()

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
