#include <stdio.h>

int main() {
    char str[100], reversed[100];
    int length = 0, i;

    // Ask the user for a string
    printf("Enter a string: ");
    fgets(str, sizeof(str), stdin); // Read the string, including spaces

    // Find the length of the string manually (excluding the newline character if present)
    while (str[length] != '\0' && str[length] != '\n') {
        length++;
    }

    // Reverse the string
    for (i = 0; i < length; i++) {
        reversed[i] = str[length - i - 1];
    }
    reversed[length] = '\0'; // Add null character to terminate the reversed string

    // Print the reversed string
    printf("Reversed string: %s\n", reversed);

    return 0;
}