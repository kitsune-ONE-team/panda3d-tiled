cmake_minimum_required(VERSION 3.10)
project(panda3d-tiled)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_DISABLE_IN_SOURCE_BUILD ON)
set(CMAKE_INSTALL_RPATH "$ORIGIN/../../..")
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_subdirectory(ptiled)
