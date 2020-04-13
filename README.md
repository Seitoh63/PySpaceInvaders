# PySpaceInvaders

[![Language](https://img.shields.io/badge/language-python-blue.svg?style=flat)](https://www.python.org)
[![Module](https://img.shields.io/badge/module-pygame-brightgreen.svg?style=flat)](http://www.pygame.org/news.html)
[![Release](https://img.shields.io/badge/release-v1.0-orange.svg?style=flat)]()

## Space Invaders

Space invaders is originally an arcade game released in 1978. It is a 2D shooter, the first of its genre. 
The goal, as for most of the arcade game of this time, is to obtain the highest score by destroying continuously the incoming aliens.

Here a screenshot from my implementation :
<p float="left">
  <img src="https://i.imgur.com/WKrfXYW.gif" />
  <img src="https://i.imgur.com/H9q8WB7.gif" />
</p>


## Gameplay 

Many aliens are invading world and move slowly to you, shooting laser randomly in your direction.

The spaceship (aka the player) can move on the horizontal axis, avoiding laser shots. 
The spaceship can also fire at aliens, but it should aim properly since it's only one shot at a time.
It can take cover below barriers, but they are gradually destroyed by enemy lasers and spaceship missiles.

Hit aliens are destroyed and award points. Periodicaly, a mistery saucer will appear, granting a lot of bonus point if destroyed.

## How to play

Download the source code and type :

```bash
C:\.\PySpaceInvaders python main.py
```

- Arrow keys to move
- Space key to shoot

## Requirements

python : >= 3.7.6  
pygame : >= 1.9


## Technical informations

This game was implemented to reproduce as faithfully as possible the original arcade game.

Sprites come from :
- https://www.deviantart.com/gooperblooper22/art/Space-Invaders-Sprite-Sheet-135338373
- https://www.spriters-resource.com/arcade/spaceinv/

Sounds have been edited but the original material comes from : 
- https://www.classicgaming.cc/classics/space-invaders/sounds

Gameplay inspiration comes from youtube :
- https://www.youtube.com/watch?v=MU4psw3ccUI
- https://www.youtube.com/watch?v=EqZY2CB_t2A

There is a configuration file *config.py* which contains all the configuration data.
It can be modified to customize the game experience.


## Contact

I'm very glad you take some time to look at my game and at my code!
You can contact me at :  sethogeek@gmail.com
