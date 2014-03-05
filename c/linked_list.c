#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct Element {
  struct Element *next;
  void *data;
} Element; 

/* Function prototypes */
bool createStack(Element **stack);
bool deleteStack(Element **stack);
bool push(Element **stack, void *data);
bool pop(Element **stack, void **data);

bool createStack(Element **stack) {
  *stack = NULL;
  return true;
}
bool deleteStack(Element **stack){
  struct Element *next;
  next = malloc(sizeof(struct Element));
  while(*stack) {
    next = (*stack)->next;
    free(*stack);
    *stack = next;
  }
  return true;
}

bool push(Element **stack, void *data) {
  struct Element *elem;
  elem = malloc(sizeof(struct Element));
  if(!elem) return false;

  elem->data = data;
  elem->next = *stack;
  *stack = elem;
  return true;
}

bool pop(Element **stack, void **data) {
  struct Element *elem;
  elem = malloc(sizeof(struct Element));
  if(!(elem = *stack)) return false;

  *data = elem->data;
  *stack = elem->next;
  free(elem);
  return true;
}

int main(int argc, char **argv) {
  printf("Function Prototypes correct\n");
}  
