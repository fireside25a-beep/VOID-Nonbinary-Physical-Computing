cmake_minimum_required(VERSION 3.17)
project(EntropyAVXEngine CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(MSVC)
    add_compile_options(/O2 /LTGC /std:c++17 /arch:AVX2)
else()
    if(NOT CMAKE_SYSTEM_PROCESSOR MATCHES "^(x86_64|amd64|AMD64|i[3-6]86)$")
        message(FATAL_ERROR "EntropyAVX is AVX2/x86-only. macOS Apple Silicon cannot execute this target natively.")
    endif()
    add_compile_options(-O2 -pthread -std=c++17 -mavx2)
endif()

add_executable(EntropyAVXEngine
    main.cpp
    engine_core.h
    engine_core.cpp
    bvh_spatial.h
    bvh_spatial.cpp
    procedural.h
    procedural.cpp
    shader_pipeline.h
    shader_pipeline.cpp
    snn_compiler.h
    snn_compiler.cpp
)
