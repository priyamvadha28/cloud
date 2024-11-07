'''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

int main() {
    int parent_to_child[2], child_to_parent[2];
    pid_t pid;
    char parent_message[] = "Hello from parent!";
    char child_message[] = "Hello from child!";
    char buffer[1024];

    // Create two pipes
    if (pipe(parent_to_child) == -1 || pipe(child_to_parent) == -1) {
        perror("Pipe creation failed");
        return 1;
    }

    // Fork the process to create a child
    pid = fork();

    if (pid < 0) {
        perror("Fork failed");
        return 1;
    } else if (pid > 0) { // Parent process
        // Close unused ends of pipes
        close(parent_to_child[0]); // Close reading end of parent-to-child pipe
        close(child_to_parent[1]); // Close writing end of child-to-parent pipe

        // Write message to the child
        write(parent_to_child[1], parent_message, strlen(parent_message) + 1);
        printf("Parent: Sent message to child.\n");

        // Read response from the child
        read(child_to_parent[0], buffer, sizeof(buffer));
        printf("Parent: Received response from child: %s\n", buffer);

        // Close the used ends of pipes
        close(parent_to_child[1]);
        close(child_to_parent[0]);
    } else { // Child process
        // Close unused ends of pipes
        close(parent_to_child[1]); // Close writing end of parent-to-child pipe
        close(child_to_parent[0]); // Close reading end of child-to-parent pipe

        // Read message from the parent
        read(parent_to_child[0], buffer, sizeof(buffer));
        printf("Child: Received message from parent: %s\n", buffer);

        // Write response to the parent
        write(child_to_parent[1], child_message, strlen(child_message) + 1);
        printf("Child: Sent response to parent.\n");

        // Close the used ends of pipes
        close(parent_to_child[0]);
        close(child_to_parent[1]);
    }

    return 0;
}'''

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

void child_process(HANDLE read_handle, HANDLE write_handle) {
    char buffer[1024];
    DWORD bytes_read, bytes_written;

    // Child reads a message from the parent
    if (ReadFile(read_handle, buffer, sizeof(buffer), &bytes_read, NULL)) {
        buffer[bytes_read] = '\0';  // Null-terminate the string
        printf("Child: Received message from parent: %s\n", buffer);
    } else {
        fprintf(stderr, "Child: ReadFile failed.\n");
        return;
    }

    // Child sends a response back to the parent
    const char *child_message = "Hello from child!";
    if (!WriteFile(write_handle, child_message, strlen(child_message) + 1, &bytes_written, NULL)) {
        fprintf(stderr, "Child: WriteFile failed.\n");
    }
    printf("Child: Sent response to parent.\n");
}

int main() {
    HANDLE parent_to_child_read, parent_to_child_write;
    HANDLE child_to_parent_read, child_to_parent_write;
    SECURITY_ATTRIBUTES sa;
    DWORD bytes_written, bytes_read;
    char buffer[1024];

    // Set up security attributes for the pipes
    sa.nLength = sizeof(SECURITY_ATTRIBUTES);
    sa.bInheritHandle = TRUE;
    sa.lpSecurityDescriptor = NULL;

    // Create pipes for parent-to-child and child-to-parent communication
    if (!CreatePipe(&parent_to_child_read, &parent_to_child_write, &sa, 0)) {
        fprintf(stderr, "Failed to create parent-to-child pipe.\n");
        return 1;
    }
    if (!CreatePipe(&child_to_parent_read, &child_to_parent_write, &sa, 0)) {
        fprintf(stderr, "Failed to create child-to-parent pipe.\n");
        return 1;
    }

    // Write a message from parent to child
    const char *parent_message = "Hello from parent!";
    if (!WriteFile(parent_to_child_write, parent_message, strlen(parent_message) + 1, &bytes_written, NULL)) {
        fprintf(stderr, "Parent: WriteFile failed.\n");
        return 1;
    }
    printf("Parent: Sent message to child.\n");

    // Create a child thread to handle child process logic
    DWORD thread_id;
    HANDLE child_thread = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE) child_process, (void*)parent_to_child_read, 0, &thread_id);
    if (child_thread == NULL) {
        fprintf(stderr, "Failed to create child thread.\n");
        return 1;
    }

    // Parent reads the response from child
    if (ReadFile(child_to_parent_read, buffer, sizeof(buffer), &bytes_read, NULL)) {
        buffer[bytes_read] = '\0';
        printf("Parent: Received response from child: %s\n", buffer);
    } else {
        fprintf(stderr, "Parent: ReadFile failed.\n");
    }

    // Wait for the child thread to finish
    WaitForSingleObject(child_thread, INFINITE);

    // Close handles
    CloseHandle(child_thread);
    CloseHandle(parent_to_child_read);
    CloseHandle(parent_to_child_write);
    CloseHandle(child_to_parent_read);
    CloseHandle(child_to_parent_write);

    return 0;
}