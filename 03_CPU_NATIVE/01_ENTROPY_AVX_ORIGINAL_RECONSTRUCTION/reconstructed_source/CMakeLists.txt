cmake_minimum_required(VERSION 3.17)
project(EntropyAVXEngine CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(MSVC)
    add_compile_options(/O2 /LTGC /std:c++17 /arch:AVX2)
else()
    add_compile_options(-O3 -march=native -ffast-math -pthread -std=c++17 -mavx2)
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
