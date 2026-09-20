#include <BWAPI.h>
#include "BOSS.h"
#include "SparCraft.h"
#include "UAlbertaBotModule.h"

#ifdef _WIN32
#define UALBERTA_EXPORT __declspec(dllexport)
#else
#define UALBERTA_EXPORT __attribute__((visibility("default")))
#endif

extern "C" UALBERTA_EXPORT void gameInit(BWAPI::Game* game)
{
    BWAPI::BroodwarPtr = game;
}

extern "C" UALBERTA_EXPORT BWAPI::AIModule* newAIModule()
{
    static bool initialized = false;
    if (!initialized)
    {
        SparCraft::init();
        BOSS::init();
        initialized = true;
    }
    return new UAlbertaBot::UAlbertaBotModule();
}
