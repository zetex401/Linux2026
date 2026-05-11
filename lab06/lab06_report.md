# lab06 репорт
# Блок 0. ps, /proc, chrt

# 1 ps
PID  NI PRI CLS COMMAND
      1   0  19  TS systemd
    142   0  19  TS (udev-worker)
     52  -1  20  TS systemd-journal
     98   0  19  TS systemd-udevd
    105   0  19  TS (udev-worker)
    170   0  19  TS dbus-daemon
    206   0  19  TS rsyslogd
  17102   0  19  TS Relay(17103)
    183   0  19  TS systemd-logind
    135   0  19  TS (udev-worker)
    134   0  19  TS (udev-worker)
  17231   0  19  TS bash
  17210   0  19  TS systemd
    140   0  19  TS (udev-worker)

# 2 proc
PID=17231 PRI=20 NI=0

# 3 chrt
pid 17231's current scheduling policy: SCHED_OTHER
pid 17231's current scheduling priority: 0


#Блок 1 часть 1. эксперимент nice 0 vs nice 19

Процесс с меньшим nice получает больше CPU, потому что у него выше приоритет для планировщика CFS.

[1] 26898
[2] 26899
    PID  NI PRI %CPU COMMAND
  26898   0  19  0.0 dd
  26899  19   0  0.0 dd
HIGH: PRI=20 NI=0
LOW:  PRI=39 NI=19
[1]-  Done                    nice -n 0 dd if=/dev/urandom of=/dev/null bs=1M count=200 2> /dev/null
[2]+  Done                    nice -n 19 dd if=/dev/urandom of=/dev/null bs=1M count=200 2> /dev/null



# Блок 1 часть 2. Эксперимент nice 10 vs nice 19

Разница между nice 10 и nice 19 есть, но она меньше, чем между nice 0 и nice 19.

[1] 28040
[2] 28041
    PID  NI PRI %CPU COMMAND
  28040  10   9  0.0 dd
  28041  19   0  0.0 dd
HIGH: PRI=30 NI=10
LOW:  PRI=39 NI=19
[1]-  Done                    nice -n 10 dd if=/dev/urandom of=/dev/null bs=1M count=200 2> /dev/null
[2]+  Done                    nice -n 19 dd if=/dev/urandom of=/dev/null bs=1M count=200 2> /dev/null



## Блок 2. renice

По правилам обычный пользователь может только увеличивать nice, то есть понижать приоритет процесса. Уменьшать nice обратно может только root через sudo.
28915 (process ID) old priority 15, new priority 0
    PID  NI PRI %CPU
  28915   0  19 92.2



### Блок 3. Эксперимент со временем

Процесс с nice 19 завершится позже, чем процесс с nice 0, если оба запущены одновременно на загруженном CPU.

### Результаты
[1] 29942
[2] 29943
[3] 29944
[4] 29945
[5] 29946

# Вывод
Процесс с nice 0 должен получить больше CPU, потому что его nice ниже. Планировщик CFS учитывает nice через вес процесса: чем ниже nice, тем больше процессорного времени получает процесс.

