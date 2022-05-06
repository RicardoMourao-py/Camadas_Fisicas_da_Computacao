// ARQUIVO PARA CRIAÇÃO DE FUNÇÕES

// importando as variáveis
#include "sw_uart.h"
// importação para melhorar compilamento do computador
#pragma GCC optimize ("-O3")

void sw_uart_setup(due_sw_uart *uart, int tx) {
  uart->pin_tx     = tx;
  pinMode(tx, OUTPUT); 
}


int calc_even_parity(char data) {
  int ones = 0;
  for(int i = 0; i < 8; i++) {
    ones += (data >> i) & 0x01;
  }
  return ones % 2;
}

void sw_uart_send_byte(due_sw_uart *uart) {
  
  digitalWrite(uart->pin_tx, HIGH);
  digitalWrite(uart->pin_tx, LOW);
  _sw_uart_wait_T(uart);
  

  //01110010 = r
  digitalWrite(uart->pin_tx, LOW);
  _sw_uart_wait_T(uart);

  digitalWrite(uart->pin_tx, HIGH);
  _sw_uart_wait_T(uart);

  digitalWrite(uart->pin_tx, LOW);
  _sw_uart_wait_T(uart);
  
  digitalWrite(uart->pin_tx, LOW);
  _sw_uart_wait_T(uart);

  digitalWrite(uart->pin_tx, HIGH);
  _sw_uart_wait_T(uart);

  digitalWrite(uart->pin_tx, HIGH);
  _sw_uart_wait_T(uart);

  digitalWrite(uart->pin_tx, HIGH);
  _sw_uart_wait_T(uart);

  digitalWrite(uart->pin_tx, LOW);
  _sw_uart_wait_T(uart);

  digitalWrite(uart->pin_tx, 0);
  _sw_uart_wait_T(uart);

  digitalWrite(uart->pin_tx, HIGH);
  _sw_uart_wait_T(uart);
}


// MCK 21MHz
void _sw_uart_wait_half_T(due_sw_uart *uart) {
  for(int i = 0; i < 1093; i++)
    asm("NOP");
}

void _sw_uart_wait_T(due_sw_uart *uart) {
  _sw_uart_wait_half_T(uart);
  _sw_uart_wait_half_T(uart);
}
