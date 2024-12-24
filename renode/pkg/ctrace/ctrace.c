#include "ctrace.h"

ctrace_buffer ctrace_buff;
static uint16_t pre_cnt = 0;
static uint64_t time_stamp = 0;
#define MAX_TIME_STAMP          0xFFFFFFFFFFFFFFFF
#define MAX_COUNTER             0xFFFF
void convert_16b_2_64b(void){
    uint16_t cnt = get_timer();

    if(cnt < pre_cnt){
        /* TO-DO
        prevent overflow of time_stamp
        if 64bits is full, then start over
        this case has to be handled by python script
        */
        if(MAX_TIME_STAMP - time_stamp < MAX_COUNTER){
            time_stamp = 0;
        }
        else{
            time_stamp += MAX_COUNTER;
        }
    }
    time_stamp += cnt;
    pre_cnt = cnt;
}
void __cyg_profile_func_enter(void *func_add, void *caller_add)
{
    // // Check if function and caller addresses are valid
    // if (func_add == NULL_PTR || caller_add == NULL) {
    //     return;
    // }
    if (timer_ready()==1)
    {
        // Set the event ID for function entry
        uint8_t event_id = ENTRY_FUNC_ID;

        // Get the timestamp
        uint64_t timestamp = time_stamp;

        // Save the timestamp, called function address, function address, and event ID
        save_trace_data(timestamp,(uint64_t)caller_add, (uint64_t)func_add, event_id);
    }
}

void __cyg_profile_func_exit(void* func_add, void* caller_add)
{
    // // Check if function and caller addresses are valid
    // if (func_add == NULL || caller_add == NULL) {
    //     return;
    // }
    if (timer_ready()==1)
    {
        // Set the event ID for function exit (type uint8_t)
        uint8_t eventId = EXIT_FUNC_ID;

        // Get the timestamp (type uint64_t)
        uint64_t timestamp = time_stamp;

        // Save the timestamp, calling function address, exited function address, and event ID
        save_trace_data(timestamp, (uint64_t)caller_add, (uint64_t)func_add, eventId);
    }
}

void __attribute__((no_instrument_function)) save_trace_data(uint64_t time_stamp, uint64_t caller_add, uint64_t func_add, uint8_t event_id)
{
    if (ctrace_buff.cur_pos <= (sizeof(ctrace_buff.data) / sizeof(ctrace_buff.data[0]))){
        
        uint16_t id = ctrace_buff.cur_pos;
        ctrace_buff.data[id].time_stamp = time_stamp;
        ctrace_buff.data[id].caller_add = caller_add;
        ctrace_buff.data[id].func_add = func_add;
        ctrace_buff.data[id].event_id = event_id;

        ctrace_buff.cur_pos++;
    }
    else{
        ctrace_buff.cur_pos=0;
    }
}