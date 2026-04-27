# HW05 — fork, exec, wait

Данная работа посвящена жизненному циклу процессов в Linux.
В заданиях используются системные вызовы fork(), exec() и wait()/waitpid().

fork() создаёт новый процесс (дочерний), exec() запускает другую программу внутри процесса, а wait() позволяет родительскому процессу дождаться завершения дочернего и получить его код выхода.

---

## Компиляция

```bash
gcc -Wall -o task1 task1_fork.c
gcc -Wall -o task2 task2_launcher.c
```

### Что означает эта команда

* `gcc` — компилятор языка C (превращает .c файл в программу)
* `-Wall` — включает все предупреждения (важно, чтобы не было ошибок)
* `-o task1` — создаёт исполняемый файл с именем `task1`
* `task1_fork.c` — исходный файл с кодом

Пример:

```bash
gcc -Wall -o task1 task1_fork.c
```

означает: скомпилировать файл `task1_fork.c` и создать программу `task1`.

-

## Запуск

```bash
./task1
./task2 ls
./task2 fakecmd
./task2
```

-

## Как работает программа

### fork()

Создаёт новый процесс (child). После вызова fork() есть два процесса:

* parent (родитель)
* child (дочерний)

Возвращаемое значение:

* `0` → в child
* `>0` → в parent (PID дочернего процесса)
* `-1` → ошибка

-

### exec() (execlp)

Запускает другую программу внутри процесса.

Пример:

```c
execlp("ls", "ls", NULL);
```

Это означает, что процесс начнёт выполнять команду `ls`.

Важно: если exec() успешно выполнен, код ниже не выполняется.

-

### wait() / waitpid()

Родительский процесс ждёт завершения дочернего:

```c
int status;
waitpid(pid, &status, 0);
```

Если не вызвать wait(), дочерний процесс станет zombie (зомби-процессом).

-

### WEXITSTATUS

Позволяет получить код завершения программы:

```c
WEXITSTATUS(status)
```

-

## Пример вывода task1

```bash
Before fork: PID=1234
I am parent, PID=1234, child PID=1235
I am child, PID=1235, PPID=1234
Parent: child exited with code 0
```

-

## Пример вывода task2

```bash
./task2 ls
task1  task1_fork.c  task2  task2_launcher.c  task3_signals.md  README.md
Child (PID=1235) exited with code 0
```

```bash
./task2 fakecmd
exec failed: No such file or directory
Child (PID=1236) exited with code 1
```

```bash
./task2
Usage: ./task2 <command>
```

-

## Описание файлов

* task1_fork.c — демонстрация fork(), getpid(), getppid() и wait()
* task2_launcher.c — запуск программы через fork + exec + wait
* task3_signals.md — ответы на вопросы про сигналы
* README.md — описание задания, инструкции и примеры
* Ну, и лично от меня эту информацию я попросил написать ЛЛМКУ

