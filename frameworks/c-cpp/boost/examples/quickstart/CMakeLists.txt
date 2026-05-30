cmake_minimum_required(VERSION 3.28)

project(BoostQuickstart VERSION 1.0.0 LANGUAGES CXX)

find_package(Boost REQUIRED)

add_executable(boost_quickstart src/main.cpp)
target_compile_features(boost_quickstart PRIVATE cxx_std_23)
target_link_libraries(boost_quickstart PRIVATE Boost::headers)
