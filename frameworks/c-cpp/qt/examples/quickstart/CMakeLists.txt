cmake_minimum_required(VERSION 3.28)

project(QtQuickstart VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_AUTOMOC ON)

find_package(Qt6 REQUIRED COMPONENTS Core)

add_executable(qt_quickstart src/main.cpp)
target_compile_features(qt_quickstart PRIVATE cxx_std_23)
target_link_libraries(qt_quickstart PRIVATE Qt6::Core)
