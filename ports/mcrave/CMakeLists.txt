cmake_minimum_required(VERSION 3.20)
project(mcrave_openbw LANGUAGES CXX)

if(NOT BWAPI_ROOT OR NOT BWAPI_BUILD)
  message(FATAL_ERROR "Set BWAPI_ROOT and BWAPI_BUILD")
endif()
set(BWAPI_OFFICIAL_ROOT "${CMAKE_CURRENT_LIST_DIR}/../../third_party/bwapi-official" CACHE PATH
  "Official BWAPI 4.4 checkout used for the object-only compatibility check")
set(MCRAVE_SOURCE_ROOT "${CMAKE_CURRENT_LIST_DIR}/../../third_party/mcrave" CACHE PATH
  "McRave source checkout")
file(GLOB_RECURSE MCRAVE_SOURCES CONFIGURE_DEPENDS
  "${MCRAVE_SOURCE_ROOT}/Source/*.cpp")
add_library(McRave MODULE ${MCRAVE_SOURCES})
target_compile_features(McRave PRIVATE cxx_std_17)
target_compile_definitions(McRave PRIVATE BWEM_USE_WINUTILS=0)
target_compile_options(McRave PRIVATE -include cfloat -fdelayed-template-parsing)
target_include_directories(McRave PRIVATE
  "${BWAPI_ROOT}/bwapi/include"
  "${MCRAVE_SOURCE_ROOT}/Source"
  "${MCRAVE_SOURCE_ROOT}/Source/BWEM"
  "${MCRAVE_SOURCE_ROOT}/Source/BWEB"
  "${MCRAVE_SOURCE_ROOT}/Source/Horizon"
  "${MCRAVE_SOURCE_ROOT}/Source/McRave")
target_link_directories(McRave PRIVATE "${BWAPI_BUILD}/lib")
target_link_libraries(McRave PRIVATE BWAPILIB)
set_target_properties(McRave PROPERTIES PREFIX "" SUFFIX ".dylib")

# Compile every translation unit against official BWAPI headers without linking
# that ABI into the OpenBW runtime module.
add_library(McRaveOfficialHeaders OBJECT EXCLUDE_FROM_ALL ${MCRAVE_SOURCES})
target_compile_features(McRaveOfficialHeaders PRIVATE cxx_std_17)
target_compile_definitions(McRaveOfficialHeaders PRIVATE BWEM_USE_WINUTILS=0)
target_compile_options(McRaveOfficialHeaders PRIVATE -include cfloat -fdelayed-template-parsing)
target_include_directories(McRaveOfficialHeaders PRIVATE
  "${BWAPI_OFFICIAL_ROOT}/bwapi/include"
  "${MCRAVE_SOURCE_ROOT}/Source"
  "${MCRAVE_SOURCE_ROOT}/Source/BWEM"
  "${MCRAVE_SOURCE_ROOT}/Source/BWEB"
  "${MCRAVE_SOURCE_ROOT}/Source/Horizon"
  "${MCRAVE_SOURCE_ROOT}/Source/McRave")
