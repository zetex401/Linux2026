#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        printf("Child exiting: PID=%d\n", getpid());
        exit(0);
    } else if (pid > 0) {
        printf("Parent sleeping, PID=%d\n", getpid());
        sleep(60);
    } else {
        perror("fork failed");
        return 1;
    }

    return 0;
}
