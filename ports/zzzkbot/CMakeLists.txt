cmake_minimum_required(VERSION 3.16)
project(ZZZKBotNative LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_SHARED_LIBRARY_PREFIX "")

if(NOT DEFINED ZZZKBOT_SOURCE_DIR)
  message(FATAL_ERROR "Set ZZZKBOT_SOURCE_DIR to the pinned ZZZKBot checkout")
endif()
if(NOT DEFINED OPENBW_BWAPI_DIR)
  message(FATAL_ERROR "Set OPENBW_BWAPI_DIR to the OpenBW BWAPI checkout")
endif()
if(NOT DEFINED OPENBW_BWAPI_BUILD_DIR)
  message(FATAL_ERROR "Set OPENBW_BWAPI_BUILD_DIR to its completed build directory")
endif()

add_library(ZZZKBot SHARED
  "${ZZZKBOT_SOURCE_DIR}/ZZZKBot/Source/Dll.cpp"
  "${ZZZKBOT_SOURCE_DIR}/ZZZKBot/Source/ZZZKBotAIModule.cpp"
)
target_include_directories(ZZZKBot PRIVATE
  "${ZZZKBOT_SOURCE_DIR}/ZZZKBot/Source"
  "${OPENBW_BWAPI_DIR}/bwapi/include"
)
target_link_directories(ZZZKBot PRIVATE "${OPENBW_BWAPI_BUILD_DIR}/lib")
target_link_libraries(ZZZKBot PRIVATE BWAPILIB)
set_target_properties(ZZZKBot PROPERTIES
  BUILD_RPATH "${OPENBW_BWAPI_BUILD_DIR}/lib"
  LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib"
)
