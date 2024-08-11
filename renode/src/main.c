#include "stm32f4xx.h"
#include <stm32f4xx_rcc.h>
#include <stm32f4xx_usart.h>
#include <stm32f4xx_can.h>
#include <stdio.h>

void print(char * data){

  while (*data) {
    USART_SendData(USART2, (uint8_t)(*data++));
  }
  USART_SendData(USART2,'\n');
}

int main()
{
  // Switch on blue LED on STM32F407Discovery

  RCC_AHB1PeriphClockCmd(RCC_APB1Periph_USART2, ENABLE);
  RCC_AHB1PeriphClockCmd(RCC_APB1Periph_CAN1, ENABLE);
  USART_ClockInitTypeDef USART_ClockInitStruct;
  USART_ClockStructInit(&USART_ClockInitStruct);
  USART_ClockInit(USART2,&USART_ClockInitStruct);
  USART_InitTypeDef USART_InitStruct;
  USART_StructInit(&USART_InitStruct);
  USART_Init(USART2,&USART_InitStruct);
  CAN_InitTypeDef CAN_InitStruct;
  CAN_StructInit(&CAN_InitStruct);
  CAN_Init(CAN1, &CAN_InitStruct);
  uint8_t TxData[8] = {0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08};
  CanTxMsg TxMsg ;

  TxMsg.StdId = 1;
  TxMsg.ExtId = 0;
  TxMsg.IDE = 0;
  TxMsg.RTR = 0;
  TxMsg.DLC = 8;
  memcpy(TxMsg.Data, TxData, sizeof(TxData));
  uint8_t cnt = 0;
  while(cnt < 3){
    CAN_Transmit(CAN1, &TxMsg);
    cnt++;
  }
  char data[] = "Hello World!";
  print(data);
  
  for (;;);

  return 0;
}
