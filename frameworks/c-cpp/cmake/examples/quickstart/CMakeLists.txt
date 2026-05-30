cmake_minimum_required(VERSION 3.28)

project(CMakeQuickstart VERSION 1.0.0 LANGUAGES CXX)

add_executable(cmake_quickstart src/main.cpp)
target_compile_features(cmake_quickstart PRIVATE cxx_std_23)
target_compile_definitions(
    cmake_quickstart
    PRIVATE CMAKE_QUICKSTART_VERSION="${PROJECT_VERSION}"
)
