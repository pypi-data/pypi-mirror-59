//social init
PyDoc_STRVAR(socialInit_doc,
	"init the social system \n"\
	"\n"\
	"social.init()");

//social release
PyDoc_STRVAR(socialRelease_doc,
	"release the social system\n"\
	"\n"\
	"social.release()");

//social GamesServices init
PyDoc_STRVAR(socialGamesServicesInit_doc,
	"init the social gamesServices system \n"\
	"\n"\
	"gamesServices.init()");

//social GamesServices release
PyDoc_STRVAR(socialGamesServicesRelease_doc,
	"release the social gamesServices system\n"\
	"\n"\
	"gamesServices.release()");

//social GamesServices sign in
PyDoc_STRVAR(socialGamesServicesSignIn_doc,
	"the social gamesServices sign in\n"\
	"\n"\
	"gamesServices.signIn()");

//social GamesServices sign out
PyDoc_STRVAR(socialGamesServicesSignOut_doc,
	"the social gamesServices sign out\n"\
	"\n"\
	"gamesServices.signOut()");

//social GamesServices is signed in
PyDoc_STRVAR(socialGamesServicesIsSignedIn_doc,
	"the social gamesServices is signed in\n"\
	"\n"\
	"gamesServices.isSignedIn()\n"\
	"Returns\n"\
	"-------\n"\
	"    result : bool");

//social GamesServices show leaderboard
PyDoc_STRVAR(socialGamesServicesShowLeaderboard_doc,
	"show the game leaderboard\n"\
	"\n"\
	"gamesServices.showLeaderboard(id)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    id : string (optional)\n"\
	"        the leaderboard id to display");

//social GamesServices submit the new score leaderboard
PyDoc_STRVAR(socialGamesServicesSubmitScoreLeaderboard_doc,
	"submit the new score leaderboard\n"\
	"\n"\
	"gamesServices.submitScoreLeaderboard(id, value)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    id : string\n"\
	"        the leaderboard id to update\n"\
	"    value : uint\n"\
	"        the new score");

//social GamesServices show achievement
PyDoc_STRVAR(socialGamesServicesShowAchievement_doc,
	"show the game achievement\n"\
	"\n"\
	"gamesServices.showAchievement()");

//social GamesServices unlock the achievement
PyDoc_STRVAR(socialGamesServicesUnlockAchievement_doc,
	"unlock the game achievement\n"\
	"\n"\
	"gamesServices.unlockAchievement(id)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    id : string\n"\
	"        the achievement id to unlock");

//social GamesServices increase the achievement (the value)
PyDoc_STRVAR(socialGamesServicesIncrementAchievement_doc,
	"increase (the value) the game achievement\n"\
	"\n"\
	"gamesServices.incrementAchievement(id, value)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    id : string\n"\
	"        the achievement id to unlock\n"\
	"    value : uint\n"\
	"        the value to increase");

//social GamesSharing init
PyDoc_STRVAR(socialGamesSharingInit_doc,
	"init the social gamesSharing system \n"\
	"\n"\
	"gamesSharing.init(sns)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    sns : int (optional)\n"\
	"        the sns type (Facebook = 0)");

//social GamesSharing release
PyDoc_STRVAR(socialGamesSharingRelease_doc,
	"release the social gamesSharing system\n"\
	"\n"\
	"gamesSharing.release(sns)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    sns : int (optional)\n"\
	"        the sns type (Facebook = 0)");

//social GamesSharing sign in
PyDoc_STRVAR(socialGamesSharingSignIn_doc,
	"the social gamesSharing sign in\n"\
	"\n"\
	"gamesSharing.signIn(sns)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    sns : int (optional)\n"\
	"        the sns type (Facebook = 0)");

//social GamesSharing sign out
PyDoc_STRVAR(socialGamesSharingSignOut_doc,
	"the social gamesSharing sign out\n"\
	"\n"\
	"gamesSharing.signOut(sns)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    sns : int (optional)\n"\
	"        the sns type (Facebook = 0)");

//social GamesSharing is signed in
PyDoc_STRVAR(socialGamesSharingIsSignedIn_doc,
	"the social gamesSharing is signed in\n"\
	"\n"\
	"gamesSharing.isSignedIn(sns)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    sns : int (optional)\n"\
	"        the sns type (Facebook = 0)\n"\
	"Returns\n"\
	"-------\n"\
	"    result : bool");

//social GamesSharing share
PyDoc_STRVAR(socialGamesSharingShare_doc,
	"social sharing\n"\
	"\n"\
	"gamesSharing.share(value, sns, share)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    value : string\n"\
	"        the link to share\n"\
	"    sns : int (optional)\n"\
	"        the sns type (Facebook = 0)\n"\
	"    share : int (optional)\n"\
	"        the share type (Link = 0, Photo = 1)");

//social GamesSharing get profile id
PyDoc_STRVAR(socialGamesSharingGetProfileID_doc,
	"get user profile id\n"\
	"\n"\
	"gamesSharing.getProfileID(sns)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    sns : int (optional)\n"\
	"        the sns type (Facebook = 0)\n"\
	"Returns\n"\
	"-------\n"\
	"    result : string");

//social GamesSharing get profile name
PyDoc_STRVAR(socialGamesSharingGetProfileName_doc,
	"get user profile name\n"\
	"\n"\
	"gamesSharing.getProfileName(sns)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    sns : int (optional)\n"\
	"        the sns type (Facebook = 0)\n"\
	"Returns\n"\
	"-------\n"\
	"    result : string");