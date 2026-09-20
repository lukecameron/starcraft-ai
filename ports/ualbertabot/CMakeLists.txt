cmake_minimum_required(VERSION 3.20)
project(ualbertabot_native LANGUAGES CXX)

if(NOT UALBERTA_SOURCE OR NOT BWAPI_ROOT OR NOT BWAPI_BUILD)
  message(FATAL_ERROR "Set UALBERTA_SOURCE, BWAPI_ROOT, and BWAPI_BUILD")
endif()

set(UAB_ROOT "${UALBERTA_SOURCE}/UAlbertaBot")
file(GLOB UAB_SOURCES CONFIGURE_DEPENDS "${UAB_ROOT}/Source/*.cpp")
list(REMOVE_ITEM UAB_SOURCES "${UAB_ROOT}/Source/main.cpp")
list(REMOVE_ITEM UAB_SOURCES "${UAB_ROOT}/Source/UnitInfoManager.cpp")
file(GLOB BOSS_SOURCES CONFIGURE_DEPENDS "${UALBERTA_SOURCE}/BOSS/source/*.cpp")
list(FILTER BOSS_SOURCES EXCLUDE REGEX "(Experiments|Experiment|StarCraftGUI|BOSS_main|BuildOrderTester|BOSSPlotBuildOrders|BOSSParameters)\\.cpp$")
file(GLOB SPARCRAFT_SOURCES CONFIGURE_DEPENDS "${UALBERTA_SOURCE}/SparCraft/source/*.cpp")
list(FILTER SPARCRAFT_SOURCES EXCLUDE REGEX "(TutorialCode)\\.cpp$")

add_library(UAlbertaBot MODULE
  ${UAB_SOURCES}
  ${BOSS_SOURCES}
  ${SPARCRAFT_SOURCES}
  "${CMAKE_CURRENT_LIST_DIR}/Dll.cpp")
target_compile_features(UAlbertaBot PRIVATE cxx_std_14)
target_compile_definitions(UAlbertaBot PRIVATE
  NOMINMAX
  UALBERTA_CONFIG_FILE="bwapi-data/AI/UAlbertaBot_Config.txt")
target_compile_options(UAlbertaBot PRIVATE -include cfloat -fdelayed-template-parsing)
target_include_directories(UAlbertaBot PRIVATE
  "${BWAPI_ROOT}/bwapi/include"
  "${UAB_ROOT}/Source"
  "${UALBERTA_SOURCE}/BOSS/source"
  "${UALBERTA_SOURCE}/SparCraft/source")
target_link_directories(UAlbertaBot PRIVATE "${BWAPI_BUILD}/lib")
target_link_libraries(UAlbertaBot PRIVATE BWAPILIB)
set_target_properties(UAlbertaBot PROPERTIES PREFIX "" SUFFIX ".dylib")

if(BWAPI_OFFICIAL_ROOT)
  add_library(UAlbertaBotOfficialHeaders OBJECT EXCLUDE_FROM_ALL
    ${UAB_SOURCES} ${BOSS_SOURCES} ${SPARCRAFT_SOURCES}
    "${CMAKE_CURRENT_LIST_DIR}/Dll.cpp")
  target_compile_features(UAlbertaBotOfficialHeaders PRIVATE cxx_std_14)
  target_compile_definitions(UAlbertaBotOfficialHeaders PRIVATE
    NOMINMAX UALBERTA_CONFIG_FILE="bwapi-data/AI/UAlbertaBot_Config.txt")
  target_compile_options(UAlbertaBotOfficialHeaders PRIVATE -include cfloat -fdelayed-template-parsing)
  target_include_directories(UAlbertaBotOfficialHeaders PRIVATE
    "${BWAPI_OFFICIAL_ROOT}/bwapi/include"
    "${UAB_ROOT}/Source"
    "${UALBERTA_SOURCE}/BOSS/source"
    "${UALBERTA_SOURCE}/SparCraft/source")
endif()
