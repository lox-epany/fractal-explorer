cmake_minimum_required(VERSION 3.10)
project(mandelbrot C)

set(CMAKE_C_STANDARD 17)

# РАЗНЫЕ НАСТРОЙКИ ДЛЯ WINDOWS/LINUX
if(WIN32)
    add_compile_definitions(MANDELBROT_EXPORTS)
    set(LIBRARY_OUTPUT_NAME "mandelbrot.dll")
else()
    # Для Linux
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fPIC")
    set(LIBRARY_OUTPUT_NAME "libmandelbrot.so")
endif()

# Поиск OpenMP (пока ещё не нужен)
# find_package(OpenMP REQUIRED)

add_library(mandelbrot SHARED mandelbrot.c)

# Для OpenMP (раскомментируем позже)
# if(OpenMP_C_FOUND)
#     target_link_libraries(mandelbrot OpenMP::OpenMP_C)
# endif()

# ВЫХОДНЫЕ ПУТИ
set_target_properties(mandelbrot PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/../lib
        LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/../lib
        OUTPUT_NAME ${LIBRARY_OUTPUT_NAME}
        PREFIX ""
)