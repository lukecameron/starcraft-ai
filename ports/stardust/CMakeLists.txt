cmake_minimum_required(VERSION 3.24)
project(stardust_openbw LANGUAGES CXX)

if(NOT STARDUST_SOURCE_ROOT OR NOT BWAPI_ROOT OR NOT BWAPI_BUILD)
  message(FATAL_ERROR "Set STARDUST_SOURCE_ROOT, BWAPI_ROOT and BWAPI_BUILD")
endif()

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(ZSTD_BUILD_CONTRIB OFF CACHE BOOL "" FORCE)
set(ZSTD_BUILD_PROGRAMS OFF CACHE BOOL "" FORCE)
set(ZSTD_BUILD_SHARED OFF CACHE BOOL "" FORCE)
set(ZSTD_BUILD_STATIC ON CACHE BOOL "" FORCE)
set(ZSTD_BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(ZSTD_LEGACY_SUPPORT OFF CACHE BOOL "" FORCE)
set(ZSTD_LZMA_SUPPORT OFF CACHE BOOL "" FORCE)
set(ZSTD_MULTITHREAD_SUPPORT OFF CACHE BOOL "" FORCE)
set(ZSTD_ZLIB_SUPPORT OFF CACHE BOOL "" FORCE)
add_subdirectory("${STARDUST_SOURCE_ROOT}/3rdparty/zstd/build/cmake" zstd)

add_library(stardust_zstdstream STATIC
  "${STARDUST_SOURCE_ROOT}/3rdparty/zstdstream/zstdstream.cpp")
target_include_directories(stardust_zstdstream SYSTEM PUBLIC
  "${STARDUST_SOURCE_ROOT}/3rdparty"
  "${STARDUST_SOURCE_ROOT}/3rdparty/zstdstream")
target_link_libraries(stardust_zstdstream PUBLIC libzstd_static)
target_compile_options(stardust_zstdstream PRIVATE -w)

file(GLOB STARDUST_BWEM_SOURCES CONFIGURE_DEPENDS
  "${STARDUST_SOURCE_ROOT}/3rdparty/BWEM/src/*.cpp")
add_library(stardust_bwem STATIC ${STARDUST_BWEM_SOURCES})
target_include_directories(stardust_bwem SYSTEM PUBLIC
  "${STARDUST_SOURCE_ROOT}/3rdparty/BWEM"
  "${STARDUST_SOURCE_ROOT}/3rdparty/BWEM/include")
target_include_directories(stardust_bwem PRIVATE "${BWAPI_ROOT}/bwapi/include")
target_link_directories(stardust_bwem PRIVATE "${BWAPI_BUILD}/lib")
target_link_libraries(stardust_bwem PUBLIC BWAPILIB)
target_compile_options(stardust_bwem PRIVATE -w)

file(GLOB_RECURSE STARDUST_SOURCES CONFIGURE_DEPENDS
  "${STARDUST_SOURCE_ROOT}/src/*.cpp")
set(STARDUST_INCLUDE_DIRS
  "${STARDUST_SOURCE_ROOT}/src"
  "${STARDUST_SOURCE_ROOT}/src/Builder"
  "${STARDUST_SOURCE_ROOT}/src/General"
  "${STARDUST_SOURCE_ROOT}/src/Instrumentation"
  "${STARDUST_SOURCE_ROOT}/src/Map"
  "${STARDUST_SOURCE_ROOT}/src/Map/PathFinding"
  "${STARDUST_SOURCE_ROOT}/src/Players"
  "${STARDUST_SOURCE_ROOT}/src/Producer"
  "${STARDUST_SOURCE_ROOT}/src/Strategist"
  "${STARDUST_SOURCE_ROOT}/src/Units"
  "${STARDUST_SOURCE_ROOT}/src/Util"
  "${STARDUST_SOURCE_ROOT}/src/Workers")
set(STARDUST_VENDOR_INCLUDE_DIRS
  "${STARDUST_SOURCE_ROOT}/3rdparty"
  "${STARDUST_SOURCE_ROOT}/3rdparty/FAP"
  "${STARDUST_SOURCE_ROOT}/3rdparty/nlohmann"
  "${STARDUST_SOURCE_ROOT}/3rdparty/bitsery/include"
  "${STARDUST_SOURCE_ROOT}/3rdparty/cppcrc"
  "${STARDUST_SOURCE_ROOT}/3rdparty/zstdstream")

add_library(Stardust MODULE ${STARDUST_SOURCES})
target_compile_definitions(Stardust PRIVATE IS_OPENBW=0 LOGGING_ENABLED=true)
target_compile_options(Stardust PRIVATE -Wall -Werror)
target_include_directories(Stardust SYSTEM PRIVATE "${BWAPI_ROOT}/bwapi/include")
target_include_directories(Stardust PRIVATE ${STARDUST_INCLUDE_DIRS})
target_include_directories(Stardust SYSTEM PRIVATE ${STARDUST_VENDOR_INCLUDE_DIRS})
target_link_directories(Stardust PRIVATE "${BWAPI_BUILD}/lib")
target_link_libraries(Stardust PRIVATE BWAPILIB stardust_bwem stardust_zstdstream)
set_target_properties(Stardust PROPERTIES PREFIX "" SUFFIX ".dylib")

if(BWAPI_OFFICIAL_ROOT)
  add_library(StardustGameplayOfficialHeaders OBJECT EXCLUDE_FROM_ALL
    ${STARDUST_SOURCES})
  target_compile_definitions(StardustGameplayOfficialHeaders PRIVATE IS_OPENBW=0 LOGGING_ENABLED=true)
  target_compile_options(StardustGameplayOfficialHeaders PRIVATE -Wall -Werror)
  target_include_directories(StardustGameplayOfficialHeaders SYSTEM PRIVATE
    "${BWAPI_OFFICIAL_ROOT}/bwapi/include")
  target_include_directories(StardustGameplayOfficialHeaders PRIVATE ${STARDUST_INCLUDE_DIRS})
  target_include_directories(StardustGameplayOfficialHeaders SYSTEM PRIVATE
    "${STARDUST_SOURCE_ROOT}/3rdparty/BWEM"
    "${STARDUST_SOURCE_ROOT}/3rdparty/BWEM/include"
    ${STARDUST_VENDOR_INCLUDE_DIRS})

  # Compile BWEM independently so its case-sensitive `base.h` include cannot
  # resolve Stardust's `Map/Base.h` on a case-insensitive filesystem. BWEM's
  # upstream warnings receive the same treatment as the linked runtime target.
  add_library(StardustBWEMOfficialHeaders OBJECT EXCLUDE_FROM_ALL
    ${STARDUST_BWEM_SOURCES})
  target_compile_options(StardustBWEMOfficialHeaders PRIVATE -w)
  target_include_directories(StardustBWEMOfficialHeaders SYSTEM PRIVATE
    "${BWAPI_OFFICIAL_ROOT}/bwapi/include"
    "${STARDUST_SOURCE_ROOT}/3rdparty/BWEM"
    "${STARDUST_SOURCE_ROOT}/3rdparty/BWEM/include")

  add_custom_target(StardustOfficialHeaders
    DEPENDS StardustGameplayOfficialHeaders StardustBWEMOfficialHeaders)
endif()
