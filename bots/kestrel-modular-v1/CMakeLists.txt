cmake_minimum_required(VERSION 3.24)
project(kestrel_modular_v1 LANGUAGES CXX)

if(NOT BWAPI_ROOT OR NOT BWAPI_BUILD)
  message(FATAL_ERROR "Set BWAPI_ROOT and BWAPI_BUILD")
endif()

set(KESTREL_MODULAR_INCLUDE "${CMAKE_CURRENT_LIST_DIR}/include")
set(KESTREL_MODULAR_SOURCES
  src/CommandArbiter.cpp
  src/ConstructionController.cpp
  src/Kestrel.cpp
  src/ProductionController.cpp
  src/ScoutingController.cpp
  src/SquadController.cpp
  src/StrategyPlanner.cpp
  src/Telemetry.cpp
  src/WorldMemory.cpp
  src/WorldState.cpp
  src/WorkerAllocator.cpp)

add_library(KestrelModular MODULE ${KESTREL_MODULAR_SOURCES})
set_target_properties(KestrelModular PROPERTIES PREFIX "" SUFFIX ".dylib")
target_compile_features(KestrelModular PRIVATE cxx_std_14)
target_compile_options(KestrelModular PRIVATE -Wall -Wextra -Werror)
target_include_directories(KestrelModular SYSTEM PRIVATE "${BWAPI_ROOT}/bwapi/include")
target_include_directories(KestrelModular PRIVATE "${KESTREL_MODULAR_INCLUDE}")
target_link_directories(KestrelModular PRIVATE "${BWAPI_BUILD}/lib")
target_link_libraries(KestrelModular PRIVATE BWAPILIB)

if(BWAPI_OFFICIAL_ROOT)
  add_library(KestrelModularOfficialHeaders OBJECT EXCLUDE_FROM_ALL ${KESTREL_MODULAR_SOURCES})
  target_compile_features(KestrelModularOfficialHeaders PRIVATE cxx_std_14)
  target_compile_options(KestrelModularOfficialHeaders PRIVATE -Wall -Wextra -Werror)
  target_include_directories(KestrelModularOfficialHeaders SYSTEM PRIVATE "${BWAPI_OFFICIAL_ROOT}/bwapi/include")
  target_include_directories(KestrelModularOfficialHeaders PRIVATE "${KESTREL_MODULAR_INCLUDE}")
endif()

enable_testing()
add_executable(KestrelModularUnitTests tests/OpeningPolicyTests.cpp)
target_compile_features(KestrelModularUnitTests PRIVATE cxx_std_14)
target_compile_options(KestrelModularUnitTests PRIVATE -Wall -Wextra -Werror)
target_include_directories(KestrelModularUnitTests SYSTEM PRIVATE "${BWAPI_ROOT}/bwapi/include")
target_include_directories(KestrelModularUnitTests PRIVATE "${KESTREL_MODULAR_INCLUDE}")
add_test(NAME KestrelModularUnitTests COMMAND KestrelModularUnitTests)
