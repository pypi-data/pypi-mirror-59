#include <Python.h>
#include "Social.h"
#include "GamesServices.h"

typedef struct {
	PyObject_HEAD
		Social* social;
} social_obj;


typedef struct {
	PyObject_HEAD
		GamesServices* gamesServices;
} gamesServices_obj;


extern PyTypeObject SocialType;
extern PyTypeObject GamesServicesType;
