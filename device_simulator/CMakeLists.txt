cmake_minimum_required(VERSION 3.16)

project(device_simulator LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(device_core
    src/DeviceConfig.cpp
    src/Device.cpp
    src/TelemetryManager.cpp
    src/TelemetrySerializer.cpp
    src/Watchdog.cpp
    src/HealthMonitor.cpp
    src/RecoveryManager.cpp
)

target_include_directories(device_core
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

add_executable(device_simulator
    src/main.cpp
)

target_link_libraries(device_simulator
    PRIVATE
        device_core
)

enable_testing()

add_executable(device_core_tests
    tests/test_device_core.cpp
)

target_link_libraries(device_core_tests
    PRIVATE
        device_core
)

add_test(NAME device_core_tests COMMAND device_core_tests)
set_tests_properties(device_core_tests PROPERTIES
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)
