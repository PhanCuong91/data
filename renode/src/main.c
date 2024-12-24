#include "stm32f4xx.h"
#include <stm32f4xx_rcc.h>
#include <stm32f4xx_usart.h>
#include <stm32f4xx_can.h>
#include <stm32f4xx_tim.h>
#include <stdio.h>
// #include "ctrace.h"
#include <string.h>
void print(char * data){

  while (*data) {
    USART_SendData(USART2, (uint8_t)(*data++));
  }
  USART_SendData(USART2,'\n');
}
static uint8_t timer_ready_var = 0;


void timer_APB2_initialization(uint32_t RCC_APB2Periph, TIM_TypeDef* TIMx){
  TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStruct;
  /*Enable clock */
  RCC_APB2PeriphClockCmd(RCC_APB2Periph_TIM9, ENABLE);
  /*timer setting*/
  TIM_TimeBaseStructInit(&TIM_TimeBaseInitStruct);
  TIM_TimeBaseInit(TIMx,&TIM_TimeBaseInitStruct);
  TIM_CounterModeConfig(TIMx,TIM_CounterMode_Up);
  TIM_Cmd(TIMx,ENABLE);
  timer_ready_var = 1;
}


uint8_t timer_ready_app(void){
  return timer_ready_var;
}

uint16_t get_timer_app(void){
  if (timer_ready_var == 1){
    return TIM_GetCounter(TIM9);
  }
  return 0;
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

  
  // timer_APB2_initialization(RCC_APB2Periph_TIM9,TIM9);

  // char data[] = "Hello World!";
  uint8_t TxData[8] = {0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08};
  CanTxMsg TxMsg ;
  TxMsg.StdId = 1;
  TxMsg.ExtId = 0;
  TxMsg.IDE = 0;
  TxMsg.RTR = 0;
  TxMsg.DLC = 8;
  memcpy(TxMsg.Data, TxData, sizeof(TxData));
  uint8_t cnt = 0;
  while(cnt < 2){
    CAN_Transmit(CAN1, &TxMsg);
    cnt++;
  }
  for(;;);
  return 0;
}
