cmake_minimum_required(VERSION 3.10)
project(mandelbrot C)

set(CMAKE_C_STANDARD 17)

# Для Windows - правильное создание DLL
if(WIN32)
    add_compile_definitions(MANDELBROT_EXPORTS)
endif()

# Поиск OpenMP (пока ещё не нужен)
# find_package(OpenMP REQUIRED)

# Создание shared library
add_library(mandelbrot SHARED mandelbrot.c)

# Для OpenMP (раскомментируем позже)
# if(OpenMP_C_FOUND)
#     target_link_libraries(mandelbrot OpenMP::OpenMP_C)
# endif()

# DLL создаётся в папку lib/
set_target_properties(mandelbrot PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/../lib
        LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/../lib
)