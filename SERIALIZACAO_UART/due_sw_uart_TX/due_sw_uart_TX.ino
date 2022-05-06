// ARQUIVO PARA REALIZAR O PROCESSO COM AS VARIÁVEIS E FUNÇÕES

#include "sw_uart.h"

due_sw_uart uart;

void setup() {
  Serial.begin(9600);
  sw_uart_setup(&uart, 2);
}

void loop() {
  sw_uart_send_byte(&uart);
  delay(2000);
}
