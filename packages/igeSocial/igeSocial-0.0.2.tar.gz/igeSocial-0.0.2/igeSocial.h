#include <Python.h>
#include "Social.h"
#include "GamesServices.h"
#include "GamesSharing.h"

typedef struct {
	PyObject_HEAD
		Social* social;
} social_obj;


typedef struct {
	PyObject_HEAD
		GamesServices* gamesServices;
} gamesServices_obj;

typedef struct {
	PyObject_HEAD
		GamesSharing* gamesSharing;
} gamesSharing_obj;


extern PyTypeObject SocialType;
extern PyTypeObject GamesServicesType;
extern PyTypeObject GamesSharingType;
