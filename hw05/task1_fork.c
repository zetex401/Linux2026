#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main() {
    printf("Before fork: PID=%d\n", getpid());

    pid_t pid = fork();

    if (pid == 0) {
        printf("I am child, PID=%d, PPID=%d\n", getpid(), getppid());
    } else if (pid > 0) {
        int status;
        printf("I am parent, PID=%d, child PID=%d\n", getpid(), pid);

        waitpid(pid, &status, 0);

        if (WIFEXITED(status)) {
            printf("Parent: child exited with code %d\n", WEXITSTATUS(status));
        }
    } else {
        perror("fork failed");
        return 1;
    }

    return 0;
}
