#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        // CHILD: запускаем программу
        execlp("ls", "ls", NULL);  // используем команду ls

        // если ошибка
        perror("exec failed");
        exit(1);
    } else if (pid > 0) {
        // PARENT: ждём child
        int status;
        waitpid(pid, &status, 0);
        if (WIFEXITED(status)) {
            printf("Child exited with code: %d\n", WEXITSTATUS(status));
        }
    } else {
        perror("fork failed");
        return 1;
    }

    return 0;
}
