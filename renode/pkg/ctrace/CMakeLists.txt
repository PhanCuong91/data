# Define a CMake project for the ctrace library
# This project includes the ctrace.c and ctrace.h files

cmake_minimum_required(VERSION 3.0.0)
project(ctrace VERSION 0.1.0 LANGUAGES C)

# Add a library target for the ctrace library
add_library(ctrace)

# Specify the include directories for the ctrace library
target_include_directories(ctrace PUBLIC ${CMAKE_CURRENT_LIST_DIR})

# Specify the source files for the ctrace library
target_sources(ctrace
    PUBLIC
        ${CMAKE_CURRENT_LIST_DIR}/ctrace.c
        ${CMAKE_CURRENT_LIST_DIR}/ctrace.h
)