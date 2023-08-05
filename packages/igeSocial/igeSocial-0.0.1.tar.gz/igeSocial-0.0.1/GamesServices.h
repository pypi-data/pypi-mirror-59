#pragma once
#include "Social.h"
#include "GamesServicesImpl.h"

class IGE_EXPORT GamesServices : public Social
{
public:
	GamesServices();
	~GamesServices();
	void init();
	void release();
	void signIn();
	void signOut();
	bool isSignedIn();
	void showLeaderboard(const char* id);
	void submitScoreLeaderboard(const char* id, uint16_t value);
	void showAchievement();
	void unlockAchievement(const char* id);
	void incrementAchievement(const char* id, uint16_t value);

private:
	GamesServicesImpl* m_gamesServicesImpl;
};
