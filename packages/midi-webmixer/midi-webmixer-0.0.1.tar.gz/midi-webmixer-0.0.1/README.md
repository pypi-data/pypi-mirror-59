[![CircleCI](https://circleci.com/gh/adamcathersides/midi-webmixer/tree/master.svg?style=svg)](https://circleci.com/gh/adamcathersides/midi-webmixer/tree/master)
# Midi Webmixer

The aim of this project was to allow me to remotely control the 4 aux sends of my Yamaha 01V desk via midi.
The idea being that each of the members in my band can control their own monitor mix on anything that can load a browser (phones etc)

# Installation

I recommend using the docker compose file if you wan to get started quickly.  However here are some manual installation steps..

Clone the repo:
```
git clone git@github.com:adamcathersides/midi-webmixer.git
```

Install
```
cd midi-webmixer
pip3 install . --user
```

# Running

Once installed the application `webmixer` should be available

The application if comprised to two parts.  
* RestAPI 
* GUI (webpage) 

## General archetecture overview

This application is split into two parts; a rest API and a the main GUI - both of which can be run from the `webmixer` command.  Data storage and persistance is dealt with via redis.
Both the rest API and mixer GUI need to be externally accessible as the GUI sends requests to the rest API using [sendBeacon](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/sendBeacon) messages.

It is reccomended to run this application using the docker-compose file provided.  However due to the (probably shortsighted) design the GUI container needs to know what the externally accessible hostname of the rest API therefore this has to be manually provided at the point of running `docker-compose up`.  See [docker-compose](#docker-compose) section for an example. 

You can run the restapi by itself and access it manually if required (I use the amazing [Insomnia](https://insomnia.rest/) to do this.)
The GUI part relies on the restapi to be running.

## Poke the rest API

The rest API accepts POST requests like so:
`http://rest_api:5001/mixer/<aux>/<channel>/<value>`

So if you wanted to set aux1, channel 2 to full volume:
`http://rest_api:5001/mixer/aux1/2/127`

## Running the REST api

`webmixer --config config.ini --restapi --port 5001`

## Running the GUI

`webmixer --config config.ini --gui --port 5000`


# Config file

The config file is pretty self explanatory.  As well as normal midi and networking settings, it also allows you to define custom channel names.

The midi port is the number of the midi out port you would like to use.  Find out what you have installed by running `webmix --listmidi` 
If midi port is set to `virtual` the system will create a fake midi port which is handy for debugging.

If `rest_host` is left blank it will attempt to use an environment variable called `REST_HOST`.  This is required when deploying in containerised enviroments.

Here is an example:

```
[Network]
interface = lo

[Services]
redis_host = redis
redis_port = 6379
rest_host =
rest_port = 5001
gui_host = gui
gui_port = 5000

[Midi]
port = virtual

[ChannelNames]
1 = Kick
2 = SNR
3 = OH
4 =
5 = Dave
6 = Jon
7 = Adam
8 = Paul
9 =
10 = Bass
11 = AdamGit
12 = JonGit
```

# Get midiport numbers

```
webmixer --listmidi
```

# Docker

```
cd midi-webmixer
docker build -t webmixer:1 .
docker run --net=host -v /home/adam/github/01v-midi/config.ini:/config.ini webmixer:1 /config.ini --restapi
docker run --net=host -v /home/adam/github/01v-midi/config.ini:/config.ini webmixer:1 /config.ini --gui
```

# Docker Compose (Reccomended)

This is an example of how to run on the webmixer from a single machine.  
The `HOSTNAME` variable is required in order for the GUI to contact the rest API.  It can also be set in the `config.ini`

```
cd midi-webmixer
docker-compose build
HOSTNAME=$(hostname) docker-compose up
```



