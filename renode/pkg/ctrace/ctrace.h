#ifndef CTRACE_H
#define CTRACE_H

#include <stdint.h>

/*These definitions depend on metadata file*/
#define ENTRY_FUNC_ID              0
#define EXIT_FUNC_ID               1



#define SIZE_OF_BUFFER              100 

/*
each ctrace data includes
    uint64 time_stamp -> 8Bytes
    uint32 caller_add -> 4Bytes
    uint32 func_add   -> 4Bytes
    uint16 event_id   -> 2Bytes
total 18Bytes
*/
typedef struct{
    uint64_t time_stamp;
    uint32_t caller_add;
    uint32_t func_add;
    uint16_t event_id;
}ctrace_data;

typedef struct {
    uint16_t cur_pos;
    ctrace_data data[SIZE_OF_BUFFER];
} ctrace_buffer;
// ctrace_buffer ctrace_buff;

/* timer_api() shall be defined in application */ 
extern uint8_t timer_ready_app(void);
extern uint16_t get_timer_app(void);
#define get_timer()             get_timer_app()
#define timer_ready()           timer_ready_app()


void __attribute__((no_instrument_function)) __cyg_profile_func_exit(void *func_add, void *caller_add);
void __attribute__((no_instrument_function)) __cyg_profile_func_enter(void *func_add, void *caller_add);
void __attribute__((no_instrument_function)) convert_16b_2_64b(void);
// void save_trace_data(uint64_t time_stamp, uint64_t caller_add, uint64_t func_add, uint8_t event_id);

#endif /*CTRACE_H*/
/*End of file*/